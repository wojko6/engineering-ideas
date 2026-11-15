# Fedora Upgrade Readiness Engine

**Status (2026-11-13):** future reusable automation concept, not an existing tool. The [manual Fedora 45 / NVIDIA 620 preflight B1–B8 record](https://github.com/wojko6/fedora-workstation-setup/blob/main/docs/upgrade-preflights/2026-11-04-fedora45-nvidia620.md) documents a **historical** checkpoint at which B9 and the actual upgrade had not been performed. The [Fedora workstation project status](https://github.com/wojko6/fedora-workstation-setup/blob/main/PROJECT-STATUS.md) separately confirms a **physical Fedora 44 → 45 upgrade on 2026-11-10** with bounded operational acceptance. A full Fedora 45/KDE clean-room restore and desired-state promotion remain **HOLD**; successful host upgrade does not retrospectively complete B9 or validate a reusable automation engine.

## Goal

Assess whether the workstation is ready for a Fedora major-version upgrade
before the upgrade is started.

## Scope boundary

The current Fedora major-upgrade lifecycle is already operationally tracked in
the public
[Fedora Workstation Engineering Roadmap](https://github.com/wojko6/fedora-workstation-setup/blob/main/ROADMAP.md)
and its Issue #13.

That active repository owns:

- the current upgrade checklist;
- target-release compatibility review;
- clean-room validation;
- physical upgrade acceptance;
- promotion of a new accepted Fedora baseline.

This incubator concept owns only the **future reusable automation layer** that
could turn parts of that mature checklist into a readiness engine.

Do not duplicate the active upgrade procedure here. Promote automation into the
Fedora repository only when the manual workflow is stable enough to encode
without hiding operator decisions.

## Intended checks

- package/repository compatibility;
- KDE Plasma/Wayland session and Qt/KF6 integration, plus GNOME extensions only where a GNOME profile is actually targeted;
- custom localization overlays and version pins;
- Flatpak state;
- kernel/modules and third-party drivers;
- systemd failures;
- SELinux issues;
- storage/free-space state;
- rollback/recovery readiness;
- known local customizations likely to drift.

## Output

Produce a simple readiness report:

```text
READY
BLOCKED
REVIEW REQUIRED
```

with explicit reasons and affected components.

## Promotion criterion

Move to implementation when the current workstation upgrade process can be
described as a stable checklist that can be automated without hiding manual
decisions.
