# packaged-system-skills Specification

## Purpose
TBD - created by archiving change package-system-skills-as-assets. Update Purpose after archive.
## Requirements
### Requirement: System Skills Are Package Assets
The system SHALL distribute official non-development Isomer system skills as package-owned resources under the `isomer_labs` package.

#### Scenario: Packaged root contains distributable skillset material
- **WHEN** package resources are inspected for system skills
- **THEN** the packaged root contains `manifest.toml`, `README.md`, `misc/`, `operator/`, `research-paradigm/`, and `service/`
- **AND** it does not contain `dev/`

#### Scenario: Manifest-listed skills resolve inside package assets
- **WHEN** the system loads `assets/system_skills/manifest.toml`
- **THEN** every skill path listed in every manifest group resolves below the packaged system-skill root
- **AND** each listed skill directory contains `SKILL.md`

### Requirement: System Skill Discovery Uses Package Resources
The system SHALL expose package-resource helpers for discovering and reading official system skills without a repository checkout.

#### Scenario: Installed package can list system skill groups
- **WHEN** code asks for packaged system-skill groups
- **THEN** the result is derived from the packaged `manifest.toml`
- **AND** group skill paths are returned as manifest-relative paths rather than repository checkout paths

#### Scenario: Package resource lookup avoids checkout assumptions
- **WHEN** code locates packaged system skills
- **THEN** it uses package resources rather than `Path(__file__)` repository-root traversal
- **AND** it does not require repository-root `skillset/` to exist

### Requirement: System Skills Can Be Materialized Safely
The system SHALL support copying manifest-selected packaged system skills to a filesystem target while preserving relative skill paths.

#### Scenario: Materialize selected group
- **WHEN** a caller materializes the `core` group to an empty target directory
- **THEN** the target receives `manifest.toml` and only the skill directories listed for that group
- **AND** each copied skill keeps its manifest-relative path such as `operator/isomer-op-project-mgr`

#### Scenario: Development skills are never materialized from package assets
- **WHEN** a caller materializes any packaged system-skill group
- **THEN** no `dev/` directory or `isomer-dev-*` skill is copied from package assets

### Requirement: Core Packaged Skills Include Entrypoint
The packaged core system-skill group SHALL include `operator/isomer-op-entrypoint` and materialize it with the rest of the core operator, service, and misc skills.

#### Scenario: Core manifest includes entrypoint
- **WHEN** `src/isomer_labs/assets/system_skills/manifest.toml` is inspected
- **THEN** `groups.core.skills` includes `operator/isomer-op-entrypoint`
- **AND** the listed path resolves below the packaged system-skill root
- **AND** the listed directory contains `SKILL.md`

#### Scenario: Core materialization copies entrypoint
- **WHEN** a caller materializes the `core` group to an empty target directory
- **THEN** the target receives `operator/isomer-op-entrypoint/SKILL.md`
- **AND** it receives the entrypoint's `agents/openai.yaml` and directly linked references

#### Scenario: Packaged skill discovery returns entrypoint
- **WHEN** code asks for manifest-relative skill paths for the `core` group
- **THEN** the result includes `operator/isomer-op-entrypoint`
- **AND** it keeps the path manifest-relative rather than deriving a repository checkout path

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

### Requirement: Public System Skill Installation Documentation
The system SHALL document how users install packaged Isomer system skills into supported agent hosts from the published repository.

#### Scenario: Install docs prefer skills CLI
- **WHEN** a user follows public system-skill installation documentation
- **THEN** the docs SHALL recommend `npx skills add CodeGandee/isomer-labs` or an equivalent repository URL as the primary installation mechanism
- **AND** the docs SHALL show how to select skills with `--skill`

#### Scenario: Agent target is explicit
- **WHEN** docs show a skill installation command
- **THEN** the command SHALL include or explain `--agent <agent>` so users know which agent host receives the skills

#### Scenario: Entrypoint skill is discoverable
- **WHEN** docs explain operator skill installation
- **THEN** they SHALL identify `isomer-op-entrypoint` as the recommended first operator skill for users who already know the system
- **AND** they SHALL identify `isomer-op-welcome` as the orientation menu skill

#### Scenario: Extension skills are optional
- **WHEN** docs explain DeepSci skill installation
- **THEN** they SHALL state that DeepSci skills are optional extension skills and do not need to be installed for basic Project lifecycle CLI usage

