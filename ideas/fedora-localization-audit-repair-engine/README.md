# Fedora Localization Audit & Repair Engine

**Status:** concept

## Goal

Turn the localization work already proven on the Fedora workstation into a
general audit-and-repair pipeline.

## Core workflow

```text
SCAN -> CLASSIFY -> REPORT -> GENERATE -> REVIEW -> INSTALL -> VERIFY
```

The engine would:

- discover untranslated or inconsistent user-visible strings;
- identify producer/version drift;
- classify gettext, JSON, resource/DataPack and desktop-file sources;
- generate candidate overlays or patches;
- keep manual review in the loop;
- install only against exact validated producer state;
- verify both repository state and physical UI state.

## Why

The existing Fedora localization project already demonstrated that narrow
technical tests and visual acceptance are different layers. This idea would
generalize that process instead of keeping each application as a one-off fix.

## Promotion criterion

Promote to its own repo when one reusable scanner can successfully audit at
least two different localization mechanisms without weakening exact-version
validation.
