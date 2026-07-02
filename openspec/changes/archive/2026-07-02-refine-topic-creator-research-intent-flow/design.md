## Context

`isomer-admin-topic-creator` is becoming the front door for blank-state or partial-state manual research setup. The current topic creator wording still carries an overloaded `define-topic` stage that can imply topic naming, registration, `topic.intent.overview` writing, topic environment source-intent writing, and Topic Actor setup intent are one operation. The rest of the platform already has clearer primitives: Workspace Path Resolution exposes `topic.intent.overview` and `topic.intent.topic_env_requirements`, and Topic Team Specialization separates topic intent, topic env gate definition, and environment setup. This change adapts that separation for manual Topic Actor research and adds actor-definition surfaces.

The refined flow needs to make one invariant explicit: a topic starts from user-given Research Topic substance. The source can be a prompt, a Markdown file, existing context, or a registered concrete topic statement, but missing or generic topic material must block before the system derives a topic id, names a Topic Workspace, creates a directory, writes `topic-overview.md`, writes `topic-env-gate.md`, writes `actor-definitions.md`, or derives actor env gates.

## Goals / Non-Goals

**Goals:**

- Make concrete Research Topic input a hard gate for Topic Creator initialization.
- Split topic identity resolution from research intent writing, topic env definition, actor definition, and setup.
- Add `create-research-intent` as the Topic Creator step that only creates or updates `topic.intent.overview`.
- Add `define-topic-env` as the Topic Creator step that creates or refines `topic.intent.topic_env_requirements` and waits for user verification unless running under `fast-forward`.
- Add `define-actors` as the Topic Creator step that creates or refines `topic.intent.actor_definitions`, including actor duties, intended usage, and per-actor source env gates.
- Ensure `setup-topic-env` consumes `topic.intent.topic_env_requirements` and writes derived setup gates before materializing or installing topic environment work.
- Ensure `setup-actors` consumes `topic.intent.actor_definitions`, materializes actor workspaces, writes derived actor env gates, and verifies those gates.
- Keep lower-level Project, registration, runtime, environment, actor, bootstrap, and start-pack ownership delegated.
- Update validation so the skill cannot regress to the old `define-topic`/implicit-intent shape.

**Non-Goals:**

- Do not change Workspace Path Resolution beyond adding `topic.intent.actor_definitions`, `topic.env.actor_env_gates`, and their default storage paths.
- Do not change `isomer-cli project topics create` semantics.
- Do not change the topic-team-specialization `resolve-topic-intent` workflow except as a reference pattern.
- Do not create formal Topic Agent Team Profile, Agent Workspace, or Agent Team Instance behavior in Topic Creator.

## Decisions

1. Replace `define-topic` with a topic-input helper plus narrow topic intent creation.

   `define-topic` is ambiguous because it can mean derive a topic id, write topic intent, prepare registration, or infer environment needs. The refined skill should use a helper such as `resolve-topic-input` for concrete topic source extraction and topic id/workspace seed derivation, then use `create-research-intent` only for writing the user-editable topic overview. Alternative considered: keep env and actor intent inside `create-research-intent`. That would make user review harder because topic definition, environment setup, and worker topology are different decisions.

2. Treat topic env definition as its own user-facing subcommand.

   `define-topic-env` should create or refine `topic.intent.topic_env_requirements`, defaulting to `<topic-workspace>/intent/src/topic-env-gate.md`. Outside `fast-forward`, it should stop for user verification because the topic env gate controls later derived setup gates and installation work. In `fast-forward`, it may proceed without an interactive stop, but it must report the generated gate and any assumptions.

3. Keep topic env setup downstream of the topic env gate.

   `setup-topic-env` should read `topic.intent.topic_env_requirements`, then create or validate derived gates such as `topic.env.topic_setup_target_spec`, defaulting to `<topic-workspace>/intent/derived/isomer-env-gate.md`, before delegating installation, Pixi configuration, repo setup, or command verification. It must not invent a topic env gate when one is missing except through `define-topic-env`.

4. Treat actor definition as its own user-facing subcommand.

   `define-actors` should create or refine `topic.intent.actor_definitions`, defaulting to `<topic-workspace>/intent/src/actor-definitions.md`. The file should include each actor's name, duty, intended usage, controller/runtime assumptions when known, and source env gate requirements. If invoked without additional actor details, or if the user says only "create the operator actor" or equivalent, it should create the default `operator` actor definition.

5. Keep actor setup downstream of actor definitions.

   `setup-actors` should read `topic.intent.actor_definitions`, then delegate actor registration and workspace materialization to `isomer-admin-topic-workspace-mgr`, write or validate derived actor env gates at `topic.env.actor_env_gates`, defaulting to `<topic-workspace>/intent/derived/actor-env-gates.md`, and verify that the declared actor env gates pass from each actor cwd. It should not accept actor readiness from a workspace path alone.

6. Register or otherwise establish a candidate Topic Workspace before writing intent.

   `topic.intent.overview`, `topic.intent.topic_env_requirements`, `topic.intent.actor_definitions`, and derived gate labels are semantic Topic Workspace surfaces, so the workflow must have a registered or candidate Topic Workspace that can resolve those labels before it writes. For a new unregistered topic, the skill can derive a safe topic id/workspace seed from concrete topic substance and then create/register the Topic Workspace before `create-research-intent`. It must not infer a workspace name from an empty prompt, generic `default` topic, sibling directory names, or placeholder registration.

7. Preserve semantic label authority.

   The workflow may document that `isomer-default.v1` resolves `topic.intent.overview` to `<topic-workspace>/intent/src/topic-overview.md`, `topic.intent.topic_env_requirements` to `<topic-workspace>/intent/src/topic-env-gate.md`, `topic.intent.actor_definitions` to `<topic-workspace>/intent/src/actor-definitions.md`, and `topic.env.actor_env_gates` to `<topic-workspace>/intent/derived/actor-env-gates.md`, but the implementation and skill text should instruct agents to resolve the labels first and report semantic label evidence.

## Risks / Trade-offs

- [Risk] `create-research-intent` can be confused with Project registration or environment setup. → Mitigation: make its inputs and non-goals explicit; it writes only `topic.intent.overview` and does not register topics, define env gates, or create workspaces from nothing.
- [Risk] `topic.intent.topic_env_requirements` can be confused with the operational `topic.env.topic_setup_target_spec`. → Mitigation: describe it as source intent for later setup; the setup target spec, dependency installation, and readiness evidence remain outside `create-research-intent`.
- [Risk] `topic.intent.actor_definitions` can be confused with formal per-agent `topic.intent.agent_env_requirements`. → Mitigation: describe actor definitions as manual Topic Actor intent for `topic.actors.workspace`, and keep formal Agent Workspace cwd readiness on `agent.workspace` plus `topic.intent.agent_env_requirements`.
- [Risk] Fast-forward may skip useful human review of `topic-env-gate.md`. → Mitigation: require non-fast-forward `define-topic-env` to wait for user verification, and require `fast-forward` to report generated gate assumptions before setup.
- [Risk] Moving `define-topic` may break existing help text or tests that still list it. → Mitigation: update the entrypoint, help page, reference pages, validator constants, and unit fixtures together.
- [Risk] The skill may over-block when context contains a usable registered topic statement. → Mitigation: allow topic source to come from prompt, Markdown file, existing context, or registered concrete statement, while rejecting missing/generic placeholders.
- [Risk] Agents may hard-code `<topic-workspace>/intent/src/topic-overview.md`, `<topic-workspace>/intent/src/topic-env-gate.md`, `<topic-workspace>/intent/src/actor-definitions.md`, or `<topic-workspace>/intent/derived/actor-env-gates.md`. → Mitigation: validation and reference text should require Workspace Path Resolution and treat the default paths as explanatory only.

## Migration Plan

1. Update `isomer-admin-topic-creator` subcommand tables and flow narrative.
2. Add `references/create-research-intent.md` based on the existing `resolve-topic-intent` pattern, scoped to `topic.intent.overview`.
3. Add `references/define-topic-env.md` for `topic.intent.topic_env_requirements` and user verification behavior.
4. Add `references/define-actors.md` for `topic.intent.actor_definitions`, including the default `operator` behavior.
5. Replace or retire `references/define-topic.md` in favor of topic-input resolution, research-intent creation, topic env definition, and actor definition references.
6. Update `fast-forward`, `status`, `repair`, `help`, setup references, and validation to reflect the staged ladder.
7. Add Workspace Path Resolution support for `topic.intent.actor_definitions` and `topic.env.actor_env_gates`.
8. Run operator skill validation and targeted unit tests.

## Open Questions

- Should the lower-level helper be named `resolve-topic-input`, `resolve-topic-source`, or `resolve-topic-seed`?
- Should Topic Creator keep a compatibility mention for explicit `define-topic` user prompts, routing them to `create-research-intent`, or should `define-topic` disappear completely from public help?
