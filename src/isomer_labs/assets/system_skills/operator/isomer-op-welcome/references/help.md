# Isomer Admin Welcome Help

## Workflow

1. Print a concise description of `isomer-op-welcome` as the action-oriented menu and path chooser for Isomer Labs operator workflows.
2. List the visible usage paths `start-research-manually` and `start-research-by-agent-team`.
3. List the routing and support subcommands `help`, `show-options`, `choose-path`, `show-skill-map`, and `next-step`.
4. Name the active owner skills: `isomer-op-project-mgr`, `isomer-op-switch-identity`, `isomer-op-topic-creator`, `isomer-op-topic-mgr`, and `isomer-op-topic-team-specialize`.
5. State that the welcome skill is read-only by default and does not initialize Projects, create Research Topics, mutate Topic Workspaces, install packages, specialize teams, launch agents, or bootstrap research-paradigm v2 artifacts.
6. Invite the user to choose a visible usage path, describe their goal, or invoke the named owner skill directly. State that Houmao-specific support is routed by the owning operator workflow to `isomer-srv-houmao-interop` when needed.

If the user's task does not map cleanly to these steps, use your native planning tool to build a bounded welcome response from the visible usage paths, active owner skills, output contract, and guardrails, then recommend one safe owner workflow or ask for the missing decision.

## Visible Usage Paths

| Subcommand | Purpose | Owner Skill |
| --- | --- | --- |
| `start-research-manually` | Prepare a Research Topic for human-orchestrated research with Topic Actors. | `isomer-op-topic-creator` |
| `start-research-by-agent-team` | Specialize a Domain Agent Team Template over a Research Topic. | `isomer-op-topic-team-specialize` |

## Routing and Support Subcommands

| Subcommand | Purpose | Produces |
| --- | --- | --- |
| `help` | Print usage, owner routes, outputs, and guardrails. | Help output. |
| `show-options` | Print the default action menu and visible usage paths. | Option menu with owner skills. |
| `choose-path` | Interpret an ambiguous goal and recommend a visible usage path. | `status`, `interpreted_goal`, `recommended_workflow`, `owner_skill`, `safe_first_command`, `blockers`, `next_action`. |
| `show-skill-map` | Show direct invocation guidance. | Compact intent-to-owner table. |
| `next-step` | Inspect Project context with read-only commands when requested. | Recommended owner workflow plus blockers. |

## Output Contract

Default to **Essential Output** in chat. Print **Complete Output** only when the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output.

### Essential Output

- `status`
- `interpreted_goal`
- `recommended_workflow`
- `owner_skill`
- `safe_first_command`
- `blockers`
- `next_action`

### Complete Output

- `context_evidence`
- `read_only_commands_run`
- `alternate_owner_workflows`
- `routing_rationale`
- `retired_route_exclusions`
