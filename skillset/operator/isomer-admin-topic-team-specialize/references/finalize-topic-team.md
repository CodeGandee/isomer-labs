# Finalize Topic Team

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run and tell the user why.
2. Read the topic overview, registration assurance evidence, specialization outputs, durable setup records including `isomer-srv-topic-env-setup` evidence, Agent Workspace records, agent names, branch plans, `isomer-managed/` regime status, generated links, delegated Git-backed workspace manager evidence, delegated `isomer-srv-agent-env-setup` evidence when present, validation status, blockers, deferrals, and next action refs.
3. Create or update `isomer-topic-summary.md` in the registered Topic Workspace root, or stop with an explicit registration blocker when only a provisional topic workspace seed exists.
4. Include the sections in **Summary Template** and keep blockers visible when validation is incomplete, including registration blockers, missing Topic Workspace Pixi binding evidence, missing delegated `isomer-admin-topic-workspace-mgr` evidence when Git-backed Agent Workspace worktrees were requested, and missing delegated `isomer-srv-agent-env-setup` evidence when per-Agent Workspace cwd verification was requested.
5. Report `isomer_topic_summary_path`, `topic_team_validation_status`, blockers, deferrals, and next operator action.
6. Stop at the final summary boundary unless the user explicitly asks for `approve-profile` or `materialize-profile`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step static finalization plan from the topic-team artifacts, setup records, validation outputs, and guardrails, then execute the plan.

## Prerequisite Artifacts

Required predecessor artifact:

- `topic_team_validation_status` from `validate-topic-team`, including ready, ready-with-deferrals, or blocked status.
- Registration assurance from `ensure-topic-registration`, carried through validation.

If validation status is missing, refuse to run, explain that the final summary depends on readiness validation, and tell the user to run `validate-topic-team` first.

If registration assurance is missing from the validation context, refuse to run, explain that the final summary must report authoritative topic refs or blockers, and tell the user to run `ensure-topic-registration` and then `validate-topic-team`.

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

In `## Topic Registration`, summarize `topic_registration_status`, `registered_research_topic_ref`, `registered_topic_workspace_ref`, `registration_command_evidence`, `environment_binding_status`, and registration blockers. In `## Environment Setup`, summarize `topic_environment_status`, `env_gate_path`, `derived_gate_path`, Topic Workspace predecessor readiness status, setup commands, changed files, per-agent readiness not checked when reported, and blockers from `isomer-srv-topic-env-setup` when available. In `## Agent Workspace Layout`, report semantic labels first, including `topic.repos.main`, `topic.repos.main.tmp`, `topic.repos.main.isomer_managed`, `agent.workspace`, `agent.tmp`, `agent.private_artifacts`, `agent.public_share`, and `agent.links`, then show concrete paths, path sources, Agent Names, branch plans, local tmp posture, validation status, and blockers. Include `user-intent/src/agent-env-gate.md`, `user-intent/derived/isomer-agent-env-gate.md`, per-agent readiness by Agent Name, branch, resolved `agent.workspace`, command evidence, selected-agent partial evidence, blockers, and next action from `isomer-srv-agent-env-setup` when present. Identify default paths as `isomer-default.v1` rather than implying fixed-path authority, distinguish Local Tmp Surfaces from worker-visible, owner-preserved `topic.records.*`, and runtime-internal `topic.runtime`, and state that tmp contents are local, ignored, disposable, not shared, and not durable evidence.

Include cwd-friendly guidance: an agent running inside its own Agent Workspace can query its own agent-scoped labels without passing Agent Name; cross-agent queries require explicit Agent Name, Agent Instance, handoff, Artifact, or boundary-approved share context. State that cwd inference is a path-resolution convenience, not filesystem-grade identity or access control.

Do not summarize stale workspace setup evidence as ready when it names legacy support roots, top-level Topic Main Repository collaboration directories, or hard-coded default-only paths without semantic label and path-source evidence.

## Guardrails

Do not claim live team readiness, Workspace Runtime readiness, Agent Team Instance creation, adapter preflight, or launch readiness from the summary. Agent environment readiness is static setup evidence from `isomer-srv-agent-env-setup`, not runtime evidence.

Do not hide blockers in prose. Put them in `## Blockers and Deferrals`.

Do not include secrets, raw command payloads, live provider state, or transient adapter state in `isomer-topic-summary.md`.
