# Btrfs Safe Change & Rollback

**Status:** concept

## Goal

Create a guarded workflow for risky Fedora changes using Btrfs snapshots and
explicit rollback validation.

## Intended use

Before operations such as:

- major package changes;
- GNOME/session experiments;
- low-level configuration changes;
- potentially disruptive hardening.

The workflow would:

1. perform preflight checks;
2. create/verify a snapshot;
3. apply the planned change;
4. run post-change validation;
5. make rollback explicit if acceptance fails.

## Boundary

This is not a substitute for the independent disaster-recovery backup. Local
snapshots and external recovery copies solve different failure classes.

## Promotion criterion

Promote after a full change -> failure -> rollback drill succeeds in a safe
test environment.
