# Open Questions — Universal Tabs for GNOME

## Naming

Working names currently include:

- Universal Tabs;
- GNOME Sets;
- Tab Groups;
- Windows Sets.

No final public project name has been selected.

"Universal Tabs" currently describes the long-term goal best because the design
may eventually include both whole windows and application-native tabs.

## Window visibility model

When switching tabs, should inactive members be:

- minimized;
- hidden through Shell/Mutter state;
- moved away from the active workspace;
- kept stacked behind the active member?

This must be tested for focus reliability, task-switcher behavior and app
compatibility.

## Tab bar placement

Possible models require prototyping:

- attached visually to the active window;
- top-of-screen shell component;
- floating group bar.

The UI should feel like one logical set without falsely implying that the
extension owns the underlying client surfaces.

## Window identity and restore

How should a persisted group identify a window across sessions?

Potential signals include:

- application ID;
- WM class/app identity;
- title hints;
- application-provided adapter identity.

Titles alone are not reliable enough for long-term restore.

## State storage

Candidates:

- GSettings;
- `groups.json`;
- user service with IPC and structured storage.

The choice depends on how quickly deep application adapters are introduced.

## Browser semantics

Questions for browser adapters:

- does a browser-native tab become a first-class Universal Tab;
- can top-level browser windows and internal tabs coexist in one group;
- who owns close/reorder/restore behavior;
- how are private/incognito windows isolated?

## LibreOffice semantics

Start with top-level document windows.

Later UNO research must determine whether document identity and switching can
be exposed safely without building brittle version-specific logic.

## VSCodium semantics

Need to determine whether internal editor tabs/workspaces can be surfaced
through a stable extension/API bridge rather than UI automation.

## GNOME upgrades

A Shell extension can depend on GNOME internals.

The implementation should explicitly track:

- supported GNOME Shell versions;
- API drift;
- compatibility tests;
- Wayland-only assumptions.

## Accessibility and keyboard model

A real implementation must define:

- keyboard-only group creation/switching;
- focus semantics;
- screen-reader/tab labels;
- shortcuts that do not conflict with application-native bindings.

## Promotion decision

Before this concept becomes an implementation repository, answer at least:

1. Can a GNOME Shell extension switch arbitrary grouped windows reliably?
2. What visibility mechanism behaves best on Wayland?
3. Where should the tab bar live?
4. Is persistence initially local to the extension or a separate service?
5. Which GNOME version becomes the first supported target?
