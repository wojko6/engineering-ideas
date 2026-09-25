# Privacy & Telemetry Audit

**Status:** concept

## Goal

Build a repeatable method for measuring what a workstation, browser or mobile
device contacts during controlled scenarios.

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
