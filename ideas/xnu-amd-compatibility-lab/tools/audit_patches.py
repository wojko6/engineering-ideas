#!/usr/bin/env python3
"""Read-only offline audit of the pinned NullMoth Darwin 27 AMD patch set.

No networking, file writes, boot changes, or Apple binaries are distributed.
The simulator is NOT a substitute for OpenCore, disassembly, or a boot test.
"""
from __future__ import annotations

import argparse
import base64
from bisect import bisect_right
import hashlib
import json
from pathlib import Path
import plistlib
import struct

FIELDS = ("Identifier", "Base", "Find", "Mask", "Count", "Limit", "Skip")
REFERENCE_SHA = "3c9317518535791503970fbec322b9bba70e91f3a233536205ccd77b047ffc83"
SIMULATED_SHA = "8084cc15ec1e17846246ff8e51627a97ba812b8f1901baaa8a7de3f0fcae9cee"


def patch_identity(patch: dict) -> str:
    fields = []
    for key in FIELDS:
        value = patch.get(key)
        if value is None:
            fields.append("")
        elif isinstance(value, (bytes, bytearray)):
            fields.append(base64.b64encode(value).decode("ascii"))
        elif isinstance(value, bool):
            fields.append(str(value).lower())
        else:
            fields.append(str(value))
    return hashlib.sha256(("|".join(fields) + "|").encode()).hexdigest()


def search_masked(data: bytes, first: int, last: int, pattern: bytes, mask: bytes = b"") -> list[int]:
    size = len(pattern)
    if not size:
        raise ValueError("Empty Find is forbidden")
    if not mask:
        mask = bytes([255]) * size
    if len(mask) != size or first < 0 or first > last or last > len(data):
        raise ValueError("Invalid search bounds or mask length")
    anchor_start, anchor_len = 0, 0
    run_start, run_len = 0, 0
    for j, value in enumerate(mask):
        if value == 255:
            if not run_len:
                run_start = j
            run_len += 1
            if run_len > anchor_len:
                anchor_start, anchor_len = run_start, run_len
        else:
            run_len = 0

    def matches(pos: int) -> bool:
        return all((data[pos + k] & mask[k]) == (pattern[k] & mask[k]) for k in range(size))

    if anchor_len == 0:
        return [i for i in range(first, last - size + 1) if matches(i)]
    anchor = pattern[anchor_start:anchor_start + anchor_len]
    offsets = []
    cursor = first + anchor_start
    while cursor < last:
        hit = data.find(anchor, cursor, last)
        if hit < 0:
            break
        start = hit - anchor_start
        if start >= first and start + size <= last and matches(start):
            offsets.append(start)
        cursor = hit + 1
    return offsets


def replace_masked(original: bytes, replacement: bytes, mask: bytes = b"") -> bytes:
    if not mask:
        mask = bytes([255]) * len(replacement)
    if not (len(original) == len(replacement) == len(mask)):
        raise ValueError("Replacement width mismatch")
    return bytes((old & (~bits & 255)) | (new & bits) for old, new, bits in zip(original, replacement, mask))


class MachO:
    """Minimal, bounds-checked 64-bit x86_64 Mach-O symbol and segment reader."""

    def __init__(self, data: bytes):
        if len(data) < 32 or data[:4] != b"\xcf\xfa\xed\xfe":
            raise ValueError("Expected thin Mach-O 64-bit little-endian")
        if struct.unpack_from("<I", data, 4)[0] != 0x01000007:
            raise ValueError("Expected x86_64 CPU type")
        ncmds, cmdsize = struct.unpack_from("<II", data, 16)
        if 32 + cmdsize > len(data) or ncmds > 1000:
            raise ValueError("Invalid Mach-O commands")
        segments = []
        symtab = None
        cursor = 32
        for _ in range(ncmds):
            if cursor + 8 > 32 + cmdsize:
                raise ValueError("Truncated load command")
            cmd, length = struct.unpack_from("<II", data, cursor)
            if length < 8 or cursor + length > 32 + cmdsize:
                raise ValueError("Invalid load command size")
            if cmd == 0x19:  # LC_SEGMENT_64
                if length < 72:
                    raise ValueError("Short LC_SEGMENT_64")
                vm, _, fileoff, filesz = struct.unpack_from("<QQQQ", data, cursor + 24)
                if fileoff + filesz > len(data):
                    raise ValueError("Segment exceeds file")
                segments.append((vm, fileoff, filesz))
            elif cmd == 0x2:  # LC_SYMTAB
                if length < 24:
                    raise ValueError("Short LC_SYMTAB")
                symtab = struct.unpack_from("<IIII", data, cursor + 8)
            cursor += length
        if symtab is None:
            raise ValueError("Missing LC_SYMTAB")
        symoff, nsyms, stroff, strsize = symtab
        if nsyms > 1000000 or symoff + nsyms * 16 > len(data) or stroff + strsize > len(data):
            raise ValueError("Symbol/string table exceeds file")
        self.data = data
        self.segments = segments
        self.symbols = {}
        for i in range(nsyms):
            strx, typ, _, _, address = struct.unpack_from("<IBBHQ", data, symoff + 16 * i)
            if (typ & 0x0E) != 0x0E or strx == 0:
                continue
            if strx >= strsize:
                raise ValueError("String index exceeds table")
            end = data.find(b"\0", stroff + strx, stroff + strsize)
            if end < 0:
                raise ValueError("Unterminated symbol")
            name = data[stroff + strx:end].decode("latin1")
            self.symbols[name] = address
        self.starts = sorted(
            (offset, name) for name, address in self.symbols.items()
            if (offset := self.file_offset(address)) is not None
        )
        self.starts_offsets = [x[0] for x in self.starts]

    def file_offset(self, address: int) -> int | None:
        for vm, fileoff, length in self.segments:
            if vm <= address < vm + length:
                return fileoff + address - vm
        return None

    def owner(self, offset: int) -> str | None:
        index = bisect_right(self.starts_offsets, offset) - 1
        return self.starts[index][1] if index >= 0 else None

    def hits(self, p: dict, data: bytes) -> list[int]:
        base = p.get("Base") or ""
        if base:
            if base not in self.symbols:
                raise ValueError(f"Missing exact base symbol: {base!r}")
            first = self.file_offset(self.symbols[base])
            if first is None:
                raise ValueError("Symbol not mapped in file")
        else:
            first = 0
        limit = int(p.get("Limit") or 0)
        last = min(len(data), first + limit) if limit else len(data)
        return search_masked(data, first, last, bytes(p["Find"]), bytes(p.get("Mask") or b""))


def enabled_on_25_7(p: dict) -> bool:
    def vt(value: str, default: tuple[int, int, int]) -> tuple[int, int, int]:
        if not value:
            return default
        nums = tuple(int(s) for s in value.split("."))
        return (nums + (0, 0, 0))[:3]
    return bool(p.get("Enabled")) and vt(p.get("MinKernel", ""), (0, 0, 0)) <= (25, 7, 0) <= vt(p.get("MaxKernel", ""), (999, 999, 999))


def prepare_patches(plist: Path, kit: dict, manifest: dict) -> list[dict]:
    with plist.open("rb") as handle:
        items = plistlib.load(handle)["Kernel"]["Patch"]
    originals = [dict(p) for p in items if enabled_on_25_7(p)]
    if len(originals) != 15:
        raise ValueError(f"Expected 15 macOS 26 active patches, found {len(originals)}")
    for p in originals:
        if "Force cpuid_cores_per_package" in p.get("Comment", ""):
            if p["Replace"] != bytes.fromhex("ba00000000"):
                raise ValueError("Unexpected CPUID replacement")
            p["Replace"] = bytes.fromhex("ba08000000")
        if "Force CPUFAMILY_INTEL_PENRYN" in p.get("Comment", ""):
            if p["Base"] != "_cpuid_set_info ":
                raise ValueError("Unexpected untrimmed CPUID symbol")
            p["Base"] = "_cpuid_set_info"
    valid = {item["mark"] for item in manifest["carried"]}
    chosen = [p for p in originals if patch_identity(p) in valid]
    if len(chosen) != 13:
        raise ValueError("Expected 13 selected carried patches")
    own = kit["patches_27_own"]
    if len(own) != 2:
        raise ValueError("Expected two NullMoth entries")
    for item in own:
        p = item["patch"]
        if p["identifier"] != "kernel" or p["base"] != item["in"]:
            raise ValueError("NullMoth patch identity mismatch")
        chosen.append({
            "Identifier": p["identifier"], "Base": p["base"], "Comment": p["comment"],
            "Find": base64.b64decode(p["find"], validate=True),
            "Replace": base64.b64decode(p["replace"], validate=True),
            "Mask": base64.b64decode(p["mask"], validate=True),
            "ReplaceMask": base64.b64decode(p["replace_mask"], validate=True),
            "Count": p["count"], "Limit": p["limit"], "Skip": 0,
        })
    return chosen


def audit(kernel_path: Path, manifest_path: Path, kit_path: Path, plist_path: Path) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    kit = json.loads(kit_path.read_text(encoding="utf-8"))
    pristine = kernel_path.read_bytes()
    if manifest["kernel_27_sha256"] != REFERENCE_SHA or hashlib.sha256(pristine).hexdigest() != REFERENCE_SHA:
        raise ValueError("Source kernel does not match pinned Darwin 27.2 reference")
    image = MachO(pristine)
    patches = prepare_patches(plist_path, kit, manifest)
    expected = {p["mark"]: p for p in manifest["carried"]}
    working = bytearray(pristine)
    changed_addresses = set()
    windows = []
    selected_sites = 0
    for number, patch in enumerate(patches, 1):
        if patch["Identifier"] != "kernel" or int(patch.get("Skip") or 0) != 0:
            raise ValueError("Only kernel entries with Skip=0 are supported")
        before = image.hits(patch, pristine)
        after = image.hits(patch, working)
        if before != after:
            raise ValueError(f"Patch {number}: later search targets changed")
        count = int(patch.get("Count") or 0)
        selected = after[:count] if count else after
        if not selected or (count and len(selected) != count):
            raise ValueError(f"Patch {number}: invalid selected count")
        if number <= 13:
            record = expected[patch_identity(patch)]
            if len(after) != record["found_27"] or [image.owner(i) for i in selected] != record["in"]:
                raise ValueError(f"Patch {number}: manifest match/owner drift")
        elif len(after) != 1:
            raise ValueError(f"Patch {number}: own patch not unique")
        find = bytes(patch["Find"])
        repl = bytes(patch["Replace"])
        if len(find) != len(repl):
            raise ValueError("Find/Replace size mismatch")
        for start in selected:
            stop = start + len(find)
            if any(max(start, a) < min(stop, b) for a, b in windows):
                raise ValueError(f"Patch {number}: overlapping match windows")
            windows.append((start, stop))
            orig = bytes(working[start:stop])
            changed = replace_masked(orig, repl, bytes(patch.get("ReplaceMask") or b""))
            for index, (old, new) in enumerate(zip(orig, changed)):
                if old != new:
                    address = start + index
                    if address in changed_addresses:
                        raise ValueError("Duplicate changed byte")
                    changed_addresses.add(address)
            working[start:stop] = changed
        selected_sites += len(selected)
    final_digest = hashlib.sha256(working).hexdigest()
    if (len(patches), selected_sites, len(changed_addresses), final_digest) != (15, 20, 233, SIMULATED_SHA):
        raise ValueError("Reference result differs from observed L3.9 baseline")
    return {"patches": 15, "sites": selected_sites, "changed_bytes": len(changed_addresses),
            "overlapping_windows": 0, "retargeted_patches": 0, "simulation_sha256": final_digest,
            "boot_validated": False, "files_written": False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kernel", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--kit", type=Path, required=True)
    parser.add_argument("--plist", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(audit(args.kernel, args.manifest, args.kit, args.plist), indent=2))


if __name__ == "__main__":
    main()
