# ASUS Edge Architecture Maturity Roadmap

**Status:** concept / architecture hardening roadmap

## Goal

Take the existing ASUS TUF-AX5400 security-edge project from a feature-rich,
well-evidenced home/SMB lab toward a more mature network-engineering design
without pretending that a 512 MiB consumer router is an enterprise firewall.

The emphasis is no longer "add more services". The next stage is to improve:

- policy precision;
- configuration consistency;
- deployment safety;
- drift detection;
- packet-level test coverage;
- resilience and recovery;
- observability and measurable service objectives;
- IPv6 assurance;
- WLAN / latency engineering;
- documented migration boundaries toward a dedicated x86 edge.

The active implementation source of truth remains the
`Advanced-ASUS-Edge-Gateway-ZTNA-Infrastructure` repository. This document is
an incubator roadmap only.

## Architectural principle

Prefer:

```text
simple router runtime
+ validated generated policy
+ strong external testing
+ measurable recovery
```

over continually adding heavyweight services directly to the router.

## Workstream 1 — Policy Model v3

### Problem

The current project already has strong source scoping for router management and
the printer-specific policy, but generic allowed-LAN forwarding is defined as a
host-list x port-list product, and exit-node authorization relies primarily on
Tailscale Grants plus a broad local `tailscale0 -> WAN` forwarding permission.

This is a valid layered design, but the local firewall can become a more
independent enforcement boundary.

### Target model

Represent policy as explicit source / destination / service tuples.

Example:

```text
source           destination     protocol    port
fedora-admin     router          tcp         8443
poco             printer         tcp         631
poco             printer         udp         161
fedora           nas             tcp         443
exit-user        wan             any         any
```

Possible future configuration representation:

```yaml
rules:
  - name: admin_https
    src: fedora-admin
    dst: router
    proto: tcp
    port: 8443

  - name: phone_print
    src: poco
    dst: printer
    proto: tcp
    port: 631
```

### Acceptance goals

- no accidental Cartesian-product broadening;
- each rule has an explicit source, destination and service;
- exit-node forwarding can be source-scoped locally;
- generated rules remain deterministic;
- invalid or over-broad rules are rejected before router mutation.

## Workstream 2 — Policy compiler and validation

Move complex validation away from BusyBox where practical.

Proposed flow:

```text
policy source
    ↓
offline validator / compiler
    ↓
generated deterministic router policy
    ↓
static tests
    ↓
router deployment
```

Potential checks:

- invalid addresses / ports;
- duplicate rules;
- rule shadowing;
- unexpected `0.0.0.0/0`;
- unrestricted `any:any`;
- conflicting policy;
- source groups without a known mapping;
- policy that is broader than intended Tailscale authorization.

The router should consume the simplest possible validated representation rather
than becoming the policy compiler itself.

## Workstream 3 — Tailscale Grants ↔ local firewall consistency

Add a policy-consistency check between the identity/control-plane policy and the
router's data-plane policy.

Example:

```text
Tailscale Grants        Local firewall
---------------------------------------
Fedora -> NAS:443       ALLOW
Fedora -> NAS:443       ALLOW
                       => consistent

Phone -> NAS:443        DENY
Phone -> NAS:443        ALLOW
                       => policy drift / review required
```

A mismatch is not automatically a security vulnerability because the stricter
layer may still deny the flow. It is an architectural drift signal.

The checker should classify at least:

- consistent allow;
- consistent deny;
- control-plane stricter;
- data-plane stricter;
- ambiguous / unmapped.

## Workstream 4 — Deployment manifest and runtime drift

Create a deployed-state manifest containing at minimum:

- project version;
- Git commit/revision;
- hashes of managed scripts;
- hashes of generated policy artifacts;
- firmware version;
- material package versions.

Example:

```text
project-version=...
git-commit=...
firewall-start=SHA256...
services-start=SHA256...
healthcheck=SHA256...
wan-event-handler=SHA256...
```

The health check should be able to compare expected and running state and report:

```text
DEPLOYMENT DRIFT: NONE
```

or a scoped finding such as:

```text
CRITICAL: firewall-start differs from deployed manifest
```

The repository becomes desired state; the router exposes running state.

## Workstream 5 — Kernel-level network CI

Extend repository testing beyond command mocks by building an isolated Linux
network topology with namespaces and `veth` pairs.

Conceptual topology:

```text
TAILNET namespace
        |
        v
 ROUTER namespace
      /       \
    LAN       WAN
```

Test actual kernel packet behavior for cases such as:

- authorized management succeeds;
- unauthorized management is denied;
- approved LAN service succeeds;
- unlisted service is denied;
- LAN external UDP/TCP 53 follows the intended redirect behavior;
- direct LAN TCP/853 is rejected when policy is enabled;
- exit-node forwarding obeys source policy;
- IPv6 unauthorized paths fail closed.

Mock tests remain useful for rendering and failure injection; namespace tests
prove packet behavior in a real Linux netfilter dataplane.

## Workstream 6 — Safer firewall deployment / commit-confirmed behavior

Design a bounded rollback watchdog for policy changes.

Target flow:

```text
snapshot known-good policy
        ↓
start rollback watchdog
        ↓
apply candidate
        ↓
health / management / policy checks
        ↓
confirm
        ↓
cancel rollback
```

If confirmation does not occur or validation fails, restore the previous state.

Before implementation, verify the exact behavior and availability of
`iptables-save` / `iptables-restore` or an equivalent safe mechanism on the
reference GNUton firmware.

Do not replace the current fail-closed rebuild behavior unless the new mechanism
is proven safer.

## Workstream 7 — Transactional Tailscale update

Extend the current guarded update workflow with package-level rollback.

Possible sequence:

```text
record current version
cache / preserve rollback package
backup relevant state
        ↓
upgrade
        ↓
managed service recovery
        ↓
healthcheck
        ↓
PASS -> accept
FAIL -> restore previous package
        ↓
healthcheck
```

Do not automate package mutation at boot.

## Workstream 8 — Network assurance and observability

Keep the router lightweight and export measurements to a workstation / collector.

Candidate router metrics:

- CPU and load;
- RAM / swap pressure;
- temperature;
- uptime and reboot reason where observable;
- conntrack utilization;
- WAN state;
- DNS query latency;
- Unbound cache statistics;
- Tailscale state;
- managed firewall counters;
- SSD free space / filesystem errors;
- service restart counts.

External systems can provide storage, dashboards and alerting.

Do not install heavyweight monitoring stacks on the ASUS merely to make the
project look more "enterprise".

## Workstream 9 — Evidence-backed SLI / SLO

Move from a binary health result toward measured service behavior.

Possible SLI classes:

- DNS success rate and latency;
- router readiness after boot;
- Tailscale recovery time;
- WAN reachability;
- log-delivery delay;
- backup freshness;
- storage pressure;
- packet loss and latency under load.

Do not invent production-grade targets. Establish baselines first, then define
bounded lab SLOs from measured data.

## Workstream 10 — Fault injection and recovery testing

Controlled failure scenarios:

- terminate `tailscaled`;
- terminate Unbound;
- stop the remote log collector;
- WAN down/up;
- DNS unavailable;
- delayed or missing SSD/Entware;
- missing swap where it is required;
- nearly-full filesystem;
- repeated concurrent firewall hook execution;
- reboot during degraded WAN/DNS state.

For each scenario record:

- detection;
- safe-state behavior;
- automated recovery;
- recovery time;
- residual failure;
- alert/recovery signal;
- cleanup.

Run destructive or availability-affecting tests only in a planned maintenance
window or disposable lab environment.

## Workstream 11 — Continuous attack-surface baseline

Create a repeatable service exposure matrix from multiple trust positions:

```text
WAN
LAN
guest / isolated Wi-Fi
authorized Tailscale admin
ordinary / restricted Tailscale peer
```

Correlate:

- active listeners;
- nmap results from owned/authorized clients;
- firewall counters;
- expected policy.

Example result model:

| Service | WAN | LAN | Guest | TS admin |
| --- | --- | --- | --- | --- |
| HTTPS management | denied | allowed | denied | allowed |
| SSH | denied | policy | denied | policy |
| DNS | denied | allowed | policy | allowed |
| SMB | denied | denied | denied | denied |

This should integrate with the separate Home Lab Attack Surface & Vulnerability
Assessment rather than duplicate it.

## Workstream 12 — IPv6 assurance

The current fail-closed Tailscale IPv6 guard is a good interim design.

Two acceptable future outcomes:

1. implement and validate a granular IPv6 policy equivalent in intent to IPv4;
2. retain a deliberately disabled / blocked IPv6 path and continuously verify
   that no uncontrolled IPv6 route exists.

A real IPv6 implementation must explicitly account for:

- ICMPv6;
- Neighbor Discovery;
- router advertisements;
- DNS behavior;
- Tailscale IPv6;
- management access;
- LAN forwarding;
- WAN policy;
- encrypted-DNS bypass paths.

Do not treat IPv6 as a mechanical translation of IPv4 rules.

## Workstream 13 — WLAN assurance and performance

Build on the
[LAN / Wi-Fi Performance & Latency Benchmark Lab](../lan-wifi-performance-latency-benchmark/README.md)
instead of duplicating its test matrix or evidence here.

The benchmark owns the client capability checks, 80/160 MHz A/B methodology,
iperf3 measurements and optional application-level validation. This roadmap owns
only the architectural question: which WLAN assurance signals should eventually
be exposed, validated or monitored by the active ASUS project.

Record where available:

- band / channel;
- channel width;
- DFS state;
- RSSI;
- noise / SNR;
- PHY rate;
- MCS;
- NSS;
- retry rate;
- channel utilization;
- disconnects / reassociations;
- LAN latency and jitter;
- latency under load.

Use the same-client / same-server methodology whenever possible.

A current controlled validation showed that configured 160 MHz state and
operational radio width can diverge. Treat configured state, runtime AP state
and client association as separate evidence layers. Keep raw operational
evidence in the active ASUS implementation repository after sanitization rather
than turning this incubator roadmap into a second source of truth.

## Workstream 14 — Bufferbloat / QoS assessment

Measure latency before and during link saturation.

Test classes:

```text
Ethernet
Wi-Fi
Tailscale subnet routing
Tailscale exit node
```

For each path:

- idle RTT;
- upload saturation RTT;
- download saturation RTT;
- packet loss;
- throughput;
- CPU load.

Only evaluate QoS/SQM changes after obtaining a clean baseline and confirming
that the reference firmware exposes a controllable, reversible mechanism.

## Workstream 15 — Trust-zone evolution

The current platform does not provide the same clean segmentation model as a
dedicated firewall plus managed switching.

Do not force an enterprise VLAN architecture onto the ASUS solely for portfolio
appearance.

Long-term target:

```text
OPNsense / x86 edge
        |
 managed switch
        |
        +-- management
        +-- trusted
        +-- IoT
        +-- lab
        +-- guest
```

The ASUS can then remain an access point or secondary lab node.

## Ordered implementation path

Recommended order:

1. **Policy Model v3**
   - explicit source/destination/service tuples;
   - source-scoped exit-node forwarding.
2. **Policy consistency**
   - Tailscale Grants ↔ local firewall checker.
3. **Deployment drift**
   - deployed manifest and hash verification.
4. **Kernel network CI**
   - namespace/veth packet tests.
5. **Resilience**
   - commit-confirmed style firewall rollback;
   - transactional Tailscale update.
6. **Observability**
   - metrics export, SLI and later evidence-backed SLO.
7. **Fault injection**
   - controlled failure/recovery measurements.
8. **WLAN / QoS**
   - 80/160 MHz assurance and bufferbloat.
9. **IPv6**
   - granular policy or continuously verified fail-closed state.
10. **Architecture migration**
   - OPNsense / VLAN / IDS work only after the ASUS design reaches its sensible
     platform ceiling.

## MVP

A first architecture-maturity iteration should stop after:

- source-scoped explicit policy tuples;
- a policy consistency checker;
- deployment manifest / drift detection;
- one namespace-based kernel packet test suite.

This is enough to materially improve the engineering quality of the project
without adding operational risk to the reference router.

## Promotion criterion

Do not create a separate implementation repository for this roadmap. Promote
individual workstreams directly into the active ASUS project only when:

- the design is bounded;
- rollback exists;
- CI/static validation exists first where practical;
- live deployment is necessary and scheduled;
- evidence requirements are defined;
- the change does not overload the reference router merely to demonstrate a
  technology.

The final architectural ceiling for the ASUS project is reached when further
improvement primarily requires hardware features the platform does not provide,
such as clean multi-zone VLAN segmentation, stronger IDS/IPS capacity,
redundancy or higher sustained inspection throughput. At that point, move the
enforcement role to a dedicated x86 edge instead of continuing to stretch the
consumer router.
