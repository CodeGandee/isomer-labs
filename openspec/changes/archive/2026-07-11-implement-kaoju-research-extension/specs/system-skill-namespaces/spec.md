## ADDED Requirements

### Requirement: Active Kaoju Namespace Inventory
The packaged system-skill catalog SHALL use `isomer-kaoju-<purpose>` for the Kaoju domain-extension family.

#### Scenario: Kaoju paths use active namespace
- **WHEN** the packaged Kaoju extension is inspected
- **THEN** every production skill path has the form `research-paradigm/kaoju/isomer-kaoju-<purpose>`
- **AND** no active Kaoju path uses `isomer-ext-*`, `isomer-rsch-*`, or a version-suffixed compatibility name

#### Scenario: Kaoju identity matches folder name
- **WHEN** a manifest-listed Kaoju skill is inspected
- **THEN** its folder, `SKILL.md` frontmatter name, `agents/openai.yaml` display name, and default-prompt skill invocation are identical

#### Scenario: Namespace documentation includes Kaoju example
- **WHEN** packaged system-skill namespace documentation describes domain-extension families
- **THEN** it identifies `kaoju` as an active example of `isomer-<extension-name>-<purpose>`
- **AND** it keeps Kaoju distinct from cross-domain `isomer-misc-*` helpers
