## ADDED Requirements

### Requirement: Guardrails format applies to sub-pages
Every subcommand and reference page that contains behavioral guidance SHALL use the same `DO NOT ...` / `MUST ...` guardrail format as the parent `SKILL.md`.

#### Scenario: Sub-page with old Common Mistakes
- **WHEN** a subcommand or reference page contains a `## Common Mistakes` section
- **THEN** the section is renamed to `## Guardrails` and every bullet is rewritten to start with `DO NOT` or `MUST`

### Requirement: Loose guardrails are normalized
Every existing `## Guardrails` section in a subcommand or reference page SHALL be normalized so that each bullet starts with `DO NOT` or `MUST`.

#### Scenario: Sub-page with lowercase guardrails
- **WHEN** a sub-page guardrail uses "Do not ...", "Never ...", or an imperative statement such as "Use..." / "Preserve..."
- **THEN** the bullet is rewritten to start with `DO NOT` or `MUST`

### Requirement: No Common Mistakes in sub-pages
No subcommand or reference page SHALL contain a `## Common Mistakes` section after this change.

#### Scenario: Validating sub-page compliance
- **WHEN** a validator searches subcommand and reference pages for `## Common Mistakes`
- **THEN** zero matches are found
