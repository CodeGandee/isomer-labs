## MODIFIED Requirements

### Requirement: Guardrails section format
Every active packaged Isomer system skill SHALL include exactly one `## Guardrails` section in its `SKILL.md` file.

#### Scenario: Packaged skill is created or migrated
- **WHEN** an agent creates or migrates an active packaged Isomer system skill using the current template
- **THEN** the resulting `SKILL.md` includes exactly one `## Guardrails` section

### Requirement: No Common Mistakes section remains
No active packaged Isomer system-skill entrypoint SHALL contain a `## Common Mistakes` section after migration.

#### Scenario: Validating packaged skill entrypoints
- **WHEN** the validator searches manifest-declared active `SKILL.md` files for `## Common Mistakes`
- **THEN** zero matches are found

### Requirement: Single Guardrails section per skill
Each active packaged Isomer system-skill entrypoint SHALL contain one `## Guardrails` section. If an entrypoint previously contained both `## Guardrails` and `## Common Mistakes`, the sections SHALL be merged, duplicates SHALL be removed, and distinct behavioral constraints SHALL be preserved.

#### Scenario: Merging dual-section skill
- **WHEN** an active `SKILL.md` contains both old and current behavioral sections
- **THEN** all distinct prohibited and required behaviors are consolidated under one `## Guardrails` section

### Requirement: Guardrails format applies to sub-pages
Every active packaged Isomer command, procedure, scenario, binding, or reference page that contains behavioral guardrails SHALL use the same `DO NOT ...` and `MUST ...` format as its parent `SKILL.md`.

#### Scenario: Subpage with old Common Mistakes
- **WHEN** an active subpage contains a `## Common Mistakes` section
- **THEN** prohibited and required behaviors move to `## Guardrails` and every guardrail bullet begins with `DO NOT` or `MUST`

### Requirement: Loose guardrails are normalized
Every existing `## Guardrails` section in an active packaged Isomer entrypoint or behavioral subpage SHALL use concise top-level bullets that begin with `DO NOT` or `MUST`. Supporting explanation that does not fit one rule SHALL move to an appropriate detail section instead of being discarded.

#### Scenario: Page contains loosely phrased guardrails
- **WHEN** an active page uses `Do not`, `Never`, a bare imperative, or explanatory prose as a top-level Guardrails bullet
- **THEN** the rule is normalized to `DO NOT` or `MUST` and any necessary supporting detail remains available outside the concise rule

### Requirement: No Common Mistakes in sub-pages
No active packaged Isomer command, procedure, scenario, binding, or reference page SHALL contain a `## Common Mistakes` section after migration.

#### Scenario: Validating active subpages
- **WHEN** the validator searches active pages below every manifest-declared skill root
- **THEN** zero `## Common Mistakes` headings are found outside excluded provenance, migration, and passive-template zones
