# Raven Windows Compatibility Runtime — Fedora Evaluation

**Status:** Concept / parked — upstream research only (2026-11-15).
**Local validation:** NOT TESTED.
**Upstream:** [mirkobrombin/raven](https://github.com/mirkobrombin/raven) · [project documentation](https://useraven.org).

## Problem

Windows-only applications and games remain a Linux compatibility gap. Wine,
Bottles and Proton already cover many workflows, but Raven proposes an
alternative Windows API/runtime implementation and sandbox model. We need a
reproducible way to decide whether it offers a practical benefit without
disturbing the working Fedora KDE environment.

## Goal

Observe Raven's maturity and, only when suitable, evaluate its compatibility,
security boundary and user experience against existing Wine/Bottles/Proton
paths. This document does **not** authorize installation or replacement of
working tooling.

## Why it is interesting

The upstream README describes:
- native execution of Windows application code on the Linux CPU, with Raven
  providing Windows kernel/service-facing interfaces;
- separate application prefixes with registry, drive mapping, snapshots and
  per-application write layers;
- Wayland/Vulkan graphics integration and optional DXVK/vkd3d-proton for
  Direct3D workloads;
- support claims for both x86 and x86_64 programs, common installers, selected
  .NET Framework scenarios and selected Direct3D versions.

These are **upstream claims**, not Fedora 45 validation. The upstream README
publishes a small compatibility matrix and benchmark methodology; its scores
cannot be generalized to all Windows software or gaming workloads.

## Constraints

- Target for a future review: Fedora 45 KDE/Wayland on an AMD Ryzen 7 5800H
  and NVIDIA RTX 3060 Laptop GPU; verify the actual host state again before
  designing a pilot.
- Preserve the existing system Wine/Proton/Bottles installations and prefix
  data, Steam configuration, GPU drivers, KDE session and launchers.
- No upstream build, provisioning/download script, system package installation,
  prefix migration, privileged sandbox change or GPU stack modification is
  approved by this concept.
- Upstream currently documents building from source; no polished Fedora
  package or production maturity should be assumed.
- Treat sandboxing as a security design claim requiring independent review,
  not as a proven containment guarantee.

## Related work and scope boundary

- [Fedora Application Discovery and Controlled Evaluation](../fedora-application-discovery-evaluation/README.md)
  owns general-purpose application shortlisting; this entry owns the
  Raven-versus-existing-Windows-runtime evaluation question.
- [Reproducible KDE Wayland Session](../reproducible-kde-wayland-session/README.md)
  owns host/session reproducibility.
- Operational system modifications, if eventually authorized, belong in
  [Fedora Workstation Setup](https://github.com/wojko6/fedora-workstation-setup).
- Existing game launchers and streaming services are outside this idea's
  implementation scope.

## Proposed evaluation architecture

1. **Read-only upstream watch:** track tagged releases, build instructions,
   documented limitations, compatibility matrix revisions, security fixes and
   licensing changes.
2. **Relevance gate:** identify one Windows application/workflow that works
   poorly through established tools and is explicitly worth testing.
3. **Separate approval gate:** design a disposable, non-production Fedora
   environment with an isolated prefix, fixed upstream revision, reproducible
   dependencies and teardown procedure.
4. **Comparison (optional):** test the identical application version and
   workflow against Wine/Bottles or Proton, recording failures, launch time,
   functional behavior, CPU/memory use and graphics issues where applicable.
5. **Evidence-based decision:** keep parked, reject, repeat after an upstream
   release or promote a narrowly scoped pilot.

## Bounded MVP

**Phase 0 — documentation only, no commands on the workstation:**
- Inspect upstream changelog, build prerequisites, CI and reproducible tests.
- Verify the compatibility matrix and benchmark conditions from primary
  sources, distinguishing upstream-reported from independently reproduced.
- Review Landlock/sandbox permissions, host-file access and network mediation,
  alongside the supply chain for provisioned libraries.
- Record one meaningful use case and a testability decision.

**Phase 1 — future, separately authorized:** a single application in a
disposable environment, no real personal data, no production prefixes.

## Validation

| Outcome | Required evidence |
| --- | --- |
| PASS | Independently reproduced target application workflow and isolation/cleanup checks, with a meaningful benefit against the baseline. |
| FAIL | Reproduced blocker, unacceptable privileges, harmful side effects or no distinct value for the target workflow. |
| INCONCLUSIVE | Missing build dependencies, unstable upstream behavior or insufficient comparable evidence. |
| NOT TESTED | Current state; only upstream documentation reviewed. |

Do not infer broad Windows compatibility from an installer success or a
single game benchmark.

## Risks and rollback

Primary risks include immature Windows API coverage, installer side effects,
host-file/network escape paths, supply-chain exposure from provision scripts,
graphics-stack instability and misleading performance comparisons.

No rollback is currently necessary because no deployment is planned.
Any future experiment requires an isolated environment and documented teardown;
do not run its cleanup against existing user prefixes or system directories.

## Public-data boundary

Publish only upstream links, non-sensitive test methodology and sanitized
measurements. Do not publish personal files, host identifiers, private game
data, credentials, raw logs or local deployment paths. Follow the repository's
[publication policy](../../PUBLICATION.md).

## Promotion criterion

Revisit when Raven has reproducible release/build evidence, a substantially
broader tested application matrix, a reviewable confinement model and a
specific Windows workflow where a disposable Fedora comparison can answer a
real question. Until then: **watch, do not install**.
