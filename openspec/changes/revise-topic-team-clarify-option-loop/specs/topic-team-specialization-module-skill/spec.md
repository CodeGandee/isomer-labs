## ADDED Requirements

### Requirement: Clarification Option Loop
The module skill SHALL make `clarify-topic` and `clarify-topic-team` use a bounded option-asking clarification loop that updates static topic-team artifacts directly instead of creating separate user-decision records.

#### Scenario: Topic clarification scans and asks focused questions
- **WHEN** the `clarify-topic` subcommand runs after its predecessor artifacts exist
- **THEN** it performs a coverage and clarity scan of `<topic-dir>/topic-def/topic-overview.md`, identifies unresolved questions that materially affect topic scope, objectives, assumptions, open questions, or template selection, and asks at most one focused clarification question at a time

#### Scenario: Team clarification scans and asks focused questions
- **WHEN** the `clarify-topic-team` subcommand runs after its predecessor artifacts exist
- **THEN** it performs a coverage and clarity scan of the topic overview, copied template material, `team-specialization-guide.md`, `team-specialization-plan.md`, `Final Report`, placeholder resolutions, deferrals, and draft packet/profile inputs, then asks at most one focused clarification question at a time about role, workflow, policy, binding, copied-material, setup, validation, or blocker ambiguity

#### Scenario: Clarification question format is structured
- **WHEN** either `clarify-topic` or `clarify-topic-team` asks a clarification question
- **THEN** the question includes a motivation, a concrete example when useful, a proposed answer or option with rationale, the downstream implication of accepting it, and either two to five mutually exclusive options with a custom short-answer path or a short-answer prompt with a proposed answer

#### Scenario: Clarification answers update topic material directly
- **WHEN** the user answers a `clarify-topic` question clearly or accepts the proposed answer
- **THEN** the subcommand validates the answer, updates `<topic-dir>/topic-def/topic-overview.md` directly, removes or revises resolved open questions and obsolete assumptions, and reports remaining open questions and readiness for `specialize-team`

#### Scenario: Clarification answers update team material directly
- **WHEN** the user answers a `clarify-topic-team` question clearly or accepts the proposed answer
- **THEN** the subcommand validates the answer, updates the relevant copied topic-team material, specialization plan, `Final Report`, placeholder resolutions, deferrals, or draft packet/profile inputs directly, and reports changed paths, remaining blockers, and readiness for setup or validation

#### Scenario: Clarification loop does not create decision logs
- **WHEN** either `clarify-topic` or `clarify-topic-team` integrates an accepted user answer
- **THEN** it does not create an ADR, decision log, user-decision record, or separate clarification transcript as the durable source of truth for that answer

#### Scenario: Clarification loop stops predictably
- **WHEN** all critical ambiguities are resolved, the user signals completion, or five clarification questions have been asked in the current clarification session
- **THEN** the subcommand stops asking questions and reports remaining open questions, deferrals, blockers, changed artifacts, and the next safe operator action
