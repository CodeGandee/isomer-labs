# Resolve Agent Env Gate

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require topic intent, topic registration evidence, topic env predecessor evidence when available, and enough topic-team or caller-provided scope to know the relevant Agent Names or selected-agent subset. If Agent Names are not authoritative and no explicit partial scope is supplied, report a blocker instead of inventing names.
2. Resolve the semantic label `topic.intent.agent_env_requirements` through Workspace Path Resolution. Record the semantic label, resolved path, storage profile, source, source detail, and diagnostics. In `isomer-default.v1`, the resolved path is `<topic-workspace>/intent/src/agent-env-gate.md`.
3. Read `topic.intent.overview`, `topic.intent.topic_env_requirements`, topic env predecessor evidence, specialization outputs, Agent Names, workspace topology evidence, and any user-provided per-agent cwd requirements.
4. Write or update the resolved `topic.intent.agent_env_requirements` path with concise high-level per-Agent Workspace cwd requirements. State what each planned Agent Workspace must be able to do from its cwd. Keep this source intent user-editable and avoid derived command matrices, worktree creation logs, or verification results.
5. If per-Agent Workspace requirements are too vague to derive a target spec later, write open questions or report `agent_env_source_status: blocked`, then stop before `setup-agent-workspace` delegates to `isomer-srv-agent-env-setup`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from topic-team material, Agent Name evidence, workspace topology evidence, user-provided cwd requirements, Workspace Path Resolution output, and this reference page, then execute the plan.

## Prerequisite Artifacts

If any required predecessor artifact is missing, refuse to run and tell the user why. Required predecessor artifacts are `topic.intent.overview`, topic registration evidence, topic env predecessor evidence when available, and enough topic-team or caller-provided scope to know authoritative Agent Names or an explicit selected-agent subset.

## Agent Env Requirements Template

```markdown
# Agent Environment Requirements

## Agent Scope

## Shared Per-Agent Cwd Requirements

## Agent-Specific Requirements

## Topic Env Predecessor Expectations

## Workspace Topology Expectations

## Assumptions

## Open Questions

## Source Material
```

## Output Contract

- `agent_env_source_status`: ready, revised, blocked, or not changed.
- `agent_env_source_label`: `topic.intent.agent_env_requirements`.
- `agent_env_source_path`: resolved path for `topic.intent.agent_env_requirements`.
- `agent_env_source_storage_profile`: usually `topic_intent_source_file`.
- `agent_env_source`: resolver source such as `default_profile`, `topic_workspace_manifest`, `env`, or `path_plan`.
- `agent_env_source_detail`: resolver source detail such as `isomer-default.v1` or manifest binding detail.
- `agent_env_source_diagnostics`: Workspace Path Resolution diagnostics and source-intent blockers.
- `agent_scope`: authoritative Agent Names, selected-agent subset, or blocker.
- `next_operator_action`: usually `setup-agent-workspace` when source intent is usable, or ask the user to answer open questions.

## Guardrails

Do not derive `topic.env.agent_setup_target_spec` here. The agent env service owns operational target-spec generation, Topic Main Repository configuration, per-agent command matrices, cwd verification, readiness by Agent Name, and execution logs.

Do not write canonical source intent to `<topic-workspace>/user-intent/src/agent-env-gate.md`. If only that legacy path exists, report a legacy-path migration note and name `topic.intent.agent_env_requirements` plus its resolved default-layout path.

Do not create Agent Workspace worktrees, mutate Topic Main Repository configuration, run per-agent commands, mutate Workspace Runtime, launch Houmao, or create live Agent Instances from this subcommand.
