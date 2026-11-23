# Evidence record — offline XNU / AMD experiments

**Date:** 2026-11-23. **Evidence type:** operator-reported terminal output from bounded local tests on Fedora 45, not independent reproduction by a second investigator. The private original logs and local Apple files are intentionally not included. All values below are scoped to the pinned files listed in [README.md](README.md).

## Apple binary provenance and extraction (L3.0–L3.5)

The operator verified a macOS 27.2 (26B123) KDK image by file length and SHA-256, then identified an Apple DMG/HFSX container, XAR `KernelDebugKit.pkg`, PBZX `KDK.pkg/Payload`, and an ASCII CPIO/odc payload. The reported PBZX decode had 330 chunks (327 XZ, 3 raw), 5,523,374,959 decoded bytes, and 7,685 CPIO entries. Extracted binary checksums matched the pinned NullMoth manifest:

| Binary | Verified SHA-256 | Observed format |
| --- | --- | --- |
| `System/Library/Kernels/kernel` | `3c9317518535791503970fbec322b9bba70e91f3a233536205ccd77b047ffc83` | x86-64 Mach-O, 21,128,776 bytes |
| `IOPCIFamily.kext/Contents/MacOS/IOPCIFamily` | `bbe5d9bc84009bc2c96d6987ae5700358eab5d885623b4cd4edb2a7f60598e0d` | Universal Mach-O, includes x86-64, 2,148,224 bytes |

The operator's symbol parser enumerated 24,399 kernel symbols and 1,485 symbols for the x86-64 IOPCIFamily slice. These are observed parser counts, not claims of all possible symbol definitions.

## Kernel patch selection and matching (L3.6)

Using the pinned `laobamac/AMD_Vanilla` plist, 15 entries were enabled for a macOS 26.7 / Darwin 25 baseline. The offline study normalized an unexpected trailing space in one CPUID base symbol and set the user's **eight physical cores** as a simulated CPUID constant **in memory only**. Of those baseline entries, 13 corresponded to entries in NullMoth's `carried` manifest. Two distinct NullMoth scheduler patches completed the 15-entry Darwin 27 candidate set.

- All 13 carried entries found the manifest's expected Darwin 27 byte-pattern counts and function-owner names, including CPUID, MSR, LAPIC, PAT and scheduler sites.
- Both NullMoth-specific entries matched once in the whole kernel at their expected functions, `_thread_block_reason` and `_thread_dispatch`, and were associated with the expected `Non-monotonic time` panic paths.
- **Not carried:** the laobamac `thread_invoke/thread_dispatch` variant and the `probeBusGated` variant. Mere byte matches are insufficient for approval: masked patterns may match other functions or rely on unknown instruction semantics.

## Alternative scheduler patch analysis (L3.7)

The omitted laobamac scheduler patch produced **seven** raw Darwin 27 matches. Its first two match addresses coincided with the two precise NullMoth candidate sites:

| Symbol | Match file offset | laobamac replacement | NullMoth replacement |
| --- | --- | --- | --- |
| `_thread_block_reason` | `0xAB5E2` | `66 90 66 90 66 90` | `66 0F 1F 44 00 00` |
| `_thread_dispatch` | `0xAC56B` | `66 90 66 90 66 90` | `66 0F 1F 44 00 00` |

Both variants replace a six-byte conditional branch with NOP instructions, with different encodings. These are *alternative strategies*, **not** patches to activate together. The omitted `probeBusGated` pattern matched once and proposed changing `e3 11 73 4d` to `e3 11 72 4d` (one changed byte); the surrounding instruction semantics and actual hardware benefit were **not** established. No conclusion that it is safe to carry to Darwin 27 follows.

## Collision and sequential simulation (L3.8–L3.9)

| Operator-observed check | Value |
| --- | ---: |
| Candidate patches | 15 |
| Selected sites under recorded `Count` rules | 20 |
| Changed byte positions | 233 |
| Overlapping matched windows | 0 |
| Overlapping written byte positions | 0 |
| Retargeted later patches after sequential in-memory changes | 0 |
| Original kernel preserved | Yes (SHA-256 rechecked) |
| Patched kernel or EFI written | **No** |

The 15-step **in-memory** simulated output SHA-256 was `8084cc15ec1e17846246ff8e51627a97ba812b8f1901baaa8a7de3f0fcae9cee`. This checksum is a local simulation artifact for a pinned input, not an Apple build hash, OpenCore runtime attestation or functional compatibility test. Patch #10 (`_i386_init` MSR removal) accounted for 123 of the 233 changed positions and warrants close instruction-level review.

## Separate macOS 26 input (L4.0–L4.1)

A legitimate KDK for macOS **26.7.1, build 25G241** was downloaded and verified by checksum, and its PBZX payload recognized. At this checkpoint, **no actual macOS 26 kernel or IOPCIFamily SHA-256 comparison has yet been reported**. In particular, there is *no verified equality* with the `kernel_26_sha256` value referenced by NullMoth. L4.2 remains pending.

## Interpretation and limits

What the evidence supports: the operator observed reproducible byte-pattern matches, non-overlapping candidate edits and stable sequential search targets in a real, checksum-verified Darwin 27.2 x86-64 kernel.

What it **does not** support: proof of code semantics, absence of race/logic regressions, behavior of a full OpenCore boot pipeline, support for AMD Ryzen 7 5800H in macOS 27, working integrated/discrete GPU, Wi-Fi or a successful macOS 27 boot. Prior unrelated OpenCore recovery failures on this hardware are **not** overridden by these offline results. Any testing of a live boot remains a separately authorized undertaking.
