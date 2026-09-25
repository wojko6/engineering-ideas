# LAN / Wi-Fi Performance & Latency Benchmark Lab

**Status:** concept / benchmark lab  
**Primary tool:** iperf3  
**Optional reference tool:** jPerf / iperf2 where a legacy GUI view is useful

## Goal

Build a repeatable local-network benchmark that compares wired Ethernet and
Wi-Fi 6 on the same ASUS-based home network without confusing LAN performance
with Internet or cloud-service variability.

The lab should measure:

- TCP throughput;
- reverse-direction throughput;
- multi-stream behavior;
- UDP jitter;
- UDP packet loss;
- latency under load;
- repeatability across Ethernet and Wi-Fi 6.

## Recommended topology

```text
          wired iperf3 server
                  |
                ASUS
               /    \
       Ethernet      Wi-Fi 6
           |            |
        client        client
        Fedora        Fedora
```

The preferred server is a separate computer connected by Gigabit Ethernet.

The current reference client is the Lenovo Legion 5 15ACH6H running Fedora
with a Realtek RTL8852AE adapter and the `rtw89_8852ae` driver. The live
capability report advertises Wi-Fi 6 on 5 GHz with `HE40/HE80/5GHz`, 2 spatial
streams for HE RX/TX up to 80 MHz, and explicitly reports `neither 160 nor
80+80` for VHT channel width. Therefore the current Legion baseline is
**80 MHz**, not 160 MHz.

A future 160 MHz comparison is valid only with a different client/adapter and
driver state that actually advertises HE 160 MHz. It must be recorded as a
separate client capability rather than assumed from the router specification.

Do not use the ASUS router itself as the primary iperf3 server for the main
comparison. Doing so could turn the test into a router-CPU benchmark rather
than a clean LAN/Wi-Fi transport benchmark.

## Why iperf3 instead of jPerf

jPerf is a graphical front end built around iperf2 and is useful mainly as a
legacy visualization tool.

For this project, iperf3 is preferred because it is:

- easy to automate;
- easy to save as structured output;
- suitable for repeatable CLI-based tests;
- straightforward to document in Git;
- useful for TCP, reverse, parallel and UDP scenarios.

jPerf can still be used optionally as a visual comparison, but it should not be
the canonical measurement path.

## MVP test matrix

### Server

```bash
iperf3 -s
```

### TCP forward

```bash
iperf3 -c SERVER_IP -t 30
```

### TCP reverse

```bash
iperf3 -c SERVER_IP -R -t 30
```

### TCP parallel streams

```bash
iperf3 -c SERVER_IP -P 4 -t 30
```

### UDP controlled load

Start conservatively and increase gradually:

```bash
iperf3 -c SERVER_IP -u -b 100M -t 30
```

Record:

- achieved bitrate;
- jitter;
- lost/total datagrams;
- loss percentage.

## Test discipline

For a valid Ethernet vs Wi-Fi comparison:

- use the same client;
- use the same server;
- keep the server wired;
- test one access method at a time;
- confirm routing/interface selection before each run;
- keep background traffic low;
- repeat each test multiple times;
- record Wi-Fi RSSI, PHY rate, channel width and band;
- do not mix Internet measurements into the LAN result.

## Suggested evidence set

For each run capture:

```text
date/time
client interface
client IP
server IP
router/AP
Wi-Fi band/channel width (when applicable)
RSSI
iperf3 command
iperf3 result
ping/latency sample
system load notes
```

Use `iperf3 --json` for machine-readable result files.

Example:

```bash
iperf3 -c SERVER_IP -t 30 --json > ethernet-tcp-forward.json
```

## Optional latency-under-load test

Run a continuous ping to the router or server while iperf3 is generating load.

Example:

```bash
ping -i 0.2 SERVER_IP
```

Then start iperf3 in a second terminal.

This helps distinguish:

- high throughput with stable latency;
- bufferbloat / latency inflation under load;
- Wi-Fi contention;
- directional differences.

## Initial acceptance goal

The first useful case study should produce a controlled comparison on the
current Legion reference client for:

```text
Gigabit Ethernet
vs
5 GHz Wi-Fi 6 / 80 MHz
```

The current Fedora/RTL8852AE capability check is part of the test preflight:

```text
VHT: neither 160 nor 80+80
HE:  HE40/HE80/5GHz
HE RX/TX MCS/NSS: up to 2 streams <= 80 MHz
```

So **160 MHz is not part of the current-client acceptance matrix**. If a later
client advertises HE 160 MHz, add a separate `Wi-Fi 6 / 160 MHz` branch to the
matrix and keep the hardware/driver identity in the evidence.

with at least:

- 3 TCP forward runs;
- 3 TCP reverse runs;
- 3 parallel-stream runs;
- 3 UDP runs at a controlled bitrate;
- latency samples before and during load.

## Relationship to existing work

This benchmark complements the existing GeForce NOW and Xbox Cloud Gaming
case studies.

The cloud-gaming projects measure real application behavior across the
Internet. This lab measures the local network path itself.

That separation is important:

```text
iperf3 LAN benchmark
    -> local transport capability

GeForce NOW / Xbox Cloud
    -> real end-to-end application behavior
```

A good LAN benchmark can help determine whether a later cloud-gaming symptom
is likely to originate locally, but it must not be used as proof that an
Internet path or cloud service is healthy.

## Promotion criterion

Promote this concept into a standalone benchmark/case-study repository if:

- the test matrix is repeatable;
- both wired and Wi-Fi results are captured in a consistent evidence format;
- latency-under-load behavior is documented;
- the methodology is stable enough to rerun after router, Wi-Fi or client
  changes.
