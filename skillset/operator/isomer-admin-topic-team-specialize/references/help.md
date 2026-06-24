# Help

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Print a concise description: `isomer-admin-topic-team-specialize` initializes and specializes one Research Topic into a topic-ready team from one Domain Agent Team Template.
2. Explain that invoking this skill without a prompt defaults to this `help` output.
3. Explain the operational modes: manual mode loads one subcommand, `step-by-step` runs the full topic-team path with user confirmation before each step, and `fast-forward` runs the full topic-team path through `finalize-topic-team` without per-step confirmation.
4. Print the user-facing flow: `init-topic`, optional `clarify-topic`, `specialize-team`, optional `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, then explicit `approve-profile`, `materialize-profile`, or `launch-team`.
5. List subcommands in three groups: procedural subcommands, helper subcommands, and misc subcommands.
6. Name the required inputs and outputs: Research Topic, topic workspace directory, Domain Agent Team Template, `topic-overview.md`, copied template material, `team-specialization-guide.md`, `team-specialization-plan.md`, `Final Report`, environment setup status, Agent Workspace paths, validation status, `isomer-topic-summary.md`, and next operator action.
7. State the key guardrails: provisional topic workspace seeds are not Project Manifest registrations, do not edit Domain Agent Team Template source, do not hide setup or validation, do not bypass approval/materialization/runtime/adapter validation, and do not launch from copied template material alone.

If the user's task does not map cleanly to these steps, use your native planning tool to decide which parts of the skill usage information to print, then execute the plan.

## Subcommand Groups

Procedural subcommands are the public single-step workflow API:

- `init-topic`
- `clarify-topic`
- `specialize-team`
- `clarify-topic-team`
- `setup-topic-env`
- `setup-agent-workspace`
- `validate-topic-team`
- `finalize-topic-team`
- `approve-profile`
- `materialize-profile`
- `launch-team`

Helper subcommands are five lower-level implementation commands:

- `resolve-project`
- `inspect-template`
- `resolve-context`
- `map-placeholders`
- `draft-profile`

Misc subcommands are public support commands and shortcuts:

- `help`
- `fast-forward`
- `step-by-step`

## Usage Notes

Use `init-topic` first when the Research Topic is new, missing from the Project Manifest, or needs a topic workspace seed. It writes `<topic-dir>/topic-def/topic-overview.md` and reports provisional status until registration is handled by supported Isomer CLI/API surfaces.

Use `specialize-team` after the topic is clear. It selects one Domain Agent Team Template, runs the five helper subcommands as needed, adapts copied template material, and reports draft Topic Agent Team Profile Bundle inputs.

Use `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, and `finalize-topic-team` after specialization to prepare the topic for team work and write `isomer-topic-summary.md`.
