# Architecture — Universal Tabs for GNOME

## Proposed high-level architecture

```text
                       +----------------------+
                       |   Universal Tab Bar  |
                       +----------+-----------+
                                  |
                                  v
                       +----------------------+
                       |    Group Manager     |
                       +---+--------------+---+
                           |              |
                 +---------+--+        +--+----------------+
                 | Window      |        | Persistent State |
                 | Controller  |        | / Service        |
                 +------+------+        +-------------------+
                        |
            +-----------+-----------+
            |                       |
            v                       v
+----------------------+  +--------------------------+
| Focus / Hide / Show  |  | Geometry / Workspace    |
| Controller           |  | Synchronization         |
+----------------------+  +--------------------------+
            |
            v
      GNOME Shell / Mutter
        Meta.Window surfaces
```

## Components

### Group Manager

Responsible for:

- creating and deleting groups;
- adding/removing windows;
- ordering tabs;
- tracking the active member;
- exposing the group state to the UI.

Example conceptual model:

```text
Group
  id
  name
  pinned
  active_window
  windows[]
```

### Universal Tab Bar

Shell UI representing the current logical group.

Initial responsibilities:

- show one tab per grouped window;
- identify the active window;
- switch the active member;
- expose basic add/remove/reorder operations later.

The tab bar should be desktop-level UI rather than application-owned UI.

### Focus / Hide / Show Controller

Coordinates the illusion of one tabbed set while the compositor still owns
independent windows.

Responsibilities may include:

- activate selected window;
- hide/minimize/de-emphasize previous member;
- restore the newly selected member;
- prevent obvious focus loops.

Exact hide/show semantics require prototyping against GNOME Shell APIs.

### Window Geometry Controller

Not required for the smallest MVP, but planned shortly afterward.

Potential responsibilities:

- keep group members on the same monitor;
- keep them on the same workspace;
- synchronize position and dimensions;
- react safely if a member becomes fullscreen/maximized.

### Persistent State / Universal Tabs Service

Stores logical groups beyond a single ephemeral interaction.

Candidate implementation:

- GSettings for small configuration/state;
- or a structured file such as `groups.json`;
- or a lightweight user service if application adapters need IPC.

The persistence layer should eventually support:

- group IDs;
- ordering;
- pinned state;
- application/window identity hints;
- restore metadata.

A final storage format has not been selected.

## Application adapter layer

Later architecture:

```text
                       Universal Tabs Service
                              |
        +---------------------+----------------------+
        |                     |                      |
        v                     v                      v
 Browser adapter       LibreOffice adapter      VSCodium adapter
 WebExtension +        window model first,      editor-tab bridge
 Native Messaging      UNO later
```

The generic GNOME-window path must remain useful even when an application has
no adapter.

## Wayland / Mutter boundary

The extension does not own or embed application client surfaces.

It coordinates Mutter windows.

This boundary means:

- a grouped application remains a real independent process/window;
- some application-native chrome may remain visible;
- true client reparenting is not the MVP;
- compositor changes would be a separate, much more invasive architecture.

## Design principle

Prefer a maintainable GNOME Shell extension/service implementation that
delivers a strong approximation of system-wide tabs before considering a
Mutter fork.

The project should not claim "one physical container window" unless the
implementation actually reaches compositor-level integration.
