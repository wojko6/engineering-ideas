# GeForce NOW Packet-Loss Correlation Lab

**Status:** concept / diagnostic lab

## Goal

Locate where intermittent real-time packet loss appears instead of relying only
on the GeForce NOW overlay or hop-by-hop ICMP.

This idea is intentionally **symptom-driven**. It should become active only when
packet loss is reproducible often enough to justify synchronized capture and
correlation.

## Scope boundary

This lab owns:

- synchronized packet capture around a reproducible GFN loss event;
- localization of missing/delayed packets across client, LAN/router and WAN
  boundaries;
- correlation between application-visible loss and packet evidence.

It does **not** own the general 80 MHz vs 160 MHz Wi-Fi performance comparison.
That work belongs in
[LAN / Wi-Fi Performance & Latency Benchmark Lab](../lan-wifi-performance-latency-benchmark/README.md).

A controlled GFN 80/160 comparison may be used there as an optional
application-level validation after the LAN benchmark is complete. That does not
turn ordinary latency differences into packet-loss localization evidence.

## Proposed capture path

Normal wired path:

```text
GeForce NOW
-> Internet
-> ASUS WAN
-> ASUS LAN bridge
-> client
```

Exit-node path adds:

```text
client Tailscale interface
-> ASUS Tailscale interface
-> ASUS WAN
```

Use abstract interface roles in public documentation unless the exact interface
name is both necessary and safe to publish.

## Method

When the symptom is reproduced:

- identify the actual GFN UDP flow;
- capture the same stream concurrently at client and router boundaries;
- compare packet counts, timestamps and sequence information where available;
- correlate application-visible loss with interface/capture evidence;
- note Wi-Fi/Ethernet access state and channel width as context;
- use mtr/traceroute only as supporting context, not as packet-loss proof.

## Interpretation discipline

A missing packet on the client does not by itself tell whether it was lost on
Wi-Fi/LAN, the router, ISP path or service side.

Likewise:

- a clean LAN iperf3 result does not prove the Internet path is healthy;
- a GFN overlay value does not identify the loss location;
- ICMP loss on an intermediate hop does not automatically prove forwarding loss;
- a difference between 80 MHz and 160 MHz does not prove the Wi-Fi width caused
  an Internet-side event.

## Evidence

For a useful incident preserve, after sanitization:

- timestamp and test duration;
- client access path;
- GFN stream statistics;
- capture points;
- flow identification method;
- packet-count/timestamp correlation;
- router/client state relevant to the event;
- limitations and any unsynchronized evidence.

Raw packet captures, real deployment addresses, MAC addresses and unrelated
traffic must follow [PUBLICATION.md](../../PUBLICATION.md) and should normally
remain in the implementation/evidence repository rather than this incubator.

## Promotion criterion

Promote to an active diagnostic project when:

- the intermittent symptom is reproducible;
- synchronized captures can be collected safely;
- the same GFN flow can be identified at more than one boundary;
- the result can distinguish at least local-path loss from downstream
  uncertainty without overstating what the captures prove.
