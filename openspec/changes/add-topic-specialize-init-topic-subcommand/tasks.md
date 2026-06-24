## 1. Skill Entrypoint and Subcommand

- [x] 1.1 Add `init-topic`, `clarify-topic`, `specialize-team`, `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, and `finalize-topic-team` to the `isomer-admin-topic-team-specialize` subcommands table with short purposes and local reference links.
- [x] 1.2 Update the main workflow text so the user-facing flow is `init-topic`, optional `clarify-topic`, `specialize-team`, optional `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, then explicit approval, materialization, or launch boundaries.
- [x] 1.3 Group subcommands in the entrypoint and help text as procedural subcommands, helper subcommands, and misc subcommands.
- [x] 1.4 Document procedural subcommands as the public single-step workflow API: `init-topic`, `clarify-topic`, `specialize-team`, `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, `approve-profile`, `materialize-profile`, and `launch-team`.
- [x] 1.5 Document helper subcommands as five lower-level implementation commands: `resolve-project`, `inspect-template`, `resolve-context`, `map-placeholders`, and `draft-profile`.
- [x] 1.6 Document misc subcommands as public supporting commands or shortcuts: `help`, `fast-forward`, and `step-by-step`.
- [x] 1.7 Create `references/init-topic.md` with a near-top numbered `## Workflow`, Imsight-style fallback, input clarification rules, output contract, and guardrails.
- [x] 1.8 Ensure `init-topic` asks for more Research Topic detail before mutation when the topic is absent or unclear.
- [x] 1.9 Ensure `init-topic` asks for the topic workspace directory before mutation when the directory is absent.
- [x] 1.10 Create `references/clarify-topic.md` for optional interactive topic refinement and topic overview updates.
- [x] 1.11 Create `references/specialize-team.md` as the user-facing Domain Agent Team Template selection and specialization command.
- [x] 1.12 Create `references/clarify-topic-team.md` for optional interactive revision of specialized topic-team outputs.
- [x] 1.13 Create `references/setup-topic-env.md` for explicit topic development environment setup.
- [x] 1.14 Create `references/setup-agent-workspace.md` for per-agent workspace creation and boundary notes.
- [x] 1.15 Create `references/validate-topic-team.md` for readiness validation before the team starts work.
- [x] 1.16 Create `references/finalize-topic-team.md` for writing `isomer-topic-summary.md`.

## 2. Topic Seed File Behavior

- [x] 2.1 Specify in `init-topic.md` that the subcommand creates the selected topic directory and `<topic-dir>/topic-def/`.
- [x] 2.2 Specify that `topic-overview.md` is generated from the agent's understanding of the Research Topic.
- [x] 2.3 Require `topic-overview.md` sections for Research Topic, agent understanding, scope, initial objectives, assumptions, open questions, and source prompt or source material.
- [x] 2.4 Require output to label unregistered created material as a provisional topic workspace seed, not an authoritative Research Topic or Topic Workspace registration.
- [x] 2.5 Preserve the Project Config mutation boundary by routing registration through supported Isomer CLI/API surfaces when available and otherwise reporting a blocker.

## 3. Workflow Integration

- [x] 3.1 Update `references/resolve-project.md` to call out `init-topic` when no registered Research Topic matches but the user has supplied enough topic material to seed a topic workspace.
- [x] 3.2 Update `references/fast-forward.md` so automatic specialization follows the same required path as `init-topic` when needed, `specialize-team`, setup, validation, and `finalize-topic-team` through `isomer-topic-summary.md`.
- [x] 3.3 Update `references/step-by-step.md` so guided specialization pauses between `init-topic`, `clarify-topic`, `specialize-team`, `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, and `finalize-topic-team` steps.
- [x] 3.4 Update `references/help.md` to document the user-facing flow, subcommand groups, required inputs, generated topic overview, provisional status, team specialization output, environment setup, agent workspace setup, validation, final summary, and registration boundary.
- [x] 3.5 Update output contracts or guardrails in the skill entrypoint as needed to report `topic_overview_path`, provisional status, `selected_domain_team_template_ref`, topic-team revision status, `topic_environment_status`, `agent_workspace_paths`, `topic_team_validation_status`, `isomer_topic_summary_path`, and next registration or approval action.
- [x] 3.6 Ensure lower-level manual subcommands remain available for `resolve-project`, `inspect-template`, `resolve-context`, `map-placeholders`, and `draft-profile`.

## 4. Setup, Validation, and Final Summary Details

- [x] 4.1 Specify that `setup-topic-env` records environment setup commands, status, blockers, and validation refs without hiding mutating setup work.
- [x] 4.2 Specify that `setup-agent-workspace` creates or reports per-agent workspace directories, ownership/boundary notes, and blockers based on the specialized topic-team shape.
- [x] 4.3 Specify that `validate-topic-team` checks topic overview, specialized team material, environment setup, per-agent workspaces, deferrals, blockers, and readiness to start.
- [x] 4.4 Specify that `finalize-topic-team` writes `isomer-topic-summary.md` with topic team, goal, working logic, environment setup, agent workspace layout, validation status, blockers, and next actions.

## 5. Validation and Documentation

- [x] 5.1 Extend `scripts/validate_skillsets.py` so the topic-team specialization module requires all new user-facing subcommands, their local reference pages, required subcommand groups, required topic-overview, team-specialization, setup, validation, and final-summary terms, no `evals/`, no external support refs, and workflow fallback.
- [x] 5.2 Update `tests/unit/test_validate_skillsets.py` with accepted fixture coverage and negative checks for missing new subcommands, missing subcommand groups, missing fallback, missing topic-overview, setup, validation, final-summary, or team-specialization terms, and forbidden external refs.
- [x] 5.3 Update `skillset/operator/README.md` to explain the user-facing flow from `init-topic` through setup, validation, and `finalize-topic-team`.
- [x] 5.4 Update OpenSpec-facing wording if implementation reveals a narrower topic seed, setup, validation, final-summary, or registration-boundary term.

## 6. Verification

- [x] 6.1 Run skill-creator quick validation for `skillset/operator/isomer-admin-topic-team-specialize`.
- [x] 6.2 Run `pixi run validate-operator-skills`.
- [x] 6.3 Run focused validator unit tests for topic-team specialization skill validation.
- [x] 6.4 Run `openspec validate add-topic-specialize-init-topic-subcommand --strict`.
- [x] 6.5 Run `openspec validate --all`.
