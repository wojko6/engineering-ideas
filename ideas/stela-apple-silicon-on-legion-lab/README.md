# Stela Apple Silicon-on-x86 Compatibility Lab — Lenovo Legion 5

**Status:** concept / parked; upstream must be rechecked before testing; no live Stela tests performed

## Problem

The previous OpenCore-based Hackintosh research on the Lenovo Legion 5 15ACH6H
(82JU) did not reach a usable macOS boot. Further blind EFI/ACPI iteration is
not justified without new evidence. The existing OpenCore experiment remains
**ON HOLD**, with its logs, tested candidates and limitations retained in the
owning project repository.

[Stela](https://github.com/tylertms/Stela) offers a different architecture:
a UEFI loader translating Apple Silicon ARM64 macOS code to x86-64, emulating
Apple Silicon hardware, and implementing a Metal path for supported NVIDIA
GPUs. It is **not** an OpenCore configuration or a conventional Intel
Hackintosh.

## Goal

Assess, using a bounded and reversible experiment, whether Stela can start
its loader and macOS installer on the Legion 5 without compromising the
working Fedora workstation or internal storage. A successful boot would be
an experimental result, **not** evidence of reliable daily usability.

## Upstream sources (always check the current state)

- [Latest Stela releases](https://github.com/tylertms/Stela/releases)
- [Current upstream README and hardware requirements](https://github.com/tylertms/Stela#hardware-requirements)
- [Open startup and compatibility issues](https://github.com/tylertms/Stela/issues?q=is%3Aissue+is%3Aopen)
- Historical examples of boot failures: [Realtek startup issue #20](https://github.com/tylertms/Stela/issues/20) and [PCI/USB startup issue #26](https://github.com/tylertms/Stela/issues/26).

Recent upstream development has focused on boot diagnostics, firmware and PCI
initialization, networking, USB detection and translation performance. These
features and their support status must be **revalidated against the current
release notes and hardware reports at test time**. A source-level fix or VM
result does not establish that it works on the target laptop. Stela is
experimental and may not boot on otherwise supported hardware.

## Hardware feasibility and unknowns

| Component | Reference hardware | Initial assessment |
| --- | --- | --- |
| CPU | AMD Ryzen 7 5800H | Meets x86-64-v2 requirement; AVX2 available |
| dGPU | NVIDIA RTX 3060 Laptop | RTX 30 family listed; mobile GPU behavior **not validated** |
| iGPU | AMD Radeon (Cezanne) | No advertised Stela AMD iGPU graphics support |
| Memory | 16 GB installed | Meets stated 8 GB minimum; practical headroom unknown |
| Firmware | UEFI, Secure Boot disabled during prior lab | Verify state afresh before any boot |
| Ethernet | Realtek RTL8111/8168/8411 family | Listed families; actual PCI ID and runtime startup unverified |
| Wi-Fi | Realtek RTL8852 family | Support must be checked against the current upstream release; no local validation |
| Audio | Realtek ALC287 | Support must be checked against the current upstream release; no local validation |
| Display | Internal eDP and external DP | GPU wiring, display output and MUX/dGPU-only behavior unverified |
| Storage | Internal NVMe drives | **Do not select them** for an experimental install |

Check the **current** upstream storage and USB capacity requirements before
any trial; installation requirements can change. USB capacity must not be
confused with permission to erase an install target.

## Related work and scope boundary

- The prior **OpenCore/Hackintosh** investigation is archived as historical
  evidence and stays ON HOLD. Do not reopen it merely to test Stela.
- The Fedora workstation repository remains the operational source of truth
  for backups, boot configuration and any actual system changes.
- This incubator owns **the feasibility hypothesis, bounded test plan and
  promotion gate**, not a second live-worklog or EFI repository.
- The previous SanDisk USB medium labeled `TAHOE_OC` (~57.7 GiB reported)
  can be **repurposed only after** a verified identity/capacity check,
  preservation of any irreplaceable EFI/logs, and explicit authorization to
  erase it. The old name is a historical label, not a destination selector.

## Proposed architecture

1. Fedora is the unchanged host used for **read-only** source, binary,
   dependency and CLI analysis.
2. A verified, disposable USB becomes the Stela installation/boot medium.
   Use the official Linux x86-64 release with its published SHA256SUMS.
3. UEFI boots Stela from USB for a controlled diagnostic observation.
4. Saved boot logs are sanitized and analyzed; only then decide whether a
   dedicated, non-production macOS target disk or partition is justified.

No internal disk installation belongs to the first MVP.

## Bounded MVP

### Phase 0 — read-only preflight

- Review the **latest available** requirements, release notes and outstanding
  issues for AMD, RTX 30 mobile, USB/xHCI, Realtek Ethernet and GPU initialization.
- Inventory UEFI boot mode, graphics/display routing, PCI device IDs,
  USB identity, and storage **read-only**.
- Confirm existing OpenCore research and relevant USB data have copies if
  those artifacts are to be retained.
- Identify whether Stela has diagnostic/read-only commands that can be used
  safely before media creation.

### Phase 1 — optional USB preparation (requires separate approval)

- Explicitly select the disposable SanDisk device **by verified identifier**;
  do not infer the device from the `TAHOE_OC` label or fixed `/dev/sdX`.
- Verify the downloaded archive hash and confirm the USB is not a Fedora
  root, boot, mounted backup or any valuable data volume.
- Only after a separate user confirmation, prepare the Stela USB, knowing
  that `sudo ./stela setup` **erases the selected USB**.
- Prefer the offline installer if capacity and download requirements permit.
- Leave internal NVMe/GPT/EFI untouched.

### Phase 2 — controlled boot diagnostics (requires separate approval)

- Observe UEFI startup, CPU/handoff, PCI enumeration, USB initialization,
  firmware loading, NVIDIA initialization, screen output and networking.
- Stop before any installer action that formats, repartitions or writes an
  internal disk. A visible installer is an acceptable first-stage outcome.
- Recover logs using the upstream documented interface, when available:
  `sudo ./stela setup boot-log --output log.txt`.
- Compare observations to upstream issue reports; do not infer support from
  an advertised GPU family alone.

## Validation and evidence

| Result | Evidence |
| --- | --- |
| PASS (diagnostic MVP) | Stela starts from the disposable USB, reaches a stable loader/installer milestone, and the boot log confirms device state without touching internal storage |
| PARTIAL | Progress beyond prior failure points but blocked by GPU, display, USB, Ethernet or firmware limitations, with actionable log evidence |
| FAIL | Reproducible failure with a bounded diagnosis and retained sanitized log |
| INCONCLUSIVE | No reliable log, ambiguous media/PCI state or no authorized boot test |
| NOT TESTED | No execution on the Legion has been documented in this concept |

Record the exact **tested build/revision in test evidence** (not in this
long-lived concept), checksums, firmware settings, device IDs without serial
numbers, boot-stage milestones and sanitized evidence. Do not claim
that a completed installation or usable Metal acceleration has been proven
unless separately verified.

## Risks and rollback

- **High data-loss risk:** Stela setup erases the selected USB; the installer
  may partition or overwrite the selected macOS destination.
- Misidentifying storage could destroy Fedora, backup media or existing EFI.
- The RTX 3060 Laptop, muxless iGPU routing, external output and power
  management are unproven. Recheck the current Wi-Fi and audio support status
  before testing.
- Runtime speed and macOS reliability are unproven.
- Apple's software licensing may restrict installation on non-Apple hardware;
  review the applicable license before undertaking the experiment.
- Rollback is removal of the dedicated test USB and restoration of its
  previous contents from verified backups if desired; Fedora internal disks
  should remain unchanged throughout the MVP.

**Default gate: NO USB ERASE / NO INTERNAL DISK WRITES / NO INSTALLATION.**
A documented concept is not permission to execute the test.

## Public-data boundary

Never publish local usernames, hostnames, MAC addresses, serial numbers,
disk UUIDs, EFI secrets, Apple signing responses, private boot logs, or
deployment-specific path details. Redact diagnostic material before any
upstream issue or public repository contribution. Follow
[PUBLICATION.md](../../PUBLICATION.md).

## Promotion criterion

Promote to a controlled implementation/test project only after the read-only
preflight is complete, the disposable USB and rollback path are verified,
and the user separately approves the destructive media-preparation step.
A sustained successful boot with usable display/GPU and reproducible logs
would warrant the next, separately approved installation-stage study.
