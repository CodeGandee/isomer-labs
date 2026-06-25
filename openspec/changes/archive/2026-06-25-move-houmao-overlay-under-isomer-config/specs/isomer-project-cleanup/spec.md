## MODIFIED Requirements

### Requirement: Cleanup Parts
The system SHALL support partial cleanup by named part so users can remove selected Isomer-managed material without deleting unrelated Project files.

#### Scenario: Project config part
- **WHEN** cleanup selects `--part project-config`
- **THEN** the plan targets the Project Config Directory `.isomer-labs/`

#### Scenario: Houmao overlay part
- **WHEN** cleanup selects `--part houmao-overlay`
- **THEN** the plan targets the Isomer-managed Project-level Houmao overlay `.isomer-labs/.houmao/`, preserves root `.houmao/`, and does not stop live Houmao agents or clean external Houmao state

#### Scenario: Content policy part
- **WHEN** cleanup selects `--part content-policy`
- **THEN** the plan targets only the selected content root's generated `README.md` and `.gitignore` policy files

#### Scenario: Topic workspace part
- **WHEN** cleanup selects `--part topic-workspace --topic <topic-id>`
- **THEN** the plan targets the selected Research Topic's registered or derived Topic Workspace directory

#### Scenario: Runtime part
- **WHEN** cleanup selects `--part runtime --topic <topic-id>`
- **THEN** the plan targets `state.sqlite`, runtime-owned directories, and adapter runtime material under the selected Topic Workspace without deleting topic definition or team-profile source material

#### Scenario: Bootstrap part
- **WHEN** cleanup selects `--part bootstrap`
- **THEN** the plan includes Project config, the Isomer-managed Project-level Houmao overlay under `.isomer-labs/.houmao/`, generated content-root policy files, and known init-created Topic Workspace directories while preserving unknown files and root `.houmao/` by default

### Requirement: Cleanup Authority and Path Safety
The system SHALL resolve cleanup targets from the strongest available Project authority and SHALL refuse unsafe filesystem targets.

#### Scenario: Valid manifest is authority
- **WHEN** a valid Project Manifest exists
- **THEN** cleanup uses the manifest's path defaults, Research Topic registrations, and Topic Workspace registrations to resolve selected cleanup targets

#### Scenario: Malformed manifest limits authority
- **WHEN** `.isomer-labs/manifest.toml` exists but cannot be parsed
- **THEN** cleanup may target `.isomer-labs/`, `.isomer-labs/.houmao/`, and the built-in or explicitly supplied content root, but it does not infer Research Topics from unregistered directories and does not target root `.houmao/`

#### Scenario: Missing manifest supports explicit bootstrap cleanup
- **WHEN** no Project Manifest exists and the user supplies an explicit Project root or runs from the intended root
- **THEN** cleanup may plan removal for `.isomer-labs/`, `.isomer-labs/.houmao/`, and the built-in or explicitly supplied content root while reporting that manifest authority is unavailable and preserving root `.houmao/`

#### Scenario: External paths are refused
- **WHEN** a planned cleanup target resolves outside the Project root
- **THEN** cleanup refuses that target and does not delete it

#### Scenario: Project root is refused
- **WHEN** a planned cleanup target equals the Project root
- **THEN** cleanup refuses that target and does not delete it

#### Scenario: Symlinks are not recursively followed
- **WHEN** a planned cleanup target is a symlink
- **THEN** cleanup removes only the symlink entry when that entry is the exact planned target or refuses the target, and it does not recursively delete the symlink destination

### Requirement: Content Root Purge Safety
The system SHALL preserve unknown files under the selected generated content root unless the user explicitly requests whole-root purge behavior.

#### Scenario: Content root part requires purge opt-in
- **WHEN** a user selects `--part content-root --yes` without the purge opt-in
- **THEN** cleanup refuses whole content-root deletion, reports the safer alternatives, and does not delete the content root

#### Scenario: Purge reports unknown content
- **WHEN** a user runs `isomer-cli project cleanup --part content-root --purge-content-root --dry-run`
- **THEN** the plan lists the selected content root, reports whether unknown files are present, and marks the operation as non-mutating

#### Scenario: Confirmed purge removes selected root
- **WHEN** a user runs `isomer-cli project cleanup --part content-root --purge-content-root --yes`
- **THEN** cleanup removes the selected generated content root only after validating that the root is project-local, is not `.isomer-labs/`, is not `.isomer-labs/.houmao/`, is not root `.houmao/`, and is not the Project root
