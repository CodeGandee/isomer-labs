---
name: isomer-admin-topic-prepare
description: Prepare a Research Topic for later manual research or Topic Team Specialization by resolving topic registration, Workspace Runtime, topic environment readiness, topic-main readiness, research storage bootstrap inputs, and the default operator Topic Actor Workspace unless explicitly opted out.
---

# Isomer Admin Topic Prepare

Use this operator skill when a Project Operator Session or Operator Agent needs reusable topic preparation before either human-orchestrated Topic Actor research or formal Topic Team Specialization. The skill prepares the common topic layer and delegates topology mutation to existing owners: Project lifecycle work to `isomer-admin-project-mgr`, topic environment setup to `isomer-srv-topic-env-setup`, Topic Actor CRUD and Topic Actor Workspace materialization to `isomer-admin-topic-workspace-mgr`, and research placeholder/storage bootstrap to `isomer-rsch-workspace-mgr-v2`.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Resolve topic intent**. Resolve or create the Research Topic and registered Topic Workspace through Project Manifest-backed Isomer context. Read [references/topic-preparation-workflow.md](references/topic-preparation-workflow.md).
2. **Prepare common topic state**. Ensure Workspace Runtime exists or is valid, ensure topic intent and topic environment requirements exist when setup is requested, delegate topic environment setup, and report `topic.repos.main` as the Git anchor and integration surface. Read [references/topic-preparation-workflow.md](references/topic-preparation-workflow.md).
3. **Ensure the operator actor by default**. Unless the user explicitly says not to create it, delegate registration and materialization of the reserved `operator` Topic Actor and its `topic.actors.workspace` cwd to `isomer-admin-topic-workspace-mgr`. Read [references/operator-topic-actor.md](references/operator-topic-actor.md).
4. **Record preparation evidence**. Produce a topic operation summary with registered refs, runtime status, topic-main readiness, Topic Actor roster, storage bootstrap status, blockers, and next actions. Read [references/output-templates.md](references/output-templates.md).
5. **Return the handoff route**. Route manual or human-orchestrated research to `isomer-admin-manual-research-session`; route formal team setup to `isomer-admin-topic-team-specialize`; route pure actor CRUD or repair to `isomer-admin-topic-workspace-mgr`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a bounded preparation plan from Project context, topic registration, runtime state, semantic path evidence, and the user's requested next workflow.

## Required Inputs

- A selected Project root or Project Manifest context.
- A concrete Research Topic statement or registered Research Topic ref.
- Operator intent for mutation before creating topic registration, Workspace Runtime state, topic environment material, or Topic Actor bindings.
- An explicit opt-out when the user does not want the default `operator` Topic Actor or Topic Actor Workspace.

## Output Contract

Default to **Essential Output** in chat. Print **Complete Output** only when the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output.

### Essential Output

Report `status`, selected Research Topic and Topic Workspace refs, `topic.repos.main` readiness, Workspace Runtime readiness, default `operator` Topic Actor status or opt-out status, research storage bootstrap status, blockers, and next operator action.

### Complete Output

Include resolved semantic labels, commands run, topic environment service evidence, Topic Actor binding and workspace evidence, actor-scoped path diagnostics, runtime validation output, topic operation summary path or record ref, and next handoff route.

## Guardrails

Do not infer a Research Topic or Topic Workspace from sibling directories. Use Project Manifest-backed CLI/API surfaces.

Do not create, repair, or replace `topic.repos.main` directly from this skill. Delegate topic environment setup and topic-main readiness to `isomer-srv-topic-env-setup`.

Do not hand-edit `topic-workspace.toml` for Topic Actors. Delegate Topic Actor registration, update, archive, materialization, repair, and diagnostics to `isomer-admin-topic-workspace-mgr` or the backed `project topic-actors ...` CLI surface.

Do not require a Topic Agent Team Profile, Agent Team Instance, Agent Instance, formal Agent Workspace, Houmao launch dossier, or managed-agent launch for common topic preparation.

Do not silently recreate the `operator` Topic Actor after an explicit user opt-out. Report a repairable blocker when a later step requires it.
