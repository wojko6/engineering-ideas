# Workstation Health Dashboard

**Status:** concept

## Goal

Provide one concise view of Fedora workstation health without replacing the
underlying diagnostic tools.

## Candidate signals

- failed systemd units;
- storage/free space;
- Btrfs state;
- update status;
- SELinux/AVC summary;
- GNOME extension health;
- Tailscale state;
- backup/recovery freshness;
- desired-state drift;
- recent critical kernel/system errors.

## Design

The dashboard should summarize and link to evidence rather than invent its own
health truth.

## Promotion criterion

Promote when the dashboard can be generated from existing checks and each
status has a clear source and failure meaning.
