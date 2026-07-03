## ADDED Requirements

### Requirement: Package Assets May Carry Runtime Resources
The architecture boundary SHALL allow `src/isomer_labs/assets/` to contain package-owned static runtime resources, including official system-skill assets.

#### Scenario: Package-owned skill assets are not checkout dependencies
- **WHEN** architecture tests scan source and packaged assets
- **THEN** paths under `src/isomer_labs/assets/system_skills` are treated as package resources
- **AND** source code may refer to `assets/system_skills` through package-resource APIs
- **AND** source code still fails architecture checks if it treats repository-root `skillset/` as a runtime dependency

#### Scenario: Development skills stay outside package assets
- **WHEN** architecture tests inspect packaged system-skill assets
- **THEN** they fail if `src/isomer_labs/assets/system_skills/dev` exists
- **AND** they pass when development-only skills remain only under repository-root `skillset/dev`
