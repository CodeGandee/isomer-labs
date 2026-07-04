# Read Env Gate

Use this subcommand to read the user-authored topic environment source intent and extract what must be runnable after setup.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Workspace context | Require `project_root`, `research_topic_id`, `topic_workspace_dir`, `manifest_path_or_dir`, `manifest_path`, and `pixi_environment` from `resolve-topic-workspace`. Refuse to run if any value is missing, and tell the user to run `resolve-topic-workspace` first. |
| Topic env source intent | Resolve `topic.intent.topic_env_requirements` through Workspace Path Resolution. Under `isomer-default.v1`, this defaults to `<topic-workspace-dir>/intent/src/topic-env-gate.md`. If it is missing or unreadable, report a blocker asking the user to create or repair the resolved source intent file. |
| Optional modifiers | None for this step. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require workspace context** from `resolve-topic-workspace`:
   - Require `project_root`, `research_topic_id`, `topic_workspace_dir`, `manifest_path_or_dir`, `manifest_path`, and `pixi_environment`.
2. **Resolve the source intent label** `topic.intent.topic_env_requirements`:
   - Record semantic label, resolved path, storage profile, source, source detail, diagnostics, and blockers.
3. **Read the source intent**. If it is missing or unreadable, stop and report a blocker asking the user to create or repair the resolved source intent file.
4. **Extract setup intent**:
   - Include topic-level source intent, runnable target, desired command or commands, expected outputs, success criteria, repo hints, any full-history Git requirements or shallow-snapshot assumptions, dependency hints, native tool requirements, and any out-of-scope requests.
   - Interpret the runnable target as the commands one agent or operator must be able to run from the selected Topic Workspace, not as proof that a multi-agent team can launch.
5. **Defer repo and dependency choices**. Do not choose repos, dependency sources, Pixi install commands, or verification commands in this subcommand.
6. **Report the source gate summary** using the parent skill's output fields.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the source gate, parent guardrails, and user request, then execute the plan.

## Blockers

Report `blocked` when:

- `topic_workspace_dir` is not resolved.
- The resolved `topic.intent.topic_env_requirements` file is missing.
- The file is unreadable.
- The source gate describes live agent launch, Agent Instance creation, Topic Agent Team Profile materialization, unrelated runtime mutation, GUI operation, or research decision authority as the required setup action.

## Output Notes

The extracted source intent summary should be carried to `ensure-topic-repos` and `derive-env-gate`. Preserve uncertainty instead of pretending a vague source intent is precise. Include repo history needs when stated or implied, `topic_env_source_label`, `topic_env_source_path`, storage profile, source, source detail, diagnostics, and blockers in the output.
