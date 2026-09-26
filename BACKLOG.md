# Engineering Ideas Backlog

This backlog preserves ideas discussed before they become active implementation
projects.

The list is intentionally larger than the active work queue. The operating rule
is to keep at most one or two implementation-heavy projects active at the same
time.

## Now / finish before opening more work

### 1. LAN / Wi-Fi Performance & Latency Benchmark Lab

[Expanded concept](ideas/lan-wifi-performance-latency-benchmark/README.md)

Current status:

- Lenovo / RTL8852AE remains the validated 80 MHz reference;
- Acer / MediaTek MT7922 has a live-validated 160 MHz association and
  2402/2402 Mb/s PHY under strong-signal conditions;
- POCO F8 Pro has a live-validated 160 MHz association;
- the ASUS configured-vs-runtime 160 MHz discrepancy was isolated to a
  controlled `bw_switch_160` family test without permanently committing the
  temporary values.

Next measurement phase:

- run the same-server Acer 80 MHz vs 160 MHz iperf3 matrix;
- capture idle latency, jitter, packet loss and latency under load;
- repeat each accepted measurement enough times for a stable comparison;
- add POCO wired-vs-Wi-Fi measurements where useful;
- optionally compare GeForce NOW at 80 vs 160 MHz only as an application-level
  validation after the LAN benchmark is complete.

### 2. ASUS Edge Architecture Maturity Roadmap — MVP only

[Expanded concept](ideas/asus-edge-architecture-maturity-roadmap/README.md)

Do **not** attempt the whole roadmap at once.

Initial bounded MVP:

1. Policy Model v3 with explicit source / destination / service tuples.
2. Source-scoped exit-node forwarding at the local firewall layer.
3. Tailscale Grants ↔ local-firewall consistency checking.
4. Deployment manifest and running-state drift detection.
5. Kernel-level network namespace packet tests.

Defer fault injection, full observability, SLO work, IPv6 expansion and
architecture migration until the MVP is stable.

## Next

### Home Lab Attack Surface & Vulnerability Assessment

[Expanded concept](ideas/home-lab-attack-surface-vulnerability-assessment/README.md)

Use the ASUS, Fedora and hardened Android device first; add intentionally
vulnerable VMs for controlled exploitation later.

### Tailscale Android DNS Regression Lab

[Expanded concept](ideas/tailscale-android-dns-regression-lab/README.md)

Priority extension:

- Wi-Fi ↔ LTE/5G;
- Wi-Fi ↔ USB-C Ethernet;
- sleep/resume;
- tunnel / DNS recovery timing;
- manual-intervention requirements.

### Privacy & Telemetry Audit

[Expanded concept](ideas/privacy-telemetry-audit/README.md)

Priority extensions:

- Android DNS enforcement / resolver-bypass matrix;
- post-hardening telemetry correlation;
- controlled app / WebView / Custom Tab scenarios;
- Wi-Fi, Ethernet, LTE/5G and Tailscale path comparison where meaningful.

### Android Ad / Tracker Blocking Comparative Lab

[Expanded concept](ideas/android-ad-tracker-blocking-comparative-lab/README.md)

Keep the comparison focused on materially different blocking layers:

- Brave Shields;
- browser Content Blocker API;
- TrackerControl;
- Rethink;
- router-side filtering.

Do not expand the MVP into a catalogue of every Android ad blocker.

### System Drift Detector

[Expanded concept](ideas/system-drift-detector/README.md)

Natural next workstation-engineering project after the ASUS running-state drift
work because the same desired-state thinking can be reused.

### Fedora Upgrade Readiness Engine

[Expanded concept](ideas/fedora-upgrade-readiness-engine/README.md)

Useful before the next Fedora major-version upgrade and a good place to reuse
drift, backup and rollback checks.

## Later

### Btrfs Safe Change & Rollback

[Expanded concept](ideas/btrfs-safe-change-rollback/README.md)

Build after the desired-state / upgrade workflow is stable.

### Disaster Recovery Drill Automation

[Expanded concept](ideas/disaster-recovery-drill-automation/README.md)

Extend the already validated recovery work into repeatable clean-room drills,
measured recovery time and later evidence-backed RTO/RPO.

### Workstation Health Dashboard

[Expanded concept](ideas/workstation-health-dashboard/README.md)

Treat the dashboard as a presentation layer over real health/drift/recovery
checks, not as an independent source of truth.

### Fedora Localization Audit & Repair Engine

[Expanded concept](ideas/fedora-localization-audit-repair-engine/README.md)

Useful when localization problems recur; otherwise keep parked behind the
network/security work.

## Optional / event-driven

### GeForce NOW Packet-Loss Correlation Lab

[Expanded concept](ideas/gfn-packet-loss-correlation-lab/README.md)

Resume only when the intermittent symptom is reproducible or when a controlled
loss-localization exercise is intentionally scheduled.

A normal GeForce NOW 80/160 MHz latency comparison does not activate this lab;
that belongs to the LAN/Wi-Fi benchmark as optional application-level
validation.

### Reproducible KDE Wayland Session

[Expanded concept](ideas/reproducible-kde-wayland-session/README.md)

Interesting workstation experiment, but not part of the current
network/security path.

### Universal Tabs for GNOME

[Expanded concept](ideas/gnome-universal-tabs/README.md)

Large standalone software/desktop project. Keep parked until there is deliberate
time for application architecture work.

## Router ideas already tracked in the active ASUS project

The following remain useful, but their operational source of truth is the active
`Advanced-ASUS-Edge-Gateway-ZTNA-Infrastructure` roadmap rather than this
incubator:

- router personal cloud / automated file sync using the dedicated data SSD;
- Pi-hole + Unbound migration as an alternative DNS-filtering architecture;
- severity-aware router alerting with phone notifications and recovery events;
- off-router backup automation, retention, integrity verification and recovery
  measurement;
- OPNsense / x86 edge migration;
- VLAN / trust-zone segmentation;
- Suricata IDS/IPS evaluation;
- Wazuh / centralized detection and response;
- metrics, network assurance and later evidence-backed SLO;
- hardware/ISP failure testing and incident runbooks.

The new
[ASUS Edge Architecture Maturity Roadmap](ideas/asus-edge-architecture-maturity-roadmap/README.md)
acts as the incubator index for architectural hardening ideas that may later be
promoted into the active ASUS repository.

## Additional remembered Fedora / platform ideas not yet expanded

- Security Exposure Monitor for Fedora;
- Update Risk Analyzer before major package/system upgrades;
- SBOM / package provenance inventory;
- Policy-as-Code for workstation desired state;
- private Fedora recovery ISO built only after clean-restore validation;
- future controlled full-disk-encryption evaluation during a reinstall.

These remain remembered ideas only. Expand them when a real implementation need
appears instead of opening them merely to increase project count.

## Mobile extensions already folded into expanded concepts

The following are not separate projects:

1. **Android transport handover and Tailscale recovery**  
   Lives under
   [Tailscale Android DNS Regression Lab](ideas/tailscale-android-dns-regression-lab/README.md).

2. **Android DNS enforcement / resolver-bypass matrix**  
   Lives under
   [Privacy & Telemetry Audit](ideas/privacy-telemetry-audit/README.md).

3. **Controlled Android telemetry correlation**  
   Lives under
   [Privacy & Telemetry Audit](ideas/privacy-telemetry-audit/README.md).

4. **POCO Ethernet vs Wi-Fi 80/160 MHz**  
   Lives under
   [LAN / Wi-Fi Performance & Latency Benchmark Lab](ideas/lan-wifi-performance-latency-benchmark/README.md).

## Queue discipline

Before promoting a new idea into active work, answer:

1. Is one of the current "Now" items unfinished?
2. Does the new work reuse evidence/tools from the current project?
3. Is there a bounded MVP?
4. Is there a rollback or disposable test environment where needed?
5. Will the result produce a distinct engineering lesson rather than duplicate
   an existing case study?

If the answer is mostly "no", keep the idea documented and return to it later.
