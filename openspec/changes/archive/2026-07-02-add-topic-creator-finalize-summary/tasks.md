## 1. Path Resolution Support

- [x] 1.1 Add built-in semantic label `topic.workspace.summary` with default path `<topic-workspace>/isomer-topic-workspace-summary.md`.
- [x] 1.2 Add storage profile `topic_workspace_summary_file` as a durable topic-scoped file profile with parent-directory materialization semantics.
- [x] 1.3 Update path catalog, listing, get, explain, and materialization behavior so `topic.workspace.summary` reports label, source, resolved path, storage profile, traits, and diagnostics.
- [x] 1.4 Add or update unit tests for catalog listing, default resolution, configured overrides, materialization parent handling, and unresolved-label diagnostics.

## 2. Topic Creator Skill Surface

- [x] 2.1 Add `skillset/operator/isomer-admin-topic-creator/references/finalize.md` describing validation inputs, summary write behavior, blocked-state handling, compact terminal report, and no-next-routing boundary.
- [x] 2.2 Add `skillset/operator/isomer-admin-topic-creator/references/step-by-step.md` describing guided execution, per-step previews, option tables, recommended choices, open questions, and acknowledgement before proceeding.
- [x] 2.3 Add `skillset/operator/isomer-admin-topic-creator/references/run-to.md` describing targeted fast-forward execution, valid procedural targets, target exclusion by default, explicit inclusive execution, and blocker handling.
- [x] 2.4 Update `SKILL.md`, `references/help.md`, and command tables so user-facing commands include `finalize`, `step-by-step`, and `run-to`, remove `start-manual-research`, and invoke help for empty prompts.
- [x] 2.5 Update `references/fast-forward.md` so the happy path runs setup through research bootstrap and then runs `finalize` as the terminal step.
- [x] 2.6 Update `references/status.md` and `references/repair.md` so they recognize `topic.workspace.summary`, detect stale summaries, and report readiness without naming a next research command.
- [x] 2.7 Update `references/bootstrap-research.md` and any terminal-output guidance so they hand control to `finalize` rather than to manual research start-pack routing.

## 3. Step-by-Step Guided Execution

- [x] 3.1 Define `step-by-step` as the same main workflow order as `fast-forward`: topic input resolution, Project and Topic Workspace readiness, `create-research-intent`, `define-topic-env`, `setup-topic-env`, `define-actors`, `setup-actors`, `bootstrap-research`, and `finalize`.
- [x] 3.2 For every step in `step-by-step`, require a pre-step preview that names the step, planned action, inputs read, artifacts or semantic labels written, mutation status, and possible blockers.
- [x] 3.3 Add option-table guidance for steps with choices, using option IDs such as `A`, `B`, and `C`, plus columns for what the option is, pros, cons, open questions, recommendation status, and recommendation rationale.
- [x] 3.4 Require explicit user acknowledgement or option selection before each step mutates state, including no-choice steps.
- [x] 3.5 Define pause and direction-change behavior so `step-by-step` stops or updates the plan when the user declines acknowledgement or chooses a different path.

## 4. Finalize Readiness Logic

- [x] 4.1 Define the required readiness signals for `finalize`: Project readiness, Research Topic registration, Topic Workspace registration, Workspace Runtime, `topic.intent.overview`, topic env evidence, `topic.repos.main`, research bootstrap outputs, and placeholder-binding entrypoints.
- [x] 4.2 Define conditional actor readiness: require actor definitions, bindings, actor workspaces, derived actor env gates, and actor cwd verification when actors are requested or the default `operator` actor is not opted out; record skipped actor readiness when explicitly out of scope.
- [x] 4.3 Specify the summary structure with identity, overall status, ready, verified, blocked, skipped, installed or materialized surfaces, semantic paths, evidence, and durable-versus-editable distinctions.
- [x] 4.4 Ensure blocked finalization writes a summary when the Topic Workspace and summary path are resolvable, and reports resolver diagnostics without guessing a path when they are not.
- [x] 4.5 Remove start-pack creation and next-step routing from Topic Creator final terminal behavior.

## 5. Run-to Targeted Execution

- [x] 5.1 Define the procedural target set accepted by `run-to` from the main workflow ladder and reject helper, misc, unknown, or non-main-workflow targets.
- [x] 5.2 Make `run-to <procedural-subcommand>` reuse the same readiness ladder as `fast-forward` and exclude the target step by default.
- [x] 5.3 Add explicit inclusive parsing for wording such as `through <target>`, `include <target>`, or `<target> inclusive`, and run the target only under that explicit inclusive request.
- [x] 5.4 Make default `run-to` stop at missing input, missing selected context, unresolved semantic path, or blocked predecessor conditions without skipping ahead to the target.
- [x] 5.5 Make inclusive `run-to` stop at target missing-input blockers when the included target cannot run safely.
- [x] 5.6 Ensure inclusive `run-to finalize` writes `topic.workspace.summary`, while default `run-to finalize` stops before `finalize` and does not write or refresh the summary.

## 6. Validation and Tests

- [x] 6.1 Update operator skill validation to require `references/finalize.md`, `references/step-by-step.md`, `references/run-to.md`, `finalize` command guidance, `step-by-step` command guidance, `run-to` command guidance, `topic.workspace.summary`, and no active `start-manual-research` command guidance in Topic Creator.
- [x] 6.2 Update existing Topic Creator, manual research workflow, and skillset validation tests that still expect `plan`, `create`, `start-manual-research`, start packs, or next-action terminal output.
- [x] 6.3 Add regression tests that fail when Topic Creator terminal output recommends a next v2 research skill, Houmao launch, formal team specialization, or manual research start command.
- [x] 6.4 Add regression tests that fail when `step-by-step` guidance omits the main workflow order, per-step preview, option tables, recommended choices, open questions, or user acknowledgement before mutation.
- [x] 6.5 Add regression tests that fail when `run-to` accepts invalid targets, includes the target by default, fails to include the target under explicit inclusive wording, or skips missing-input blockers.
- [x] 6.6 Update documentation or reference indexes that list Topic Creator subcommands or manual-research operation summaries.

## 7. Verification

- [x] 7.1 Run `pixi run validate-operator-skills`.
- [x] 7.2 Run `pixi run python -m unittest tests.unit.test_validate_skillsets`.
- [x] 7.3 Run targeted path-resolution tests that cover semantic labels and storage profiles.
- [x] 7.4 Run targeted Topic Creator or manual-research workflow tests.
- [x] 7.5 Run `pixi run validate-skills`.
- [x] 7.6 Run `openspec validate add-topic-creator-finalize-summary --strict`.
