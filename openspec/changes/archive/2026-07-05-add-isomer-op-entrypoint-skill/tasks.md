## 1. Entrypoint Skill Assets

- [x] 1.1 Create `src/isomer_labs/assets/system_skills/operator/isomer-op-entrypoint/SKILL.md` with frontmatter, overview, when-to-use guidance, a near-top numbered workflow, route-and-proceed behavior, guardrails, and split Essential/Complete Output contracts.
- [x] 1.2 Add `src/isomer_labs/assets/system_skills/operator/isomer-op-entrypoint/agents/openai.yaml` with matching `isomer-op-entrypoint` display metadata and default prompt.
- [x] 1.3 Add local reference pages for routing rules, input surfaces, system skill index, extension skill index, and CLI index, each with a near-top numbered workflow and fallback guidance.
- [x] 1.4 Ensure entrypoint guidance distinguishes `isomer-op-welcome` read-only orientation from `isomer-op-entrypoint` route-and-proceed dispatch.
- [x] 1.5 Ensure entrypoint guidance uses global `isomer-cli` examples and does not use repo-local `pixi run isomer-cli` command guidance.

## 2. Routing Content

- [x] 2.1 Document operator owner routes for Project lifecycle, topic creation, initialized-topic management, identity switching, Topic Team Specialization, and welcome orientation.
- [x] 2.2 Document service skill boundaries so service skills remain bounded support routes and normal user-facing requests route through owner workflows unless a service skill is explicitly invoked.
- [x] 2.3 Document misc helper routing, especially that `isomer-misc-tool-packs` is an explicit named helper route and not an automatic package mutation path.
- [x] 2.4 Document DeepSci extension routes for workspace bootstrap, pipeline passes, scout, baseline, idea, optimize, experiment, analysis, decision, finalize, science, write, paper-outline, paper-plot, figure polish, review, rebuttal, Nature data, Nature figure, Nature paper-to-PPT, and Nature polishing.
- [x] 2.5 Document DeepSci readiness routing so missing topic, actor, agent, workspace, or bootstrap readiness routes to the appropriate operator/setup/workspace manager surface before ordinary research-stage work.
- [x] 2.6 Document CLI route families for self queries, context, paths, topics, topic actors, repositories, runtime, topic reset, artifact formats, research records, handoffs, team templates, team profiles, team instances, topic-main guidance, and outputs policy.
- [x] 2.7 Exclude retired and stale routes including `isomer-op-topic-workspace-mgr`, `isomer-op-topic-prepare`, `isomer-op-manual-research-session`, `isomer-op-houmao-interop`, and active `isomer-admin-*` names.

## 3. Manifest and Documentation

- [x] 3.1 Add `operator/isomer-op-entrypoint` to `src/isomer_labs/assets/system_skills/manifest.toml` under `groups.core.skills`.
- [x] 3.2 Update `src/isomer_labs/assets/system_skills/operator/README.md` to list `isomer-op-entrypoint`, explain its boundary, and keep the welcome skill as read-only orientation.
- [x] 3.3 Update packaged system-skill documentation if needed so the core system-skill catalog reflects the new operator entrypoint.

## 4. Validation and Tests

- [x] 4.1 Extend `scripts/validate_skillsets.py` with `ENTRYPOINT_SKILL`, required reference names, required route terms, and `validate_entrypoint_module`.
- [x] 4.2 Add entrypoint validation to `validate_operator_skillset` and require `operator/isomer-op-entrypoint` in the operator manifest inventory check.
- [x] 4.3 Add unit fixtures and tests in `tests/unit/test_validate_skillsets.py` for a valid entrypoint, missing DeepSci extension coverage, service-skill first-click misuse, retired-route misuse, missing route-and-proceed behavior, and manifest inventory coverage.
- [x] 4.4 Update `tests/unit/test_system_skill_assets.py` to assert the packaged core group includes and materializes `operator/isomer-op-entrypoint`.
- [x] 4.5 Ensure existing welcome and switch-identity validation tests continue to pass without weakening their contracts.

## 5. Verification

- [x] 5.1 Run `pixi run python scripts/validate_skillsets.py`.
- [x] 5.2 Run `pixi run test tests/unit/test_validate_skillsets.py tests/unit/test_system_skill_assets.py`.
- [x] 5.3 Run `pixi run lint`.
- [x] 5.4 Run `pixi run typecheck`.
- [x] 5.5 Run `pixi run test`.
