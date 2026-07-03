## 1. Package Specifics Skill Contract

- [x] 1.1 Update `skillset/misc/isomer-misc-pkg-specifics/SKILL.md` to state that package-specific lookup is the first step for named package source, variant, accelerator, build, and runtime verification decisions.
- [x] 1.2 Ensure the workflow reports selected package-specific evidence for listed packages and `no package-specific rule` for unlisted packages.
- [x] 1.3 Confirm package pages stay narrow and do not duplicate generic Pixi, package-source reachability, bounded-run, or full environment setup guidance.

## 2. Topic Environment Setup Routing

- [x] 2.1 Update `skillset/service/isomer-srv-topic-env-setup/references/derive-env-gate.md` so named packages consult `isomer-misc-pkg-specifics` before generic PyPI, Pixi, Conda, runtime-wiring, enclosure, or verification rules.
- [x] 2.2 Update `derive-env-gate.md` to record selected package-specific evidence or `no package-specific rule` in `topic.env.topic_setup_target_spec`.
- [x] 2.3 Update `skillset/service/isomer-srv-topic-env-setup/references/install-topic-deps.md` so install execution follows package-specific evidence recorded in the target spec.
- [x] 2.4 Update `skillset/service/isomer-srv-topic-env-setup/references/verify-env-gate.md` so package-specific runtime checks outrank solver success, metadata checks, and generic import checks.
- [x] 2.5 Ensure topic env setup guidance still treats `topic.intent.topic_env_requirements` as high-level source intent and keeps operational details in `topic.env.topic_setup_target_spec`.

## 3. Topic Manager Package Mutation

- [x] 3.1 Update `skillset/operator/isomer-admin-topic-mgr/references/env-install-packages.md` so package-specific lookup precedes generic install route selection.
- [x] 3.2 Update `skillset/operator/isomer-admin-topic-mgr/references/env-update-packages.md` so package-specific lookup precedes generic update or constraint planning.
- [x] 3.3 Update `skillset/operator/isomer-admin-topic-mgr/references/env-remove-packages.md` so package-specific caveats are checked before removal planning.
- [x] 3.4 Ensure all Topic Manager environment mutation outputs report selected package-specific evidence or `no package-specific rule`.
- [x] 3.5 Preserve the rule that ad hoc package mutation remains in Topic Manager, while full operational env gate derivation routes to `isomer-srv-topic-env-setup`.

## 4. Agent Environment Setup

- [x] 4.1 Update `skillset/service/isomer-srv-agent-env-setup/references/derive-agent-env-gate.md` to state that missing or stale topic-level package planning routes back to `isomer-srv-topic-env-setup`.
- [x] 4.2 Update `derive-agent-env-gate.md` so per-agent cwd verification matrix items can consume package-specific runtime verification evidence without creating a separate dependency plan.
- [x] 4.3 Update `skillset/service/isomer-srv-agent-env-setup/references/verify-agent-env-gate.md` if needed so package-specific runtime expectations are enforced during per-agent cwd verification.

## 5. Validation and Tests

- [x] 5.1 Extend `scripts/validate_skillsets.py` to validate package-specific-first routing terms in `isomer-misc-pkg-specifics`, `isomer-srv-topic-env-setup`, `isomer-admin-topic-mgr env-*`, and `isomer-srv-agent-env-setup`.
- [x] 5.2 Add unit tests that reject topic env setup guidance that applies generic package-source routing before package-specific lookup.
- [x] 5.3 Add unit tests that reject Topic Manager package mutation guidance that omits package-specific lookup for install, update, or removal planning.
- [x] 5.4 Add unit tests that reject Agent Env Setup guidance that duplicates topic-level package install planning instead of routing missing dependency planning back to topic env setup.

## 6. Verification

- [x] 6.1 Run `python scripts/validate_skillsets.py`.
- [x] 6.2 Run `pixi run test`.
- [x] 6.3 Run `openspec status --change standardize-package-specific-env-routing` and confirm all artifacts and implementation tasks are complete.
