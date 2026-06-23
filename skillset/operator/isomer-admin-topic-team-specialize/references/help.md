# Help

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Print a concise description of `isomer-admin-topic-team-specialize`: it specializes one Domain Agent Team Template into copied, topic-specific material for one Research Topic.
2. Explain that specialization needs enough context to identify the project, the research topic, and the Domain Agent Team Template to adapt.
3. Explain that invoking this skill without a prompt defaults to this `help` output.
4. Explain the operational modes: default help handles empty invocations, manual mode loads one subcommand, `step-by-step` runs the specialization path with user confirmation before each step, and `fast-forward` runs the full specialization path through draft profile output without per-step confirmation.
5. List the available subcommands: `help`, `resolve-project`, `inspect-template`, `resolve-context`, `map-placeholders`, `draft-profile`, `approve-profile`, `materialize-profile`, `launch-team`, `fast-forward`, and `step-by-step`.
6. Name the main outputs: copied template material under `<topic-workspace>/team-profile/`, `team-specialization-guide.md`, `team-specialization-plan.md`, `Final Report`, placeholder resolutions, deferrals, validation status, and packet/profile inputs.
7. State the key guardrails: do not edit Domain Agent Team Template source, do not create a Topic Workspace `teams` directory, do not bypass packet/profile/runtime/adapter validation, and do not launch from copied template material alone.

If the user's task does not map cleanly to these steps, use your native planning tool to decide which parts of the skill usage information to print, then execute the plan.
