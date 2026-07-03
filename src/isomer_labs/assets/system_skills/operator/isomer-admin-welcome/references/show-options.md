# Show Options

## Workflow

1. Print the visible usage paths first, before lower-level owner-skill routes.
2. Show `start-research-manually` with owner skill `isomer-admin-topic-creator` and safe first commands `Use $isomer-admin-topic-creator fast-forward` or `Use $isomer-admin-topic-creator step-by-step`.
3. Show `start-research-by-agent-team` with owner skill `isomer-admin-topic-team-specialize` and safe first command `Use $isomer-admin-topic-team-specialize fast-forward`.
4. Show additional supported actions: Project setup or checks, initialized-topic management, Topic Team Specialization, and Houmao interop.
5. Ask the user to choose a visible usage path, describe their goal, or invoke the named owner skill directly.
6. Keep the output action-oriented; do not primarily teach the Isomer system model.

If the user's task does not map cleanly to these steps, use your native planning tool to build a bounded option menu from the active owner skills and guardrails, then print the shortest helpful menu.

## Option Menu Content

| User Goal | Owner Skill | Direct Invocation |
| --- | --- | --- |
| Start research manually with human-orchestrated Topic Actors. | `isomer-admin-topic-creator` | `Use $isomer-admin-topic-creator fast-forward` or `Use $isomer-admin-topic-creator step-by-step`. |
| Start research by formal Agent Team from a Domain Agent Team Template. | `isomer-admin-topic-team-specialize` | `Use $isomer-admin-topic-team-specialize fast-forward`. |
| Initialize or check an Isomer Project, list topics, inspect context, or prepare runtime. | `isomer-admin-project-mgr` | `Use $isomer-admin-project-mgr check-project`, `list-topics`, or the needed Project subcommand. |
| Manage an initialized Research Topic, Topic Actors, package mutation, environment verification, reset checkpoints, or diagnostics. | `isomer-admin-topic-mgr` | `Use $isomer-admin-topic-mgr status` or a scoped initialized-topic subcommand. |
| Understand Houmao loop, runtime, launch profile, mailbox, gateway, or template mapping. | `isomer-admin-houmao-interop` | `Use $isomer-admin-houmao-interop help` or the relevant interop subcommand. |

Do not list `isomer-admin-topic-workspace-mgr`, `isomer-admin-topic-prepare`, or `isomer-admin-manual-research-session` as active invocations.

Do not automatically route to `isomer-misc-tool-packs`; mention it only when the user explicitly asks for installable toolsets.
