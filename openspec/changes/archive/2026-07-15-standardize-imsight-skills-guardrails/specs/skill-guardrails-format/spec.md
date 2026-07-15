## ADDED Requirements

### Requirement: Guardrails section format
Every Imsight skill SHALL include a `## Guardrails` section in its `SKILL.md` file.

#### Scenario: New skill created from template
- **WHEN** an agent creates a new Imsight skill using the `create` reference
- **THEN** the generated `SKILL.md` includes a `## Guardrails` section

### Requirement: Guardrails use prohibition and requirement statements
Each bullet in the `## Guardrails` section SHALL be a single concise statement beginning with either `DO NOT` or `MUST`.

#### Scenario: Prohibited action
- **WHEN** a guardrail prevents an action that violates the skill's design intent
- **THEN** the bullet begins with `DO NOT` followed by the prohibited action

#### Scenario: Required action
- **WHEN** a guardrail reinforces a preferred action aligned with the skill's design intent
- **THEN** the bullet begins with `MUST` followed by the required action

### Requirement: Guardrails are sparse and essential
The `## Guardrails` section SHALL contain only rules that materially protect the skill's design intent. Redundant, generic, or non-essential items SHALL be omitted.

#### Scenario: Reviewing guardrail list length
- **WHEN** an editor reviews a skill's `## Guardrails` section
- **THEN** every bullet addresses a concrete risk of acting against the skill's purpose

### Requirement: No Common Mistakes section remains
No Imsight skill SHALL contain a `## Common Mistakes` section after this change.

#### Scenario: Validating skillset compliance
- **WHEN** a validator searches the skillset for `## Common Mistakes`
- **THEN** zero matches are found

### Requirement: Single Guardrails section per skill
Each skill SHALL contain at most one `## Guardrails` section. If a skill previously contained both `## Guardrails` and `## Common Mistakes`, the two sections SHALL be merged into one `## Guardrails` section.

#### Scenario: Merging dual-section skills
- **WHEN** a skill contains both `## Guardrails` and `## Common Mistakes`
- **THEN** all rules are consolidated under a single `## Guardrails` section and duplicates are removed
