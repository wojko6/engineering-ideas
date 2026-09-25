# Tailscale Android DNS Regression Lab

**Status:** concept / investigation

## Goal

Create a reproducible Android lab for diagnosing Tailscale DNS failures and
route/DNS interactions instead of treating each phone issue as an isolated
incident.

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
