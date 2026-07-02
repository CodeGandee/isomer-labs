## 1. Refine Topic Creator Flow

- [x] 1.1 Update `skillset/operator/isomer-admin-topic-creator/SKILL.md` so concrete Research Topic input is a hard gate before topic id, Topic Workspace, registration, or intent-file creation.
- [x] 1.2 Replace stale `define-topic` intent ownership with a lower-level topic-input helper stage and user-facing `create-research-intent`, `define-topic-env`, and `define-actors` subcommands.
- [x] 1.3 Add `skillset/operator/isomer-admin-topic-creator/references/create-research-intent.md` to create or update only `topic.intent.overview` through Workspace Path Resolution.
- [x] 1.4 Add `skillset/operator/isomer-admin-topic-creator/references/define-topic-env.md` to create or refine `topic.intent.topic_env_requirements`, wait for user verification outside `fast-forward`, and report assumptions in `fast-forward`.
- [x] 1.5 Add `skillset/operator/isomer-admin-topic-creator/references/define-actors.md` to create or refine `topic.intent.actor_definitions`, including default `operator` behavior when actor details are absent.
- [x] 1.6 Update `setup-topic-env` to consume the verified topic env gate, derive `topic.env.topic_setup_target_spec`, and delegate installation/materialization without inventing missing source gates.
- [x] 1.7 Update `setup-actors` to consume actor definitions, materialize actor workspaces, generate `topic.env.actor_env_gates`, and verify those gates from actor cwd.
- [x] 1.8 Update `fast-forward`, `status`, `repair`, `help`, and dependent reference pages to route through the staged ladder: `create-research-intent`, `define-topic-env`, `setup-topic-env`, `define-actors`, `setup-actors`.
- [x] 1.9 Remove or retire stale `define-topic` reference usage so the skill no longer presents it as the research intent writer.

## 2. Update Validation and Tests

- [x] 2.1 Update `scripts/validate_skillsets.py` Topic Creator constants and checks to require `create-research-intent`, `define-topic-env`, `define-actors`, topic-input gate wording, `topic.intent.overview`, `topic.intent.topic_env_requirements`, `topic.intent.actor_definitions`, and `topic.env.actor_env_gates` semantic path resolution guidance.
- [x] 2.2 Update `tests/unit/test_validate_skillsets.py` fixtures and assertions for the new topic-input and research-intent flow.
- [x] 2.3 Add or update regression coverage that rejects missing staged topic intent guidance, missing topic env gate verification guidance, missing actor definition and derived actor env gate guidance, and stale `define-topic` research-intent ownership.

## 3. Update Storage Surface Support

- [x] 3.1 Add `topic.intent.actor_definitions` to the Workspace Path Resolution semantic surface catalog with default path `intent/src/actor-definitions.md` and a topic intent source-file storage profile.
- [x] 3.2 Add `topic.env.actor_env_gates` to the Workspace Path Resolution semantic surface catalog with default path `intent/derived/actor-env-gates.md` and a topic env target-spec storage profile.
- [x] 3.3 Add path-resolution tests for the actor definitions and derived actor env gates labels.

## 4. Verify

- [x] 4.1 Run `pixi run validate-operator-skills`.
- [x] 4.2 Run `pixi run python -m unittest tests.unit.test_validate_skillsets`.
- [x] 4.3 Run `pixi run validate-skills`.
- [x] 4.4 Run `openspec validate refine-topic-creator-research-intent-flow --strict`.
