## MODIFIED Requirements

### Requirement: Packaged Skill Listing
The system SHALL list packaged system-skill packs, their ordered public welcome and entrypoint skills, and their protected capability inventories from installed package resources.

#### Scenario: Human-readable listing distinguishes roles
- **WHEN** a user runs `isomer-cli system-skills list`
- **THEN** each pack identifies its welcome skill, designated execution entrypoint, optional extension id, and protected-member count
- **AND** public skills are not mixed with protected members as equivalent install units

#### Scenario: JSON listing is structured
- **WHEN** packaged skill listing uses JSON output
- **THEN** each pack contains ordered `public_skills` records with name, role, source path, commands, and version
- **AND** it separately contains protected capability records and their entrypoint-owned invocation designators

### Requirement: Skill Selection
The system SHALL resolve group, extension, public-skill, and compatibility selectors to complete public packs.

#### Scenario: Default selection installs core pair
- **WHEN** a user installs without a group, extension, or skill selector
- **THEN** selection contains the core pack with `isomer-op-welcome` and `isomer-op-entrypoint`

#### Scenario: Extension selection installs complete pairs
- **WHEN** a user selects extension `deepsci` or `kaoju`
- **THEN** selection includes the complete core pack and the selected extension's welcome and entrypoint
- **AND** it does not include an unselected extension

#### Scenario: Public welcome selector resolves owning pack
- **WHEN** a user supplies `--skill isomer-op-welcome`, `--skill isomer-ext-deepsci-welcome`, or `--skill isomer-ext-kaoju-welcome`
- **THEN** the selector resolves to the complete owning pack rather than one public projection
- **AND** JSON output distinguishes the requested public name from the resolved pack and its projections

#### Scenario: Entrypoint or protected selector resolves owning pack
- **WHEN** a user supplies an entrypoint, legacy public alias, or protected logical id
- **THEN** selection resolves the owning complete pack
- **AND** legacy or protected selectors retain their applicable compatibility diagnostic

### Requirement: Skill Projection
The system SHALL project every public skill of a selected pack as a flat sibling directory or symlink and SHALL treat the complete pack as one staged mutation unit.

#### Scenario: Copy projection writes public siblings
- **WHEN** a selected pack is installed in copy mode
- **THEN** each declared welcome and entrypoint is copied to `<skill-root>/<public-skill-name>`
- **AND** protected capabilities remain nested below the copied entrypoint

#### Scenario: Symlink projection writes public siblings
- **WHEN** a selected pack is installed in symlink mode
- **THEN** each declared welcome and entrypoint is linked from `<skill-root>/<public-skill-name>` to its package-owned source directory
- **AND** no protected member receives a top-level symlink

#### Scenario: One public destination conflicts
- **WHEN** any public destination of a selected pack already exists and replacement is not authorized
- **THEN** installation preserves every live destination and reports the conflict
- **AND** it does not install only the non-conflicting public skill

#### Scenario: Force replaces a complete owned pack
- **WHEN** force is true and every conflicting destination is safe to replace under ownership rules
- **THEN** the installer stages and replaces all public projections of the selected pack
- **AND** failure rolls back the pack rather than leaving one public role updated

### Requirement: Status and Uninstall
Status and uninstall SHALL operate on complete pack records while reporting each public projection and the entrypoint's protected-member integrity.

#### Scenario: Status reports pack and public state
- **WHEN** status inspects a selected pack
- **THEN** it reports aggregate pack status plus each public skill's role, path, projection mode, identity, version, compatibility, and receipt ownership
- **AND** it reports missing, extra, mismatched, or incompatible protected entrypoint members

#### Scenario: Public role is missing
- **WHEN** a pack has a valid entrypoint but its welcome is missing, or has a valid welcome but its entrypoint is missing
- **THEN** status reports the pack as incomplete
- **AND** it identifies the missing public role without treating the observed name as complete installation evidence

#### Scenario: Uninstall removes a selected pack
- **WHEN** uninstall is authorized for a receipt-owned pack
- **THEN** it removes both public projection directories or symlinks and updates the receipt as one operation
- **AND** it does not follow symlinks into their targets

#### Scenario: One public name selects uninstall
- **WHEN** a user supplies a public welcome or entrypoint name to uninstall
- **THEN** the CLI explains that the owning pack is the removal unit and identifies every public path that will be removed
- **AND** it does not remove only the named public role

### Requirement: Target Root Skill Manifest
The installer SHALL write a scope-aware v5 target-root receipt whose records describe complete packs, their public projections, and their protected capability integrity.

#### Scenario: Install writes multi-public pack receipt
- **WHEN** install successfully mutates a target root
- **THEN** `isomer-labs-skill-manifest.json` uses schema `isomer-labs-skill-manifest.v5`
- **AND** each pack record contains pack id, designated entrypoint, package version, ordered public projection records, and protected-member records

#### Scenario: Public projection record is complete
- **WHEN** a v5 public projection record is inspected
- **THEN** it contains public skill name, role, source path, projection mode, and skill version
- **AND** welcome and entrypoint records are independently verifiable

#### Scenario: Protected member record remains stable
- **WHEN** a v5 protected-member record is inspected
- **THEN** it contains logical id, entrypoint-relative path, invocation designator, and skill version
- **AND** it is associated with the pack's designated entrypoint rather than the welcome skill

#### Scenario: Earlier receipt remains readable
- **WHEN** inspection encounters a supported v1, v2, v3, or v4 receipt
- **THEN** it reports the earlier schema and available evidence without inventing a welcome projection
- **AND** authorized migration writes v5 only after all new public projections validate

### Requirement: System Skill Upgrade
Upgrade SHALL stage and validate every public skill of selected packs before replacing current projections or removing obsolete receipt-tracked paths.

#### Scenario: Current v4 pack is upgraded
- **WHEN** a v4 installation containing compacted entrypoint packs is upgraded
- **THEN** upgrade stages the independent welcome and refreshed entrypoint for each selected pack, validates both, and writes a v5 receipt
- **AND** the core entrypoint's former nested welcome disappears only as part of the validated entrypoint replacement

#### Scenario: Legacy flat installation is upgraded
- **WHEN** a supported earlier receipt tracks a top-level `isomer-op-welcome` or other flat skills
- **THEN** upgrade may reuse only receipt-owned destinations while staging the new complete packs
- **AND** it removes obsolete receipt-tracked paths only after the v5 pack is committed

#### Scenario: New welcome destination is untracked
- **WHEN** a required top-level welcome path exists without supported receipt ownership
- **THEN** upgrade preserves the path and blocks that pack with an exact conflict diagnostic
- **AND** it does not broaden force or cleanup to unrelated paths

#### Scenario: Public-pair validation fails
- **WHEN** either staged welcome or entrypoint validation fails
- **THEN** upgrade leaves old projections and the old receipt intact
- **AND** it performs no stale cleanup for that pack

#### Scenario: Commit fails after backup
- **WHEN** a filesystem or receipt write fails while committing a multi-public pack
- **THEN** upgrade restores every backed-up public projection and prior receipt
- **AND** it reports the exact rollback or retained-path state

### Requirement: Packaged Extension Discovery Commands
Extension discovery SHALL present each extension's independent welcome, execution entrypoint, entrypoint commands, and protected member metadata from the package catalog.

#### Scenario: Extension list summarizes public pairs
- **WHEN** a user runs `isomer-cli system-skills extensions list`
- **THEN** each extension row identifies its welcome skill and execution entrypoint
- **AND** it describes welcome as onboarding and entrypoint as route-and-proceed execution

#### Scenario: Extension show explains both invocations
- **WHEN** a user shows DeepSci or Kaoju
- **THEN** output presents `$<welcome>` for typical use cases and `$<entrypoint> use <command> to <task>` for execution
- **AND** it reports entrypoint commands and protected capability summaries without advertising protected direct invocation

#### Scenario: JSON discovery separates roles
- **WHEN** extension discovery uses JSON output
- **THEN** the response contains ordered public skill records with roles and a designated entrypoint field
- **AND** protected logical capabilities remain a separate collection

### Requirement: Installation Receipts Preserve Skill Versions
Installation receipts SHALL preserve version evidence for every public skill and every protected member in each installed pack.

#### Scenario: Install writes public and protected versions
- **WHEN** a selected pack is installed
- **THEN** the v5 receipt records the welcome version, entrypoint version, and each manifest-declared protected member version

#### Scenario: One public version drifts
- **WHEN** a projected welcome or entrypoint version differs from its v5 receipt record
- **THEN** status reports receipt drift for that public skill
- **AND** it does not classify the owning pack as verified

#### Scenario: Earlier receipt lacks welcome evidence
- **WHEN** a v1-v4 receipt is inspected
- **THEN** status reports legacy or incomplete public-role evidence rather than inventing a welcome version
