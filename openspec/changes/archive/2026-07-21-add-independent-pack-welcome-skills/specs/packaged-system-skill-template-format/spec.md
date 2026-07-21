## ADDED Requirements

### Requirement: Welcome Skills Use a Newcomer Teaching Format
Every public welcome `SKILL.md` SHALL use a concise progressive-disclosure format that introduces typical use cases before exhaustive command detail.

#### Scenario: Welcome entrypoint is inspected
- **WHEN** a public welcome `SKILL.md` is inspected
- **THEN** it contains `## Overview`, `## When to Use`, a near-top numbered `## Workflow`, a typical-use-case surface, a complete command-map route, an output contract, and exactly one negative-only `## Guardrails`
- **AND** it links only the selected one-level command or reference resources needed for each route

#### Scenario: Typical use-case table is inspected
- **WHEN** a welcome use-case table or equivalent structured section is inspected
- **THEN** every row has a one-sentence use condition, representative routing cues, required context, canonical entrypoint route, exact example, expected action, mutation posture, and next step
- **AND** the prose is adapted to the welcome context instead of duplicating source metadata verbatim

#### Scenario: Complete map follows progressive disclosure
- **WHEN** a welcome skill documents the sibling entrypoint's full command inventory
- **THEN** the exhaustive map is loaded only through `show-command-map`, `help`, or an explicit complete-output request
- **AND** default welcome output remains a concise selection of high-value patterns
