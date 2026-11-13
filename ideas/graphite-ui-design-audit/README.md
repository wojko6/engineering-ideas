# Graphite UI Design Audit — Unslop-inspired evaluation

**Status (2026-11-13):** Concept / first read-only audit completed on a **historical v1.9 QSS** and an isolated, independent HTML fixture; see [Phase 0 evidence](PHASE-0-2026-11-13.md). Current Charcoal v0.4 QSS and native Qt GUI have **not** been revalidated. No Unslop installation, agent integration, automatic refactoring or production changes occurred.

## Why this exists

The active [Fedora workstation project](https://github.com/wojko6/fedora-workstation-setup) has a Fedora 45 / KDE Plasma / Wayland desktop pilot, a separately developed Finder KDE LAB application and an **unpromoted** Graphite Charcoal visual candidate. The local Finder screenshots revealed inconsistent surfaces and a still-violet navigation sidebar. A one-off theme patch is not sufficient to maintain consistent visual rules across Finder, KDE properties, dock/launcher integrations and dashboards.

[Unslop](https://github.com/heydamir/unslop), by Damir Sokolovsky, is an AI-agent **skill**, not a conventional graphical application. Its design-review methodology prioritizes restrained color, consistent spacing, typography, icons and product-specific character. The upstream skill principally targets web UI stacks; it is **not** a drop-in native Qt6/QSS/QML editor.

The goal here is to evaluate the method, not adopt a generic anti-purple rule for every product or replace the native KDE appearance machinery.

## Candidate design direction

- **Character:** calm, precise, identifiable as Graphite rather than a generic AI dashboard
- **Surfaces:** dark neutral charcoal ramp; no unsolicited purple or blue-to-violet gradients in UI chrome
- **Hierarchy:** consistent text contrast, control heights, spacing and border radii, keyboard focus indicators
- **Color with meaning:** retain colors for folder icons, operational alerts, charts and semantically meaningful feedback
- **Scope:** honor Qt6/Plasma accessibility and platform conventions; retain legitimate per-app differences
- **Behavior:** no functional changes merely to achieve a cosmetic improvement

## Controlled evaluation

1. **Read-only upstream review:** record exact Unslop commit, license, current documentation, script behavior and any known security concerns.
2. **Isolated web fixture:** run a manual Unslop design audit on a synthetic HTML/CSS screen without connecting to the production Fedora workstation settings. Compare findings with a neutral reference screenshot.
3. **Qt/QSS translation:** manually adapt only the useful audit rules to Finder screenshots and selected source/QSS selectors; distinguish code-inferred appearance from measured live GUI output.
4. **Cross-window review:** compare the Finder main window, info dialog, properties tabs and dialogs; explicitly track the violet sidebar and the Properties/Tags control issues.
5. **Decision:** reject, keep as reading material, or adopt a bounded Graphite design checklist in the active Fedora repository after review.

**No automatic UI patching:** an AI agent must not edit live KDE settings, system Dolphin, Qt style plugins, the active Finder launcher or production files without isolated build/test, backup and explicit approval.

## Security, copyright and provenance

- The upstream Unslop material is [CC BY 4.0](https://github.com/heydamir/unslop/blob/main/LICENSE), while this incubator uses MIT by default. Merely linking a methodology does not import its licensed text; any adapted upstream material must retain required attribution and licensing notices.
- Upstream [issue #32](https://github.com/heydamir/unslop/issues/32) reported a path-containment weakness in `story.mjs` on 2026-11-12. Re-evaluate whether it has been resolved before running local playback/story tooling, and avoid using sensitive folders as a fixture root.
- No unreviewed third-party scripts, paid image generation, network crawls, package installs or publication of private screenshots are authorized by this concept.
- Prefer immutable commits and review changes before adoption; do not treat popular screenshots or agent output as evidence of correctness.

## Ownership boundary and promotion

The **idea and bounded experiment** live here. Actual Finder patches, KDE runtime configuration, full visual acceptance, Fedora 45 restore gates and any documented deployable Graphite design system belong to [fedora-workstation-setup](https://github.com/wojko6/fedora-workstation-setup) and its existing tracked work. Avoid a parallel operational source of truth or a new issue solely for this concept.

**Promotion criterion:** a reproducible isolated design-review procedure catches demonstrable inconsistencies that the current process misses, generates an actionable report, and causes no unintended UI/functionality regressions when an explicitly reviewed patch is later tested.
