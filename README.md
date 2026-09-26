# Engineering Ideas

Private incubator for technical concepts that are not yet mature enough to
deserve their own implementation repository.

The goal is to preserve architecture decisions, MVP boundaries, open questions
and promotion criteria before implementation work begins.

The repository is deliberately broader than the active work queue. New ideas can
be captured without turning every idea into an immediate project.

## Working rule

Keep at most **one or two implementation-heavy projects active at the same
time**. Everything else remains documented here until the current work reaches a
clear checkpoint.

## Suggested execution path

The current preferred sequence is:

1. **LAN / Wi-Fi Performance & Latency Benchmark Lab**
   - finish the 80/160 MHz validation and same-endpoint comparisons.
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

After those, choose the next item based on practical need rather than opening all
remaining concepts in parallel.

## Network, edge and security

| Idea | Status | Summary |
| --- | --- | --- |
| [ASUS Edge Architecture Maturity Roadmap](ideas/asus-edge-architecture-maturity-roadmap/README.md) | Concept / architecture hardening | Policy Model v3, policy consistency, runtime drift, kernel packet CI, safer deployment, resilience, observability, IPv6 assurance and the eventual boundary toward OPNsense. |
| [LAN / Wi-Fi Performance & Latency Benchmark Lab](ideas/lan-wifi-performance-latency-benchmark/README.md) | Concept / benchmark lab | Controlled iperf3 Ethernet vs Wi-Fi 6/80 MHz on the current Legion client; 160 MHz only with a separately verified capable client. |
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
| [Fedora Upgrade Readiness Engine](ideas/fedora-upgrade-readiness-engine/README.md) | Concept | Pre-upgrade compatibility and rollback-readiness assessment for major Fedora upgrades. |
| [Btrfs Safe Change & Rollback](ideas/btrfs-safe-change-rollback/README.md) | Concept | Guarded snapshot/change/verify/rollback workflow for risky system changes. |
| [Disaster Recovery Drill Automation](ideas/disaster-recovery-drill-automation/README.md) | Concept | Automate safe clean-room Fedora recovery drills in disposable test environments. |
| [Workstation Health Dashboard](ideas/workstation-health-dashboard/README.md) | Concept | Evidence-backed summary of workstation health and maintenance state. |
| [Fedora Localization Audit & Repair Engine](ideas/fedora-localization-audit-repair-engine/README.md) | Concept | Reusable localization scan, repair, install and verification pipeline. |
| [Reproducible KDE Wayland Session](ideas/reproducible-kde-wayland-session/README.md) | Concept | Optional KDE Wayland session without compromising canonical GNOME state. |

## Desktop / experimental software

| Idea | Status | Summary |
| --- | --- | --- |
| [Universal Tabs for GNOME](ideas/gnome-universal-tabs/README.md) | Concept / architecture | System-wide window grouping and tabbed workspace model for GNOME, with later deep application adapters. |

See [BACKLOG.md](BACKLOG.md) for the prioritized queue and additional remembered
ideas that have not yet been expanded.

## Workflow

1. Capture the problem and intended user experience.
2. Define a bounded MVP.
3. Record architectural constraints and rejected shortcuts.
4. Split implementation into stages.
5. Keep operational source-of-truth material in the active implementation
   repository rather than duplicating it here.
6. Promote an idea into its own repository only when the MVP and technical
   direction are stable enough to justify active development.

Use [the idea template](templates/IDEA-TEMPLATE.md) for future concepts.
