# Reproducible KDE Wayland Session

**Status:** concept / execution tracked in Fedora roadmap

## Goal

Add an optional KDE Plasma Wayland session to the Fedora workstation without
turning KDE into the canonical desktop or damaging the existing GNOME state.

## Scope boundary

Active planning and acceptance for GNOME + KDE Plasma coexistence belongs to
the public
[Fedora Workstation Engineering Roadmap](https://github.com/wojko6/fedora-workstation-setup/blob/main/ROADMAP.md)
and its Issue #12.

That repository owns:

- the current accepted GNOME baseline;
- the implementation plan;
- clean-room and physical validation;
- rollback and promotion decisions.

This incubator page remains a compact architecture concept. It should not become
a second execution checklist or claim that KDE has already been promoted into
the accepted workstation state.

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
