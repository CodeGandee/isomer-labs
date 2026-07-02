## 1. Retire Deprecated Operator Skills

- [x] 1.1 Remove `skillset/operator/isomer-admin-topic-prepare/` from the active operator skillset.
- [x] 1.2 Remove `skillset/operator/isomer-admin-manual-research-session/` from the active operator skillset.
- [x] 1.3 Search active operator docs, manifests, and README files for `isomer-admin-topic-prepare` and `isomer-admin-manual-research-session`; remove active routes or mark unavoidable historical mentions as archived provenance.

## 2. Decouple Topic Creator from V2 Research Bootstrap

- [x] 2.1 Update `skillset/operator/isomer-admin-topic-creator/SKILL.md` to remove v2 research bootstrap from the preserved initialization ladder, helper subcommand table, required inputs, output contract, and delegation guardrails.
- [x] 2.2 Remove or retire `skillset/operator/isomer-admin-topic-creator/references/bootstrap-research.md` from the active Topic Creator subcommand surface.
- [x] 2.3 Update `fast-forward`, `step-by-step`, `run-to`, `status`, `repair`, and related Topic Creator references so the terminal setup path ends at Topic Workspace and Topic Actor readiness.
- [x] 2.4 Update `finalize.md` so readiness validation and `topic.workspace.summary` no longer require v2 bootstrap outputs, placeholder-binding entrypoints, selected v2 skills, or research recording command shapes.
- [x] 2.5 Update `help.md`, `agents/openai.yaml`, and any Topic Creator examples so user-facing text describes v2-independent topic and actor preparation.

## 3. Add Actor Onboarding to Setup Actors

- [x] 3.1 Expand `setup-actors.md` to produce v2-independent actor onboarding material with actor identity, cwd, branch, integration surface, support labels, boundary notes, verification evidence, and blockers.
- [x] 3.2 Ensure actor onboarding material does not mention selected v2 skills, v2 placeholder binding files, v2 bootstrap records, `isomer-cli ext research records`, or accepted research artifact command shapes.
- [x] 3.3 If actor-local card or pointer behavior is documented, keep it under `topic.actors.isomer_managed` or `topic.actors.links` and describe it as startup convenience rather than authoritative research truth.
- [x] 3.4 Update summary output examples to include actor onboarding readiness and to preserve the rule that `topic.repos.main` is the integration surface, not every worker's cwd.

## 4. Update Operator Routing and Specialization References

- [x] 4.1 Update `skillset/operator/README.md` to remove retired skill rows and route manual/human-orchestrated setup through current Topic Creator subcommands only.
- [x] 4.2 Update `isomer-admin-project-mgr` skill docs and references so `prepare-topic` and `manual-research` no longer mention nonexistent `plan`, `create`, or `start-manual-research` Topic Creator subcommands.
- [x] 4.3 Update `isomer-admin-project-mgr` routing so advanced compatibility paths no longer route to retired skills.
- [x] 4.4 Update `isomer-admin-topic-team-specialize` docs and references so reusable common preparation evidence comes from Topic Creator / Topic Workspace readiness evidence rather than `isomer-admin-topic-prepare`.
- [x] 4.5 Update `isomer-admin-topic-workspace-mgr` docs and references so it no longer describes itself as complementing retired skills or creating research handoff/start-pack material.

## 5. Move V2-Specific Bootstrap Ownership to Research Paradigm

- [x] 5.1 Update `skillset/research-paradigm/v2/isomer-rsch-workspace-mgr-v2/SKILL.md` to state that it owns v2 research workspace bootstrap, selected v2 skill readiness, placeholder binding readiness, actor access plans, and accepted research artifact guidance.
- [x] 5.2 Update active `isomer-rsch-workspace-mgr-v2` references so they consume Topic Workspace and Topic Actor readiness evidence from operator skills as input.
- [x] 5.3 Preserve Topic Actor metadata in v2 outputs when human-orchestrated actors are in scope.
- [x] 5.4 Keep v2-specific recording metadata and command guidance out of operator skill files.

## 6. Validation

- [x] 6.1 Run focused stale-reference searches for retired skill names, `isomer-rsch-workspace-mgr-v2`, `placeholder-bindings.md`, `<RSCH_`, selected v2 skill wording, `isomer-cli ext research records`, and stale Topic Creator subcommands in active operator files.
- [x] 6.2 Run `openspec validate separate-operator-and-research-bootstrap --strict`.
- [x] 6.3 Run repository skill validation for operator and research-paradigm skills if available.
- [x] 6.4 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test` if implementation touches Python code or validation scripts.
- [x] 6.5 Record any skipped validation with the reason and remaining risk. No validation was skipped.
