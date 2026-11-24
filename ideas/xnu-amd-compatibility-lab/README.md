# XNU / AMD Binary Compatibility Research — Lenovo Legion 5

**Status (2026-11-24): cross-version offline binary matching, bounded instruction review and public-tool reproduction on a verified kernel observed; real macOS 27 boot NOT tested. No EFI or disk deployment authorized by this report.**

## Purpose and scope

Determine whether AMD-oriented OpenCore patches selected by [NullMoth Liberator](https://github.com/nullmoth/liberator) match the *actual x86-64 Mach-O kernel* from Apple's macOS 27.2 build 26B123. This is a narrow feasibility study for an AMD Ryzen 7 5800H laptop, not a macOS distribution, boot guide or proof of support. It is **separate** from the parked [Stela Apple Silicon-on-x86 study](../stela-apple-silicon-on-legion-lab/README.md), which uses a different architecture.

The research draws on [AMD Vanilla](https://github.com/AMD-OSX/AMD_Vanilla) and the [laobamac AMD_Vanilla fork](https://github.com/laobamac/AMD_Vanilla), but neither their patches nor any Apple binaries are mirrored here. Sources and their licenses remain with their respective owners.

## Reproducible evidence boundaries

- **Observed on the operator's Fedora 45 host:** both Apple KDKs were extracted locally; all four original binary SHA-256 values matched the pinned NullMoth manifest. The selected 15 patches matched 20 sites per macOS version, with a second matching algorithm agreeing with the upstream search. Symbol ownership still uses the upstream parser.
- **Instruction review:** 32 of 40 sites passed the bounded linear decode check; the other eight passed a local decode/resynchronization check but retain uncertainty about earlier instructions in their containing symbol. No full control-flow or semantic proof is claimed.
- **Public tool validation (L4.5):** the operator downloaded the tool and tests from commit `f1f8e90a219211e22438bfb430f8941277794f1e`, verified both Git blob hashes, ran all eight synthetic unit tests and reproduced the macOS 27.2 simulation digest with the real verified kernel. This is reproduction by a separate implementation on the same host, not by a second investigator. The public tool covers the macOS 27 kernel only; the cross-version and instruction-review scripts were separate local experiments. See [FINDINGS.md](FINDINGS.md).
- **Not observed:** OpenCore's live application of the patches, macOS 27 boot on AMD, usable GPU acceleration, supported Wi-Fi on this hardware under macOS 27, or full semantic safety.

## Pinned sources for reproducing the offline audit

| Input | Reference |
| --- | --- |
| NullMoth Liberator | [`v3.0.0-beta.6`](https://github.com/nullmoth/liberator/releases/tag/v3.0.0-beta.6), commit `237a766247b68c816facd68dab92bf90d95f9f42` |
| NullMoth machine-readable evidence | `tools/patches_27.json`, `kit/v3-kit.json`, `tools/kernel_patches_27.py` at that commit |
| AMD patch source | [`laobamac/AMD_Vanilla`](https://github.com/laobamac/AMD_Vanilla), commit `a174cca80efe2377fde3b902666c70863ea66454` |
| Apple KDK (target) | macOS 27.2 build **26B123** |
| Apple KDK (reference) | macOS 26.7.1 build **25G241**; obtain both KDKs from authorized sources under applicable terms |
| Kernel x86-64 SHA-256 | `3c9317518535791503970fbec322b9bba70e91f3a233536205ccd77b047ffc83` |
| IOPCIFamily universal binary SHA-256 (27.2) | `bbe5d9bc84009bc2c96d6987ae5700358eab5d885623b4cd4edb2a7f60598e0d` |
| Kernel x86-64 SHA-256 (26.7.1) | `7004ebc1020a5c7e3f075c631507f31fdc0ce3fe02e9f01f42dce1d178770a08` |
| IOPCIFamily universal binary SHA-256 (26.7.1) | `44c110353037ce88bfd14181c4d52c5a2c0ccd5679b8e941822dd9a825ccef04` |

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

1. **Completed (L4.2–L4.3):** extract and verify both macOS 26 reference binaries and compare the selected patches on both verified kernels. The 15-patch kernel-only subset is not the full upstream manifest, which also includes a PCI patch not enabled in the pinned fork.
2. **Bounded review completed (L4.4–L4.4a):** compare linear instruction decoding and local resynchronization. Full control flow, register/flag effects, timing invariants and MSR behavior remain unverified.
3. **Completed (L4.5):** reproduce the macOS 27.2 in-memory result with the unchanged public tool. Review actual OpenCore version gates and application semantics separately; expand negative cases and seek external reproduction.
4. Research ACPI, graphics, storage and networking as separate compatibility questions. Any physical boot would require separate explicit approval, dedicated non-production media, a tested recovery path and a verified safe target.

## Risks and publication boundary

- Applying kernel patches can cause boot failures, data loss or system instability. **No boot or installation step is authorized here.**
- Apple's licensing restricts some uses and redistribution of macOS components. This repository contains **no Apple images, executable binaries, KDK payloads, proprietary firmware, generated patched kernel, bootable EFI, serials or raw system logs**.
- The audit is written in Python's standard library, reads local paths and prints results; it is not intended as a full OpenCore simulator.
- Do not publish local account names, hostnames, serials, disks/partitions, UUIDs, device-specific EFI configuration or private logs. Follow [publication policy](../../PUBLICATION.md).

**Promotion gate:** remain an isolated research concept. Cross-version byte matching and the public-tool reproduction are complete; full semantic and OpenCore-runtime validation and a separately authorized non-production boot plan are still outstanding.
