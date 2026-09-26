# Privacy & Telemetry Audit

**Status:** concept

## Goal

Build a repeatable method for measuring what a workstation, browser or mobile
device contacts during controlled scenarios.

## Scope ownership

This idea owns the **generic telemetry and resolver-path methodology**:

- what an endpoint contacts during a controlled scenario;
- which DNS path is actually used;
- resolver bypass / enforcement behavior across transports;
- post-hardening Android telemetry correlation.

It does not own product-by-product blocker efficacy. Comparative ad/tracker
blocking belongs in
[Android Ad / Tracker Blocking Comparative Lab](../android-ad-tracker-blocking-comparative-lab/README.md).

Tailscale-specific handover, resume and DNS/routing recovery belongs in
[Tailscale Android DNS Regression Lab](../tailscale-android-dns-regression-lab/README.md).

## Candidate scenarios

- idle;
- startup/reboot;
- browser launch;
- selected application use;
- normal interactive use;
- hardened vs less-hardened configuration.

## Evidence

Potential sources:

- DNS logs;
- packet captures;
- endpoint/process context;
- destination classification;
- request frequency;
- blocked vs allowed destinations.

## Important boundary

Different devices, OS versions or app sets must not be presented as a strict
before/after experiment unless the variables are actually controlled.

## Promotion criterion

Promote when one scenario can be captured, sanitized and reproduced with a
clear evidence schema.


## High-value mobile extension — DNS enforcement / resolver bypass matrix

Use the Android device to test which DNS path is actually used under controlled
network and resolver settings.

Candidate matrix:

```text
home Wi-Fi
USB-C Ethernet
LTE/5G
LTE/5G + Tailscale
Wi-Fi + Tailscale
```

For each path, compare normal Android DNS with selected Private DNS / DoT,
application-level encrypted DNS where explicitly controllable, and the
project-owned router/Tailscale DNS policy.

Record:

- observed resolver destination;
- whether classic DNS is intercepted as intended;
- whether DoT/DoH or VPN-carried DNS bypasses router policy;
- DNS leak-test result;
- IPv4/IPv6 differences where available;
- rollback and expected behavior after each test.

Do not claim universal encrypted-DNS enforcement from one application or one
transport. Scope every result to the tested resolver mode and path.

## High-value mobile extension — controlled Android telemetry correlation

Use the hardened/debloated Android phone as a repeatable telemetry endpoint.

Controlled scenarios should include:

- idle period;
- reboot/startup;
- selected system-app use;
- browser or WebView / Custom Tab activity;
- normal interactive use;
- optional comparison of Wi-Fi, Ethernet and LTE/5G + Tailscale paths.

Correlate DNS destinations and packet-level timing with the scenario window.
Record request frequency, blocked vs allowed destinations, vendor/advertising/
telemetry classifications and any path-dependent differences.

The purpose is not to label every remote endpoint as telemetry. Keep
classification evidence-backed, sanitize identifiers and avoid publishing raw
browsing history or private hostnames.
