## Purpose

Define the required Guardrails structure and wording for active packaged Isomer system skills and behavioral subpages.

## Requirements

### Requirement: Guardrails section format
Every active packaged Isomer system skill SHALL include exactly one `## Guardrails` section in its `SKILL.md` file.

#### Scenario: Packaged skill is created or migrated
- **WHEN** an agent creates or migrates an active packaged Isomer system skill using the current template
- **THEN** the resulting `SKILL.md` includes exactly one `## Guardrails` section

### Requirement: Guardrails use prohibition and requirement statements
Each bullet in the `## Guardrails` section SHALL be a single concise statement beginning with `DO NOT` and SHALL prevent one action that violates the skill's design intent. Positive actions, required operations, ordering, recipes, routing instructions, evidence requirements, and output requirements SHALL appear in Workflow, Core Pattern, Procedure, Contract, or another substantive section instead of Guardrails.

#### Scenario: Prohibited action
- **WHEN** a guardrail prevents an action that violates the skill's design intent
- **THEN** the bullet begins with `DO NOT` followed by the prohibited action

#### Scenario: Required action
- **WHEN** a guardrail reinforces a preferred action aligned with the skill's design intent
- **THEN** the bullet begins with `MUST` followed by the required action

#### Scenario: Positive operational guidance
- **WHEN** an active skill page requires an action, ordering rule, recipe, route, evidence item, or output item
- **THEN** that guidance appears in a substantive section outside `## Guardrails`

### Requirement: Guardrails are sparse and essential
The `## Guardrails` section SHALL contain only concise prohibitions that materially protect the skill's design intent. Redundant, generic, positive, procedural, or non-essential items SHALL be omitted or relocated to the authoritative substantive section.

#### Scenario: Reviewing guardrail list length
- **WHEN** an editor reviews a skill's `## Guardrails` section
- **THEN** every bullet addresses one concrete risk of acting against the skill's purpose and does not repeat the workflow

### Requirement: No Common Mistakes section remains
No active packaged Isomer system-skill entrypoint SHALL contain a `## Common Mistakes` section after migration.

#### Scenario: Validating packaged skill entrypoints
- **WHEN** the validator searches manifest-declared active `SKILL.md` files for `## Common Mistakes`
- **THEN** zero matches are found

### Requirement: Single Guardrails section per skill
Each active packaged Isomer system-skill entrypoint SHALL contain one `## Guardrails` section. If an entrypoint previously contained positive or duplicated behavioral guidance in Guardrails, distinct prohibitions SHALL remain there, duplicate guidance SHALL be removed, and required operations SHALL move to substantive sections without losing behavioral meaning.

#### Scenario: Merging dual-section skill
- **WHEN** an active `SKILL.md` contains both old and current behavioral sections
- **THEN** all distinct prohibited and required behaviors are consolidated under one `## Guardrails` section

#### Scenario: Migrating mixed Guardrails content
- **WHEN** an active `SKILL.md` contains both prohibitions and positive operational guidance in Guardrails
- **THEN** the resulting section retains only distinct `DO NOT ...` prohibitions and preserves positive guidance in its authoritative substantive section

### Requirement: Guardrails format applies to sub-pages
Every active packaged Isomer command, procedure, scenario, binding, or reference page that contains behavioral guardrails SHALL use the same negative-only `DO NOT ...` format as its parent `SKILL.md`.

#### Scenario: Subpage with old Common Mistakes
- **WHEN** an active subpage contains a `## Common Mistakes` section
- **THEN** prohibited and required behaviors move to `## Guardrails` and every guardrail bullet begins with `DO NOT` or `MUST`

#### Scenario: Subpage contains positive Guardrails
- **WHEN** an active subpage contains a `MUST ...` Guardrails bullet or another positive operation step in Guardrails
- **THEN** the operation moves to a substantive section and any retained prohibition begins with `DO NOT`

### Requirement: Loose guardrails are normalized
Every existing `## Guardrails` section in an active packaged Isomer entrypoint or behavioral subpage SHALL use concise top-level bullets that begin with `DO NOT`. Supporting explanation and positive operational guidance SHALL move to an appropriate detail section instead of being discarded.

#### Scenario: Page contains loosely phrased guardrails
- **WHEN** an active page uses `Do not`, `Never`, `MUST`, a bare imperative, or explanatory prose as a top-level Guardrails bullet
- **THEN** a retained prohibition is normalized to `DO NOT` and all necessary positive guidance remains available outside the concise rule

### Requirement: No Common Mistakes in sub-pages
No active packaged Isomer command, procedure, scenario, binding, or reference page SHALL contain a `## Common Mistakes` section after migration.

#### Scenario: Validating active subpages
- **WHEN** the validator searches active pages below every manifest-declared skill root
- **THEN** zero `## Common Mistakes` headings are found outside excluded provenance, migration, and passive-template zones
