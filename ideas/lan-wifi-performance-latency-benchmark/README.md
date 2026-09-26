# LAN / Wi-Fi Performance & Latency Benchmark Lab

**Status:** validated baseline / deferred follow-up  
**Primary tool:** iperf3  
**Optional application-level validation:** GeForce NOW / Xbox Cloud Gaming

## Goal

Build a repeatable local-network benchmark that separates local LAN/Wi-Fi
behavior from Internet and cloud-service variability.

The lab measures:

- TCP throughput;
- reverse-direction throughput;
- multi-stream behavior;
- UDP jitter and packet loss;
- idle latency;
- latency under load;
- Wi-Fi PHY / channel-width behavior;
- repeatability across Ethernet, Wi-Fi 6 / 80 MHz and Wi-Fi 6 / 160 MHz.

## Scope ownership

This document is the source of truth inside the incubator for:

- Ethernet vs Wi-Fi transport benchmarking;
- 80 MHz vs 160 MHz comparisons;
- client capability and association validation;
- Wi-Fi latency / jitter / packet-loss measurements;
- latency under load;
- optional cloud-gaming comparison used only as an application-level
  validation layer.

It does **not** own intermittent GeForce NOW packet-loss localization. That
symptom-driven investigation remains in
[GeForce NOW Packet-Loss Correlation Lab](../gfn-packet-loss-correlation-lab/README.md).

Router architecture decisions remain in
[ASUS Edge Architecture Maturity Roadmap](../asus-edge-architecture-maturity-roadmap/README.md).

## Recommended topology

```text
          wired iperf3 server
                  |
                ASUS
                  |
        Wi-Fi 6 test client
```

The server should be connected to the ASUS by Ethernet. Do not use the ASUS
router itself as the primary iperf3 server for the main comparison because that
can turn the test into a router-CPU benchmark.

Use the same server, same client position and same test commands when comparing
80 MHz with 160 MHz.

## Current validated client capability

### Lenovo Legion 5 15ACH6H / Fedora

Adapter:

```text
Realtek RTL8852AE
rtw89_8852ae
```

Observed capability:

- Wi-Fi 6 on 5 GHz;
- HE40 / HE80;
- 2 spatial streams;
- no validated 160 MHz support on the current adapter/driver path.

Use this client as an **80 MHz reference**, not as a 160 MHz test endpoint.

### Acer Aspire 17 / Windows / MediaTek MT7922

Observed in the current controlled session:

- MediaTek Wi-Fi 6E MT7922 160 MHz adapter;
- 5 GHz / 802.11ax;
- 2x2;
- live 160 MHz association confirmed by AP telemetry;
- Windows reported 2402 / 2402 Mb/s PHY at 160 MHz under strong-signal
  conditions.

The same client previously associated at 80 MHz and approximately 1201 /
1201 Mb/s PHY, making it the preferred same-endpoint A/B client.

### POCO F8 Pro

Observed in the current controlled session:

- live 5 GHz association;
- HE-capable 2x2 client;
- 160 MHz association confirmed by AP telemetry.

The phone can therefore be used for the planned same-device transport matrix,
provided each run records the live association instead of relying on product
specifications.

## Current router-side 160 MHz finding

The ASUS accepted a configured 160 MHz chanspec while the operational radio
remained at 80 MHz.

Sanitized observation:

```text
configured state:  100/160
operational state: 100/80
DFS state:         in-service monitoring / cleared
client association: 80 MHz
```

A controlled, temporary test changed the `bw_switch_160` family of NVRAM
settings from `2` to `0` without committing them permanently, followed by a
wireless restart.

The observed result was:

```text
configured state:  100/160
operational state: 100/160
client association: 160 MHz
Acer PHY:           2402 / 2402 Mb/s
```

This is evidence that the `bw_switch_160` mechanism is involved in the
80-to-160 MHz runtime behavior on the tested firmware state.

It is **not yet evidence that one specific NVRAM key is individually causal**
because three related keys were changed together. A later isolation test may
vary one key at a time if that result is needed.

Do not treat the temporary setting as the permanent configuration until
stability, DFS behavior and comparative performance are measured.

## Active test matrix

### Phase A — 160 MHz baseline

Keep the currently validated 160 MHz state and capture:

- AP chanspec;
- DFS state;
- client channel width;
- RSSI;
- PHY rate;
- MCS / NSS where available;
- retry counters where available.

Then run:

```bash
iperf3 -c SERVER_IP -t 30
iperf3 -c SERVER_IP -P 4 -t 30
iperf3 -c SERVER_IP -R -t 30
iperf3 -c SERVER_IP -R -P 4 -t 30
```

Repeat each measurement at least three times for the final dataset.

### Phase B — latency and jitter

Record idle latency first:

```bash
ping -i 0.2 SERVER_IP
```

Then repeat the same ping while iperf3 is saturating the path.

Optional UDP controlled-load test:

```bash
iperf3 -c SERVER_IP -u -b 100M -t 30
```

Increase UDP load gradually rather than jumping directly to the estimated link
ceiling.

Record:

- achieved bitrate;
- jitter;
- lost / total datagrams;
- loss percentage;
- idle RTT;
- loaded RTT;
- notable spikes.

### Phase C — return to 80 MHz

Restore the previous router bandwidth-switch behavior in a controlled way and
verify that the same Acer client returns to 80 MHz.

Do not begin the 80 MHz measurement set until runtime state is confirmed by both
AP and client telemetry.

Repeat the exact Phase A and Phase B commands.

### Phase D — optional application-level validation

After the LAN A/B comparison is complete, optionally compare GeForce NOW on the
same Acer at 80 MHz and 160 MHz.

Keep as many variables fixed as practical:

- same client;
- same physical position;
- same GFN region/server where possible;
- same stream settings;
- comparable test duration;
- similar background traffic.

Record application-visible:

- latency;
- packet loss;
- frame loss;
- jitter / instability indicators where exposed;
- stream bitrate / quality indicators.

This phase answers whether the higher local PHY / LAN performance produces a
meaningful application-level difference. It must not be used to attribute
Internet-side loss to Wi-Fi.

## Current validated outcome

The initial HE80/HE160 investigation is complete enough to support a bounded
case study.

The current validated comparison established that:

- the Acer MT7922 performs strongly at HE80;
- the same client shows severe, direction-dependent throughput degradation at
  HE160;
- updating the Windows MT7922 driver improved the HE160 symptom but did not
  remove it;
- an independent Android 2x2 client achieved substantially higher throughput on
  the same ASUS HE160 radio;
- the ASUS/Broadcom station retry-related counters must not be interpreted
  one-to-one as TCP retransmissions.

The public case study is maintained in the implementation repository:

[Wi-Fi 6 HE160 Interoperability – MediaTek MT7922 vs ASUS/Broadcom](https://github.com/wojko6/Advanced-ASUS-Edge-Gateway-ZTNA-Infrastructure/blob/main/docs/wifi6-he160-mt7922-interoperability-case-study.md)

The incubator remains the place for follow-up experiments that are not yet
necessary to support the current published claim.

## Deferred follow-up – Fedora Live MT7922 isolation test

Do **not** install Linux on the Acer for this experiment.

When the investigation is resumed, boot Fedora Workstation from a Live USB and
use the live environment only. The Windows installation should remain
untouched.

Purpose:

- keep the same MT7922 hardware and ASUS/Broadcom AP;
- replace the Windows driver/software path with the Linux MT7922 driver path;
- determine whether the severe HE160 throughput degradation reproduces under
  Fedora Live.

Before any benchmark, capture:

```bash
lspci -nnk | grep -A4 -i network
iw dev
iw dev <interface> link
iw dev <interface> station dump
```

Confirm that the client is actually associated at 160 MHz and record:

- Linux kernel version;
- active kernel driver;
- firmware identity when available;
- channel width;
- NSS;
- RSSI;
- PHY rate.

Then repeat the same 120-second four-stream TCP pair used in the published case:

```bash
iperf3 -c SERVER_IP -t 120 -P 4
iperf3 -c SERVER_IP -t 120 -P 4 -R
```

Keep the same wired server, AP, channel-width state and approximately the same
client position.

Interpretation boundary:

- if Fedora Live produces high HE160 throughput while Windows remains poor, the
  evidence would shift strongly toward the Windows driver/software path;
- if Fedora Live reproduces the severe HE160 degradation, suspicion would shift
  away from a Windows-only explanation and toward MT7922 firmware/hardware
  behavior or MT7922 ↔ ASUS/Broadcom interoperability;
- neither outcome by itself proves a universal MediaTek or Broadcom defect.

If this follow-up materially changes the fault-domain assessment, update the
published ASUS Edge case study with a dated Linux comparison section rather than
creating a competing case study here.

## POCO same-device extension

Planned paths:

```text
POCO F8 Pro -> USB-C Ethernet adapter -> ASUS/LAN
POCO F8 Pro -> 5 GHz Wi-Fi -> 80 MHz
POCO F8 Pro -> 5 GHz Wi-Fi -> 160 MHz
```

Purpose:

- obtain a wired latency/stability reference on the same endpoint;
- compare LAN latency, jitter and packet loss;
- run local iperf3 TCP/UDP tests against the same wired server;
- measure latency under load;
- optionally reuse the same transport states in later Tailscale/DNS work.

The Ethernet path is a reference path, not an assumed throughput ceiling.
Record the negotiated Ethernet/USB link and measured performance.

## Evidence discipline

For every accepted run record:

```text
date/time
client role and public model
OS / driver identity
client interface
server role
router/AP model
Wi-Fi band
control channel
channel width
DFS state
RSSI
PHY rate
MCS / NSS where available
iperf3 command
iperf3 result
ping/latency sample
system/background-load notes
```

Prefer `iperf3 --json` for machine-readable results.

Example:

```bash
iperf3 -c SERVER_IP -t 30 --json > wifi160-tcp-forward-run01.json
```

Raw evidence containing real addresses, MAC addresses, hostnames or unrelated
private data must remain outside this public incubator or be sanitized according
to [PUBLICATION.md](../../PUBLICATION.md).

## Acceptance criteria

The first complete case study should contain:

- a validated 80 MHz state on the Acer;
- a validated 160 MHz state on the same Acer;
- at least 3 TCP forward runs per state;
- at least 3 TCP reverse runs per state;
- at least 3 parallel-stream runs per state;
- at least 3 UDP runs at a controlled bitrate per state;
- idle latency samples;
- latency-under-load samples;
- AP/client telemetry proving the channel width used for each dataset;
- limitations and uncontrolled variables.

The result should distinguish:

```text
PHY capability
!=
real LAN throughput
!=
Internet latency
!=
cloud-gaming application behavior
```

## Promotion criterion

Promote this concept into a standalone benchmark/case-study repository when:

- the 80/160 MHz A/B matrix is repeatable;
- wired and wireless results use a consistent evidence format;
- latency-under-load behavior is documented;
- the router-side 160 MHz runtime behavior is documented without overclaiming
  causality;
- the methodology is stable enough to rerun after router, firmware or client
  changes.
