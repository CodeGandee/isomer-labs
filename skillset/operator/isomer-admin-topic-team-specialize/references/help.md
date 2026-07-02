# Help

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Print a concise description:
   - `isomer-admin-topic-team-specialize` initializes and specializes one Research Topic into static Topic Team material and durable setup state from one Domain Agent Team Template.
2. Explain that invoking this skill without a prompt defaults to this `help` output.
3. Explain the operational modes:
   - Manual mode loads one subcommand.
   - `step-by-step` runs the full topic-team path with user confirmation before each step.
   - `fast-forward` runs the full topic-team path through `finalize-topic-team` without per-step confirmation.
   - If a manual subcommand is blocked by missing predecessor artifacts, targeted fast-forward recovery can prepare that subcommand's predecessors; query `scripts/query_step_dependencies.py` against `references/step-dependencies.json` for inclusive and exclusive paths.
   - Direct requests like `specialize <team-path> over topic <topic>` route to `fast-forward`, not to the internal `adapt-team-template` stage.
4. Print the user-facing flow:
   - Start with `init-topic`, `resolve-topic-intent`, optional `clarify-topic`, and `ensure-topic-registration`.
   - Continue through `resolve-topic-env-gate` and `setup-topic-env` to derive `topic.env.topic_setup_target_spec` and materialize the topic env.
   - Run `adapt-team-template`, optional `clarify-topic-team`, and optional repeated `resolve-topic-env-gate` plus `setup-topic-env` when specialization changes runnable requirements.
   - Run `resolve-agent-env-gate` and `setup-agent-workspace` with `isomer-srv-agent-env-setup` delegation to derive `topic.env.agent_setup_target_spec` and verify per-agent cwd readiness.
   - Finish with `validate-topic-team`, `finalize-topic-team`, then explicit `approve-profile` or `materialize-profile` when requested.
5. Print the available public subcommands as a three-column table:
   - Use `Subcommand`, `Purpose`, and `Produces` columns.
   - Do not list helper subcommands in help output because they are private implementation API.
6. Name the required inputs and outputs:
   - Include Research Topic, topic workspace directory, Project Manifest registration evidence, Topic Workspace Pixi binding status, semantic path evidence, Domain Agent Team Template, `topic.intent.overview`, copied template material, `team-specialization-guide.md`, `team-specialization-plan.md`, and `Final Report`.
   - Include `topic.intent.topic_env_requirements`, `topic.env.topic_setup_target_spec`, `isomer-srv-topic-env-setup` service output as Topic Workspace predecessor evidence, Topic Main Development Repository evidence, external repo projection evidence, and environment setup status.
   - Include `topic.intent.agent_env_requirements`, `topic.env.agent_setup_target_spec`, delegated agent environment service output from `isomer-srv-agent-env-setup` for per-agent worktree creation and cwd proof when requested, semantic path evidence for `topic.repos.main` and `agent.workspace`, Agent Workspace paths, validation status, `isomer-topic-summary.md`, and next operator action.
7. State the key guardrails:
   - Provisional topic workspace seeds are not Project Manifest registrations.
   - Do not edit Domain Agent Team Template source, hide setup or validation, or bypass approval or materialization checks.
   - Do not run live teams, create Agent Instances, mutate Workspace Runtime, or launch execution adapters from this skill.
8. Explain the centralized dependency contract:
   - `references/step-dependencies.json` is the local machine-readable source for procedural step dependencies, expected inputs, produced outputs, recovery conditions, and unrecoverable blockers.
   - `scripts/query_step_dependencies.py` answers `path`, `prereqs`, `produces`, `blockers`, `explain`, and `validate` queries without inspecting or mutating a Topic Workspace.

If the user's task does not map cleanly to these steps, use your native planning tool to decide which parts of the skill usage information to print, then execute the plan.

## Public Subcommands

| Subcommand | Purpose | Produces |
| --- | --- | --- |
| `init-topic` | Start a new or unclear Research Topic and topic workspace seed. | Provisional topic workspace status, open questions, next `resolve-topic-intent` action. |
| `resolve-topic-intent` | Resolve the Research Topic into `topic.intent.overview`. | `topic_overview_label`, resolved path metadata, topic overview, assumptions, open questions. |
| `clarify-topic` | Refine topic scope, assumptions, objectives, and open questions. | Updated `topic.intent.overview`, remaining open questions, readiness to register or specialize. |
| `ensure-topic-registration` | Verify or create manifest-backed Research Topic and Topic Workspace registration before registration-dependent work. | `registered_research_topic_ref`, `registered_topic_workspace_ref`, `registration_command_evidence`, `environment_binding_status`, registration blockers. |
| `resolve-topic-env-gate` | Resolve high-level Topic Workspace environment source intent. | `topic.intent.topic_env_requirements`, resolved path metadata, open questions, readiness for `setup-topic-env`. |
| `adapt-team-template` | Internal stage that copies and adapts one Domain Agent Team Template after topic intent, registration, and setup predecessors exist. | Copied template material, `team-specialization-guide.md`, `team-specialization-plan.md`, `Final Report`, draft packet/profile inputs. |
| `clarify-topic-team` | Revise the proposed specialized topic team before setup. | Revised copied material, placeholder resolutions, deferrals, draft profile inputs, revision status. |
| `setup-topic-env` | Create or validate the topic env target spec, then delegate Topic Workspace environment setup to `isomer-srv-topic-env-setup`. | `topic_environment_status`, `topic_env_source_label`, `topic_env_target_spec_label`, resolved path metadata, Topic Workspace predecessor evidence, Topic Main Development Repository evidence, projection evidence, service setup commands, changed files, validation refs, setup blockers. |
| `resolve-agent-env-gate` | Resolve high-level per-Agent Workspace cwd source intent. | `topic.intent.agent_env_requirements`, resolved path metadata, Agent Name scope, open questions, readiness for `setup-agent-workspace`. |
| `setup-agent-workspace` | Create or validate the agent env target spec, then delegate per-agent worktree setup and cwd proof to `isomer-srv-agent-env-setup` after topic-main predecessor evidence exists. | `semantic_paths`, `agent_workspace_paths`, worktree evidence, projection predecessor evidence, `agent_env_source_label`, `agent_env_target_spec_label`, `agent_environment_service_output`, ownership notes, workspace blockers, validation refs. |
| `validate-topic-team` | Check static readiness across topic definition, specialization, environment, and workspaces. | `topic_team_validation_status`, blocker list, deferrals, next safe action. |
| `finalize-topic-team` | Write the final human-readable topic-team handoff summary. | `isomer-topic-summary.md`, validation status, blockers, next actions. |
| `approve-profile` | Record explicit approval or rejection of reviewable profile material. | Approval provenance, approval state, next validation or materialization action. |
| `materialize-profile` | Validate and write the approved Topic Agent Team Profile Bundle. | `<topic-workspace>/team-profile/` profile bundle, validation output, Project Manifest registration guidance. |
| `help` | Print public usage for the skill. | Public subcommand table, flow summary, guardrails. |
| `fast-forward` | Run the full topic-team setup flow automatically where possible. | Topic overview, specialization outputs, setup records, validation status, `isomer-topic-summary.md`. |
| `step-by-step` | Run the full topic-team setup flow with confirmation before each stage. | Per-step progress summaries, confirmed artifacts, blockers, final topic summary when completed. |

## Usage Notes

Use `init-topic` first when the user supplies a concrete Research Topic that is new, missing from the Project Manifest, or needs a topic workspace seed. If the Research Topic is clear and no output directory is supplied, it derives a provisional seed under the effective Topic Workspace base, normally `isomer-content/topic-ws/<topic-slug>/`. If the user does not supply a topic, or only the Project's generic registered `default` topic is available, ask for the actual research topic and do not create files. When it does proceed, route to `resolve-topic-intent` so topic understanding is written through `topic.intent.overview` and reported with semantic label, resolved path, storage profile, source, source detail, and diagnostics.

Use `ensure-topic-registration` after the topic is clear and before registration-dependent work. It verifies Project Manifest-backed Research Topic and Topic Workspace refs, uses `isomer-cli project topics create <topic-id> --statement "<research topic>" --workspace-dir <topic-workspace-dir>` when safe, verifies either an explicit `manifest_path_or_dir` Topic Workspace Pixi binding or the implicit Topic Workspace directory default needed by `isomer-srv-topic-env-setup`, and blocks instead of hand-editing Project Config.

Use `fast-forward` for direct natural-language specialization requests such as `specialize <team-path> over topic <topic>`. Use targeted fast-forward recovery only after a specific subcommand was selected and missing predecessor artifacts block that subcommand. Query `scripts/query_step_dependencies.py path --target <subcommand> --include-target` for the inclusive recovery path, or `--exclude-target` for the exclusive path. Use `adapt-team-template` only after the topic is clear, registration blockers are resolved, and the workflow has reached the internal template-adaptation stage. It selects one Domain Agent Team Template, copies it into the Topic Workspace, adapts copied template material, and reports draft Topic Agent Team Profile Bundle inputs.

Use `isomer-admin-topic-creator` summaries, Topic Workspace registration evidence, and Topic Manager topology evidence as reusable prepared-topic evidence when they exist. They can satisfy common prerequisites such as registered Research Topic refs, Topic Workspace refs, topic overview, Workspace Runtime readiness, topic environment readiness, `topic.repos.main` readiness, current Topic Actor roster, and Topic Actor Workspace refs. Use `resolve-topic-env-gate` after `ensure-topic-registration` whenever the Topic Workspace needs environment setup or the user provides a clear runnable target. Use `setup-topic-env` after `topic.intent.topic_env_requirements` exists or an explicit topic env target spec is supplied. It creates or validates `topic.env.topic_setup_target_spec`, delegates repo, dependency, Pixi, Topic Main Development Repository, projection, and topic-root verification work to `isomer-srv-topic-env-setup`, and records the service output as durable Topic Workspace predecessor evidence. It can run before team specialization, and it can run again after specialization if copied material adds runnable requirements. Use `resolve-agent-env-gate`, `setup-agent-workspace`, `validate-topic-team`, and `finalize-topic-team` after specialization to prepare durable topic-team setup state and write `isomer-topic-summary.md`. `resolve-agent-env-gate` first ensures `topic.intent.agent_env_requirements` exists; then `setup-agent-workspace` creates or validates `topic.env.agent_setup_target_spec` and delegates per-agent worktree creation plus gate-driven cwd proof to `isomer-srv-agent-env-setup` only after Topic Workspace predecessor evidence, Topic Main Development Repository predecessor evidence, required projection predecessor evidence, and authoritative Agent Names exist. Use `isomer-admin-topic-mgr` storage, actor, team, or environment verification commands when the user explicitly asks for Topic Actor topology, actor-scoped diagnostics, topology inspection, branch helper operations, boundary summaries, stale topology repair, or topology diagnostics. Live team operation is outside this skill's scope.
