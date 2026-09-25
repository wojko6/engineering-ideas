# Universal Tabs for GNOME

**Status:** concept / architecture  
**Working names:** Universal Tabs, GNOME Sets, Tab Groups, Windows Sets  
**Target:** GNOME Shell / Wayland

## Goal

Create a system-wide tab/grouping experience in GNOME so independent
application windows can be collected into a single logical set and switched
through a shared tab bar.

The desired user experience is similar to a browser tab model, but at the
desktop/window-manager level.

Examples:

- Firefox + Files + Ptyxis grouped into one set;
- several related project windows grouped together;
- a persistent work set restored after login;
- later, deeper integrations where application-native tabs can participate in
  the same model.

The first implementation should not require applications to be modified.

## Core idea

The initial architecture is a GNOME Shell extension plus a small Universal
Tabs service/state layer.

At the generic window level:

```text
one application window = one Universal Tab
```

A group is therefore a logical collection of independent GNOME/Mutter windows.

The extension would provide:

- a shared tab bar for the active group;
- group membership management;
- focus and visibility switching;
- synchronized window placement where practical;
- persistent group state.

## MVP

The first MVP is intentionally narrow:

1. group arbitrary application windows;
2. show a shared tab bar for the current group;
3. switch between grouped windows reliably.

No deep browser, office-suite or editor integration is required for MVP.

See [MVP.md](MVP.md) for acceptance boundaries.

## Intended later behavior

After the MVP is stable, the concept can grow toward:

- shared position, size, monitor and workspace for windows in one group;
- hiding/showing inactive grouped windows instead of leaving them visually
  independent;
- drag-to-add and drag-to-reorder tabs;
- keyboard switching such as `Ctrl+Tab`;
- persistent groups and session restore;
- pinned groups;
- multi-monitor support;
- GNOME Overview integration;
- smoother transitions and visual polish.

## Deep application integrations

The generic window model is only the first layer.

Planned adapter directions include:

### Chromium / Helium and Firefox

Use browser-side integration such as:

- WebExtension;
- Native Messaging;
- browser tabs APIs.

The long-term goal is to let browser-native tabs participate in Universal
Tabs instead of exposing only the browser top-level window.

### LibreOffice

Stage 1:

- treat document windows as normal Universal Tabs.

Later:

- investigate UNO-based integration for deeper document awareness and control.

### VSCodium / VS Code

Later adapter:

- map or expose internal editor tabs/workspaces to the Universal Tabs layer.

### Future candidates

- Files / Nautilus;
- Ptyxis;
- other GNOME applications where a useful adapter exists.

## Important platform constraint

On Wayland/GNOME, a Shell extension cannot truly embed arbitrary independent
client windows inside one normal application window.

GNOME Shell/Mutter still owns separate `Meta.Window` surfaces.

Therefore the extension approach approximates the Sets experience by
coordinating independent windows:

```text
group
  -> active window visible/focused
  -> inactive group windows hidden/de-emphasized
  -> shared tab UI represents the logical set
```

A real compositor-level implementation capable of deeper window embedding
would require Mutter/compositor changes.

That could provide a more complete Microsoft-Sets-like architecture, but it
would also introduce substantial maintenance cost across GNOME releases.

The extension/service route is therefore the preferred first implementation
because it may deliver most of the desired user experience without carrying a
custom compositor fork.

## Promotion criterion

This idea should move into its own implementation repository when:

- the MVP interaction model is fixed;
- the GNOME Shell API approach has been prototyped successfully;
- window focus/visibility behavior works reliably on Wayland;
- persistence format is selected;
- the remaining limitations are understood well enough to document honestly.

See [ARCHITECTURE.md](ARCHITECTURE.md), [ROADMAP.md](ROADMAP.md) and
[OPEN-QUESTIONS.md](OPEN-QUESTIONS.md).
