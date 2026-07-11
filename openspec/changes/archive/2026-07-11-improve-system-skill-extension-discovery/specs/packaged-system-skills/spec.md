## ADDED Requirements

### Requirement: System Skill Manifest Describes Extension Entry Surfaces
The packaged system-skill manifest SHALL describe how users enter each optional system-skill extension without requiring a repository checkout or extension-specific CLI code.

#### Scenario: Extension declares entry skill and commands
- **WHEN** the system loads a packaged group whose kind is `extension`
- **THEN** the group declares one entry skill that belongs to its packaged skill inventory
- **AND** it declares an ordered list of public command ids exposed through that entry skill

#### Scenario: Extension discovery metadata is package-derived
- **WHEN** code asks for packaged system-skill extensions
- **THEN** each result includes the manifest-owned extension id, group, description, entry skill, commands, and skill paths
- **AND** the result does not depend on a repository checkout

#### Scenario: Invalid extension entry metadata is rejected
- **WHEN** an extension entry skill is missing, is not part of that extension's skill inventory, or a public command id is invalid
- **THEN** system-skill manifest loading fails with a deterministic package asset diagnostic

#### Scenario: Core groups reject extension entry metadata
- **WHEN** a core group declares an extension entry skill or public extension commands
- **THEN** system-skill manifest loading fails with a deterministic package asset diagnostic
