## Why

`isomer-admin-topic-team-specialize` has local implementation subcommands, but it does not yet present the topic-team setup path in the order users naturally experience it: define the topic, clarify it, specialize a domain-level team, clarify the specialized team, prepare the environment and agent workspaces, validate readiness, then finalize a team summary. Operators need a user-facing flow that starts with topic initialization and ends with a readable topic-team summary before launch-facing work proceeds.

## What Changes

- Add an `init-topic` local subcommand to `skillset/operator/isomer-admin-topic-team-specialize`.
- Add a `clarify-topic` local subcommand for optional interactive refinement of the topic overview and open questions.
- Add a user-facing `specialize-team` local subcommand that lets the user select a Domain Agent Team Template and asks the Operator Agent to specialize it for the topic.
- Add a `clarify-topic-team` local subcommand for optional interactive revision of the specialized topic team.
- Add `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, and `finalize-topic-team` local subcommands after `clarify-topic-team`.
- Group local subcommands into procedural subcommands, helper subcommands, and misc subcommands so the skill presents a clean public API while still exposing fine-grained implementation steps.
- Route unclear or missing Research Topic input through `clarify-topic` before creating or using topic material.
- Ask the user for the topic workspace directory when it is not supplied.
- Create the selected topic directory and `<topic-dir>/topic-def/topic-overview.md` from the agent's understanding of the Research Topic.
- Guide topic-specific development environment setup and per-agent workspace creation without hiding validation or runtime boundaries.
- Validate that topic definition, specialized team material, environment setup, and agent workspaces are ready enough for the team to start.
- Create `isomer-topic-summary.md` summarizing the topic team, goals, working logic, environment setup, workspace layout, blockers, and next actions.
- Mark `init-topic` output as a provisional topic workspace seed unless or until a supported Project Manifest registration path exists.
- Update `resolve-project`, `fast-forward`, `step-by-step`, help text, validators, and operator docs so they present the user-facing flow as `init-topic` -> optional `clarify-topic` -> `specialize-team` -> optional `clarify-topic-team` -> `setup-topic-env` -> `setup-agent-workspace` -> `validate-topic-team` -> `finalize-topic-team`.

## Capabilities

### New Capabilities

### Modified Capabilities

- `topic-team-specialization-module-skill`: Add `init-topic`, `clarify-topic`, `specialize-team`, `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, `approve-profile`, `materialize-profile`, and `launch-team` as procedural user-facing Topic Team Specialization steps, classify exactly five helper subcommands as lower-level implementation steps, classify `help`, `fast-forward`, and `step-by-step` as public misc subcommands, and include provisional topic workspace seed behavior, setup readiness, and final topic-team summary output.

## Impact

- Affected skill files: `skillset/operator/isomer-admin-topic-team-specialize/SKILL.md`, `references/init-topic.md`, `references/clarify-topic.md`, `references/specialize-team.md`, `references/clarify-topic-team.md`, `references/setup-topic-env.md`, `references/setup-agent-workspace.md`, `references/validate-topic-team.md`, `references/finalize-topic-team.md`, `references/resolve-project.md`, `references/help.md`, `references/fast-forward.md`, and `references/step-by-step.md`.
- Affected validation: `scripts/validate_skillsets.py` and `tests/unit/test_validate_skillsets.py` should require the new local subcommands and their workflow structure.
- Affected docs/specs: `skillset/operator/README.md` and the `topic-team-specialization-module-skill` OpenSpec capability should describe provisional topic initialization and its registration boundary.
- No CLI command or Project Manifest mutation is required in this change unless a future accepted change adds a supported topic registration command.
