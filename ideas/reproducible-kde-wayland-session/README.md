# Reproducible KDE Wayland Session

**Status:** concept

## Goal

Add an optional KDE Plasma Wayland session to the Fedora workstation without
turning KDE into the canonical desktop or damaging the existing GNOME state.

## Intended workflow

- preflight package/session dependencies;
- install KDE in a controlled way;
- validate portals, keyring, defaults, autostart and networking;
- test GNOME -> KDE -> GNOME transitions;
- keep session-specific settings separated;
- verify that GNOME desired state remains intact.

## Why

The project would test whether a second desktop environment can be added
reproducibly without creating uncontrolled cross-session drift.

## Promotion criterion

Promote after repeated GNOME/KDE session switching works with explicit
verification and rollback.
