# Fedora Upgrade Readiness Engine

**Status:** concept / future automation layer

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
- GNOME Shell extension compatibility;
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
