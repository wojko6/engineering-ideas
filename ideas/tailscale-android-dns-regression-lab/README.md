# Tailscale Android DNS Regression Lab

**Status:** concept / investigation

## Goal

Create a reproducible Android lab for diagnosing Tailscale DNS failures and
route/DNS interactions instead of treating each phone issue as an isolated
incident.

## Scope ownership

This lab owns **Tailscale-specific recovery and regression behavior**:

- DNS failures while Tailscale is active;
- subnet-route / exit-node recovery;
- transport handover and resume;
- time to recover tunnel, routes and DNS;
- whether manual intervention is required.

Generic DNS enforcement / resolver-bypass testing across Android transports
belongs in
[Privacy & Telemetry Audit](../privacy-telemetry-audit/README.md).

Raw Wi-Fi throughput and 80/160 MHz transport benchmarking belongs in
[LAN / Wi-Fi Performance & Latency Benchmark Lab](../lan-wifi-performance-latency-benchmark/README.md).

Reuse those transport states when useful, but keep the outcome here focused on
Tailscale recovery rather than duplicating the network benchmark.

## Candidate scope

- stock/stable vs beta/custom Tailscale client;
- Android Private DNS;
- NextDNS interaction;
- TUN/VPN routing;
- overlapping local/Tailscale subnet routes;
- ADB-based controlled tests;
- custom APK builds when needed;
- upstream-fix verification.

## Toolchain

Potentially:

```text
Git
Gradle
Go
ADB
Android device/emulator
packet/routing diagnostics
```

## Evidence goal

A case should be reproducible as:

```text
known starting state
-> one controlled variable
-> observable routing/DNS result
-> rollback
```

## Promotion criterion

Promote when one previously observed DNS failure can be reproduced and isolated
with a bounded A/B test.


## High-value mobile extension — transport handover and resume

Use a real Android device to measure how Tailscale, routing and DNS recover
when the phone changes access networks without changing the application state.

Test transitions:

```text
Wi-Fi -> LTE/5G
LTE/5G -> Wi-Fi
Wi-Fi -> USB-C Ethernet
USB-C Ethernet -> Wi-Fi
```

Also include a sleep/resume variant with the screen off for controlled
intervals before rechecking connectivity.

Record:

- time until the Tailscale peer/path is usable again;
- time until DNS resolution succeeds again;
- whether the intended exit node or subnet route is restored;
- packet loss and latency during the transition;
- whether Private DNS or resolver selection changes unexpectedly;
- whether manual intervention is required.

Keep each transition as a bounded A/B sequence with the same phone, Tailscale
configuration and target services. This can become a separate case study if
the behavior is repeatable and produces meaningful recovery evidence.
