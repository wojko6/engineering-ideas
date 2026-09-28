# Microsoft 365 on Fedora via Bottles Compatibility Lab

**Status:** parked / event-driven compatibility test

## Goal

Evaluate whether Microsoft 365 can run usefully on the Fedora workstation
through Bottles without treating an experimental compatibility layer as a
production dependency.

The objective is not to replace the normal office workflow immediately. The
test should answer whether the upstream Bottles Office 365 work has matured
enough for practical Word/Excel/PowerPoint use on Fedora.

## Upstream reference

Tracking issue:

https://github.com/bottlesdevs/programs/issues/500

At the time this idea was recorded, upstream explicitly described the Office 365
port as unstable and advised against daily use.

The reported test path required:

- a recent Bottles build;
- Pre-Release mode;
- an experimental Soda 11 runner;
- the Bottles Office installer and office-runtime dependency;
- a valid Microsoft 365 licence.

Known upstream reports included rendering defects, Excel interaction/crash
issues, Outlook rendering/search problems, incomplete application coverage and
installer/runner churn.

## Activation criterion

Do not activate this lab merely because installation is technically possible.

Revisit when at least one of these becomes true:

- upstream removes the explicit "not for daily use" guidance;
- a stable/non-experimental runner path is documented;
- normal Bottles/Flathub installation is supported without a development-build
  requirement;
- the known-issues list is materially reduced;
- there is a specific need to compare native/web/compatibility-layer Office
  workflows on Fedora.

## Test environment

Use a disposable Bottle separate from normal workstation applications.

Do not modify or replace the normal Fedora productivity stack during the first
test.

Record:

- Fedora release and kernel;
- Bottles version and distribution method;
- Soda runner version;
- Office installer edition;
- whether the Microsoft account is personal or organisational;
- GPU/session type where rendering issues are being investigated.

Do not commit credentials, activation data, organisation identifiers or account
details to the repository.

## Initial test matrix

### Installation and lifecycle

- clean Bottle creation;
- Office install from the Bottles program installer;
- first launch;
- activation/sign-in;
- update through Office;
- Bottle restart;
- Fedora reboot;
- Bottles/runner update;
- uninstall/rollback.

### Application smoke tests

Prioritise:

1. Word;
2. Excel;
3. PowerPoint;
4. Outlook Classic if needed;
5. OneNote if needed.

Treat Access, Publisher, Teams and other components as optional until upstream
marks them as tested.

### Functional checks

Word:

- open/save DOCX;
- formatting;
- fonts;
- clipboard;
- print/PDF export.

Excel:

- cell selection accuracy;
- formulas;
- filtering/sorting;
- charts;
- XLSX open/save;
- copy/paste;
- crash behaviour.

PowerPoint:

- open/save PPTX;
- slide editing;
- images;
- transitions/presentation mode.

Outlook, if tested:

- sign-in;
- mail rendering;
- search;
- compose/reply;
- attachments.

### Integration checks

- file picker behaviour;
- clipboard;
- drag and drop where relevant;
- HiDPI/scaling;
- Wayland/XWayland behaviour;
- hardware acceleration/rendering;
- fonts;
- MIME/file associations.

### Resource and stability checks

Measure only if the basic functional tests pass:

- startup time;
- idle RAM;
- CPU usage;
- repeated application launches;
- session stability;
- crash frequency.

## Acceptance boundary

Possible outcomes:

```text
USABLE FOR DAILY WORK
USABLE WITH LIMITATIONS
TESTING ONLY
NOT CURRENTLY VIABLE
```

Do not promote the result to "daily use" based only on successful installation
or application startup.

## Rollback

The first implementation must remain disposable:

- use a dedicated Bottle;
- keep the experimental runner isolated from unrelated Bottles;
- preserve no irreplaceable documents only inside the Bottle;
- removal of the Bottle must restore the workstation to its pre-test state.

## Promotion criterion

Move this idea into an active Fedora/workstation project only when the upstream
state justifies a controlled compatibility study and there is a clear practical
reason to perform it.
