# Resolve Topic Workspace

Use this subcommand to resolve the Project root, Research Topic, Topic Workspace, active Topic Workspace Pixi binding, and environment setup preconditions. This subcommand resolves Topic Workspace environment context only; it does not require Topic Agent Team Profile material, Agent Team Instance records, roles, or agent count.

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
4. **Resolve setup semantic paths** for the selected Topic Workspace:
   - Required read-only labels are `topic.workspace`, `topic.repos.main`, `topic.repos.main.isomer_managed`, `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, `topic.repos.main.projections.manifest`, `topic.records`, `topic.runtime`, `topic.intent.topic_env_requirements`, and `topic.env.topic_setup_target_spec`.
   - Report each semantic label, resolved path, storage profile, path source, source detail, and any manifest diagnostics.
5. **Resolve the effective Topic Workspace Pixi binding target** for the selected Research Topic:
   - Use an active `topic_standalone_pixi_bindings.manifest_path_or_dir` entry when present.
   - Otherwise use the registered Topic Workspace directory as the implicit default target.
   - Treat explicit targets as manifest files or directories.
   - Record the target, binding source, and `pixi_environment`.
   - Use `default` when the explicit binding omits `pixi_environment` and always use `default` for the implicit default.
6. **Ask Pixi to resolve the target** with `pixi info --json --manifest-path <manifest_path_or_dir>`:
   - Record Pixi's resolved manifest path and selected environment prefix.
   - If Pixi is missing, report a Pixi tooling blocker with online install guidance and offline executable-provisioning guidance instead of treating the topic as unbound.
7. **Confirm path boundaries**:
   - The Topic Workspace, semantic setup paths, and binding target must be inside the Project root.
   - Pixi's resolved manifest path and selected environment prefix must be confined to the selected Topic Workspace, with the prefix under `<topic-workspace>/.pixi/`.
8. **Run read-only project validation when available** before direct setup mutation:
   - Example commands are `isomer-cli --print-json project validate` and `isomer-cli --print-json doctor --with-topic <research_topic_id>`.
   - Treat diagnostics about missing `team-profile/`, Topic Agent Team Profile material, Topic Team Instantiation Packets, Agent Team Instances, Agent Workspaces, roles, role counts, or launch readiness as non-blocking for this subcommand.
   - Diagnostics about launch-facing material are non-blocking for this subcommand unless they also prevent Topic Workspace discovery, semantic path resolution, Pixi binding resolution, source gate reading, dependency setup, repo checks, or Pixi-scoped verification.
9. **Report workspace context** using the parent skill's natural-language output contract:
   - Stop with blockers for missing Project Manifest, unknown topic, missing Topic Workspace, semantic path blocker, Pixi tooling failure, unresolvable target, or invalid paths.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the parent guardrails, Project Manifest evidence, and user request, then execute the plan.

## Resolved Context

Carry these values to later subcommands:

| Value | Meaning |
| --- | --- |
| `project_root` | The Isomer Project root containing `.isomer-labs/manifest.toml`. |
| `research_topic_id` | The selected Research Topic id. |
| `topic_workspace_dir` | The Project Manifest-declared Topic Workspace directory. |
| `semantic_paths` | Resolved setup labels, paths, sources, and diagnostics. |
| `manifest_path_or_dir` | The explicit `topic_standalone_pixi_bindings.manifest_path_or_dir` target, or the registered Topic Workspace directory when using the implicit default. |
| `binding_source` | `explicit` or `implicit-default`. |
| `manifest_path` | Pixi's resolved Topic Workspace Pixi manifest path. |
| `pixi_environment` | The active Pixi environment, usually `default`. |

## Preconditions

- Do not infer the active binding from directory names or Research Topic ids.
- Do not block solely because the Project Manifest lacks an explicit `topic_standalone_pixi_bindings` entry when Pixi resolves the registered Topic Workspace directory as a confined Pixi workspace.
- Do not block solely because `<topic-workspace>/team-profile/`, Topic Agent Team Profile material, Topic Team Instantiation Packets, Agent Team Instance records, Agent Workspace plans, roles, or agent count are absent.
- Do not treat the Project-root Pixi environment as the Topic Workspace environment.
- Do not proceed to `read-env-gate`, `derive-env-gate`, `ensure-topic-main-repository`, `ensure-topic-repos`, `project-extern-repos`, `install-topic-deps`, or `verify-env-gate` when any resolved context value is missing.

## Examples

Explicit file target:

```toml
[[topic_standalone_pixi_bindings]]
research_topic_id = "alpha"
manifest_path_or_dir = "isomer-content/topic-ws/alpha/pixi.toml"
pixi_environment = "default"
```

Explicit directory target:

```toml
[[topic_standalone_pixi_bindings]]
research_topic_id = "alpha"
manifest_path_or_dir = "isomer-content/topic-ws/alpha"
pixi_environment = "default"
```

Implicit default target:

```text
registered Topic Workspace: isomer-content/topic-ws/alpha
no active topic_standalone_pixi_bindings entry
effective manifest_path_or_dir: isomer-content/topic-ws/alpha
pixi_environment: default
binding_source: implicit-default
```
