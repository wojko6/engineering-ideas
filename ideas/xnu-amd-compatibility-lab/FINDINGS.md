# Evidence record — offline XNU / AMD experiments

**Dates:** 2026-11-23 to 2026-11-24. **Evidence type:** operator-reported terminal output from bounded local tests on Fedora 45, not independent reproduction by a second investigator. The private original logs and local Apple files are intentionally not included. All values below are scoped to the pinned files listed in [README.md](README.md).

## Apple binary provenance and extraction (L3.0–L3.5)

The operator verified a macOS 27.2 (26B123) KDK image by file length and SHA-256, then identified an Apple DMG/HFSX container, XAR `KernelDebugKit.pkg`, PBZX `KDK.pkg/Payload`, and an ASCII CPIO/odc payload. The reported PBZX decode had 330 chunks (327 XZ, 3 raw), 5,523,374,959 decoded bytes, and 7,685 CPIO entries. Extracted binary checksums matched the pinned NullMoth manifest:

| Binary | Verified SHA-256 | Observed format |
| --- | --- | --- |
| `System/Library/Kernels/kernel` | `3c9317518535791503970fbec322b9bba70e91f3a233536205ccd77b047ffc83` | x86-64 Mach-O, 21,128,776 bytes |
| `IOPCIFamily.kext/Contents/MacOS/IOPCIFamily` | `bbe5d9bc84009bc2c96d6987ae5700358eab5d885623b4cd4edb2a7f60598e0d` | Universal Mach-O, includes x86-64, 2,148,224 bytes |

The operator's symbol parser enumerated 24,399 kernel symbols and 1,485 symbols for the x86-64 IOPCIFamily slice. These are observed parser counts, not claims of all possible symbol definitions.

## Kernel patch selection and matching (L3.6)

Using the pinned `laobamac/AMD_Vanilla` plist, 15 entries were enabled for a macOS 26.7 / Darwin 25 baseline. The offline study normalized an unexpected trailing space in one CPUID base symbol and set the user's **eight physical cores** as a simulated CPUID constant **in memory only**. Of those baseline entries, 13 corresponded to entries in NullMoth's `carried` manifest. Two distinct NullMoth scheduler patches completed the 15-entry macOS 27 candidate set.

- All 13 carried entries found the manifest's expected macOS 27 byte-pattern counts and function-owner names, including CPUID, MSR, LAPIC, PAT and scheduler sites.
- Both NullMoth-specific entries matched once in the whole kernel at their expected functions, `_thread_block_reason` and `_thread_dispatch`, and were associated with the expected `Non-monotonic time` panic paths.
- **Not carried:** the laobamac `thread_invoke/thread_dispatch` variant and the `probeBusGated` variant. Mere byte matches are insufficient for approval: masked patterns may match other functions or rely on unknown instruction semantics.

## Alternative scheduler patch analysis (L3.7)

The omitted laobamac scheduler patch produced **seven** raw macOS 27 matches. Its first two match addresses coincided with the two precise NullMoth candidate sites:

| Symbol | Match file offset | laobamac replacement | NullMoth replacement |
| --- | --- | --- | --- |
| `_thread_block_reason` | `0xAB5E2` | `66 90 66 90 66 90` | `66 0F 1F 44 00 00` |
| `_thread_dispatch` | `0xAC56B` | `66 90 66 90 66 90` | `66 0F 1F 44 00 00` |

Both variants replace a six-byte conditional branch with NOP instructions, with different encodings. These are *alternative strategies*, **not** patches to activate together. The omitted `probeBusGated` pattern matched once and proposed changing `e3 11 73 4d` to `e3 11 72 4d` (one changed byte); the surrounding instruction semantics and actual hardware benefit were **not** established. No conclusion that it is safe to carry to macOS 27 follows.

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

## Exact macOS 26 reference (L4.0–L4.2)

On 2026-11-24, the operator completed the extraction of the macOS **26.7.1, build 25G241** KDK. The PBZX stream decoded 297 chunks (294 XZ, 3 raw), totaling 4,982,398,616 bytes; 8,043 CPIO entries were processed, with a valid trailer and zero trailing bytes.

| Binary | Bytes | SHA-256 |
| --- | ---: | --- |
| Kernel (thin x86-64 Mach-O) | 19,006,616 | `7004ebc1020a5c7e3f075c631507f31fdc0ce3fe02e9f01f42dce1d178770a08` |
| IOPCIFamily (universal x86-64 / arm64e) | 1,406,784 | `44c110353037ce88bfd14181c4d52c5a2c0ccd5679b8e941822dd9a825ccef04` |

Both digests matched the corresponding NullMoth manifest fields exactly. Readback, Mach-O magic and final integrity checks passed. This identifies the exact reference binaries by content, rather than merely by a similar OS version.

## Cross-version reproduction (L4.3)

All four original binary digests were rechecked. The local analysis used the pinned upstream Mach-O parser and a separate regex-based masked-pattern search; the two search implementations agreed on offsets. Selected counts and nearest-symbol owners agreed across both versions for the 13 carried kernel entries. The two NullMoth scheduler entries additionally passed upstream checks for global uniqueness and expected panic-message targets in both kernels.

| Check | Result |
| --- | --- |
| Reference binary integrity | 4/4 PASS |
| Selected carried kernel entries | 13 |
| NullMoth-specific scheduler entries | 2 |
| Selected sites per kernel | 20 |
| Manifest counts and owner comparison | PASS |
| Separate matching algorithm | PASS |
| Excluded variants applied | No |

The upstream manifest includes an additional IOPCIFamily carried entry not selected by the pinned fork. Do not describe these results as validation of every upstream patch. The parser's nearest-symbol owner is not a proven function boundary.

## Bounded x86-64 instruction review (L4.4–L4.4a)

The operator used GNU objdump with anonymous memory-backed file descriptors to disassemble original and simulated byte windows. No patched kernel was saved. Across the two kernels, 32 of 40 sites passed the original linear decoding check. The same four sites in each version required targeted review.

| Patch/site | Local observed change in both versions |
| --- | --- |
| 01/01 | Shift and increment replaced by an eight-core immediate assignment to EDX |
| 03/01 | CPUID leaf immediate changed from 4 to 0x8000001D |
| 12/03 | Six-byte conditional branch replaced by three two-byte no-ops |
| 14/01 | Six-byte conditional branch replaced by one six-byte no-op |

All eight targeted sites had valid local decoding before and after simulation, with three identical following instructions at a shared resynchronization boundary. The same earlier invalid decode occurred in original and simulated buffers. This supports local structural consistency, not a proof that the earlier bytes are unreachable or data. Keep the eight results as `LOCAL_PASS_PREFIX_UNCERTAIN`; do not relabel them as full linear passes. No local review remained unresolved, but full control flow and semantic safety remain unverified. In particular, removing scheduler checks changes behavior; it does not establish correct timing.

Both simulated kernels had 233 changed byte positions. Simulation digests (not Apple release hashes):

- macOS 26.7.1: `8d46ef88379e725ce9a353e3e639404638963b4b1d0f7c09c013eb6819c0b5e5`
- macOS 27.2: `8084cc15ec1e17846246ff8e51627a97ba812b8f1901baaa8a7de3f0fcae9cee`

## Public tool reproduction (L4.5)

The operator downloaded only the Python tool and its tests from the pinned public [commit](https://github.com/wojko6/engineering-ideas/commit/f1f8e90a219211e22438bfb430f8941277794f1e), verified Git blob identities and executed them locally with the verified macOS 27.2 kernel, pinned NullMoth manifest/kit and AMD Vanilla fork.

| Check | Result |
| --- | --- |
| Tool Git blob SHA-1 | `fcd133f905191089248a39428c3f66a44aaf9025` |
| Unit tests Git blob SHA-1 | `477bfadbcfca64d27b25100daacea6d1dc9ecbab` |
| Synthetic tests | 8/8 PASS |
| Real kernel audit | PASS |
| Selected patches / sites / changed bytes | 15 / 20 / 233 |
| Overlapping windows / retargeted patches | 0 / 0 |
| Simulation SHA-256 | Same as L3.9 (above) |
| Source integrity after execution | PASS |
| Patched kernel saved / boot validated | No / No |

This is operator-observed end-to-end reproduction by the public implementation, not an independent investigator's validation, an OpenCore execution or a validation of macOS 26 by the public tool. The two tested Python blobs are unchanged by this documentation update.

## Interpretation and limits

What the evidence supports: matching selected sites in both exact reference kernels, non-overlapping candidate edits, bounded instruction-decoding consistency, and reproduction of the macOS 27.2 in-memory result by the public tool on the operator's host.

What it **does not** support: proof of code semantics, absence of race/logic regressions, behavior of a full OpenCore boot pipeline, support for AMD Ryzen 7 5800H in macOS 27, working integrated/discrete GPU, Wi-Fi or a successful macOS 27 boot. Prior unrelated OpenCore recovery failures on this hardware are **not** overridden by these offline results. Any testing of a live boot remains a separately authorized undertaking.
