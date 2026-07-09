## MODIFIED Requirements

### Requirement: System Skill CLI Surface
The system SHALL expose a top-level `isomer-cli system-skills` command group for packaged Isomer system-skill installation, upgrade, and inspection.

#### Scenario: Help lists system-skills command group
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help lists `system-skills`

#### Scenario: System skill group lists supported subcommands
- **WHEN** a user runs `isomer-cli system-skills --help`
- **THEN** the command help lists `list`, `status`, `install`, `upgrade`, and `uninstall`

### Requirement: Skill Projection
The system SHALL project selected packaged skills into target skill roots as flat skill directories or symlinks whose install slots are identified by packaged skill name.

#### Scenario: Copy projection writes flat skill directory
- **WHEN** a user installs `isomer-op-entrypoint` into a target skill root in copy mode and `<skill-root>/isomer-op-entrypoint` does not exist
- **THEN** the command creates `<skill-root>/isomer-op-entrypoint/SKILL.md`
- **AND** it copies the skill's packaged support files
- **AND** it does not create `<skill-root>/operator/isomer-op-entrypoint`
- **AND** it does not create a per-skill Isomer ownership marker file

#### Scenario: Symlink projection writes flat skill link
- **WHEN** a user installs `isomer-op-entrypoint` into a target skill root with `--mode symlink` and `<skill-root>/isomer-op-entrypoint` does not exist
- **THEN** the command creates `<skill-root>/isomer-op-entrypoint` as a symlink to the packaged skill source when the package resource is filesystem-backed
- **AND** it does not write marker files through the symlink or into the packaged skill source

#### Scenario: Existing selected path is preserved without force
- **WHEN** a user installs a selected packaged skill and `<skill-root>/<skill-name>` already exists as a file, directory, or symlink
- **THEN** the command reports the existing selected path for that skill
- **AND** it does not overwrite, unlink, or remove that path

#### Scenario: Force replaces existing selected path
- **WHEN** a user installs a selected packaged skill with `--force` and `<skill-root>/<skill-name>` already exists as a file, directory, or symlink
- **THEN** the command removes exactly `<skill-root>/<skill-name>`
- **AND** it projects the packaged skill into `<skill-root>/<skill-name>` using the requested projection mode
- **AND** it reports that the path was replaced

#### Scenario: Force switches copy projection to symlink projection
- **WHEN** `<skill-root>/isomer-op-entrypoint` exists as a real directory
- **AND** a user runs `isomer-cli system-skills install --target generic --skill isomer-op-entrypoint --mode symlink --force`
- **THEN** the command removes the real directory
- **AND** it creates `<skill-root>/isomer-op-entrypoint` as a symlink to the packaged skill source

#### Scenario: Force switches symlink projection to copy projection
- **WHEN** `<skill-root>/isomer-op-entrypoint` exists as a symlink
- **AND** a user runs `isomer-cli system-skills install --target generic --skill isomer-op-entrypoint --mode copy --force`
- **THEN** the command unlinks the symlink without deleting the symlink target
- **AND** it creates `<skill-root>/isomer-op-entrypoint` as a real copied directory

### Requirement: Status and Uninstall
The system SHALL inspect and remove selected packaged skill install slots by packaged skill name.

#### Scenario: Status reports installed and missing skills
- **WHEN** a user runs `isomer-cli system-skills status --target generic`
- **THEN** the output reports the target skill root
- **AND** it reports selected packaged skills as installed when `<skill-root>/<skill-name>` exists
- **AND** it can report missing selected skills when selectors are supplied and `<skill-root>/<skill-name>` does not exist
- **AND** it reports target-root install manifest metadata when `isomer-labs-skill-manifest.json` exists

#### Scenario: Status reports projection path shape
- **WHEN** a selected packaged skill path exists under the target skill root
- **THEN** status reports the installed skill name, projection path, packaged source path, and detected projection mode when the path is a real directory or symlink
- **AND** status reports a deterministic invalid projection diagnostic when the path exists but is neither a real directory nor a symlink directory projection

#### Scenario: Uninstall removes selected named projections
- **WHEN** a user runs `isomer-cli system-skills uninstall --target generic`
- **THEN** the command removes selected packaged skill paths under the generic skill root by packaged skill name
- **AND** it reports removed and absent skills

#### Scenario: Uninstall removes symlink projection without following it
- **WHEN** a selected packaged skill path under the target skill root is a symlink
- **THEN** uninstall removes the symlink entry itself
- **AND** it does not delete the symlink target

## ADDED Requirements

### Requirement: Target Root Skill Manifest
The system SHALL maintain an `isomer-labs-skill-manifest.json` file in each target skill root that records the Isomer CLI/package version and the Isomer system skills tracked in that root.

#### Scenario: Install writes target root manifest
- **WHEN** `isomer-cli system-skills install` mutates a target skill root
- **THEN** the command writes `<skill-root>/isomer-labs-skill-manifest.json`
- **AND** the manifest records a schema version, target name, skill root path, Isomer CLI/package version, update timestamp, and the tracked installed skills
- **AND** each tracked installed skill record includes skill name, manifest-relative source path, and projection mode

#### Scenario: Per-skill marker files are not required
- **WHEN** a selected packaged skill is installed as a copied directory or symlink
- **THEN** ownership and upgrade tracking are recorded in `<skill-root>/isomer-labs-skill-manifest.json`
- **AND** the command does not require `.isomer-system-skill.json` inside the skill directory

#### Scenario: Uninstall updates target root manifest
- **WHEN** `isomer-cli system-skills uninstall` removes one or more selected packaged skill paths
- **THEN** the command updates `<skill-root>/isomer-labs-skill-manifest.json`
- **AND** removed skill names are no longer listed as tracked installed skills

#### Scenario: Status reports unreadable manifest
- **WHEN** `<skill-root>/isomer-labs-skill-manifest.json` exists but cannot be parsed as a supported manifest
- **THEN** status reports a deterministic warning diagnostic
- **AND** status still derives selected skill path existence from the filesystem

### Requirement: System Skill Upgrade
The system SHALL provide `isomer-cli system-skills upgrade` to refresh installed packaged system skills and clean up stale manifest-tracked skill paths after Isomer CLI/package upgrades.

#### Scenario: Upgrade refreshes current selected skills
- **WHEN** a user runs `isomer-cli system-skills upgrade --target generic`
- **THEN** the command resolves the current selected packaged skill set using the same selector rules as install
- **AND** it refreshes each selected skill path from the current package resources
- **AND** it updates `<skill-root>/isomer-labs-skill-manifest.json` with the current Isomer CLI/package version

#### Scenario: Upgrade removes stale manifest-tracked skills
- **WHEN** the target root manifest lists a previously installed skill name that is not in the current selected packaged skill set
- **AND** `<skill-root>/<old-skill-name>` exists
- **THEN** upgrade removes `<skill-root>/<old-skill-name>`
- **AND** it reports the stale skill path as removed

#### Scenario: Upgrade does not remove untracked paths
- **WHEN** a path exists under the target skill root but its name is not tracked in `isomer-labs-skill-manifest.json`
- **THEN** upgrade does not remove that path as a stale installed skill

#### Scenario: Upgrade preserves recorded projection mode by default
- **WHEN** the target root manifest records a projection mode for an installed selected skill
- **AND** the user runs upgrade without an explicit projection mode override
- **THEN** upgrade refreshes that skill using the recorded projection mode

#### Scenario: Upgrade can change projection mode explicitly
- **WHEN** the user runs upgrade with an explicit projection mode
- **THEN** upgrade refreshes selected skills using the requested projection mode
- **AND** it records that projection mode in the target root manifest
