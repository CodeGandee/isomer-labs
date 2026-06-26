## 1. Parent Skill Policy

- [x] 1.1 Update `skillset/service/isomer-srv-env-setup/SKILL.md` description, help, output contract, and guardrails to name the environment enclosure policy.
- [x] 1.2 Add output fields or wording for Pixi-managed installs, Pixi-mediated external runtime wiring, topic-local user-space fallback, and enclosure blockers.
- [x] 1.3 Add no-sudo and no-global-mutation guardrails covering system package managers, global profiles, global Python or Node installs, `/etc`, `ldconfig`, daemons, and kernel driver changes.

## 2. Derived Gate Strategy

- [x] 2.1 Update `references/derive-gate.md` so `## Dependency Plan` records an enclosure strategy for each dependency or runtime need.
- [x] 2.2 Update derived-gate section guidance so non-Pixi choices record why Pixi-managed installation was not used.
- [x] 2.3 Ensure derived Pixi install and setup command guidance keeps mutation under `pixi add --manifest-path`, `pixi install --manifest-path`, and `pixi run --manifest-path ... --environment ...`.
- [x] 2.4 Add blocker guidance for privileged or machine-global setup mentioned by source gate or repo instructions.

## 3. Dependency Installation Enforcement

- [x] 3.1 Update `references/install-deps.md` with the enclosure ladder: Pixi-managed install, Pixi-mediated external runtime wiring, topic-local user-space fallback, then blocker.
- [x] 3.2 Require `install-deps` to block when a required dependency or runtime need lacks an enclosure strategy in `isomer-env-gate.md`.
- [x] 3.3 Add instructions for explicitly recording external runtime wiring, including PATH, library paths, compiler paths, package-config paths, CUDA variables, and sourced scripts.
- [x] 3.4 Add topic-local fallback instructions using `<topic-workspace-dir>/.isomer-user-env/`, including `.gitignore` updates and lower-portability reporting.
- [x] 3.5 Confirm existing Pixi, PyPI-first, NVIDIA channel, starter dependency, Python version, and VCS ignore rules still read coherently after the enclosure additions.

## 4. Verification Readiness

- [x] 4.1 Update `references/verify-gate.md` so readiness requires recorded Pixi-scoped commands and recorded runtime wiring.
- [x] 4.2 Add failure or blocker guidance for commands that only pass because of ambient shell state, global packages, unrecorded PATH entries, unrecorded library paths, or unrecorded sourced scripts.
- [x] 4.3 Add readiness warning guidance for external runtime wiring or `.isomer-user-env/` fallback when the final status is `ready`.

## 5. Orchestration and Validation

- [x] 5.1 Review `references/setup-for-topic-workspace.md` so its full-flow output carries enclosure strategy, fallback warnings, and blockers from derive, install, and verify steps.
- [x] 5.2 Validate the revised service skill with the repository skill validation checks.
- [x] 5.3 Run `openspec validate refine-env-setup-enclosure --strict`.
- [x] 5.4 Review the final diff to confirm no implementation instructions allow sudo, global package installs, global shell profile mutation, or unrecorded ambient shell readiness.
