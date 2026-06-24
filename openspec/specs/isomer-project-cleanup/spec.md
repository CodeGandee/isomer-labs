# isomer-project-cleanup Specification

## Purpose
TBD - created by archiving change add-project-cleanup-command. Update Purpose after archive.
## Requirements
### Requirement: Project Cleanup Planning
The system SHALL build a deterministic cleanup plan for selected Isomer-managed Project material before removing any filesystem entry.

#### Scenario: Dry-run reports planned removals
- **WHEN** a user runs `isomer-cli project cleanup --part project-config --dry-run`
- **THEN** the system reports a deterministic cleanup plan, marks the command as non-mutating, and does not remove `.isomer-labs/`

#### Scenario: Missing confirmation defaults to non-mutating plan
- **WHEN** a user runs `isomer-cli project cleanup --part project-config` without `--yes`
- **THEN** the system reports the cleanup plan, does not remove files, and explains that `--yes` is required for deletion

#### Scenario: Plan includes structured entries
- **WHEN** cleanup reports a planned removal in text or JSON output
- **THEN** each entry includes the cleanup part, path, action, target kind, existence status, and any warnings needed to understand why it will or will not be removed

#### Scenario: Plan is computed before mutation
- **WHEN** a user runs `isomer-cli project cleanup --part bootstrap --yes`
- **THEN** the system resolves all selected cleanup targets and validates their safety before deleting the first target

### Requirement: Cleanup Confirmation and Execution
The system SHALL require explicit confirmation before performing cleanup deletion and SHALL delete only targets present in the reviewed cleanup plan.

#### Scenario: Confirmed cleanup removes planned project config
- **WHEN** a user runs `isomer-cli project cleanup --part project-config --yes`
- **THEN** the system removes `.isomer-labs/` only if that target appears in the validated cleanup plan and reports the command as mutating

#### Scenario: Confirmed cleanup skips absent targets
- **WHEN** a selected cleanup target does not exist
- **THEN** the system reports the target as skipped or absent without treating absence as a deletion failure

#### Scenario: Failed target is reported
- **WHEN** cleanup cannot remove a planned target because of an operating-system error
- **THEN** the system returns a deterministic diagnostic for that target and reports any removals that did complete

### Requirement: Cleanup Parts
The system SHALL support partial cleanup by named part so users can remove selected Isomer-managed material without deleting unrelated Project files.

#### Scenario: Project config part
- **WHEN** cleanup selects `--part project-config`
- **THEN** the plan targets the Project Config Directory `.isomer-labs/`

#### Scenario: Houmao overlay part
- **WHEN** cleanup selects `--part houmao-overlay`
- **THEN** the plan targets the Project-level Houmao overlay `.houmao/` and does not stop live Houmao agents or clean external Houmao state

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
- **THEN** the plan includes Project config, the Project-level Houmao overlay, generated content-root policy files, and known init-created Topic Workspace directories while preserving unknown files by default

### Requirement: Cleanup Authority and Path Safety
The system SHALL resolve cleanup targets from the strongest available Project authority and SHALL refuse unsafe filesystem targets.

#### Scenario: Valid manifest is authority
- **WHEN** a valid Project Manifest exists
- **THEN** cleanup uses the manifest's path defaults, Research Topic registrations, and Topic Workspace registrations to resolve selected cleanup targets

#### Scenario: Malformed manifest limits authority
- **WHEN** `.isomer-labs/manifest.toml` exists but cannot be parsed
- **THEN** cleanup may target `.isomer-labs/`, `.houmao/`, and the built-in or explicitly supplied content root, but it does not infer Research Topics from unregistered directories

#### Scenario: Missing manifest supports explicit bootstrap cleanup
- **WHEN** no Project Manifest exists and the user supplies an explicit Project root or runs from the intended root
- **THEN** cleanup may plan removal for `.isomer-labs/`, `.houmao/`, and the built-in or explicitly supplied content root while reporting that manifest authority is unavailable

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
- **THEN** cleanup removes the selected generated content root only after validating that the root is project-local, is not `.isomer-labs/`, is not `.houmao/`, and is not the Project root

### Requirement: Reinitialization After Cleanup
The system SHALL support a safe reinitialization workflow by keeping `project init` overwrite refusal separate from explicit cleanup.

#### Scenario: Cleanup unblocks init
- **WHEN** a user removes `.isomer-labs/manifest.toml` through confirmed Project config or bootstrap cleanup
- **THEN** a later `isomer-cli project init` can proceed according to normal fresh-initialization rules if the remaining Project root satisfies init preconditions

#### Scenario: Init still refuses existing manifest
- **WHEN** `.isomer-labs/manifest.toml` exists
- **THEN** `isomer-cli project init` refuses to overwrite it and does not implicitly run cleanup

