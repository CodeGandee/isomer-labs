# system-skill-installer-cli Specification

## Purpose
TBD - created by archiving change add-system-skill-installer-cli. Update Purpose after archive.
## Requirements
### Requirement: System Skill CLI Surface
The system SHALL expose a top-level `isomer-cli system-skills` command group for packaged Isomer system-skill discovery, installation, upgrade, and inspection.

#### Scenario: Help lists system-skills command group
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help lists `system-skills`

#### Scenario: System skill group lists supported subcommands
- **WHEN** a user runs `isomer-cli system-skills --help`
- **THEN** the command help lists `extensions`, `list`, `status`, `install`, `upgrade`, and `uninstall`

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
### Requirement: System Skill Operations Report Resolved Scope
The system SHALL report the effective installation scope and resolved target bindings for every target-resolving system-skill operation, including an install whose scope came from the Project default.

#### Scenario: Concrete target reports scope
- **WHEN** a user runs `isomer-cli --print-json system-skills status --target kimi-code --scope user`
- **THEN** the result reports `user` as the selected scope
- **AND** it reports the normalized Kimi Code user skill root and the `kimi-code/user` binding

#### Scenario: Shared physical root reports all bindings
- **WHEN** `--target all --scope project` resolves both `codex` and `generic` to the same normalized physical skill root
- **THEN** JSON and human output report one physical-root result for that root
- **AND** the result includes both `codex/project` and `generic/project` bindings

#### Scenario: Omitted install scope reports effective Project scope
- **WHEN** a user runs `isomer-cli --print-json system-skills install --target generic` without `--scope`
- **THEN** the result reports `project` as the effective scope
- **AND** it reports the same normalized skill root, `generic/project` binding, diagnostics, and receipt metadata as an explicit `--scope project` install from the same current working directory

### Requirement: Target Resolution
The system SHALL require a target for every target-resolving system-skill command, SHALL default omitted scope to `project` for `system-skills install` only, SHALL require an explicit `user` or `project` scope for `status`, `upgrade`, and `uninstall`, and SHALL resolve each supported target and effective scope to a deterministic skill root.

#### Scenario: Scope is required
- **WHEN** a user runs a target-resolving `system-skills` command without `--scope`
- **THEN** the command reports a missing required option
- **AND** it does not mutate any skill root

#### Scenario: Home override is removed
- **WHEN** a user supplies `--home` to a target-resolving `system-skills` command
- **THEN** the command rejects the unknown option
- **AND** it does not mutate any skill root

#### Scenario: Claude Code project scope uses current working directory
- **WHEN** a user supplies `--target claude-code --scope project`
- **THEN** the target skill root is `<cwd>/.claude/skills`

#### Scenario: Claude Code user scope honors configuration home
- **WHEN** a user supplies `--target claude-code --scope user` and `CLAUDE_CONFIG_DIR` is set and non-empty
- **THEN** the target skill root is `$CLAUDE_CONFIG_DIR/skills`

#### Scenario: Claude Code user scope falls back to user home
- **WHEN** a user supplies `--target claude-code --scope user` and `CLAUDE_CONFIG_DIR` is unset or empty
- **THEN** the target skill root is `~/.claude/skills`

#### Scenario: Codex project scope uses shared project skills
- **WHEN** a user supplies `--target codex --scope project`
- **THEN** the target skill root is `<cwd>/.agents/skills`

#### Scenario: Codex user scope honors Codex home
- **WHEN** a user supplies `--target codex --scope user` and `CODEX_HOME` is set and non-empty
- **THEN** the target skill root is `$CODEX_HOME/skills`

#### Scenario: Codex user scope preserves the Isomer personal fallback
- **WHEN** a user supplies `--target codex --scope user` and `CODEX_HOME` is unset or empty
- **THEN** the target skill root is `~/.codex/skills`

#### Scenario: Kimi Code project scope uses current working directory
- **WHEN** a user supplies `--target kimi-code --scope project`
- **THEN** the target skill root is `<cwd>/.kimi-code/skills`

#### Scenario: Kimi Code user scope honors Kimi Code home
- **WHEN** a user supplies `--target kimi-code --scope user` and `KIMI_CODE_HOME` is set and non-empty
- **THEN** the target skill root is `$KIMI_CODE_HOME/skills`

#### Scenario: Kimi Code user scope falls back to user home
- **WHEN** a user supplies `--target kimi-code --scope user` and `KIMI_CODE_HOME` is unset or empty
- **THEN** the target skill root is `~/.kimi-code/skills`

#### Scenario: Generic project scope uses shared project skills
- **WHEN** a user supplies `--target generic --scope project`
- **THEN** the target skill root is `<cwd>/.agents/skills`

#### Scenario: Generic user scope uses shared personal skills
- **WHEN** a user supplies `--target generic --scope user`
- **THEN** the target skill root is `~/.agents/skills`

#### Scenario: Project scope is anchored exactly at the current working directory
- **WHEN** the current working directory is nested below a Git root or initialized Isomer Project and the user selects Project scope explicitly or through the install default
- **THEN** the resolver uses that current working directory as `<cwd>`
- **AND** it does not search parent directories for Git or Isomer metadata

#### Scenario: All target deduplicates shared physical roots
- **WHEN** a user supplies `--target all --scope project` or installs with `--target all` and omits scope
- **THEN** the command expands `claude-code`, `codex`, `kimi-code`, and `generic`
- **AND** it groups bindings with the same normalized absolute skill root before any filesystem operation
- **AND** it operates on each physical skill root exactly once

#### Scenario: Install scope defaults to Project
- **WHEN** a user runs `isomer-cli system-skills install --target generic` without `--scope`
- **THEN** the command behaves as if `--scope project` were supplied
- **AND** it resolves the target from the exact current working directory
- **AND** it does not inspect or mutate the generic user skill root

#### Scenario: Non-install scope is required
- **WHEN** a user runs `system-skills status`, `system-skills upgrade`, or `system-skills uninstall` with a target but without `--scope`
- **THEN** the command reports a missing required option
- **AND** it does not mutate any skill root

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
### Requirement: Documentation
The system SHALL document released-package system skill installation through a required target, a Project-scope default when install scope is omitted, and an explicit scope for user-wide installation and all status, upgrade, and uninstall operations.

#### Scenario: README describes scoped CLI skill installation
- **WHEN** the README is inspected
- **THEN** it recommends installing Isomer system skills through `isomer-cli system-skills install`
- **AND** it names the supported targets and the `user` and `project` scopes

#### Scenario: Manual CLI reference lists scoped system-skills commands
- **WHEN** the CLI reference is inspected
- **THEN** it documents `system-skills list`, `system-skills status`, `system-skills install`, `system-skills upgrade`, and `system-skills uninstall`
- **AND** its target matrix and examples use required scope syntax and contain no `--home` option

#### Scenario: Migration guidance explains the breaking syntax
- **WHEN** a caller migrates from the prior CLI contract
- **THEN** documentation explains how to replace an implicit default or `--home` invocation with the corresponding target and scope
- **AND** it states that arbitrary public install roots are no longer supported

#### Scenario: README describes install scope default
- **WHEN** the README is inspected
- **THEN** it recommends installing Isomer system skills through `isomer-cli system-skills install`
- **AND** it states that an omitted install scope selects `project` at the exact current working directory
- **AND** it names the supported targets and the explicit `user` and `project` scopes

#### Scenario: Manual CLI reference distinguishes install from other operations
- **WHEN** the CLI reference is inspected
- **THEN** it documents `system-skills list`, `system-skills status`, `system-skills install`, `system-skills upgrade`, and `system-skills uninstall`
- **AND** its Project-install examples demonstrate the omitted-scope default or an explicit equivalent
- **AND** its user install, status, upgrade, and uninstall examples retain explicit scope
- **AND** its active command examples contain no `--home` option

#### Scenario: Migration guidance explains the relaxed install syntax
- **WHEN** a caller migrates from the prior CLI contract
- **THEN** documentation explains that an install without `--scope` now selects Project scope while explicit `--scope project` remains equivalent
- **AND** it states that user-wide install still requires `--scope user`
- **AND** it states that status, upgrade, and uninstall remain scope-explicit and arbitrary public install roots remain unsupported

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

#### Scenario: Upgrade refreshes selected packs
- **WHEN** a v4 installation is upgraded
- **THEN** the installer refreshes each selected public pack as one projection unit
- **AND** it preserves the recorded projection mode unless the user explicitly changes it

#### Scenario: Upgrade refreshes current selected skills
- **WHEN** a user runs `isomer-cli system-skills upgrade --target generic --scope project`
- **THEN** the command resolves the current selected packaged skill set using the same selector rules as install
- **AND** it refreshes each selected skill path from the current package resources
- **AND** it updates `<skill-root>/isomer-labs-skill-manifest.json` with the current Isomer CLI or package version and target-scope binding

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
### Requirement: CLI Extension Namespaces Are Distinguishable
The CLI SHALL distinguish native runtime or compatibility command surfaces from installable agent-skill extensions.

#### Scenario: Runtime extension help points to system-skill discovery
- **WHEN** a user runs `isomer-cli ext --help`
- **THEN** the help describes `ext` as runtime and compatibility command surfaces
- **AND** it points to `isomer-cli system-skills extensions` for installable agent-skill extensions

#### Scenario: Kaoju remains agent-skill driven
- **WHEN** a user inspects the Kaoju extension
- **THEN** the CLI directs the user to install and invoke `$isomer-kaoju-pipeline`
- **AND** the CLI does not claim that `isomer-cli ext kaoju` exists\n

### Requirement: Packaged Skills Carry Release-Aligned Versions
Every packaged Isomer system skill SHALL declare `metadata.version` in `agents/openai.yaml` using the exact PEP 440 Isomer CLI/package version that ships the skill, including release candidate versions.

#### Scenario: Packaged source version matches the CLI release
- **WHEN** packaged system-skill assets are validated for a release
- **THEN** every skill's `agents/openai.yaml` contains a valid PEP 440 `metadata.version`
- **AND** the version equals the Isomer CLI/package version
- **AND** `SKILL.md` frontmatter does not duplicate the skill version

#### Scenario: Release candidate version is accepted
- **WHEN** the Isomer CLI/package version is a valid release candidate such as `0.3.0rc1`
- **THEN** packaged skills declare that exact release candidate version
- **AND** validation uses PEP 440 ordering rather than ad hoc string comparison

### Requirement: Package Catalog Defines Skill Compatibility Floors
The package-owned system-skill catalog SHALL define a minimum compatible skill version for each system-skill group and SHALL allow a per-skill override for a skill that requires a newer floor.

#### Scenario: Group compatibility floor applies by default
- **WHEN** a packaged skill has no per-skill compatibility override
- **THEN** compatibility evaluation uses its group's minimum compatible skill version

#### Scenario: Per-skill compatibility floor overrides the group
- **WHEN** packaged skill metadata declares a minimum compatible version newer than its group default
- **THEN** compatibility evaluation uses the per-skill minimum

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

#### Scenario: Install writes pack and member versions
- **WHEN** a selected public pack is installed
- **THEN** the v4 receipt records the pack entrypoint version and each manifest-declared protected member version

#### Scenario: Receipt and nested metadata disagree
- **WHEN** a projected member's `agents/openai.yaml` version differs from its v4 receipt record
- **THEN** status reports receipt drift for that member and does not classify the pack as verified

#### Scenario: Legacy receipt is inspected
- **WHEN** a legacy receipt lacks nested member versions
- **THEN** status reports legacy or unverified member-version evidence rather than inventing values
### Requirement: Status Classifies Skill Version Compatibility
System-skill status SHALL compare installed skill versions with the current CLI version and package-owned minimum compatibility floors using PEP 440 semantics.

#### Scenario: Compatible older skill is usable
- **WHEN** an installed skill version is at least its minimum compatible version and lower than the current CLI version
- **THEN** status reports `compatible_older`
- **AND** it may advise upgrade without classifying the skill as incompatible

#### Scenario: Obsolete skill is incompatible
- **WHEN** an installed skill version is lower than its minimum compatible version
- **THEN** status reports `obsolete_incompatible`
- **AND** it advises upgrading the target's system skills

#### Scenario: Newer skill has unknown compatibility
- **WHEN** an installed skill version is newer than the current CLI version
- **THEN** status reports `newer_than_cli`
- **AND** it advises upgrading the CLI instead of claiming compatibility

#### Scenario: Missing or malformed version is not verified
- **WHEN** projected `agents/openai.yaml` lacks `metadata.version` or contains an invalid PEP 440 version
- **THEN** status reports `unversioned` or `malformed_version`
- **AND** it does not claim compatibility

