# Android Ad / Tracker Blocking Comparative Lab

**Status:** concept / comparative privacy lab

## Goal

Compare several materially different ad- and tracker-blocking layers on Android
instead of comparing multiple tools that all use the same mechanism.

The lab should measure not only whether ads disappear, but also:

- which network requests are actually prevented;
- where in the stack blocking occurs;
- which trackers remain reachable;
- DNS / IP / connection evidence;
- page-load impact;
- CPU / RAM / battery cost where practical;
- false positives and site/app breakage;
- interaction with Tailscale and the existing ASUS DNS/filtering stack.

The primary endpoint is the hardened/debloated POCO Android device. Treat this
as a **post-hardening case study**, not as a factory-vs-debloated before/after
comparison unless equivalent pre-hardening evidence exists.

## Scope ownership

This lab owns **comparative blocking efficacy and trade-offs between blocking
layers**:

- browser-native blocking;
- browser Content Blocker API;
- Android local-VPN filtering;
- router/network-side filtering.

Generic endpoint telemetry classification and DNS resolver-bypass methodology
belong in
[Privacy & Telemetry Audit](../privacy-telemetry-audit/README.md).

Tailscale-specific DNS/routing recovery across handovers belongs in
[Tailscale Android DNS Regression Lab](../tailscale-android-dns-regression-lab/README.md).

The labs may reuse sanitized evidence, but they should not duplicate the same
measurement as separate project results.

## Main comparison set

### 1. Brave Shields

Role: browser-native reference.

Use Brave as the normal browsing baseline because it blocks within the browser
without consuming Android's VPN slot.

Measure:

- ads and trackers blocked on selected test pages;
- DNS/network destinations still contacted;
- page-load timing;
- breakage / false positives;
- interaction with router-side DNS filtering.

### 2. Adblock Fast vs AdGuard Content Blocker

Role: browser Content Blocker API comparison.

Use Samsung Internet as a controlled host browser and compare:

- no blocker;
- Adblock Fast;
- AdGuard Content Blocker.

This is a useful apples-to-apples test because both products integrate through
the browser's content-blocking API rather than Android's local VPN mechanism.

For Adblock Fast, additionally inspect the application's own background traffic.
The current Android code contains integrations for crash reporting,
notifications/analytics and background services, so test its **self-telemetry**
instead of assuming that an ad blocker is itself network-silent.

### 3. TrackerControl

Role: application-tracker analysis and evidence collection.

Use TrackerControl to inspect actual app-generated traffic and correlate:

```text
application
-> contacted domain / endpoint
-> tracker classification
-> allowed / blocked
-> frequency / timing
```

Particularly useful scenarios:

- idle;
- reboot/startup;
- selected Xiaomi/system app;
- browser / WebView / Custom Tab;
- normal interactive use.

TrackerControl uses Android `VpnService`, therefore it cannot run concurrently
with a separately active Tailscale VPN session. Treat this as a controlled test
phase rather than a permanent configuration.

### 4. Rethink DNS + Firewall

Role: on-device DNS, firewall and connection-monitor reference.

Interesting capabilities to evaluate:

- per-app firewalling;
- DNS filtering;
- domain/IP rules;
- encrypted DNS options;
- connection logging;
- routing / WireGuard-related capabilities.

Compare on-device enforcement against the existing router-side DNS/filtering
architecture.

Like TrackerControl, Rethink uses Android's VPN slot in its normal firewall
mode, so coexistence with a separate Tailscale VPN must be tested explicitly
rather than assumed.

### 5. ASUS / network-side filtering

Role: network-side reference that does not require an Android local VPN.

Use the existing ASUS DNS/filtering stack as a baseline for what can be blocked
before traffic leaves the LAN.

Compare:

```text
browser-native blocking
vs browser Content Blocker API
vs Android local-VPN filtering
vs router-side DNS filtering
```

This is important because each layer has different visibility and different
bypass paths.

## Optional comparison tools

### NetGuard

Useful primarily as a firewall / evidence tool rather than as another generic
ad blocker.

Potential experiments:

- hosts-based blocking;
- per-app connection logging;
- PCAP export where available;
- Wi-Fi vs mobile behavior;
- verify the documented limitations around wired Ethernet / USB networking on
  the POCO USB-C Ethernet path.

### AdAway

Useful as a classic hosts/local-VPN reference.

Do not prioritize it over TrackerControl or Rethink unless a simpler baseline
is needed.

### Blokada 5

Useful as another maintained on-device VPN blocker.

Keep optional because it overlaps significantly with the local-VPN blocking
class already represented by Rethink / TrackerControl.

### personalDNSfilter

Interesting because it supports both VPN-style operation and a local DNS proxy
mode. Potentially useful later for experiments involving another VPN, but it is
not required for the MVP.

### DNS66

Historical reference only. The upstream repository is archived, so do not use
it as a primary modern comparison target.

## Core experimental matrix

Use a small set of repeatable scenarios:

```text
A. Brave + router filtering
B. Brave without router ad filtering where safely isolated
C. Samsung Internet, no content blocker
D. Samsung Internet + Adblock Fast
E. Samsung Internet + AdGuard Content Blocker
F. TrackerControl test phase
G. Rethink test phase
H. router-side filtering only
```

Not every scenario needs to run concurrently. In particular, local-VPN based
tools should be evaluated in separate controlled phases.

## Measurement model

For each run record:

- Android build and app versions;
- active transport: Wi-Fi / USB-C Ethernet / LTE/5G;
- active VPN state;
- active DNS resolver path;
- router filtering state;
- page/app scenario;
- elapsed load/start time;
- DNS destinations;
- TCP/UDP destinations where observable;
- blocked / allowed request count where the tool exposes it;
- visual ad result;
- functional breakage;
- CPU / RAM / battery delta where practical;
- notes on limitations.

Use the same target pages/apps and comparable timing windows.

## Evidence sources

Possible evidence:

- router dnsmasq / Unbound / filtering logs;
- packet capture on the LAN/router where appropriate;
- Android `adb` diagnostics;
- TrackerControl logs / CSV export;
- Rethink connection logs;
- NetGuard PCAP/logs if used;
- browser developer diagnostics where available;
- screenshots only as supporting evidence, not as proof of network blocking.

## High-value questions

The lab should answer questions such as:

1. How much additional blocking does Brave provide beyond router-side DNS
   filtering?
2. How much more effective is a browser content-blocking API than DNS-only
   filtering for cosmetic and first-party ad delivery?
3. Which application trackers remain after the phone's current hardening?
4. Which requests are blocked only by the Android local-VPN layer?
5. Does any blocker create notable self-telemetry of its own?
6. What breaks when aggressive filtering is enabled?
7. How do results change when moving from Wi-Fi to USB-C Ethernet or LTE/5G?
8. How does use of the Android VPN slot interact with Tailscale?

## Suggested MVP

1. Establish a fixed browser test set.
2. Capture a Brave + ASUS baseline.
3. Compare Samsung Internet with no blocker, Adblock Fast and AdGuard Content
   Blocker.
4. Run one TrackerControl telemetry session on selected apps.
5. Run one Rethink DNS/firewall session.
6. Preserve DNS/connection evidence and record false positives.
7. Write a short comparison focused on blocking layer, evidence and trade-offs,
   not on subjective UI preference.

## Promotion criterion

Promote this idea to a standalone case-study repository when:

- at least three fundamentally different blocking layers have been tested;
- results are backed by network evidence rather than screenshots alone;
- Tailscale/VPN-slot interactions are documented;
- self-telemetry of the tested blockers is considered;
- one repeatable browser scenario and one repeatable app-telemetry scenario are
  documented;
- limitations and bypass paths are stated explicitly.
