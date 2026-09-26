# Engineering Ideas

Public engineering incubator for technical concepts that are not yet mature
enough to deserve their own implementation repository.

The purpose of this repository is to preserve architecture decisions, bounded
MVPs, open questions, validation plans and promotion criteria before active
implementation begins.

> **Status boundary:** an item marked `Concept` is a design or test plan, not a
> claim that the feature is deployed, production-ready or live-validated.

## Why this repository exists

The implementation repositories answer **what is running or being built**.
This repository answers **what may be worth building next, why, and under what
conditions**.

That distinction is deliberate:

```text
idea
  ↓
architecture / MVP / risks / acceptance criteria
  ↓
controlled implementation
  ↓
validation and evidence
  ↓
promotion into an implementation repository
```

## Working rule

Keep at most **one or two implementation-heavy projects active at the same
time**. New ideas can be captured here without becoming immediate work.

## Suggested execution path

The current preferred sequence is:

1. **LAN / Wi-Fi Performance & Latency Benchmark Lab**
   - the Acer MT7922 HE80/HE160 throughput investigation and independent Android
     HE160 reference comparison are complete;
   - the resulting bounded interoperability case study has been promoted to the
     ASUS Edge implementation repository;
   - deferred follow-up: boot the Acer from Fedora Workstation Live and repeat
     the HE160 throughput test with the Linux MT7922 driver path before deciding
     whether the case study needs an OS/driver-specific addendum.
2. **ASUS Edge Architecture Maturity Roadmap — MVP only**
   - Policy Model v3;
   - Tailscale/local-firewall consistency;
   - deployment manifest / drift detection;
   - kernel-level packet CI.
3. **Home Lab Attack Surface & Vulnerability Assessment**
   - establish exposure baselines and remediation/retest evidence.
4. **Tailscale Android DNS Regression Lab**
   - transport handover, resume and DNS/routing recovery.
5. **Privacy & Telemetry Audit**
   - Android resolver-bypass and post-hardening telemetry scenarios.
6. **Android Ad / Tracker Blocking Comparative Lab**
   - compare browser-native, local-VPN and router-side filtering layers.

After those, choose the next item based on practical need rather than opening
all remaining concepts in parallel.

## Network, edge and security

| Idea | Status | Summary |
| --- | --- | --- |
| [ASUS Edge Architecture Maturity Roadmap](ideas/asus-edge-architecture-maturity-roadmap/README.md) | Concept / architecture hardening | Policy Model v3, policy consistency, runtime drift, kernel packet CI, safer deployment, resilience, observability, IPv6 assurance and the eventual boundary toward OPNsense. |
| [LAN / Wi-Fi Performance & Latency Benchmark Lab](ideas/lan-wifi-performance-latency-benchmark/README.md) | Validated baseline / deferred follow-up | Controlled 80/160 MHz benchmarking with live-verified client capability; current follow-up is a deferred Fedora Live HE160 isolation test on the Acer MT7922. |
| [Home Lab Attack Surface & Vulnerability Assessment](ideas/home-lab-attack-surface-vulnerability-assessment/README.md) | Concept / defensive security lab | Repeatable attack-surface, exposure and vulnerability assessment across owned devices and isolated lab targets. |
| [GeForce NOW Packet-Loss Correlation Lab](ideas/gfn-packet-loss-correlation-lab/README.md) | Concept / diagnostic lab | Synchronized client/router captures to localize intermittent real-time loss. |

## Android, privacy and telemetry

| Idea | Status | Summary |
| --- | --- | --- |
| [Tailscale Android DNS Regression Lab](ideas/tailscale-android-dns-regression-lab/README.md) | Concept / investigation | Reproducible Android/Tailscale DNS, transport-handover and routing diagnostics. |
| [Privacy & Telemetry Audit](ideas/privacy-telemetry-audit/README.md) | Concept | Repeatable DNS/network telemetry measurement across controlled scenarios, including Android post-hardening evidence. |
| [Android Ad / Tracker Blocking Comparative Lab](ideas/android-ad-tracker-blocking-comparative-lab/README.md) | Concept / comparative privacy lab | Compare browser-native, Content Blocker API, local-VPN and router-side ad/tracker filtering with network evidence. |

## Fedora, recovery and workstation engineering

| Idea | Status | Summary |
| --- | --- | --- |
| [System Drift Detector](ideas/system-drift-detector/README.md) | Concept | Compare the live workstation with repository-defined desired state. |
| [Fedora Upgrade Readiness Engine](ideas/fedora-upgrade-readiness-engine/README.md) | Concept / future automation layer | Reusable readiness automation after the active Fedora major-upgrade workflow is stable; current execution remains in the Fedora workstation roadmap. |
| [Btrfs Safe Change & Rollback](ideas/btrfs-safe-change-rollback/README.md) | Concept | Guarded snapshot/change/verify/rollback workflow for risky system changes. |
| [Disaster Recovery Drill Automation](ideas/disaster-recovery-drill-automation/README.md) | Concept / future automation layer | Automate repeatable disposable-environment recovery drills after the active Fedora recovery workflow is stable. |
| [Workstation Health Dashboard](ideas/workstation-health-dashboard/README.md) | Concept | Evidence-backed summary of workstation health and maintenance state. |
| [Fedora Localization Audit & Repair Engine](ideas/fedora-localization-audit-repair-engine/README.md) | Concept | Reusable localization scan, repair, install and verification pipeline. |
| [Reproducible KDE Wayland Session](ideas/reproducible-kde-wayland-session/README.md) | Concept / execution tracked in Fedora roadmap | Architecture notes for optional KDE coexistence; current planning and acceptance remain in the Fedora workstation project. |

## Desktop / experimental software

| Idea | Status | Summary |
| --- | --- | --- |
| [Universal Tabs for GNOME](ideas/gnome-universal-tabs/README.md) | Concept / architecture | System-wide window grouping and tabbed workspace model for GNOME, with later deep application adapters. |

See [BACKLOG.md](BACKLOG.md) for the prioritized queue and additional remembered
ideas that have not yet been expanded.

## Scope ownership map

Several ideas intentionally reuse the same devices and evidence sources. To
avoid duplicate or conflicting documentation, each outcome has one primary
owner inside this incubator:

| Topic | Primary owner | Boundary |
| --- | --- | --- |
| Ethernet / Wi-Fi throughput, 80 vs 160 MHz, latency under load | [LAN / Wi-Fi Performance & Latency Benchmark Lab](ideas/lan-wifi-performance-latency-benchmark/README.md) | Cloud gaming may be used only as optional application-level validation. |
| Intermittent GeForce NOW packet-loss localization | [GeForce NOW Packet-Loss Correlation Lab](ideas/gfn-packet-loss-correlation-lab/README.md) | Activate only for reproducible loss and synchronized capture. |
| ASUS policy, drift, resilience, WLAN assurance architecture | [ASUS Edge Architecture Maturity Roadmap](ideas/asus-edge-architecture-maturity-roadmap/README.md) | Reference benchmark results; do not duplicate its measurement dataset. |
| Android telemetry and DNS resolver-bypass methodology | [Privacy & Telemetry Audit](ideas/privacy-telemetry-audit/README.md) | Owns generic endpoint/DNS-path evidence, not blocker-product comparison. |
| Android ad/tracker blocker comparison | [Android Ad / Tracker Blocking Comparative Lab](ideas/android-ad-tracker-blocking-comparative-lab/README.md) | Owns comparative blocking efficacy and trade-offs. |
| Tailscale Android handover / DNS / route recovery | [Tailscale Android DNS Regression Lab](ideas/tailscale-android-dns-regression-lab/README.md) | Reuse transport states without duplicating raw Wi-Fi benchmarking. |
| Home-lab exposure and vulnerability assessment | [Home Lab Attack Surface & Vulnerability Assessment](ideas/home-lab-attack-surface-vulnerability-assessment/README.md) | ASUS roadmap may reference the resulting exposure model. |

If a test can support more than one idea, store the result with the owner of the
**question being answered** and link to it from the other concept. Do not
publish the same evidence as independent findings in multiple projects.

## Relationship to implementation repositories

Ideas that become active should move into the repository that owns the running
implementation and its evidence. Current examples include:

- [Advanced ASUS Edge Gateway & Zero-Trust Lab](https://github.com/wojko6/Advanced-ASUS-Edge-Gateway-ZTNA-Infrastructure)
- [Fedora Workstation Setup](https://github.com/wojko6/fedora-workstation-setup)

This repository should not become a second operational source of truth for those
projects.

## Public-data boundary

This repository is intentionally suitable for public viewing.

Do not commit credentials, auth keys, private keys, real deployment addresses,
hostnames, MAC addresses, raw packet captures, browser dumps, private logs,
device identifiers, storage identifiers, personal browsing history or
deployment-specific configuration.

Use abstract names or documentation-only example ranges instead.

See [PUBLICATION.md](PUBLICATION.md) for the publication checklist and
[SECURITY.md](SECURITY.md) for reporting accidental sensitive-data exposure.

A lightweight automated check runs in CI to catch common publication mistakes,
but human review remains required.

## Workflow

1. Capture the problem and intended user experience.
2. Define a bounded MVP.
3. Record architectural constraints and rejected shortcuts.
4. Split implementation into stages.
5. Define evidence and rollback requirements before risky live changes.
6. Keep operational source-of-truth material in the active implementation
   repository rather than duplicating it here.
7. Promote an idea into its own repository only when the MVP and technical
   direction are stable enough to justify active development.

Use [the idea template](templates/IDEA-TEMPLATE.md) for future concepts.

## Contributing

Corrections, methodology improvements and architecture discussion are welcome.
See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Unless stated otherwise, this repository is licensed under the
[MIT License](LICENSE).
