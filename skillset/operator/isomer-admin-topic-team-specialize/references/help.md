# Help

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Print a concise description: `isomer-admin-topic-team-specialize` initializes and specializes one Research Topic into static Topic Team material and durable setup state from one Domain Agent Team Template.
2. Explain that invoking this skill without a prompt defaults to this `help` output.
3. Explain the operational modes: manual mode loads one subcommand, `step-by-step` runs the full topic-team path with user confirmation before each step, and `fast-forward` runs the full topic-team path through `finalize-topic-team` without per-step confirmation.
4. Print the user-facing flow: `init-topic`, optional `clarify-topic`, `ensure-topic-registration`, `specialize-team`, optional `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, then explicit `approve-profile` or `materialize-profile`.
5. Print the available public subcommands as a three-column table with `Subcommand`, `Purpose`, and `Produces` columns. Do not list helper subcommands in help output because they are private implementation API.
6. Name the required inputs and outputs: Research Topic, topic workspace directory, Project Manifest registration evidence, Topic Workspace Pixi binding status, Domain Agent Team Template, `topic-overview.md`, copied template material, `team-specialization-guide.md`, `team-specialization-plan.md`, `Final Report`, `env-gate.md`, `isomer-srv-env-setup` service output, environment setup status, Agent Workspace paths, delegated Git-backed workspace evidence from `isomer-admin-topic-workspace-mgr` when requested, validation status, `isomer-topic-summary.md`, and next operator action.
7. State the key guardrails: provisional topic workspace seeds are not Project Manifest registrations, do not edit Domain Agent Team Template source, do not hide setup or validation, do not bypass approval or materialization checks, and do not run live teams, create Agent Instances, mutate Workspace Runtime, or launch execution adapters from this skill.

If the user's task does not map cleanly to these steps, use your native planning tool to decide which parts of the skill usage information to print, then execute the plan.

## Public Subcommands

| Subcommand | Purpose | Produces |
| --- | --- | --- |
| `init-topic` | Start a new or unclear Research Topic and topic workspace seed. | `<topic-dir>/topic-def/topic-overview.md`, provisional topic workspace status, open questions. |
| `clarify-topic` | Refine topic scope, assumptions, objectives, and open questions. | Updated `topic-overview.md`, remaining open questions, readiness to specialize. |
| `ensure-topic-registration` | Verify or create manifest-backed Research Topic and Topic Workspace registration before registration-dependent work. | `registered_research_topic_ref`, `registered_topic_workspace_ref`, `registration_command_evidence`, `environment_binding_status`, registration blockers. |
| `specialize-team` | Select one Domain Agent Team Template and specialize it for the topic. | Copied template material, `team-specialization-guide.md`, `team-specialization-plan.md`, `Final Report`, draft packet/profile inputs. |
| `clarify-topic-team` | Revise the proposed specialized topic team before setup. | Revised copied material, placeholder resolutions, deferrals, draft profile inputs, revision status. |
| `setup-topic-env` | Prepare the `env-gate.md` handoff and delegate heavy Topic Workspace environment setup to `isomer-srv-env-setup`. | `topic_environment_status`, `env_gate_path`, `derived_gate_path`, service setup commands, changed files, validation refs, setup blockers. |
| `setup-agent-workspace` | Create or report per-agent Agent Workspace directories and boundaries, delegating Git-backed worktree setup to `isomer-admin-topic-workspace-mgr` when requested. | `agent_workspace_paths`, `agent_workspace_ref` evidence, ownership notes, workspace blockers, validation refs. |
| `validate-topic-team` | Check static readiness across topic definition, specialization, environment, and workspaces. | `topic_team_validation_status`, blocker list, deferrals, next safe action. |
| `finalize-topic-team` | Write the final human-readable topic-team handoff summary. | `isomer-topic-summary.md`, validation status, blockers, next actions. |
| `approve-profile` | Record explicit approval or rejection of reviewable profile material. | Approval provenance, approval state, next validation or materialization action. |
| `materialize-profile` | Validate and write the approved Topic Agent Team Profile Bundle. | `<topic-workspace>/team-profile/` profile bundle, validation output, Project Manifest registration guidance. |
| `help` | Print public usage for the skill. | Public subcommand table, flow summary, guardrails. |
| `fast-forward` | Run the full topic-team setup flow automatically where possible. | Topic overview, specialization outputs, setup records, validation status, `isomer-topic-summary.md`. |
| `step-by-step` | Run the full topic-team setup flow with confirmation before each stage. | Per-step progress summaries, confirmed artifacts, blockers, final topic summary when completed. |

## Usage Notes

Use `init-topic` first when the user supplies a concrete Research Topic that is new, missing from the Project Manifest, or needs a topic workspace seed. If the Research Topic is clear and no output directory is supplied, it derives a provisional seed under the effective Topic Workspace base, normally `isomer-content/topic-ws/<topic-slug>/`. If the user does not supply a topic, or only the Project's generic registered `default` topic is available, ask for the actual research topic and do not create files. When it does proceed, it writes `<topic-dir>/topic-def/topic-overview.md` and reports provisional status until `ensure-topic-registration` verifies or creates authoritative refs through supported Isomer CLI/API surfaces.

Use `ensure-topic-registration` after the topic is clear and before registration-dependent work. It verifies Project Manifest-backed Research Topic and Topic Workspace refs, uses `isomer-cli project topics create <topic-id> --statement "<research topic>" --workspace-dir <topic-workspace-dir>` when safe, verifies either an explicit `manifest_path_or_dir` Topic Workspace Pixi binding or the implicit Topic Workspace directory default needed by `isomer-srv-env-setup`, and blocks instead of hand-editing Project Config.

Use `specialize-team` after the topic is clear and registration blockers are resolved. It selects one Domain Agent Team Template, runs the internal specialization path as needed, adapts copied template material, and reports draft Topic Agent Team Profile Bundle inputs.

Use `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, and `finalize-topic-team` after specialization to prepare durable topic-team setup state and write `isomer-topic-summary.md`. `setup-topic-env` prepares or checks `<topic-workspace>/user-intent/src/env-gate.md`, then delegates repo, dependency, Pixi, and verification work to `isomer-srv-env-setup` and records the service output as evidence. If the user wants `<topic-workspace-dir>/repos/topic-main` plus per-agent Git worktrees, `setup-agent-workspace` delegates that setup to `isomer-admin-topic-workspace-mgr` and records its static output as evidence. Live team operation is outside this skill's scope.
