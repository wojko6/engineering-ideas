# System Drift Detector

**Status:** concept

## Goal

Compare the live Fedora workstation with the repository-defined desired state
and identify meaningful drift.

## Candidate scope

- GNOME/dconf settings;
- installed packages and Flatpaks;
- GNOME extensions and exact versions;
- project-managed localization files;
- systemd user/system units;
- selected configuration files;
- security/hardening settings.

## Design principle

Do not automatically promote live state into Git. A live mismatch is evidence
to investigate, not proof that the repository is stale.

## Output

```text
MATCH
EXPECTED DIFFERENCE
DRIFT
UNKNOWN
```

with enough evidence to decide whether to restore the live system or update the
desired state.

## Promotion criterion

Promote once the detector can distinguish deliberate exceptions from accidental
drift for the current Fedora workstation.
