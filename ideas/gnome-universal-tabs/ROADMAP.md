# Roadmap — Universal Tabs for GNOME

## Phase 0 — concept and feasibility

- preserve architecture and constraints;
- inspect current GNOME Shell/Mutter APIs for window enumeration, focus,
  workspace movement and visibility handling;
- prototype a minimal Shell UI bound to selected `Meta.Window` objects.

Exit criterion: prove that the generic window-group model is technically viable
on the target GNOME/Wayland release.

## Phase 1 — Universal Window Tabs MVP

Implement:

- Group Manager;
- shared Tab Bar;
- arbitrary window membership;
- active-window switching;
- safe removal/dissolve behavior.

Exit criterion: reliable manual grouping and switching across unrelated
applications.

## Phase 2 — group behavior

Add:

- geometry synchronization;
- same-monitor/workspace behavior;
- drag-to-add;
- tab reordering;
- keyboard navigation such as `Ctrl+Tab`;
- basic persistence.

Exit criterion: groups behave like a coherent workspace object rather than a
visual tab switcher only.

## Phase 3 — persistence and GNOME integration

Add:

- persistent groups;
- session restore;
- pinned groups;
- multi-monitor behavior;
- Overview integration;
- visual transitions and polish.

Exit criterion: Universal Tabs can be used as part of normal daily GNOME
workflow.

## Phase 4 — application adapters

### Browsers

Prototype Chromium/Helium and Firefox integration through:

- WebExtension;
- Native Messaging;
- browser tabs APIs.

### LibreOffice

Start with document-window grouping, then investigate UNO.

### VSCodium

Investigate an adapter that exposes editor tabs/workspaces to the system layer.

### Additional applications

Evaluate Files/Nautilus, Ptyxis and other GNOME applications where adapter
value justifies maintenance cost.

## Phase 5 — deep tabs

Explore a unified model where:

- a normal window can be a tab;
- an application-native document/tab can also be a tab;
- adapters expose application semantics to Universal Tabs.

This is the stage closest to a true system-wide tabs platform.

## Separate research path — compositor-level Sets

Only after the extension/service approach has demonstrated its limits:

- study Mutter changes needed for deeper surface composition/embedding;
- estimate maintenance burden per GNOME release;
- compare benefit against the extension approximation.

A custom Mutter/compositor fork is not the default implementation path.
