## ADDED Requirements

### Requirement: DeepSci Entrypoint Explains Every Protected Route
The `isomer-ext-deepsci-entrypoint` skill SHALL provide one context-aware `When to Route Here` sentence for every protected DeepSci subskill in its protected-subskill table. Each sentence SHALL assume the DeepSci pack context and identify the research-stage condition or bounded support need that selects the member.

#### Scenario: DeepSci protected inventory is inspected
- **WHEN** `isomer-ext-deepsci-entrypoint/SKILL.md` is inspected
- **THEN** all 21 protected-member rows contain one routing sentence
- **AND** the existing member names, logical ids, and internal designators remain unchanged

#### Scenario: Early research routes overlap
- **WHEN** a task may require framing, comparator establishment, hypothesis development, optimization, or a bounded experiment
- **THEN** the applicable routing sentences distinguish `scout`, `baseline`, `idea`, `optimize`, and `experiment` by readiness and intended output

#### Scenario: Publication routes overlap
- **WHEN** a task may require paper planning, plotting, visual refinement, Nature-specific data or figure work, review, rebuttal, finalization, or prose polishing
- **THEN** the applicable routing sentences distinguish the protected publication members by artifact state and requested transformation

#### Scenario: Shared support is selected
- **WHEN** a DeepSci task needs cross-stage context, output, lineage, evidence, or recording rules rather than a standalone research stage
- **THEN** the `shared` sentence identifies it as internal cross-stage support and does not present it as an independent public workflow
