# Show Options

## Workflow

1. Print the visible usage paths first, before lower-level owner-skill routes.
2. Show `start-research-manually` with owner skill `isomer-op-topic-creator` and safe first commands `Use $isomer-op-topic-creator fast-forward` or `Use $isomer-op-topic-creator step-by-step`.
3. Show `start-research-by-agent-team` with owner skill `isomer-op-topic-team-specialize` and safe first command `Use $isomer-op-topic-team-specialize fast-forward`.
4. Show additional supported actions: Project setup or checks, Project Web GUI lifecycle and backend API guidance, switched Topic Actor or Agent workspace cwd work, project-local Toolbox management, initialized-topic management, and Topic Team Specialization. Do not present service skills as direct first-click owner routes.
5. Ask the user to choose a visible usage path, describe their goal, or invoke the named owner skill directly.
6. Keep the output action-oriented; do not primarily teach the Isomer system model.

If the user's task does not map cleanly to these steps, use your native planning tool to build a bounded option menu from the active owner skills and guardrails, then print the shortest helpful menu.

## Option Menu Content

| User Goal | Owner Skill | Direct Invocation |
| --- | --- | --- |
| Start research manually with human-orchestrated Topic Actors. | `isomer-op-topic-creator` | `Use $isomer-op-topic-creator fast-forward` or `Use $isomer-op-topic-creator step-by-step`. |
| Start research by formal Agent Team from a Domain Agent Team Template. | `isomer-op-topic-team-specialize` | `Use $isomer-op-topic-team-specialize fast-forward`. |
| Initialize or check an Isomer Project, list topics, inspect context, or prepare runtime. | `isomer-op-project-mgr` | `Use $isomer-op-project-mgr check-project`, `list-topics`, or the needed Project subcommand. |
| Start, inspect, refresh, debug, or troubleshoot the Project Web GUI, or look up GUI Backend API routes. | `isomer-op-gui-mgr` | `Use $isomer-op-gui-mgr help`, `launch`, `status`, `api-reference`, `refresh-records`, or `troubleshoot`. |
| Act from a selected Topic Actor or Agent workspace cwd for takeover or one-time prompt execution. | `isomer-op-switch-identity` | `Use $isomer-op-switch-identity switch` or `Use $isomer-op-switch-identity act-as`. |
| Manage an initialized Research Topic, Topic Actors, package mutation, environment verification, reset checkpoints, or diagnostics. | `isomer-op-topic-mgr` | `Use $isomer-op-topic-mgr status` or a scoped initialized-topic subcommand. |
| Create, convert, install, inspect, update, disable, uninstall, or explain project-local Toolboxes, callback insertion points, callback declarations, or Toolbox Runtime Params. | `isomer-op-toolbox-mgr` | `Use $isomer-op-toolbox-mgr help` or a specific Toolbox subcommand. |
| Need Houmao adapter support during Project or Topic Team work. | Owning operator workflow | Use `isomer-op-project-mgr` for Project bootstrap or checks, or `isomer-op-topic-team-specialize` for Topic Team Specialization and launch-facing work. |

Do not list `isomer-op-topic-workspace-mgr`, `isomer-op-topic-prepare`, or `isomer-op-manual-research-session` as active invocations.

Do not list `isomer-srv-houmao-interop` as a direct first-click owner route; it is bounded service support delegated by the owning operator workflow.

Do not automatically route to `isomer-misc-tool-packs`; mention it only when the user explicitly asks for installable toolsets.

Do not mutate Toolbox source, callback registries, or Runtime Params from this welcome surface; recommend `isomer-op-toolbox-mgr` as the owner workflow.
