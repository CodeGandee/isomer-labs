## ADDED Requirements

### Requirement: Core Packaged Skills Include Operation Set Recording
The packaged core system-skill group SHALL include `research/isomer-research-operation-set-recording` as the provider-neutral owner of operation-set research acceptance guidance.

#### Scenario: Core manifest includes recording skill
- **WHEN** `src/isomer_labs/assets/system_skills/manifest.toml` is inspected
- **THEN** `groups.core.skills` includes `research/isomer-research-operation-set-recording`
- **AND** the path resolves to a skill directory containing `SKILL.md`, `agents/openai.yaml`, and its directly required references

#### Scenario: Recording skill has a bounded workflow
- **WHEN** the packaged skill is inspected
- **THEN** its numbered workflow covers worker context, inspection, binding resolution, manifest completion, preview, apply, verify, partial recovery, and legacy repair
- **AND** it forbids inferred record or Research Idea lineage

#### Scenario: Core materialization copies recording skill
- **WHEN** a caller materializes or installs the core system-skill group
- **THEN** the target includes the operation-set recording skill and its required resources at the manifest-relative path

#### Scenario: Skill metadata version matches package release
- **WHEN** a release or release candidate validates packaged system skills
- **THEN** the new skill's `agents/openai.yaml` metadata version matches `project.version` under the existing release rule
