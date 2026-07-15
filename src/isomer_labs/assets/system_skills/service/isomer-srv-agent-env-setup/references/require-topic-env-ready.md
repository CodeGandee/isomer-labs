# Require Topic Env Ready

Use this subcommand to require the Topic Workspace environment predecessor before claiming any Agent Workspace cwd readiness.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Agent env context | Require `project_root`, `research_topic_id`, `topic_workspace_dir`, `topic_workspace_pixi_binding`, `manifest_path`, `pixi_environment`, and semantic topic labels from `resolve-agent-env-context`. |
| Topic env target spec | Resolve `topic.env.topic_setup_target_spec` through Workspace Path Resolution. Under `isomer-default.v1`, this defaults to `<topic-workspace-dir>/intent/derived/isomer-env-gate.md`. |
| Topic Workspace Pixi files | Check the resolved `manifest_path`, `<topic-workspace-dir>/pixi.lock`, and `<topic-workspace-dir>/.pixi/`. |
| Topic env service evidence | When available, consume `isomer-srv-topic-env-setup` output including Topic Main Development Repository and projection evidence; `require-topic-main-ready` checks those details next. |
| Optional modifiers | None for this step. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require resolved context** from `resolve-agent-env-context`:
   - Refuse to run if Project, Research Topic, Topic Workspace, manifest path, Pixi environment, or semantic path evidence is missing.
2. **Check Topic Workspace Pixi predecessor files**:
   - Check resolved Topic Workspace Pixi manifest path, selected Pixi environment, `pixi.lock`, `.pixi/`, and resolved `topic.env.topic_setup_target_spec`.
3. **Read the topic env target spec and service output as predecessor evidence**:
   - Record semantic label, path, storage profile, source, source detail, readiness posture, Topic Main Development Repository summary, projection summary, verification commands, cwd assumptions, execution log, and blockers when present.
4. **Classify readiness** as ready, missing, stale, blocked, failed, or not checked:
   - A Topic Workspace root pass is predecessor evidence only.
   - It is not Agent Workspace cwd readiness.
5. **Report missing or stale topic environment readiness** as a repair next action for `isomer-srv-topic-env-setup` instead of mutating dependencies, topic-main, or projections in this service.
6. **Report topic env predecessor evidence** in service output:
   - Do not create per-agent Pixi manifests, per-agent lockfiles, per-agent `.pixi/` directories, or topic dependency mutations.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step predecessor check from the resolved context, topic env gate, Pixi files, and parent guardrails, then execute the plan.

## Readiness Rules

- `ready`: the resolved manifest path exists, `pixi.lock` exists, `.pixi/` exists, `topic.env.topic_setup_target_spec` exists, and Topic Workspace predecessor evidence is not blocked.
- `blocked`: predecessor artifacts, Pixi files, topic env gate commands, cwd assumptions, or expected results are missing or ambiguous.
- `failed`: predecessor verification ran and failed.
- `missing`: required predecessor files are absent.
- `stale`: predecessor evidence exists but no longer matches the selected Topic Workspace Pixi binding.

## Operational Contract

- Report next action as `isomer-srv-topic-env-setup` when dependency, topic-main, or projection readiness is missing or stale; this is a repair route for predecessor evidence, not downstream readiness ownership by topic env setup.

## Guardrails

- DO NOT install dependencies or repair Pixi state here.
- DO NOT claim per-agent cwd readiness from topic-root verification.
- DO NOT duplicate or reinterpret dependency installation policy as a separate per-agent dependency plan.
