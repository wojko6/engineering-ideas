# Engineering Ideas

Private incubator for technical concepts that are not yet mature enough to
deserve their own implementation repository.

The goal is to preserve architecture decisions, MVP boundaries, open
questions and promotion criteria before implementation work begins.

## Ideas

| Idea | Status | Summary |
| --- | --- | --- |
| [Universal Tabs for GNOME](ideas/gnome-universal-tabs/README.md) | Concept / architecture | System-wide window grouping and tabbed workspace model for GNOME, with later deep application adapters. |
| [Fedora Localization Audit & Repair Engine](ideas/fedora-localization-audit-repair-engine/README.md) | Concept | Reusable localization scan, repair, install and verification pipeline. |
| [Fedora Upgrade Readiness Engine](ideas/fedora-upgrade-readiness-engine/README.md) | Concept | Pre-upgrade compatibility and rollback-readiness assessment for major Fedora upgrades. |
| [System Drift Detector](ideas/system-drift-detector/README.md) | Concept | Compare the live workstation with repository-defined desired state. |
| [Btrfs Safe Change & Rollback](ideas/btrfs-safe-change-rollback/README.md) | Concept | Guarded snapshot/change/verify/rollback workflow for risky system changes. |
| [Privacy & Telemetry Audit](ideas/privacy-telemetry-audit/README.md) | Concept | Repeatable DNS/network telemetry measurement across controlled scenarios. |
| [Workstation Health Dashboard](ideas/workstation-health-dashboard/README.md) | Concept | Evidence-backed summary of workstation health and maintenance state. |
| [Disaster Recovery Drill Automation](ideas/disaster-recovery-drill-automation/README.md) | Concept | Automate safe clean-room Fedora recovery drills in disposable test environments. |
| [Reproducible KDE Wayland Session](ideas/reproducible-kde-wayland-session/README.md) | Concept | Optional KDE Wayland session without compromising canonical GNOME state. |
| [Tailscale Android DNS Regression Lab](ideas/tailscale-android-dns-regression-lab/README.md) | Concept / investigation | Reproducible Android/Tailscale DNS and routing diagnostics. |
| [GeForce NOW Packet-Loss Correlation Lab](ideas/gfn-packet-loss-correlation-lab/README.md) | Concept / diagnostic lab | Synchronized client/router captures to localize intermittent real-time loss. |

| [LAN / Wi-Fi Performance & Latency Benchmark Lab](ideas/lan-wifi-performance-latency-benchmark/README.md) | Concept / benchmark lab | Controlled iperf3 Ethernet vs Wi-Fi 6 throughput, jitter, loss and latency-under-load testing. |

See [BACKLOG.md](BACKLOG.md) for additional ideas that have not yet been expanded.

## Workflow

1. Capture the problem and intended user experience.
2. Define a bounded MVP.
3. Record architectural constraints and rejected shortcuts.
4. Split implementation into stages.
5. Promote an idea into its own repository only when the MVP and technical
   direction are stable enough to justify active development.

Use [the idea template](templates/IDEA-TEMPLATE.md) for future concepts.
