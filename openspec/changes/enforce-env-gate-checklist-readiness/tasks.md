## 1. Topic Env Service

- [x] 1.1 Update `skillset/service/isomer-srv-topic-env-setup/references/derive-env-gate.md` so `## Gate Checklist` is defined as required readiness work, optional diagnostics live outside the checklist, and each required item needs a pass condition and evidence source.
- [x] 1.2 Update `skillset/service/isomer-srv-topic-env-setup/references/verify-env-gate.md` so `readiness_status: ready` requires every required checklist item to be checked with supporting evidence.
- [x] 1.3 Update topic env verification wording so unchecked checklist items become `blocked`, `failed`, or `not checked` with the exact item, reason, and next action.
- [x] 1.4 Update topic env guardrails so bounded real-path checks can complete heavy items only when they exercise the named critical path, while unrelated smoke tests cannot complete those items unless the user records an explicit downgrade.

## 2. Agent Env Service

- [x] 2.1 Update `skillset/service/isomer-srv-agent-env-setup/references/derive-agent-env-gate.md` so `## Gate Checklist` is required per-agent readiness work and optional diagnostics stay outside the checklist.
- [x] 2.2 Update `skillset/service/isomer-srv-agent-env-setup/references/verify-agent-env-gate.md` so per-agent readiness requires every targeted required checklist item to be checked with cwd evidence from the resolved Agent Workspace.
- [x] 2.3 Update agent env verification wording so `overall_readiness_status: ready` requires the complete planned Agent Name matrix, and selected-agent checks remain partial unless the full matrix has already passed.
- [x] 2.4 Update agent env guardrails so weaker smoke tests cannot complete critical per-agent checklist items unless a user downgrade is explicitly recorded.

## 3. Operator Handoff

- [x] 3.1 Update `skillset/operator/isomer-admin-topic-team-specialize/references/setup-topic-env.md` so delegated topic env readiness is accepted only when the topic gate checklist is complete or incomplete items are reported as blockers, failures, or not checked.
- [x] 3.2 Update `skillset/operator/isomer-admin-topic-team-specialize/references/setup-agent-workspace.md` so delegated agent env readiness is accepted only when required per-agent checklist evidence is complete, with selected-agent evidence preserved as partial.
- [x] 3.3 Update `skillset/operator/isomer-admin-topic-team-specialize/references/validate-topic-team.md` and final summary guidance so incomplete delegated checklist items block static readiness and smoke-test downgrades remain visible.

## 4. Validation

- [x] 4.1 Extend `scripts/validate_skillsets.py` to require checklist-readiness language in the topic env service, agent env service, and topic-team specialization operator instructions.
- [x] 4.2 Extend `tests/unit/test_validate_skillsets.py` to cover complete-checklist readiness, explicit blocked checklist items, and the ban on unrelated smoke-test completion.
- [x] 4.3 Run `pixi run python scripts/validate_skillsets.py --scope service`, `pixi run python scripts/validate_skillsets.py --scope operator`, and `pixi run python -m unittest tests.unit.test_validate_skillsets`.
- [x] 4.4 Run `openspec validate enforce-env-gate-checklist-readiness --strict`.
