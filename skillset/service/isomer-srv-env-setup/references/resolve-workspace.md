# Resolve Workspace

Use this subcommand to resolve the Project root, Research Topic, Topic Workspace, active Topic Workspace Pixi binding, and setup preconditions.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Project root | Use the provided path or current working directory; confirm `.isomer-labs/manifest.toml` exists. |
| Research Topic or Topic Workspace selector | Read a `research_topic_id`, Topic Workspace ref, or Topic Workspace path from the prompt or Project Manifest context. If several topics remain plausible, ask the user which one to use. |
| Optional modifiers | None for this step. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Resolve the Project root** from the prompt or current working directory. Confirm `.isomer-labs/manifest.toml` exists.
2. **Resolve `research_topic_id`** from the prompt or Project Manifest. If more than one Research Topic remains plausible, ask the user which one to use.
3. **Read the Project Manifest** and locate the Project Manifest-declared Topic Workspace for the selected Research Topic.
4. **Resolve the active `topic_standalone_pixi_bindings` entry** for the selected Research Topic. Record `manifest_path` and `pixi_environment`; use `default` only when the binding omits `pixi_environment`.
5. **Confirm path boundaries**. The Topic Workspace and `manifest_path` must be inside the Project root, and `manifest_path` must refer to the selected Topic Workspace Pixi manifest.
6. **Run read-only project validation when available** before direct setup mutation, such as `pixi run isomer-cli --print-json project validate` and `pixi run isomer-cli --print-json project doctor --topic <research_topic_id>`.
7. **Report workspace context** using the parent skill's output fields and stop with blockers for missing Project Manifest, unknown topic, missing Topic Workspace, missing active binding, or invalid paths.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the parent guardrails, Project Manifest evidence, and user request, then execute the plan.

## Resolved Context

Carry these values to later subcommands:

| Value | Meaning |
| --- | --- |
| `project_root` | The Isomer Project root containing `.isomer-labs/manifest.toml`. |
| `research_topic_id` | The selected Research Topic id. |
| `topic_workspace_dir` | The Project Manifest-declared Topic Workspace directory. |
| `manifest_path` | The active Topic Workspace Pixi manifest path from `topic_standalone_pixi_bindings`. |
| `pixi_environment` | The active Pixi environment, usually `default`. |

## Preconditions

- Do not infer the active binding from directory names.
- Do not treat the Project-root Pixi environment as the Topic Workspace environment.
- Do not proceed to `read-gate`, `ensure-repos`, `derive-gate`, `install-deps`, or `verify-gate` when any resolved context value is missing.
