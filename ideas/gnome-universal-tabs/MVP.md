# MVP — Universal Tabs for GNOME

## Objective

Prove that arbitrary GNOME/Wayland application windows can behave as one
logical tab group without modifying the applications.

## MVP user story

A user can:

1. select two or more existing windows;
2. place them in one Universal Tabs group;
3. see one desktop-level tab per member;
4. click a tab to switch reliably between members;
5. remove a window from the group without closing the application.

## Required MVP capabilities

### Grouping

- create one logical group;
- add arbitrary top-level windows;
- remove a member;
- dissolve a group safely.

### Tab UI

- display member title/application identity;
- identify the active tab;
- switch active member by click.

### Focus and visibility

- selected member receives focus;
- inactive members do not compete visually with the active member;
- switching does not unexpectedly close or move applications.

### Safety

The extension must tolerate:

- a grouped application closing itself;
- a window title changing;
- focus changes caused by the application;
- a member becoming unavailable.

## Explicitly outside MVP

Not required for the first proof:

- browser-native tab import;
- LibreOffice UNO integration;
- VSCodium editor-tab integration;
- session restoration after login;
- pinned groups;
- multi-monitor polish;
- drag/reorder;
- `Ctrl+Tab`;
- GNOME Overview integration;
- animations;
- compositor/Mutter modifications.

## MVP acceptance

The MVP is successful when several unrelated applications can be grouped and
switched repeatedly on the target Fedora/GNOME Wayland workstation without
crashes, lost windows, broken focus or manual geometry repair after each
switch.

Suggested first test set:

```text
Firefox
Files / Nautilus
Ptyxis
VSCodium
```

The exact application set is representative, not a hard architectural
dependency.
