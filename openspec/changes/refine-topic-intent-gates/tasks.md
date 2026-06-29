## 1. Topic Team Intent Resolution

- [x] 1.1 Update `skillset/operator/isomer-admin-topic-team-specialize/SKILL.md` to present the canonical process as `team specialization invoked -> resolve-project -> resolve-topic-intent -> resolve-topic-env-gate -> derive topic env spec -> materialize topic env -> resolve-agent-env-gate -> derive agent env spec -> materialize agent env -> validate-topic-team`.
- [x] 1.2 Add reference pages for `resolve-topic-intent`, `resolve-topic-env-gate`, and `resolve-agent-env-gate` with workflows, predecessor semantic labels, default-layout source file templates, output contracts, and guardrails.
- [x] 1.3 Revise `resolve-project`, `init-topic`, and `clarify-topic` references so project resolution precedes intent mutation and topic understanding is written and revised through `topic.intent.overview`.
- [x] 1.4 Revise `fast-forward`, `step-by-step`, and `help` references so the flow uses project resolution, semantic label resolution, source intent creation, derived spec creation, materialization, and validation as separate stages.

## 2. Semantic Storage Surfaces

- [x] 2.1 Add Workspace Path Resolution support for `topic.intent.overview`, `topic.intent.topic_env_requirements`, `topic.intent.agent_env_requirements`, `topic.env.topic_setup_target_spec`, and `topic.env.agent_setup_target_spec`.
- [x] 2.2 Add default `isomer-default.v1` bindings for those labels to the current `intent/src/*` and `intent/derived/*` Markdown files.
- [x] 2.3 Add Topic Workspace Manifest support for `topic_intent_source_file` and `topic_env_target_spec_file` storage profiles, including validation, safe overrides, and CLI-backed binding registration.
- [x] 2.4 Update skill outputs to report semantic label, resolved path, storage profile, source, source detail, and diagnostics for intent and target-spec surfaces.

## 3. Setup Handoff Boundaries

- [x] 3.1 Revise `setup-topic-env` so the operator flow requires `topic.intent.topic_env_requirements`, does not generate the source gate during setup, and treats `topic.env.topic_setup_target_spec` as the target spec consumed before topic env materialization.
- [x] 3.2 Revise `setup-agent-workspace` so the operator flow requires `topic.intent.agent_env_requirements` before agent env service delegation and treats `topic.env.agent_setup_target_spec` as the target spec consumed before agent env materialization.
- [x] 3.3 Revise `validate-topic-team` and `finalize-topic-team` so they report semantic labels plus resolved evidence paths and treat old `topic-def/` or `user-intent/` paths as legacy blockers or migration notes.

## 4. Service Skill Path Contracts

- [x] 4.1 Update `isomer-srv-topic-env-setup` docs and references so the service accepts a derived topic env target spec from `topic.env.topic_setup_target_spec`, source-intent derivation from `topic.intent.topic_env_requirements`, or explicit manual file, prompt, or context input.
- [x] 4.2 Update topic env service references so source gates stay high level, target specs contain Pixi commands, repo acquisition details, dependency plans, expected outputs, blockers, and execution logs, and materialization records the target spec source.
- [x] 4.3 Update `isomer-srv-agent-env-setup` docs and references so the service accepts a derived agent env target spec from `topic.env.agent_setup_target_spec`, source-intent derivation from `topic.intent.agent_env_requirements`, or explicit manual file, prompt, or context input.
- [x] 4.4 Update agent env service references so `topic.env.topic_setup_target_spec` is the topic env predecessor, `topic.env.agent_setup_target_spec` is the per-agent cwd verification matrix, materialization records the target spec source, and manual invocation does not require `topic.intent.agent_env_requirements` when an explicit target spec is supplied.
- [x] 4.5 Update environment enclosure references to validate package-source, fallback, runtime wiring, and verification details in explicit or resolved topic env target specs before mutation.

## 5. Process Docs and Call Graphs

- [x] 5.1 Revise `context/design/skill-process/team-specialization.md` to show intent resolution before setup delegation in the Mermaid sequence, skill call graph, formal process sketch, explanation, and evidence handoffs.
- [x] 5.2 Revise `skillset/callgraph.md` so top-level skill routes show topic-team specialization resolving intent before calling topic env or agent env setup services.
- [x] 5.3 Search and update remaining docs that present `<topic-workspace>/topic-def/topic-overview.md`, `<topic-workspace>/user-intent/src/env-gate.md`, or `<topic-workspace>/user-intent/src/agent-env-gate.md` as canonical current paths.

## 6. Validation

- [x] 6.1 Run `openspec validate refine-topic-intent-gates --strict` and fix any artifact errors.
- [x] 6.2 Run skill validation for the updated operator and service skills, including `skill-creator` quick validation where applicable.
- [x] 6.3 Run repo skillset or unit validation commands that cover required skill terms and semantic path contracts.
- [x] 6.4 Report changed files, validation commands, remaining legacy-path notes, and any deferred compatibility decisions.
