# Secure Mobile Grafana Access over Tailscale

**Status:** parked / event-driven mobile access idea

## Goal

Provide secure access to the self-hosted Grafana dashboards from Android without
publishing Grafana to the public Internet.

The current reference Grafana deployment is intentionally loopback-only on the
Fedora workstation and is fronted locally by Caddy.

Current local operator path:

```text
https://grafana.home.arpa/
```

Current backend path:

```text
127.0.0.1:443 Caddy
 -> 127.0.0.1:3000 Grafana
```

Any mobile-access design must preserve the existing principle that monitoring
services are not exposed broadly to LAN or WAN by default.

## Current upstream constraint

As of 2026-09-28, Grafana's official mobile documentation describes the Android
and iOS application as a Grafana Cloud client. The documented sign-in flow
requires a Grafana Cloud account/stack.

Therefore, do not assume the native mobile app can connect directly to the
current self-managed Grafana OSS instance.

The first practical self-hosted path should be evaluated through the Android
browser over Tailscale.

Re-evaluate the native mobile application later if Grafana adds documented
self-managed Grafana support.

## Candidate architecture

Initial concept:

```text
Android phone
 -> Tailscale
 -> Fedora Tailscale interface
 -> Caddy HTTPS
 -> Grafana on 127.0.0.1:3000
```

The preferred design should avoid:

- public Internet exposure;
- generic LAN exposure;
- binding Grafana itself to all interfaces;
- bypassing Grafana authentication;
- weakening the existing local HTTPS setup merely to make mobile access easier.

## DNS / naming

The current local name `grafana.home.arpa` is appropriate for local use but
does not automatically become a remote Tailscale name.

Possible approaches to evaluate:

- Tailscale split DNS for a private Grafana name;
- a MagicDNS-compatible hostname;
- a dedicated private name that resolves only inside the tailnet.

Do not publish the monitoring hostname through public DNS unless there is a
separate, justified design for that.

## TLS options to compare

The mobile path needs a certificate model that the Android client can validate.

Candidates:

1. continue using Caddy internal PKI and install only the public root CA on the
   trusted Android device;
2. use a tailnet/private certificate path if the selected naming model supports
   it cleanly;
3. keep the current local `home.arpa` path separate and create a second,
   Tailscale-only HTTPS listener/name.

The private CA key must remain private and must never be copied to the phone.

## Access controls

Minimum acceptance controls:

- listener bound only to the intended Tailscale interface/address;
- no WAN listener;
- no broad LAN listener unless separately justified;
- Tailscale ACL/Grants restricted to the intended user/device;
- Grafana authentication remains enabled;
- no anonymous dashboard access;
- no credentials embedded in URLs or mobile shortcuts.

Optional hardening:

- source-specific host firewall rule;
- dedicated Grafana Viewer account for phone use;
- shorter mobile session lifetime;
- read-only dashboard permissions where practical.

## Mobile usability test

If activated, validate at least:

- Android over home Wi-Fi with Tailscale active;
- Android over LTE/5G with Tailscale active;
- dashboard load time;
- panel readability in portrait and landscape;
- refresh behavior;
- login persistence;
- alert page usability;
- no certificate warnings;
- no loss of desktop/local access;
- access fails when Tailscale is disconnected.

## Alerting follow-up

A separate optional follow-up is phone notification delivery.

Do not assume the self-hosted Grafana OSS deployment can use the official
Grafana mobile-app push path.

Possible future options:

- Grafana-supported mobile push if self-managed support appears;
- a supported notification contact point;
- a separate self-hosted notification relay;
- browser-based access only, with notifications left outside scope.

## Rollback

The first implementation must be easy to remove:

- delete the Tailscale-only Caddy listener/name;
- remove its private DNS entry;
- remove the host-firewall rule;
- remove the Tailscale ACL/Grant;
- remove the Android trust anchor if one was installed specifically for this
  test.

The existing loopback-only `grafana.home.arpa` path must continue to work
unchanged after rollback.

## Acceptance boundary

Possible outcomes:

```text
MOBILE ACCESS ACCEPTED
BROWSER-ONLY ACCEPTED
NATIVE APP NOT SUPPORTED
REQUIRES REDESIGN
```

Do not call the mobile path secure merely because it works remotely. Acceptance
requires verified interface binding, firewall/access policy, TLS validation and
negative testing with Tailscale disabled.

## Promotion criterion

Promote this idea into the active ASUS observability project when remote mobile
dashboard access becomes operationally useful and the current Grafana/issue
#108 work is otherwise stable.
