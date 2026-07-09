## ADDED Requirements

### Requirement: Production Skills Teach the Display Contract
Production DeepSci system skills SHALL teach agents to create supported v2 structured research records with canonical `title` and `summary` display fields.

#### Scenario: Shared guidance defines display fields
- **WHEN** an agent reads production DeepSci shared guidance or directly linked record-authoring references
- **THEN** the guidance defines `title` as the concise display name and `summary` as the brief display description
- **AND** it tells agents to include both fields in supported v2 accepted structured payloads

#### Scenario: Idea-stage guidance defines idea display fields
- **WHEN** an agent reads production DeepSci idea-stage, decision-stage, writing-stage, or other idea-producing guidance
- **THEN** the guidance instructs the agent to include `title` and `summary` on each idea-bearing payload entry that can become a canonical Research Idea
- **AND** it treats source labels and candidate ids as aliases rather than display-field replacements

#### Scenario: Skills avoid stale one-liner terminology
- **WHEN** active production DeepSci skill text describes accepted structured record or Research Idea display fields
- **THEN** it uses `summary` instead of `one_liner`
- **AND** any retained `one_liner` reference is clearly marked as legacy migration context

#### Scenario: Skills avoid stale v1 authoring guidance
- **WHEN** active production DeepSci skill text describes accepted structured record writes
- **THEN** it uses the supported v2 display contract
- **AND** any retained v1 reference is clearly marked as legacy validation, repair, or migration context

### Requirement: Skill Validation Checks Display Contract
The research-paradigm validation harness SHALL check active production DeepSci skills for display-contract compliance.

#### Scenario: Validation detects missing title-summary instruction
- **WHEN** validation inspects active production DeepSci skill text and directly linked active references
- **THEN** it reports missing `title` and `summary` guidance for structured record authoring surfaces that produce accepted payloads

#### Scenario: Validation detects stale one-liner instruction
- **WHEN** validation finds active skill guidance that tells agents to create `one_liner` for accepted records or ideas
- **THEN** validation reports the stale instruction with file path and skill name

#### Scenario: Validation detects stale v1 instruction
- **WHEN** validation finds active skill guidance that tells agents to create `structured-record.v1` payloads for accepted new records
- **THEN** validation reports the stale instruction with file path and skill name
