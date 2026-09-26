# Engineering Ideas Backlog

This backlog preserves ideas discussed before they become active implementation
projects.

## Expanded concepts

- [LAN / Wi-Fi Performance & Latency Benchmark Lab](ideas/lan-wifi-performance-latency-benchmark/README.md)

- [Universal Tabs for GNOME](ideas/gnome-universal-tabs/README.md)
- [Fedora Localization Audit & Repair Engine](ideas/fedora-localization-audit-repair-engine/README.md)
- [Fedora Upgrade Readiness Engine](ideas/fedora-upgrade-readiness-engine/README.md)
- [System Drift Detector](ideas/system-drift-detector/README.md)
- [Btrfs Safe Change & Rollback](ideas/btrfs-safe-change-rollback/README.md)
- [Privacy & Telemetry Audit](ideas/privacy-telemetry-audit/README.md)
- [Workstation Health Dashboard](ideas/workstation-health-dashboard/README.md)
- [Disaster Recovery Drill Automation](ideas/disaster-recovery-drill-automation/README.md)
- [Reproducible KDE Wayland Session](ideas/reproducible-kde-wayland-session/README.md)
- [Tailscale Android DNS Regression Lab](ideas/tailscale-android-dns-regression-lab/README.md)
- [GeForce NOW Packet-Loss Correlation Lab](ideas/gfn-packet-loss-correlation-lab/README.md)
- [Home Lab Attack Surface & Vulnerability Assessment](ideas/home-lab-attack-surface-vulnerability-assessment/README.md)
- [Android Ad / Tracker Blocking Comparative Lab](ideas/android-ad-tracker-blocking-comparative-lab/README.md)

## Additional remembered ideas not yet expanded

- Security Exposure Monitor for Fedora;
- Update Risk Analyzer before major package/system upgrades;
- SBOM / package provenance inventory;
- Policy-as-Code for workstation desired state;
- private Fedora recovery ISO built only after clean-restore validation;
- router personal cloud / automated file sync using the dedicated data SSD;
- Pi-hole + Unbound migration as an alternative DNS-filtering architecture;
- severity-aware router alerting with phone notifications and recovery events;
- mobile telemetry case studies for Android/Xiaomi devices;
- future controlled full-disk-encryption evaluation during a reinstall.

Some router ideas already have detailed design material in the active ASUS
project roadmap. They are listed here only as remembered concepts so this
incubator can serve as a single idea index without duplicating operational
source-of-truth documentation.


## Selected mobile test extensions

Three high-value phone-based extensions are now retained in the expanded ideas:

1. **Android transport handover and Tailscale recovery** — Wi-Fi, LTE/5G and
   USB-C Ethernet transitions plus sleep/resume recovery; see
   `ideas/tailscale-android-dns-regression-lab/README.md`.
2. **Android DNS enforcement / resolver-bypass matrix** — verify actual resolver
   paths across Wi-Fi, Ethernet, LTE/5G and Tailscale, including controlled
   Private DNS / encrypted-DNS cases; see
   `ideas/privacy-telemetry-audit/README.md`.
3. **Controlled Android telemetry correlation** — correlate idle, reboot,
   selected-app and WebView/Custom Tab scenarios with DNS/network evidence,
   optionally across multiple access paths; see
   `ideas/privacy-telemetry-audit/README.md`.
