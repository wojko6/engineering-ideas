# Fedora Application Discovery and Controlled Evaluation — AlternativeTo Shortlist

**Status:** Concept / parked — shortlist captured on 2026-11-12; no local installation, compatibility testing or adoption has been performed under this idea.

## Problem

Useful desktop and self-hosted applications are easy to collect but difficult to
evaluate consistently. Installing each discovery on a working Fedora KDE
workstation would add redundant tools, background services, security exposure
and configuration drift without first establishing any measurable benefit.

This concept records a small candidate set originally identified through
[AlternativeTo](https://alternativeto.net) for later evaluation. It is a
**research queue**, not a list of installed, compatible or endorsed software.
Upstream functionality, maintenance, licensing and distribution methods must be
verified again before any test.

## Goal

Find applications that genuinely improve a KDE Wayland workstation, its
existing desktop workflows and an adjacent self-hosted monitoring environment,
without duplicating working tools or compromising stability.

## Why it is interesting

- Compare native KDE capabilities with alternative desktop workflows.
- Improve AppImage and Flatpak lifecycle hygiene without disrupting pinned apps.
- Evaluate whether a small number of self-hosted tools adds useful evidence
  beyond existing logs, metrics and dashboards.
- Document a reusable, reversible candidate-assessment method rather than
  starting many parallel implementation projects.

## Candidate inventory

Priorities are **triage hypotheses**, not a decision to install.

| Candidate and upstream | Area | Initial priority | Specific question / duplication boundary |
| --- | --- | --- | --- |
| [Vicinae](https://github.com/vicinaehq/vicinae) | Qt launcher and productivity | High | Does it improve searchable actions, commands and workflow extensions beyond KRunner, AppBay and Nexus Launcher? Check Plasma Wayland shortcuts and extension trust. |
| [Gear Lever](https://github.com/mijorus/gearlever) | AppImage management | High | Can it simplify launcher/icon integration and application updates without taking ownership of existing custom launchers? |
| [Warehouse](https://github.com/flattool/warehouse) | Flatpak maintenance | High | Does it provide clear, safe inventory and data-management features missing from the existing application-update workflow? Avoid overlapping update authority. |
| [Glance](https://github.com/glanceapp/glance) | Self-hosted home dashboard | Medium | Would a lightweight service and source index improve access to existing monitoring without replacing Grafana? |
| [NetAlertX](https://github.com/jokob-sk/NetAlertX) | LAN inventory and change alerts | Medium | Can discovery of authorized devices add value beyond router/DNS client visibility with acceptable scan noise and network privileges? |
| [Scrutiny](https://github.com/AnalogJ/scrutiny) | SMART drive health | Medium | Are drive trends and alerts meaningfully better than an existing SMART/metrics pipeline, and what hardware privileges are needed? |
| [Kando](https://github.com/kando-menu/kando) | Radial desktop actions | Medium | Does its menu model help with repeatable actions without invasive KWin/Wayland integration? |
| [Ludusavi](https://github.com/mtkennerly/ludusavi) | Local game-save backups | Medium | Can it safely back up and restore Steam/Proton local saves? Cloud-only console saves are outside scope. |
| [FSearch](https://github.com/cboxdoerfer/fsearch) | File indexing and search | Medium | Does it outperform Baloo/KDE search for an explicit workload without needless duplicate indexing? |
| [Czkawka](https://github.com/qarmin/czkawka) | Duplicate and file hygiene audit | Medium | Can a read-only scan expose safely reviewable duplicates? Automatic deletion is excluded. |
| [Spacedrive](https://github.com/spacedriveapp/spacedrive) | Cross-device file organization | Low | Does its library model solve a concrete gap beyond Dolphin and the Finder KDE experiment? |
| [GOverlay](https://github.com/benjamimgois/goverlay) | Game telemetry overlay configuration | Low | Is there a measurable benefit over existing MangoHud/Proton tooling for locally running games? |

Candidates can be dropped after a read-only assessment. Adding a candidate to
this table does not promote it into an independent project.

## Constraints

- Baseline platform for a future compatibility review: Fedora KDE Plasma on
  Wayland. Recheck actual versions, packaging and runtime requirements at test
  time rather than baking release versions into this concept.
- Keep the existing dock, application launchers, Flatpak management, file
  managers, GPU driver stack, Tailscale and monitoring services unchanged during
  the discovery phase.
- Do not assume that a tool listed on AlternativeTo supports Linux, Fedora or
  KDE merely because it appears in search results.
- Do not pipe third-party installation scripts directly to a shell during
  discovery. Inspect provenance, checksums/signatures, permissions and package
  contents first.
- Do not enable privileged disk, input, screen-capture or network-scan features
  without a separate, bounded approval and rollback plan.
- Prefer self-contained, disposable or user-level evaluation where the relevant
  functionality does not require a system-wide modification.
- One or two implementation-heavy projects at most remain active repository-wide.

## Related work and scope boundary

- [Reproducible KDE Wayland Session](../reproducible-kde-wayland-session/README.md)
  owns workstation-session reproducibility; this idea owns only candidate
  selection, not KDE deployment/configuration instructions.
- [Workstation Health Dashboard](../workstation-health-dashboard/README.md)
  owns the health presentation model. Scrutiny can be considered as a possible
  input, not a second canonical health dashboard.
- [System Drift Detector](../system-drift-detector/README.md) owns desired-state
  checking and can supply change evidence.
- [Home Lab Attack Surface & Vulnerability Assessment](../home-lab-attack-surface-vulnerability-assessment/README.md)
  owns exposure evaluation. NetAlertX is only a possible inventory source.
- Runtime notes and implementation changes belong in the relevant Fedora or
  infrastructure repository, not duplicated here.

## Proposed evaluation architecture

1. **Read-only intake:** collect official sources, license, release status,
   package formats, permissions, Wayland/KDE compatibility claims and overlap
   with existing software.
2. **Shortlist gate:** rank by distinct benefit, maturity, maintenance,
   permission footprint, reversibility and absence of duplication.
3. **Disposable pilot:** select at most one or two candidates and use temporary
   profiles, scoped directories or isolated environments where feasible.
4. **Evidence review:** compare observed results with baseline and record the
   recommendation: reject, keep parked, pilot further or promote.

## Bounded MVP

### Phase 0 — no host changes

- Review Vicinae, Gear Lever and Warehouse first against their official
  documentation and available packages.
- Check Glance and NetAlertX separately only if they address a documented gap.
- For each candidate, record: supported platforms, sandbox/permission
  requirements, potential conflicts, upstream maintenance status and the
  existing baseline feature it would replace or complement.
- Mark every unexecuted check **NOT TESTED**. Do not infer performance or
  security from an appealing UI or project popularity.

### Phase 1 — optional isolated pilot, separately authorized

- Choose one candidate whose unique value survives Phase 0.
- Define a reversible setup that avoids changing host-wide desktop defaults,
  kernel modules, firewall policy or production observability configuration.
- Measure startup/memory footprint, feature usability, KDE Wayland integration,
  persistence/autostart behavior and uninstall cleanliness.
- Capture only sanitized findings and references to retained private evidence.

## Validation

| Outcome | Acceptance evidence |
| --- | --- |
| PASS | Documented unique improvement over baseline; reproducible compatibility result; bounded permissions and clean removal. |
| FAIL | Reproducible incompatibility, unacceptable data/privilege exposure, material instability or no benefit over existing tools. |
| INCONCLUSIVE | Insufficient comparable measurements, incomplete upstream documentation or environment-specific ambiguity. |
| NOT TESTED | No local execution has taken place; upstream descriptions alone do not count. |

For tools that touch disks, game saves or network inventory, the pilot must
include a dry run and explicit write/scope controls. Do not treat duplicate-file
findings or discovery results as authorization to delete or scan anything.

## Risks and rollback

- Duplicate autostart services, conflicting global shortcuts or changes to
  launcher associations: disable only the pilot integration and restore its
  isolated configuration.
- Flatpak/AppImage housekeeping that modifies application data: use a bounded
  test profile and verified restore point; exclude live data from destructive
  trials.
- Network discovery and SMART access: verify capability/permission scope before
  deployment. No production-device scan or privileged container is implied.
- Third-party extensions, shell hooks or installation scripts: inspect source
  and privileges first; revert by deleting the disposable environment when
  possible.

## Public-data boundary

Do not publish real device inventories, usernames, file paths, network
addresses, mounted-drive identifiers, personal game-save content, screenshots
with sensitive windows, local API tokens, raw logs or unsanitized system
configuration. Follow the repository's [publication policy](../../PUBLICATION.md).
Public evidence may contain only sanitized, high-level findings.

## Promotion criterion

Promote a single candidate only after Phase 0 confirms a distinctive need and
an approved reversible pilot meets its acceptance criteria. Otherwise leave
this shortlist parked and revisit it only when the baseline has a real gap.
