## Context

`isomer-admin-topic-creator` now has a staged setup ladder: topic input, topic registration, topic overview, runtime, topic env gate, topic env setup, actor definitions, actor setup, and research bootstrap. The current terminal shape still includes `start-manual-research`, which makes the skill sound like a research-route handoff tool. The desired boundary is narrower: Topic Creator prepares the Topic Workspace, verifies what it can, records a durable summary, and prints readiness facts without telling the user what research step to run next.

Topic Creator also needs targeted and guided execution styles for the same ladder. `fast-forward` is the automatic happy path. `step-by-step` is the guided happy path: it advances through the same main workflow, but pauses before each step so the user understands the next mutation, can resolve choices, and can acknowledge before work proceeds. `run-to` is targeted automatic execution: it advances through the same ladder as `fast-forward`, then stops before a named procedural step by default.

This change also needs a stable place for the final workspace summary. The default path should be `<topic-workspace>/isomer-topic-workspace-summary.md`, but the skill should resolve it through Workspace Path Resolution so future layouts can move it without rewriting skill logic.

## Goals / Non-Goals

**Goals:**

- Make `finalize` the terminal Topic Creator subcommand.
- Add `step-by-step` as the guided counterpart to `fast-forward`.
- Add `run-to` as a targeted counterpart to `fast-forward`.
- Remove `start-manual-research` from the Topic Creator command surface and fast-forward path.
- Validate that required Topic Workspace preparation stages exist or are intentionally skipped.
- Write `topic.workspace.summary`, defaulting to `<topic-workspace>/isomer-topic-workspace-summary.md`.
- Print a compact final report organized as ready, verified, and blocked.
- Treat actor readiness as conditional: required only when actors are requested or the default `operator` actor was not explicitly opted out.
- Keep Topic Creator from recommending next research actions or v2 skill routes.
- Require `step-by-step` to present each upcoming step, option tables when choices exist, recommended choices, open questions, and an explicit user acknowledgement before proceeding.
- Require `run-to` to accept a procedural subcommand target, run the main workflow up to but not including that target by default, and include the target only when the user explicitly requests inclusive execution.

**Non-Goals:**

- Do not change lower-level Project, environment setup, Topic Actor topology, or v2 research bootstrap ownership.
- Do not launch agents, start manual research sessions, create start packs, or choose a research route.
- Do not make formal Topic Agent Team Profile or Agent Workspace readiness part of Topic Creator finalization.
- Do not replace `isomer-rsch-finalize-v2`, which finalizes research work; this `finalize` only finalizes Topic Workspace preparation.

## Decisions

1. `finalize` is a readiness certifier, not a workflow router.

   The subcommand should inspect the ladder and write a durable summary. It should not recommend "run scout next", "start manual research", or any other route. Alternative considered: keep `start-manual-research` after `finalize`. That keeps a handoff-shaped end state and weakens the workspace-preparation boundary.

2. `fast-forward` ends at `finalize`.

   The happy path should run setup stages, run `bootstrap-research`, then run `finalize`. If a predecessor is blocked, `fast-forward` stops at the blocker as today; if all predecessor stages are ready or intentionally skipped, `finalize` produces the terminal summary.

3. `step-by-step` runs the same ladder as `fast-forward`, but with user acknowledgement before every step.

   The guided path should use the same stage order and readiness checks as `fast-forward`: topic input, project and topic registration, `create-research-intent`, `define-topic-env`, `setup-topic-env`, `define-actors`, `setup-actors`, `bootstrap-research`, and `finalize`. Before each stage, it should explain what it is about to do, what it will read or write, what can block, and whether the step can mutate state. If multiple choices exist, it should show a Markdown table with option IDs such as `A`, `B`, and `C`, the meaning of each choice, pros, cons, open questions, and the recommended choice. It should proceed only after explicit user acknowledgement or option selection. Alternative considered: make `step-by-step` a documentation-only mode. That would not give the user controlled execution through the same workflow.

4. `run-to` is an exclusive targeted fast-forward by default.

   The command should accept a procedural subcommand target from the main workflow and execute the same readiness ladder as `fast-forward` until the predecessor immediately before that target. The target step is excluded by default, so `run-to setup-actors` prepares everything before `setup-actors` and stops without invoking `setup-actors`. If the user explicitly asks for inclusive execution, for example "run through setup-actors", "include setup-actors", or "run-to setup-actors inclusive", then `run-to` includes the target when its prerequisites and required inputs are available. If a predecessor cannot run because required inputs are missing, `run-to` stops at that blocker and reports the missing inputs without skipping ahead. If inclusive execution is requested and the target itself lacks required inputs, `run-to` stops at the target blocker. Helper or misc commands should not be accepted as targets; the user should receive a diagnostic listing valid procedural targets. Alternative considered: include the target by default. Exclusive default better supports using `run-to` as a preparation boundary before a potentially important mutation.

5. The summary is a Topic Workspace semantic surface.

   Add `topic.workspace.summary` with default path `isomer-topic-workspace-summary.md` and storage profile `topic_workspace_summary_file`. Topic Creator should resolve the label before writing. Alternative considered: hard-code the root-level Markdown path in the skill. That would make the path harder to evolve and inconsistent with the existing semantic-label contract.

6. Summary contents should separate readiness classes.

   The file and printed output should include at least these sections: identity, ready, verified, blocked, skipped, installed or materialized, semantic paths, and evidence. `Ready` names usable surfaces, `Verified` names checks with evidence, `Blocked` names failed or missing required signals, and `Skipped` names optional work that was intentionally not required.

7. Actor readiness is optional but explicit.

   If actor setup is requested, or the default `operator` actor has not been opted out, `finalize` requires actor definitions, actor bindings, actor workspace readiness, derived actor env gates, and actor cwd verification evidence. If actors are not requested or the default operator actor was explicitly opted out, `finalize` records actor readiness as skipped with the reason.

8. No-next-routing applies to all terminal output.

   The final chat output and summary file can include blockers and evidence, but not next-action advice. If something is blocked, the system says what is blocked and why; it does not prescribe the next subcommand or research step.

## Risks / Trade-offs

- [Risk] Removing `start-manual-research` may break tests or docs that still expect start-pack handoff. → Mitigation: update the Topic Creator validator and contract tests to require `finalize` and reject stale `start-manual-research` command guidance.
- [Risk] `finalize` can be confused with `isomer-rsch-finalize-v2`. → Mitigation: document that Topic Creator `finalize` finalizes workspace preparation only, while research finalization remains a research-paradigm skill.
- [Risk] Summary output can become too verbose for chat. → Mitigation: write the full summary to `topic.workspace.summary` and print a compact ready/verified/blocked subset.
- [Risk] Actor readiness may be treated as mandatory even when the user opted out. → Mitigation: model actor readiness as required, skipped, or blocked based on requested actor scope and explicit opt-out state.
- [Risk] Stale summaries may mislead users after later setup changes. → Mitigation: `status` and `repair` should treat a summary as stale when predecessor evidence changed after the summary was written.
- [Risk] `step-by-step` may become a second workflow that drifts from `fast-forward`. → Mitigation: define it as the same main workflow and stage order, with only interaction and acknowledgement semantics changed.
- [Risk] `run-to` target names may be confused with helper or misc commands. → Mitigation: validate the target against the procedural main workflow steps and print valid targets when the supplied target is invalid.

## Migration Plan

1. Add Workspace Path Resolution label `topic.workspace.summary`.
2. Add `references/finalize.md`, `references/step-by-step.md`, and `references/run-to.md` to Topic Creator.
3. Remove `start-manual-research` from Topic Creator command tables, validator constants, and tests.
4. Update `fast-forward`, `step-by-step`, `run-to`, `status`, `repair`, `help`, and `bootstrap-research` references to end at `finalize` where the selected execution mode reaches it.
5. Update validator and unit tests for `finalize`, `step-by-step`, `run-to`, summary labels, option-table prompts, user acknowledgement, default target exclusion, explicit inclusive execution, no-next-routing, and stale command rejection.
6. Run operator skill validation, targeted unit tests, full skill validation, and OpenSpec validation.

## Open Questions

None.
