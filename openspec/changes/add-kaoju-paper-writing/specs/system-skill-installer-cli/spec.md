## MODIFIED Requirements

### Requirement: Packaged Extension Discovery Commands
The system SHALL provide focused commands for discovering optional packaged system-skill extensions and their agent-facing entry surfaces.

#### Scenario: Extension list summarizes available extensions
- **WHEN** a user runs `isomer-cli system-skills extensions list`
- **THEN** the output lists each packaged extension id, description, and entry skill in manifest order
- **AND** the output points to extension inspection for complete usage

#### Scenario: Extension show explains Kaoju usage
- **WHEN** a user runs `isomer-cli system-skills extensions show kaoju`
- **THEN** the output identifies `$isomer-kaoju-pipeline` as the entry skill
- **AND** it lists Kaoju's public procedure and helper command ids, including `paper-pass` and `create-paper-template`
- **AND** it provides commands to install and inspect the Kaoju extension

#### Scenario: Kaoju writing skill is discoverable
- **WHEN** a user inspects Kaoju extension details in text or JSON form
- **THEN** the skill inventory includes `isomer-kaoju-write` and the command inventory includes `paper-pass` and `create-paper-template`
- **AND** the invocation guidance continues to route users through `$isomer-kaoju-pipeline` for the procedural entry surface

#### Scenario: JSON discovery is structured
- **WHEN** a user requests JSON output for extension list or show
- **THEN** each extension object includes its id, group, description, entry skill, commands, skills, install command, status command, and invocation
- **AND** the response reports `mutated` as false

#### Scenario: Unknown extension show fails safely
- **WHEN** a user runs `isomer-cli system-skills extensions show <unknown-id>`
- **THEN** the command reports a deterministic unknown-extension error
- **AND** it does not mutate files
