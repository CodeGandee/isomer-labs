# Finalize Topic Team

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run directly and use **Targeted Fast-Forward Recovery** from the entrypoint when the missing predecessor can be created by the canonical flow.
2. Read finalization inputs:
   - Topic overview, registration assurance evidence, specialization outputs, and durable setup records including `isomer-srv-topic-env-setup` evidence.
   - Topic Main Development Repository predecessor evidence, projection predecessor evidence, Agent Workspace records, agent names, branch plans, `isomer-managed/` regime status, generated links, and optional delegated workspace-manager inspection evidence when present.
   - Delegated `isomer-srv-agent-env-setup` evidence when present, validation status, blockers, deferrals, and next action refs.
3. Create or update `isomer-topic-summary.md` only in a registered Topic Workspace root:
   - Stop with an explicit registration blocker when only a provisional topic workspace seed exists.
4. Include the sections in **Summary Template** and keep blockers visible when validation is incomplete:
   - Include registration blockers.
   - Include missing Topic Workspace Pixi binding evidence.
   - Include missing delegated `isomer-srv-agent-env-setup` evidence when per-Agent Workspace cwd verification was requested.
   - Include incomplete required `## Gate Checklist` items, smoke-test downgrades, selected-agent partial evidence, and next repair actions when delegated env setup evidence is not fully ready.
5. Report `isomer_topic_summary_path`, `topic_team_validation_status`, blockers, deferrals, and next operator action.
6. Stop at the final summary boundary unless the user explicitly asks for `approve-profile` or `materialize-profile`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step static finalization plan from the topic-team artifacts, setup records, validation outputs, and guardrails, then execute the plan.

## Prerequisite Artifacts

Required predecessor artifact:

- `topic_team_validation_status` from `validate-topic-team`, including ready, ready-with-deferrals, or blocked status.
- Registration assurance from `ensure-topic-registration`, carried through validation.

If validation status is missing, refuse to run directly, explain that the final summary depends on readiness validation, and offer targeted fast-forward recovery to `finalize-topic-team`. Use `python scripts/query_step_dependencies.py path --target finalize-topic-team --include-target` for the inclusive default path and `python scripts/query_step_dependencies.py path --target finalize-topic-team --exclude-target` for the exclusive path.

If registration assurance is missing from the validation context, refuse to run directly, explain that the final summary must report authoritative topic refs or blockers, and offer targeted fast-forward recovery through `ensure-topic-registration` and `validate-topic-team` to `finalize-topic-team`.

## Summary Template

Write `isomer-topic-summary.md` with these sections:

```markdown
# Isomer Topic Summary

## Research Topic

## Topic Registration

## Topic Team

## Goal

## Working Logic

## Environment Setup

## Agent Workspace Layout

## Validation Status

## Blockers and Deferrals

## Next Actions
```

In `## Topic Registration`, summarize `topic_registration_status`, `registered_research_topic_ref`, `registered_topic_workspace_ref`, `registration_command_evidence`, `environment_binding_status`, and registration blockers. In `## Environment Setup`, summarize `topic_environment_status`, `topic.intent.topic_env_requirements`, `topic.env.topic_setup_target_spec`, resolved paths, storage profiles, path sources, Topic Workspace predecessor readiness status, Topic Main Development Repository Git state, external repository projection metadata, required topic `## Gate Checklist` completion evidence, setup commands, changed files, per-agent readiness not checked when reported, and blockers from `isomer-srv-topic-env-setup` when available. In `## Agent Workspace Layout`, report semantic labels first, including `topic.repos.main`, `topic.repos.main.tmp`, `topic.repos.main.isomer_managed`, `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, `topic.repos.main.projections.manifest`, `agent.workspace`, `agent.tmp`, `agent.private_artifacts`, `agent.public_share`, and `agent.links`, then show concrete paths, path sources, Agent Names, branch plans, local tmp posture, validation status, and blockers. Include `topic.intent.agent_env_requirements`, `topic.env.agent_setup_target_spec`, their resolved paths and path-source metadata, required per-agent `## Gate Checklist` completion evidence, per-agent readiness by Agent Name, branch, resolved `agent.workspace`, worktree evidence, command evidence, selected-agent partial evidence, smoke-test downgrades, blockers, and next action from `isomer-srv-agent-env-setup` when present. Identify default paths as `isomer-default.v1` rather than implying fixed-path authority, distinguish Local Tmp Surfaces from worker-visible, owner-preserved `topic.records.*`, and runtime-internal `topic.runtime`, and state that tmp contents are local, ignored, disposable, not shared, and not durable evidence.

Include cwd-friendly guidance: an agent running inside its own Agent Workspace can query its own agent-scoped labels without passing Agent Name; cross-agent queries require explicit Agent Name, Agent Instance, handoff, Artifact, or boundary-approved share context. State that cwd inference is a path-resolution convenience, not filesystem-grade identity or access control.

Do not summarize stale workspace setup evidence as ready when it names legacy support roots, top-level Topic Main Development Repository collaboration directories, or hard-coded default-only paths without semantic label and path-source evidence.

## Guardrails

Do not claim live team readiness, Workspace Runtime readiness, Agent Team Instance creation, adapter preflight, or launch readiness from the summary. Agent environment readiness is static setup evidence from `isomer-srv-agent-env-setup`, not runtime evidence.

Do not hide blockers in prose. Put them in `## Blockers and Deferrals`.

Do not summarize incomplete required checklist items or weaker smoke-test downgrades as full environment readiness. Name the affected checklist item, weaker evidence, limitation, and next repair action.

Do not include secrets, raw command payloads, live provider state, or transient adapter state in `isomer-topic-summary.md`.
