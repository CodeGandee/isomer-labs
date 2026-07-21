## MODIFIED Requirements

### Requirement: Packaged Skill Listing
The system-skill CLI SHALL list public packs separately from their protected logical capabilities.

#### Scenario: List reads package manifest
- **WHEN** a user runs `isomer-cli system-skills list`
- **THEN** the command reports each public pack, its kind, optional extension id, installed-by-default posture, and public commands from the package manifest
- **AND** it reports protected members as parent-owned capabilities rather than separate install choices

#### Scenario: JSON list includes identity layers
- **WHEN** a user runs the list command in JSON mode
- **THEN** each public pack includes its manifest-relative source path and each protected member includes its logical id, nested path, scoped member name, invocation designator, dependencies, and version metadata

#### Scenario: JSON list includes source paths
- **WHEN** a user runs `isomer-cli --print-json system-skills list`
- **THEN** the JSON payload includes groups, extensions, and skills
- **AND** each skill includes its install name and manifest-relative source path

### Requirement: Skill Selection
System-skill installation SHALL resolve user selectors to complete public packs and SHALL NOT independently install protected members into an ordinary host skill root.

#### Scenario: Install defaults to core pack
- **WHEN** install runs without a group, extension, all-extensions, or skill selector
- **THEN** the selection contains only `isomer-op-entrypoint`

#### Scenario: Install selected extension
- **WHEN** install selects extension `deepsci` or `kaoju`
- **THEN** the selection contains the core public pack and the named extension public pack
- **AND** it contains no independently projected protected member

#### Scenario: Install all extensions
- **WHEN** install selects all extensions
- **THEN** the selection contains exactly the core, DeepSci, and Kaoju public packs

#### Scenario: Install explicit public skill
- **WHEN** install selects `--skill isomer-op-entrypoint`, `--skill isomer-ext-deepsci-entrypoint`, or `--skill isomer-ext-kaoju-entrypoint`
- **THEN** the selector resolves to the matching complete public pack and required core pack

#### Scenario: Extension selector advertises packaged ids
- **WHEN** a user inspects help or shell completion for a `system-skills` command with `--extension`
- **THEN** the selector advertises the extension ids from the packaged manifest
- **AND** the selector does not require ids to be hardcoded separately from package metadata

#### Scenario: Legacy protected selector is used
- **WHEN** install selects a known protected logical id or old pipeline id during the compatibility window
- **THEN** the selector resolves to the complete owning public pack
- **AND** output reports that the selector is deprecated and names the canonical public entrypoint

#### Scenario: Unknown selector is rejected
- **WHEN** a selector matches no public pack, extension id, protected logical id, or declared legacy alias
- **THEN** selection fails before filesystem mutation with a deterministic diagnostic

### Requirement: Skill Projection
The installer SHALL project each selected public pack as one top-level copy or symlink and SHALL preserve its protected nested tree.

#### Scenario: Copy projection writes public pack directory
- **WHEN** a selected pack is installed with copy projection
- **THEN** the destination is `<skill-root>/<public-entrypoint>/`
- **AND** the complete protected inventory remains below that destination's `subskills/` directory
- **AND** no protected logical id is created as a sibling top-level directory

#### Scenario: Symlink projection writes public pack link
- **WHEN** a selected pack is installed with symlink projection
- **THEN** `<skill-root>/<public-entrypoint>` is one symlink to the complete packaged pack directory
- **AND** nested protected members resolve through that link

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

#### Scenario: Existing selected pack is preserved without force
- **WHEN** the destination public pack path already exists and force is false
- **THEN** the installer preserves the existing path, reports its path kind, and does not partially update nested members

#### Scenario: Force replaces one owned pack
- **WHEN** force is true and the destination is safe to replace under existing ownership rules
- **THEN** the installer replaces the complete public pack as one projection unit
- **AND** it does not delete unrelated sibling skills or untracked paths

#### Scenario: Force switches copy projection to symlink projection
- **WHEN** `<skill-root>/isomer-op-entrypoint` exists as a real directory
- **AND** a user runs `isomer-cli system-skills install --target generic --scope project --skill isomer-op-entrypoint --mode symlink --force`
- **THEN** the command removes the real directory
- **AND** it creates `<skill-root>/isomer-op-entrypoint` as a symlink to the packaged skill source

#### Scenario: Force switches symlink projection to copy projection
- **WHEN** `<skill-root>/isomer-op-entrypoint` exists as a symlink
- **AND** a user runs `isomer-cli system-skills install --target generic --scope project --skill isomer-op-entrypoint --mode copy --force`
- **THEN** the command unlinks the symlink without deleting the symlink target
- **AND** it creates `<skill-root>/isomer-op-entrypoint` as a real copied directory

### Requirement: Status and Uninstall
Status and uninstall SHALL operate on public pack projections while reporting protected member integrity.

#### Scenario: Status reports pack and member state
- **WHEN** status inspects a selected public pack
- **THEN** it reports the top-level projection mode, receipt ownership, pack version, and aggregate compatibility
- **AND** it reports missing, extra, mismatched, or incompatible protected members from the expected nested inventory

#### Scenario: Missing nested member makes pack incomplete
- **WHEN** a public entrypoint exists but one declared protected member is absent or invalid
- **THEN** status reports the pack as incomplete
- **AND** it does not treat the entrypoint name alone as complete installation evidence

#### Scenario: Status reports installed and missing skills
- **WHEN** a user runs `isomer-cli system-skills status --target generic --scope project`
- **THEN** the output reports the target, project scope, and resolved skill root
- **AND** it reports selected packaged skills as installed when `<skill-root>/<skill-name>` exists
- **AND** it can report missing selected skills when selectors are supplied and `<skill-root>/<skill-name>` does not exist
- **AND** it reports target-root install manifest metadata when `isomer-labs-skill-manifest.json` exists

#### Scenario: Status reports projection path shape
- **WHEN** a selected packaged skill path exists under the explicitly resolved target skill root
- **THEN** status reports the installed skill name, projection path, packaged source path, and detected projection mode when the path is a real directory or symlink
- **AND** status reports a deterministic invalid projection diagnostic when the path exists but is neither a real directory nor a symlink directory projection

#### Scenario: Uninstall removes selected pack
- **WHEN** uninstall is authorized for a receipt-owned public pack
- **THEN** it removes the public pack directory or symlink as one unit and updates the receipt
- **AND** it does not follow a symlink into its target

#### Scenario: Uninstall removes selected named projections
- **WHEN** a user runs `isomer-cli system-skills uninstall --target generic --scope project`
- **THEN** the command removes selected packaged skill paths under the resolved project skill root by packaged skill name
- **AND** it reports removed and absent skills

#### Scenario: Protected selector requests uninstall
- **WHEN** a user supplies a protected logical id to uninstall during the compatibility window
- **THEN** the CLI explains that the owning public pack is the removal unit and requires that pack selection
- **AND** it does not remove one nested member from an installed complete pack

### Requirement: Target Root Skill Manifest
The installer SHALL write a scope-aware v4 target-root receipt whose projection records are public packs and whose nested inventory records protected capability integrity.

#### Scenario: Install writes pack-aware receipt
- **WHEN** install successfully mutates a target root
- **THEN** `isomer-labs-skill-manifest.json` uses schema `isomer-labs-skill-manifest.v4`
- **AND** each projection record contains public skill name, pack id, source path, projection mode, package version, pack version, and the expected protected member inventory
- **AND** each member record contains logical id, relative nested path, invocation designator, and version

#### Scenario: Shared root records scope bindings
- **WHEN** multiple target and scope bindings resolve to one physical root
- **THEN** one v4 receipt retains every compatible binding without duplicating the public pack projection records

#### Scenario: Later mutation merges a compatible binding
- **WHEN** a v3 receipt exists and a later authorized operation reaches the same physical root through another target-scope binding
- **THEN** the writer preserves existing bindings and adds the current binding
- **AND** it does not duplicate per-skill records or discard prior ownership metadata

#### Scenario: Per-skill marker files are not required
- **WHEN** a selected packaged skill is installed as a copied directory or symlink
- **THEN** ownership and upgrade tracking are recorded in `<skill-root>/isomer-labs-skill-manifest.json`
- **AND** the command does not require `.isomer-system-skill.json` inside the skill directory

#### Scenario: Legacy receipt remains readable
- **WHEN** inspection encounters a supported v1, v2, or v3 receipt
- **THEN** it reports the legacy schema and tracked flat paths without inventing pack or nested-member proof

#### Scenario: Legacy receipt remains readable without invented scope
- **WHEN** status reads a supported v1 or v2 receipt
- **THEN** it preserves the receipt as legacy evidence
- **AND** it reports the missing scope or binding metadata as unknown rather than inferring it from the path

#### Scenario: Authorized mutation upgrades receipt
- **WHEN** install or upgrade successfully converts a supported legacy receipt
- **THEN** it writes v4 only after the new public packs validate
- **AND** it retains enough legacy path evidence to perform bounded stale cleanup

#### Scenario: Uninstall updates target root manifest
- **WHEN** `isomer-cli system-skills uninstall` removes one or more selected packaged skill paths
- **THEN** the command updates `<skill-root>/isomer-labs-skill-manifest.json`
- **AND** removed skill names are no longer listed as tracked installed skills

#### Scenario: Status reports unreadable manifest
- **WHEN** `<skill-root>/isomer-labs-skill-manifest.json` exists but cannot be parsed as a supported manifest
- **THEN** status reports a deterministic warning diagnostic
- **AND** status still derives selected skill path existence from the filesystem

### Requirement: System Skill Upgrade
Upgrade SHALL stage and validate selected public packs before removing obsolete receipt-tracked flat projections.

#### Scenario: Upgrade refreshes selected packs
- **WHEN** a v4 installation is upgraded
- **THEN** the installer refreshes each selected public pack as one projection unit
- **AND** it preserves the recorded projection mode unless the user explicitly changes it

#### Scenario: Upgrade refreshes current selected skills
- **WHEN** a user runs `isomer-cli system-skills upgrade --target generic --scope project`
- **THEN** the command resolves the current selected packaged skill set using the same selector rules as install
- **AND** it refreshes each selected skill path from the current package resources
- **AND** it updates `<skill-root>/isomer-labs-skill-manifest.json` with the current Isomer CLI or package version and target-scope binding

#### Scenario: Legacy flat installation is upgraded
- **WHEN** a supported legacy receipt tracks flat skills that now belong to selected public packs
- **THEN** upgrade checks destination conflicts, stages the complete new packs, validates their nested inventories, and writes a v4 receipt
- **AND** only after those steps succeed does it remove obsolete top-level paths tracked by the legacy receipt

#### Scenario: Upgrade removes stale manifest-tracked skills
- **WHEN** the target root manifest lists a previously installed skill name that is not in the current selected packaged skill set
- **AND** `<skill-root>/<old-skill-name>` exists
- **THEN** upgrade removes `<skill-root>/<old-skill-name>`
- **AND** it reports the stale skill path as removed

#### Scenario: Untracked path resembles a legacy skill
- **WHEN** a top-level path has an old protected skill name but is not tracked by the supported receipt
- **THEN** upgrade preserves it and reports that it is untracked

#### Scenario: Upgrade does not remove untracked paths
- **WHEN** a path exists under the target skill root but its name is not tracked in `isomer-labs-skill-manifest.json`
- **THEN** upgrade does not remove that path as a stale installed skill

#### Scenario: New pack validation fails
- **WHEN** staging or recursive validation of a selected public pack fails
- **THEN** upgrade leaves the old projections and receipt intact
- **AND** it reports the failed pack and diagnostic without stale cleanup

#### Scenario: Cleanup is partial
- **WHEN** new packs and the v4 receipt are valid but one receipt-tracked obsolete path cannot be safely removed
- **THEN** upgrade reports a partial migration with the exact retained path and repair guidance
- **AND** it does not broaden deletion to unverified paths

### Requirement: Packaged Extension Discovery Commands
Extension discovery SHALL present public entrypoints, public commands, and protected member metadata from the package catalog.

#### Scenario: Extension list summarizes public packs
- **WHEN** a user runs `isomer-cli system-skills extensions list`
- **THEN** the result identifies extension ids `deepsci` and `kaoju`, their `isomer-ext-*-entrypoint` public skills, descriptions, and availability posture

#### Scenario: Extension list summarizes available extensions
- **WHEN** a user runs `isomer-cli system-skills extensions list`
- **THEN** the output lists each packaged extension id, description, and entry skill in manifest order
- **AND** the output points to extension inspection for complete usage

#### Scenario: Extension show explains invocation
- **WHEN** a user shows DeepSci or Kaoju
- **THEN** output presents `$<entrypoint> use <subcommand> to <task>`, ordered public commands, and protected capability summaries
- **AND** it does not tell users to install protected members independently

#### Scenario: JSON discovery is structured
- **WHEN** extension discovery uses JSON output
- **THEN** the response distinguishes the public pack record from protected logical capability records and includes current invocation designators

#### Scenario: Unknown extension fails safely
- **WHEN** a user shows an unknown extension id
- **THEN** the command fails without filesystem or Project mutation

### Requirement: Installation Receipts Preserve Skill Versions
Installation receipts SHALL preserve version evidence for each public pack and every protected member.

#### Scenario: Install writes pack and member versions
- **WHEN** a selected public pack is installed
- **THEN** the v4 receipt records the pack entrypoint version and each manifest-declared protected member version

#### Scenario: Receipt and nested metadata disagree
- **WHEN** a projected member's `agents/openai.yaml` version differs from its v4 receipt record
- **THEN** status reports receipt drift for that member and does not classify the pack as verified

#### Scenario: Legacy receipt is inspected
- **WHEN** a legacy receipt lacks nested member versions
- **THEN** status reports legacy or unverified member-version evidence rather than inventing values
