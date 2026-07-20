# Resolve Agent Env Gate

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require enough input to describe per-agent cwd requirements:
   - Require topic intent and topic registration evidence.
   - Use topic env predecessor evidence when available.
   - Require enough topic-team or caller-provided scope to know the relevant Agent Names or selected-agent subset.
   - If Agent Names are not authoritative and no explicit partial scope is supplied, report a blocker instead of inventing names.
2. Resolve the semantic label `topic.intent.agent_env_requirements` through Workspace Path Resolution:
   - Record the semantic label, resolved path, storage profile, source, source detail, and diagnostics.
   - In `isomer-default.v1`, the resolved path is `<topic-workspace>/intent/src/agent-env-gate.md`.
3. Read agent env source inputs:
   - Include `topic.intent.overview`, `topic.intent.topic_env_requirements`, topic env predecessor evidence, Topic Main Development Repository predecessor evidence, projection predecessor expectations, specialization outputs, and Agent Names.
   - Include any user-provided per-agent cwd requirements.
4. Write or update the resolved `topic.intent.agent_env_requirements` path:
   - Keep the file concise and high-level.
   - State what each planned Agent Workspace must be able to do from its cwd.
   - Keep this source intent user-editable and avoid derived command matrices, worktree creation logs, or verification results.
5. If per-Agent Workspace requirements are too vague to derive a target spec later:
   - Write open questions or explain that Agent environment source intent is blocked.
   - Stop before `setup-agent-workspace` delegates to `isomer-srv-agent-env-setup`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from topic-team material, Agent Name evidence, workspace topology evidence, user-provided cwd requirements, Workspace Path Resolution output, and this reference page, then execute the plan.

## Prerequisite Artifacts

If any required predecessor artifact is missing, refuse to run directly and use **Targeted Fast-Forward Recovery** from the entrypoint when the missing predecessor can be created by the canonical flow. Required predecessor artifacts are `topic.intent.overview`, topic registration evidence, topic env predecessor evidence when available, and enough topic-team or caller-provided scope to know authoritative Agent Names or an explicit selected-agent subset.

When topic intent, registration evidence, topic env predecessor evidence, or specialization scope is missing but recoverable, offer targeted fast-forward recovery to `resolve-agent-env-gate`. Use `python scripts/query_step_dependencies.py path --target resolve-agent-env-gate --include-target` for the inclusive default path and `python scripts/query_step_dependencies.py path --target resolve-agent-env-gate --exclude-target` for the exclusive path.

When Agent Names are not authoritative and the caller did not provide an explicit selected-agent subset, ask for the missing scope or route through `adapt-team-template` when team specialization can produce it. Do not invent Agent Names.

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

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

### Essential Output

State whether the Agent environment source intent is ready, revised, blocked, or unchanged. Give the resolved requirements path, authoritative Agent Names or selected subset, source-intent blockers or open questions, and the next operator action.

### Complete Output

Group the complete explanation by source-intent status, semantic label and path, storage profile, source and diagnostics, Agent scope, and next operator action.

## Operational Notes

- The `setup-agent-workspace` operator flow creates or validates the operational target spec before service delegation, while direct service invocation may accept an explicit target spec.
- This subcommand only writes high-level source intent.
- If only that legacy path exists, report a breaking-layout diagnostic and name `topic.intent.agent_env_requirements` plus its resolved default-layout path.

## Guardrails

- DO NOT derive `topic.env.agent_setup_target_spec` here.
- DO NOT write canonical source intent to `<topic-workspace>/user-intent/src/agent-env-gate.md`.
- DO NOT create Agent Workspace worktrees, mutate Topic Main Development Repository configuration, run per-agent commands, mutate Workspace Runtime, launch Houmao, or create live Agent Instances from this subcommand.
