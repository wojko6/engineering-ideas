# XNU / AMD Binary Compatibility Research — Lenovo Legion 5

**Status (2026-11-23): offline binary matching and simulated patch ordering observed; real macOS 27 boot NOT tested. No EFI or disk deployment authorized by this report.**

## Purpose and scope

Determine whether AMD-oriented OpenCore patches selected by [NullMoth Liberator](https://github.com/nullmoth/liberator) match the *actual x86-64 Mach-O kernel* from Apple's macOS 27.2 build 26B123. This is a narrow feasibility study for an AMD Ryzen 7 5800H laptop, not a macOS distribution, boot guide or proof of support. It is **separate** from the parked [Stela Apple Silicon-on-x86 study](../stela-apple-silicon-on-legion-lab/README.md), which uses a different architecture.

The research draws on [AMD Vanilla](https://github.com/AMD-OSX/AMD_Vanilla) and the [laobamac AMD_Vanilla fork](https://github.com/laobamac/AMD_Vanilla), but neither their patches nor any Apple binaries are mirrored here. Sources and their licenses remain with their respective owners.

## Reproducible evidence boundaries

- **Observed on an operator's Fedora 45 host:** verified Apple KDK DMG, unpacked the KDK locally, checked kernel and IOPCIFamily SHA-256 values, used a pinned NullMoth analyzer to examine patch symbols and masked-byte hits, and ran two follow-on overlap/order audits. Results are summarized in [FINDINGS.md](FINDINGS.md). Original terminal records and local artifacts remain unpublished.
- **Locally unit-tested in this repository:** the independent, read-only Python audit tool's match/mask/version and replacement primitives (synthetic data only). **It has not yet been rerun end-to-end against the actual Apple kernel.** A regression check is included for the operator-observed result, but that is not independent validation until it runs on another verified local KDK copy.
- **Not observed:** a verified macOS 26 reference kernel matching NullMoth's hash, OpenCore's live application of the patches, macOS 27 boot on AMD, usable GPU acceleration, or supported Wi-Fi on this hardware under macOS 27.

## Pinned sources for reproducing the offline audit

| Input | Reference |
| --- | --- |
| NullMoth Liberator | [`v3.0.0-beta.6`](https://github.com/nullmoth/liberator/releases/tag/v3.0.0-beta.6), commit `237a766247b68c816facd68dab92bf90d95f9f42` |
| NullMoth machine-readable evidence | `tools/patches_27.json`, `kit/v3-kit.json`, `tools/kernel_patches_27.py` at that commit |
| AMD patch source | [`laobamac/AMD_Vanilla`](https://github.com/laobamac/AMD_Vanilla), commit `a174cca80efe2377fde3b902666c70863ea66454` |
| Apple KDK | macOS 27.2 build **26B123**; obtain legally from an authorized source, verify its published checksum locally |
| Kernel x86-64 SHA-256 | `3c9317518535791503970fbec322b9bba70e91f3a233536205ccd77b047ffc83` |
| IOPCIFamily universal binary SHA-256 | `bbe5d9bc84009bc2c96d6987ae5700358eab5d885623b4cd4edb2a7f60598e0d` |

The tool consumes **local** files. It has no download, installation, EFI, partition, NVRAM or patch-output capability. Source revisions should be checked before running.

## Reproduce the isolated check

After independently obtaining and verifying the exact files, run from this directory:

```bash
python3 -B -m unittest discover -s tests -v
python3 -I -B tools/audit_patches.py \
  --kernel /path/to/verified/kernel \
  --manifest /path/to/liberator/tools/patches_27.json \
  --kit /path/to/liberator/kit/v3-kit.json \
  --plist /path/to/laobamac-AMD_Vanilla/patches.plist
```

Expected *for these pinned inputs*: 15 candidate patches, 20 selected match sites, 233 changed bytes, zero conflicting match windows, and final **in-memory simulation SHA-256** `8084cc15ec1e17846246ff8e51627a97ba812b8f1901baaa8a7de3f0fcae9cee`. The audit never saves patched code. A matching output establishes only that this simulator reproduced the observed byte-level transformation, **not** that the patches are operationally safe or correctly applied by OpenCore. An exception/nonzero exit indicates a mismatch, not permission to force deployment.

## Validation gates and next research

1. Independently extract macOS 26.7.1 build 25G241's x86-64 kernel and IOPCIFamily and compare SHA-256 values against NullMoth's `kernel_26_sha256` and `sha256_26`. This phase is **pending**; a legitimate but different binary must not be treated as an exact reference.
2. Compare source and target instruction boundaries, call/control flow, register use, and disassembly for each patched site. Special attention: CPUID, MSR, PAT, LAPIC and scheduler-panic conditions. Masked pattern matches are not instruction-level safety proofs.
3. Independently review version gates and OpenCore-specific application semantics; compare against Darwin 25/26 baseline and inspect synthetic negative cases.
4. Research ACPI, graphics, storage and networking as separate compatibility questions. Any physical boot would require separate explicit approval, dedicated non-production media, a tested recovery path and a verified safe target.

## Risks and publication boundary

- Applying kernel patches can cause boot failures, data loss or system instability. **No boot or installation step is authorized here.**
- Apple's licensing restricts some uses and redistribution of macOS components. This repository contains **no Apple images, executable binaries, KDK payloads, proprietary firmware, generated patched kernel, bootable EFI, serials or raw system logs**.
- The audit is written in Python's standard library, reads local paths and prints results; it is not intended as a full OpenCore simulator.
- Do not publish local account names, hostnames, serials, disks/partitions, UUIDs, device-specific EFI configuration or private logs. Follow [publication policy](../../PUBLICATION.md).

**Promotion gate:** remain an isolated research concept until independent cross-version analysis, code-reviewable tools and a separately authorized non-production boot plan exist.
