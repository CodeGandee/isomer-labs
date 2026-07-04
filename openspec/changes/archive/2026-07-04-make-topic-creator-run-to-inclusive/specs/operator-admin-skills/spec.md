## MODIFIED Requirements

### Requirement: Operator Skill Validation
The repository SHALL validate operator/admin skill structure, command surfaces, and naming separately from research-paradigm skill validation.

#### Scenario: Operator validation checks structure
- **WHEN** the operator skill validation runs
- **THEN** it confirms each `skillset/operator/isomer-admin-*` folder has a valid `SKILL.md`, valid frontmatter, expected manifest metadata, and directly linked local references when present

#### Scenario: Operator validation checks old active names
- **WHEN** the operator skill validation scans active docs, team profiles, fixtures, and skill manifests
- **THEN** it fails if a migrated operator skill is still referenced by its old active `isomer-rsch-*` name outside historical provenance or archived change text

#### Scenario: Repository skill validation covers operator skills
- **WHEN** a developer or agent runs the repository skill validation command
- **THEN** validation covers the research, operator, and service skillsets or clearly prints the separate commands required to validate each skillset

#### Scenario: Operator validation checks Topic Creator finalization surface
- **WHEN** operator skill validation scans `skillset/operator/isomer-admin-topic-creator`
- **THEN** it requires local `references/finalize.md`, `references/step-by-step.md`, and `references/run-to.md` subcommand pages, user-facing command guidance for `finalize`, `step-by-step`, and `run-to`, and references to `topic.workspace.summary`
- **AND** it rejects active Topic Creator command guidance that lists `start-manual-research` as a subcommand
- **AND** it rejects terminal Topic Creator guidance that includes next-step routing, manual research start-pack handoff, or production DeepSci research skill recommendations

#### Scenario: Operator validation checks Topic Creator guided execution
- **WHEN** operator skill validation scans Topic Creator `step-by-step` guidance
- **THEN** it requires wording that the subcommand follows the same main workflow order as `fast-forward`
- **AND** it requires per-step preview, option table, recommended choice, open question, and user acknowledgement guidance
- **AND** it fails if `step-by-step` can mutate a workflow step before user acknowledgement

#### Scenario: Operator validation checks Topic Creator run-to execution
- **WHEN** operator skill validation scans Topic Creator `run-to` guidance
- **THEN** it requires wording that the subcommand accepts a procedural subcommand target and follows the same readiness ladder as `fast-forward`
- **AND** it requires target inclusion by default, explicit exclusion behavior, invalid-target diagnostics, and missing-input blocker behavior
- **AND** it requires explicit exclusion wording such as "before", "stop before", "excluding", or "up to but not including" before `run-to` stops short of the named target
- **AND** it fails if `run-to` accepts helper, misc, unknown, or non-main-workflow targets as executable targets

#### Scenario: Topic Creator bare creation defaults to inclusive finalize
- **WHEN** Topic Creator dispatch handles a topic creation, preparation, or start request without explicit `fully automatic`, `fast-forward`, `manually`, `step-by-step`, stop-before, status, repair, or named procedural-target wording
- **THEN** it routes the request to `run-to finalize`
- **AND** it treats `finalize` as included by default, subject to the same required inputs, mutation approval, semantic path, and predecessor-readiness blockers as other `run-to` targets

#### Scenario: Topic Creator explicit exclusion stops before target
- **WHEN** Topic Creator dispatch handles a `run-to` request with wording such as "before <target>", "stop before <target>", "excluding <target>", or "up to but not including <target>"
- **THEN** it treats the named target as excluded
- **AND** it stops after the target's predecessors complete or reports the first blocker before reaching that stop point

#### Scenario: Topic Creator explicit modes remain distinct
- **WHEN** Topic Creator dispatch handles explicit `fast-forward`, `step-by-step`, `status`, `repair`, or named procedural subcommand wording
- **THEN** it routes to that explicit mode rather than the bare topic-creation default
