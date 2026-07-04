## 1. Topic Creator Guidance

- [x] 1.1 Update `skillset/operator/isomer-admin-topic-creator/SKILL.md` so bare topic creation routes to `run-to finalize` with the `finalize` target included by default.
- [x] 1.2 Update `skillset/operator/isomer-admin-topic-creator/references/run-to.md` to state that `run-to <target>` includes the named procedural target unless the user explicitly asks to stop before or exclude it.
- [x] 1.3 Update Topic Creator help and operator README guidance so examples distinguish inclusive `run-to`, explicit stop-before wording, `fast-forward`, and `step-by-step`.

## 2. Validation and Tests

- [x] 2.1 Update operator skill validation expectations from target exclusion by default to target inclusion by default with explicit exclusion behavior.
- [x] 2.2 Add or revise unit coverage for bare topic creation defaulting to inclusive `run-to finalize`.
- [x] 2.3 Add or revise unit coverage for explicit exclusion phrases such as `before`, `stop before`, `excluding`, and `up to but not including`.
- [x] 2.4 Preserve test coverage that rejects helper, misc, unknown, and non-main-workflow targets as executable `run-to` targets.

## 3. Consistency Checks

- [x] 3.1 Search active operator skill docs and tests for stale exclusion-by-default wording.
- [x] 3.2 Confirm explicit `fast-forward`, `step-by-step`, `status`, `repair`, and named procedural subcommand routing still overrides the bare topic-creation default.

## 4. Verification

- [x] 4.1 Run `pixi run python -m unittest tests.unit.test_manual_research_topic_skills`.
- [x] 4.2 Run `pixi run validate-skills`.
- [x] 4.3 Run `openspec status --change make-topic-creator-run-to-inclusive`.
