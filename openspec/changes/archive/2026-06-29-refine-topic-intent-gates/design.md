## Context

The current Topic Team Specialization flow has two intent problems. First, topic overview material is written under `topic-def/`, while environment gate material is written under `user-intent/`, so the user-facing specification surface is scattered. Second, `setup-topic-env` and `setup-agent-workspace` may create source gate files while preparing setup handoffs, which makes setup stages interpret vague research intent at the same time they delegate concrete environment work.

The storage layer now lives behind Workspace Path Resolution and `isomer-cli` path surfaces. This change therefore must not make skills remember fixed Markdown paths as contracts. Skills should request semantic labels, receive resolved paths and diagnostics, and treat concrete paths such as `intent/src/topic-env-gate.md` as the default layout, not the public interface.

The prior `refactor-topic-env-skill-boundary` change split Topic Workspace readiness from Agent Workspace readiness. This change moves one level upstream: topic-team specialization should resolve user intent into high-level source specifications before setup services translate those specifications into concrete commands, dependency plans, and verification evidence.

The intended high-level process is:

```text
team specialization invoked
  -> resolve project
  -> resolve topic and create associated intent
  -> resolve topic env requirements and create source intent
  -> create the derived topic env operational spec from topic env intent
  -> materialize topic env
  -> resolve agent env requirements and create source intent
  -> create the derived agent env operational spec from agent env intent
  -> materialize agent env
  -> validate topic team
```

## Goals / Non-Goals

**Goals:**

- Add explicit `resolve-topic-intent`, `resolve-topic-env-gate`, and `resolve-agent-env-gate` subcommands to `isomer-admin-topic-team-specialize`.
- Make `resolve-project` the first process stage after Topic Team Specialization is invoked.
- Define semantic labels for topic overview, topic environment source intent, agent environment source intent, topic env setup target specs, and agent env setup target specs.
- Keep `isomer-default.v1` path bindings for `intent/src/` and `intent/derived/` as default layout examples while requiring skills to resolve those surfaces through Workspace Path Resolution.
- Keep source intent files concise, high level, and user-editable; treat implementation-specific commands and dependency plans as derived target specs for service setup.
- Treat derived operational target spec availability and environment materialization as distinct stages for both topic env and agent env setup.
- Update topic and agent env service contracts so they consume derived target specs from resolved semantic labels, source-intent derivation, or explicit manual file, prompt, or context input.
- Update process docs, output contracts, validation language, and call graphs so intent resolution is distinct from setup execution.

**Non-Goals:**

- Do not add a new runtime service or Python API.
- Do not change Topic Workspace Pixi binding semantics beyond how intent and target-spec surfaces are named and resolved.
- Do not make `setup-topic-env` or `setup-agent-workspace` responsible for understanding vague research topics.
- Do not launch live teams, create Agent Instances, or mutate Workspace Runtime.

## Decisions

### Decision: Use semantic labels as the intent storage contract

The canonical source and target surfaces are semantic labels, not physical paths:

- `topic.intent.overview`: high-level topic understanding.
- `topic.intent.topic_env_requirements`: high-level Topic Workspace environment requirements.
- `topic.intent.agent_env_requirements`: high-level per-Agent Workspace cwd requirements.
- `topic.env.topic_setup_target_spec`: operational topic env setup target spec.
- `topic.env.agent_setup_target_spec`: operational agent env setup target spec.

Skills must resolve these labels through Workspace Path Resolution before reading, writing, materializing, or reporting them. Skill outputs should include the semantic label, resolved path, storage profile, source, source detail, and diagnostics when the resolver provides them.

Alternative considered: make `<topic-workspace>/intent/src/` the skill contract directly. That is easy to explain in docs, but it bypasses the storage layer and recreates the path-memory problem that `isomer-cli` path resolution is meant to remove.

### Decision: Keep `intent/src/` as the default user-editable source layout

The built-in `isomer-default.v1` layout maps `topic.intent.overview` to `<topic-workspace>/intent/src/topic-overview.md`, `topic.intent.topic_env_requirements` to `<topic-workspace>/intent/src/topic-env-gate.md`, and `topic.intent.agent_env_requirements` to `<topic-workspace>/intent/src/agent-env-gate.md`. This keeps the user's topic specification in one predictable default place and removes the split between `topic-def/` and `user-intent/`, while still letting Topic Workspace Manifest bindings relocate those surfaces when needed.

Alternative considered: keep `topic-def/topic-overview.md` and only rename `user-intent/src/env-gate.md`. That would preserve more existing paths, but it would keep topic intent scattered across two concepts and make it harder to explain what users can safely edit.

### Decision: Make the process resolve, target-spec, then materialize

The canonical operator process separates semantic resolution from operational target spec creation and materialization. Topic Team Specialization first resolves the Project and Research Topic context, then creates user-editable source intent through semantic labels. The service skills then consume operational target specs, normally resolved from target-spec semantic labels, and only after those target specs exist do they materialize the topic or agent environment.

Alternative considered: keep `setup-topic-env` and `setup-agent-workspace` as broad stages that both derive and materialize without naming the sub-stages. That is shorter, but it hides the important checkpoint where a human or another agent can inspect the derived spec before any environment mutation.

### Decision: Split environment gate resolution into topic and agent stages

`resolve-topic-env-gate` writes only the high-level Topic Workspace source gate. `resolve-agent-env-gate` writes only the high-level per-Agent Workspace source gate. The topic gate can be resolved before team specialization when the Research Topic already states shared environment needs. The agent gate normally runs only after the process has enough topic-team shape, Agent Name, role expectation, and workspace topology context to describe per-agent cwd needs.

Alternative considered: one `resolve-env-gates` subcommand that writes both files. That is compact, but it hides a real dependency: agent env requirements depend on the planned agents and workspace cwd model, while topic env requirements often do not.

### Decision: Keep source gates high level and derived gates operational

Source files should say what the topic needs, not how Isomer will verify it. For example, the `topic.intent.topic_env_requirements` surface may say "This topic requires NVIDIA Nsight Compute (`ncu`) to be runnable for GPU profiling." The concrete commands, package-source choices, Pixi operations, cwd matrices, expected command output, and execution logs belong in the derived target-spec surfaces.

Alternative considered: allow source gates to include full command matrices whenever the agent can infer them. That makes setup more direct, but it turns user-editable intent into generated implementation detail and makes future user edits risky.

### Decision: Preserve derived gate filenames while moving directories

The topic env target spec is resolved through `topic.env.topic_setup_target_spec`; the default layout path is `<topic-workspace>/intent/derived/isomer-env-gate.md`. The agent env target spec is resolved through `topic.env.agent_setup_target_spec`; the default layout path is `<topic-workspace>/intent/derived/isomer-agent-env-gate.md`. Keeping the existing derived filenames in the default profile reduces churn in output examples and validation language while still moving implementation-specific material out of `user-intent/`.

Alternative considered: rename the topic derived gate to `isomer-topic-env-gate.md`. That is more explicit, but it adds another rename on top of the source path break and does not solve a separate boundary problem.

### Decision: Allow manual service invocation with explicit derived gates

`isomer-srv-topic-env-setup` and `isomer-srv-agent-env-setup` can be invoked manually with an existing derived gate file, an explicitly supplied target-spec prompt, or target-spec context from a caller. In that mode, the service should validate that the target spec is operational enough to materialize, record the target spec source in output, and avoid requiring source-intent semantic labels as the only input.

Alternative considered: require every manual invocation to first write `intent/src/*` and then derive `intent/derived/*`. That keeps one path, but it makes the service less useful as a low-level setup executor and blocks expert users who already have an operational target spec.

### Decision: Treat old paths as legacy blockers, not silent inputs

The new docs should stop presenting `<topic-workspace>/topic-def/topic-overview.md`, `<topic-workspace>/user-intent/src/env-gate.md`, and `<topic-workspace>/user-intent/src/agent-env-gate.md` as canonical. If a workflow finds only an old path, it should report a legacy-path blocker or migration note and name the relevant semantic label and default-layout path to create or move, rather than silently reading the old file as current intent.

Alternative considered: read both old and new paths during a compatibility window. That would reduce immediate friction, but it would keep two active sources of truth and make the process less inspectable.

### Decision: Keep `init-topic` as bootstrap, but move topic understanding into `resolve-topic-intent`

`init-topic` can still create or identify a provisional Topic Workspace seed when the user starts from a new topic. The canonical topic understanding surface, however, should be produced by `resolve-topic-intent` at `topic.intent.overview`. Existing `clarify-topic` behavior should revise that same semantic surface.

Alternative considered: replace `init-topic` entirely with `resolve-topic-intent`. That would simplify the public list, but `init-topic` still names the useful bootstrap job of choosing a safe provisional workspace before any intent file can be written.

## Risks / Trade-offs

- Legacy path churn may confuse existing operators → Mitigate by updating help text, output contracts, validation, and final summaries to name the new paths consistently.
- Semantic-label indirection may make docs less immediately concrete → Mitigate by always reporting both the semantic label and the resolved path, and by showing `isomer-default.v1` paths as examples.
- High-level source gates may become too vague for service setup → Mitigate by requiring `resolve-topic-env-gate` and `resolve-agent-env-gate` to preserve open questions and blockers when the user intent is not specific enough for derived setup.
- Agent gate resolution may run before Agent Names are stable → Mitigate by requiring authoritative Agent Names or an explicit partial scope before `resolve-agent-env-gate` claims readiness for service delegation.
- Derived gate references are widespread → Mitigate by preserving the existing derived filenames in `isomer-default.v1`, treating them as target specs, and changing the skill contract to semantic labels.

## Migration Plan

1. Update OpenSpec specs for Workspace Path Resolution and Topic Workspace Manifest to define the new intent and target-spec semantic labels, default bindings, and storage profiles.
2. Update `isomer-admin-topic-team-specialize` and its reference pages to add the three new subcommands, revise the fast-forward and step-by-step order, and remove setup-stage source gate generation.
3. Update `isomer-srv-topic-env-setup` docs and output contracts so materialization consumes a topic env target spec from `topic.env.topic_setup_target_spec`, a freshly derived spec from `topic.intent.topic_env_requirements`, or an explicit manual target spec input.
4. Update `isomer-srv-agent-env-setup` docs and output contracts so materialization consumes an agent env target spec from `topic.env.agent_setup_target_spec`, a freshly derived spec from `topic.intent.agent_env_requirements`, or an explicit manual target spec input.
5. Update process design docs and skill call graphs so they show intent resolution before setup delegation.
6. Run skill validation and OpenSpec validation. Rollback is documentation-only: revert the docs and specs to the previous `topic-def/` and `user-intent/` paths if implementation discovers a required compatibility constraint.

## Open Questions

- Should implementation include a temporary helper note that tells users how to move old files into `intent/src/`, or should the docs only report blockers and expected new paths?
