# Reproducible KDE Wayland Session

**Status (2026-11-13):** the physical workstation runs **Fedora 45 / KDE Plasma 6.8.2 / Wayland** (upgrade reported 2026-11-10). The most recently fully accepted reproducible restore baseline is **historical Fedora 44 / GNOME 50.5**. A separate [Fedora 45 KDE Graphite design branch](https://github.com/wojko6/fedora-workstation-setup/tree/feature/fedora45-kde-graphite-restore) contains operator-confirmed read-only host inventories, observed RPM versions, and a planned VirtualBox clean-room test. **No Fedora 45 KDE clean-room restore, independent KDE installer, or ISO is accepted.**

## Goal

Document how the already-running KDE Plasma Wayland workstation can become a reproducible, optional and verified Fedora profile while preserving the historical GNOME restore baseline. The existing KDE pilot is not automatically an accepted restore configuration.

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
- reproduce KDE in a disposable Fedora 45 VM with reviewed manifests;
- validate portals, keyring, defaults, autostart and networking;
- keep GNOME/KDE coexistence or transition requirements explicit rather than assuming both remain installed;
- keep session-specific settings separated;
- verify that GNOME desired state remains intact.

## Why

The project would test whether a second desktop environment can be added
reproducibly without creating uncontrolled cross-session drift.

## Promotion criterion

Promote only after a repeated clean-room Fedora 45/KDE restore and the relevant session, portal, integration and rollback tests pass. GNOME coexistence/switching tests apply if that remains an explicitly selected target.
