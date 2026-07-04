## MODIFIED Requirements

### Requirement: Production DeepSci User Skill Callback Participation
The production `isomer-deepsci-*` skill family SHALL participate in the User Skill Callback mechanism through explicit numbered workflow steps at the beginning and end of each top-level workflow while preserving DeepSci methodology guardrails.

#### Scenario: Top-level workflow includes callback steps
- **WHEN** a production `isomer-deepsci-*` `SKILL.md` is inspected
- **THEN** its `## Workflow` numbered step list includes explicit `begin` and `end` User Skill Callback resolution steps for that skill name
- **AND** callback participation is not represented only as unnumbered reminder prose outside the step list

#### Scenario: Begin callback runs before primary workflow action
- **WHEN** an agent invokes a production `isomer-deepsci-*` top-level workflow
- **THEN** the skill instructs the agent in a numbered workflow step to resolve `begin` callbacks through `isomer-cli project skill-callbacks resolve --skill <skill-name> --stage begin` after mandatory context checks and before the first workflow-specific research action

#### Scenario: End callback runs before final completion
- **WHEN** an agent reaches the end of a production `isomer-deepsci-*` top-level workflow
- **THEN** the skill instructs the agent in a numbered workflow step to resolve `end` callbacks through `isomer-cli project skill-callbacks resolve --skill <skill-name> --stage end` after tentative outputs exist and before final response, handoff, or treating the workflow as complete

#### Scenario: Empty callback resolution does not block workflow
- **WHEN** `isomer-cli project skill-callbacks resolve` returns no active callbacks for a production DeepSci skill and stage
- **THEN** the skill continues through its normal workflow without treating the missing callback as a blocker

#### Scenario: Callback instructions remain subordinate to DeepSci rules
- **WHEN** resolved callback instructions conflict with `isomer-deepsci-shared`, the skill's own guardrails, required placeholder discipline, evidence discipline, validation gates, or the current user request
- **THEN** the skill preserves the owning DeepSci requirements and reports any callback conflict that affects the workflow

#### Scenario: DeepSci validation checks callback workflow steps
- **WHEN** the repository DeepSci skill validation harness inspects production `isomer-deepsci-*` skills
- **THEN** it confirms each participating skill includes the required User Skill Callback resolution guidance for the `begin` and `end` stages as numbered workflow steps
- **AND** it reports callback guidance that appears only as a free-floating reminder under `## Workflow`
