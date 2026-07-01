## ADDED Requirements

### Requirement: Writing Artifacts Use Paper-Line Placeholder Bindings
The research-paradigm v2 skillset SHALL map writing-related placeholders to paper-line storage profiles through local `placeholder-bindings.md` pages while preserving placeholders in workflow prose.

#### Scenario: Paper contract binding uses a paper contract view
- **WHEN** a v2 skill binds a placeholder that represents the active paper contract, selected outline, evidence view, paper view, section writing plan, or claim-evidence boundary
- **THEN** the binding maps it to an Isomer record kind and profile that preserves its paper-line role, such as `view_manifest` with `paper.contract.selected-outline`, `artifact` with `paper.outline.*`, or `view_manifest` with `paper.claim-evidence-map`

#### Scenario: Paper control surfaces use view records
- **WHEN** a v2 skill binds a placeholder that represents the paper evidence ledger, experiment matrix, manuscript validation, outline validation, paper-line state, or other paper control surface
- **THEN** the binding uses `topic.records.views` with a paper-specific profile such as `paper.evidence-ledger`, `paper.experiment-matrix`, `paper.validation.*`, or `paper.line-state`

#### Scenario: Paper bodies use artifact records
- **WHEN** a v2 skill binds a placeholder that represents manuscript drafts, LaTeX material, bibliography files, compile reports, PDFs, review reports, rebuttal packets, response letters, final summaries, or paper bundle manifests
- **THEN** the binding uses `topic.records.artifacts` with a paper, review, rebuttal, figure, release, or package profile rather than a generic report or handoff profile when a more precise profile exists

#### Scenario: Paper work queues use task records when resumable
- **WHEN** a v2 skill binds a placeholder that represents a resumable writing plan, reviewer-linked evidence TODO, or paper-facing work queue
- **THEN** the binding uses `research_task` under `topic.records.tasks` when the item must be resumed, assigned, or queried as work, and may use `view_manifest` only when the item is a read-only board

#### Scenario: Binding commands include queryable paper metadata
- **WHEN** a v2 skill binding provides an `isomer-cli ext research records` create or update command for a writing-related placeholder
- **THEN** the command includes explicit `--semantic-label`, `--profile`, `--placeholder`, `--skill`, producer, consumer, and any natural query metadata such as `selected_outline_ref`, `paper_surface`, `package_type`, `section_id`, `claim_id`, or `reviewer_item_id`

#### Scenario: Binding convention avoids paper-specific semantic labels
- **WHEN** writing-related v2 binding pages are updated
- **THEN** they use existing semantic labels such as `topic.records.views`, `topic.records.artifacts`, `topic.records.tasks`, `topic.records.runs`, and `topic.records.logs`
- **AND** they do not introduce paper-specific top-level semantic labels as required storage surfaces

#### Scenario: Workflow placeholders remain stable
- **WHEN** writing-related binding rows are updated
- **THEN** `SKILL.md` workflow prose keeps the existing placeholder tokens and relies on `placeholder-bindings.md` for storage mapping

#### Scenario: Placeholder registries change only for real drift
- **WHEN** implementation inspects `migrate/placeholders.md` for writing-related skills
- **THEN** it changes placeholder definitions only when a placeholder is missing or its kind conflicts with the durable storage role that the binding page must express
