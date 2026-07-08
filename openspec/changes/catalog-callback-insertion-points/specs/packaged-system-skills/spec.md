## ADDED Requirements

### Requirement: System Skill Manifest Classifies Groups
The packaged system-skill manifest SHALL classify each manifest group as core or extension so callers can distinguish always-available system skills from optional system extensions.

#### Scenario: Core group is always available
- **WHEN** the system loads the packaged system-skill manifest
- **THEN** each core group declares that its skills are always available for Project operator discovery
- **AND** the core group does not require a Project Manifest operator extension declaration before its catalog metadata is listed

#### Scenario: Extension group has stable extension id
- **WHEN** the system loads a packaged system-skill manifest group whose kind is extension
- **THEN** the group declares a stable extension id
- **AND** callers can filter catalog metadata by that extension id

#### Scenario: Invalid group classification is rejected
- **WHEN** a packaged system-skill manifest group omits group classification or declares an invalid extension id
- **THEN** system-skill manifest loading fails with a deterministic package asset diagnostic

### Requirement: System Skill Manifest Declares Callback Insertion Points
The packaged system-skill manifest SHALL declare callback stage definitions and per-skill callback insertion points as catalog metadata.

#### Scenario: Stage definitions are loaded from manifest
- **WHEN** the system loads `assets/system_skills/manifest.toml`
- **THEN** callback insertion point stage ids, labels, and descriptions are derived from the manifest rather than hardcoded only in Python

#### Scenario: Per-skill insertion points are manifest-relative
- **WHEN** the manifest declares callback insertion points for a packaged system skill
- **THEN** the declaration is keyed by the skill's manifest-relative path
- **AND** every declared stage id resolves to a manifest callback stage definition
- **AND** every referenced skill path resolves below the packaged system-skill root and contains `SKILL.md`

#### Scenario: Skills without declarations expose no insertion points
- **WHEN** a packaged system skill has no callback insertion point declaration in the manifest
- **THEN** the system treats that skill as exposing no callback insertion points

#### Scenario: Callback insertion point discovery is deterministic
- **WHEN** code asks for packaged callback insertion points
- **THEN** the result is derived from the packaged manifest, grouped by manifest group, and returned in deterministic manifest order with target skill name, skill path, group name, optional extension id, stage id, and stage metadata
