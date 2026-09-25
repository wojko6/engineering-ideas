# GeForce NOW Packet-Loss Correlation Lab

**Status:** concept / diagnostic lab

## Goal

Locate where intermittent real-time packet loss appears instead of relying only
on the GeForce NOW overlay or hop-by-hop ICMP.

## Proposed capture path

Normal wired path:

```text
GeForce NOW
-> Internet
-> ASUS ppp0
-> ASUS br0
-> Fedora eno1
```

Exit Node path adds:

```text
Fedora tailscale0
-> ASUS tailscale0
-> ASUS ppp0
```

## Method

When the symptom is reproduced:

- capture the same stream concurrently at client and router boundaries;
- identify the actual GFN UDP flow;
- compare packet counts, timestamps and sequence information where available;
- correlate application-visible loss with interface/capture evidence;
- use mtr/traceroute only as supporting context, not as packet-loss proof.

## Why

A missing packet on the client does not by itself tell whether it was lost on
Wi-Fi/LAN, the router, ISP path or service side.

## Promotion criterion

Promote to an active diagnostic project when the intermittent loss can be
reproduced often enough to justify synchronized captures.
