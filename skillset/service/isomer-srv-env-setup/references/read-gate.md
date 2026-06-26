# Read Gate

Use this subcommand to read the user-authored source gate and extract what must be runnable after setup.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Workspace context | Require `project_root`, `research_topic_id`, `topic_workspace_dir`, `manifest_path`, and `pixi_environment` from `resolve-workspace`. Refuse to run if any value is missing, and tell the user to run `resolve-workspace` first. |
| `env_gate_path` | Use `<topic-workspace-dir>/user-intent/src/env-gate.md`. If it is missing or unreadable, report a blocker asking the user to create or repair that file. |
| Optional modifiers | None for this step. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require workspace context** from `resolve-workspace`: `project_root`, `research_topic_id`, `topic_workspace_dir`, `manifest_path`, and `pixi_environment`.
2. **Resolve the source gate path** as `<topic-workspace-dir>/user-intent/src/env-gate.md`.
3. **Read the source gate**. If it is missing or unreadable, stop and report a blocker asking the user to create or repair that file.
4. **Extract setup intent**: source intent, runnable target, desired command or commands, expected outputs, success criteria, repo hints, dependency hints, native tool requirements, and any out-of-scope requests.
5. **Defer repo and dependency choices**. Do not choose repos, dependency sources, Pixi install commands, or verification commands in this subcommand.
6. **Report the source gate summary** using the parent skill's output fields.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the source gate, parent guardrails, and user request, then execute the plan.

## Blockers

Report `blocked` when:

- `topic_workspace_dir` is not resolved.
- `<topic-workspace-dir>/user-intent/src/env-gate.md` is missing.
- The file is unreadable.
- The source gate describes live agent launch, Agent Instance creation, unrelated runtime mutation, GUI operation, or research decision authority as the required setup action.

## Output Notes

The extracted source gate summary should be carried to `ensure-repos` and `derive-gate`. Preserve uncertainty instead of pretending a vague source gate is precise.
