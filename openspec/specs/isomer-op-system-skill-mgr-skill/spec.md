# isomer-op-system-skill-mgr-skill Specification

## Purpose
TBD - created by archiving change agent-guided-system-extension-reconciliation. Update Purpose after archive.
## Requirements
### Requirement: System Skill Manager Bundle
The core public pack SHALL preserve protected logical capability `isomer-op-system-skill-mgr` as member `system-skills` for working-agent pack detection, reconciliation, installation, status, upgrade, and repair.

#### Scenario: Protected bundle is complete
- **WHEN** the core pack is inspected
- **THEN** it contains `operator/isomer-op-entrypoint/subskills/isomer-op-system-skill-mgr/SKILL.md`, `agents/openai.yaml`, and all directly linked local resources
- **AND** its folder and frontmatter retain logical id `isomer-op-system-skill-mgr`

#### Scenario: Owner subcommands are available
- **WHEN** protected manager help is inspected
- **THEN** it exposes `detect-extensions`, `reconcile-extensions`, `install-extension`, `status`, `upgrade`, and `repair`
- **AND** each routine states its read-only or mutation posture

#### Scenario: Public entrypoint routes management
- **WHEN** a user asks to manage system skills
- **THEN** `$isomer-op-entrypoint use system-skills to <task>` invokes `isomer-op-entrypoint->system-skills`

### Requirement: System Skill Manager Uses Ordered Extension Evidence
The protected manager SHALL reason about Project declarations, v4 pack receipts, explicit-root verification, and limited live-inventory observations in a deterministic order.

#### Scenario: Project declaration exists
- **WHEN** the selected Project declares an extension
- **THEN** the manager treats the declaration as authoritative Project routing state
- **AND** separately verifies current-host pack usability when the task requires execution

#### Scenario: Project declaration wins
- **WHEN** the Project Manifest declares an extension
- **THEN** the manager trusts that declaration and does not require receipt or inventory confirmation before routing
- **AND** it reports later load or execution failure as stale user-controlled state rather than silently removing the declaration

#### Scenario: Supported v4 receipt exists
- **WHEN** explicit-root inspection reports a current receipt and complete nested pack coverage
- **THEN** the manager treats it as verified managed installation evidence

#### Scenario: Receipt-backed fallback uses host-known roots
- **WHEN** an undeclared extension may exist in a project-scope root known to the working agent
- **THEN** the manager passes that explicit root to `internals inspect-system-skill-root`
- **AND** it does not teach or guess provider-specific root names, receipt filenames, or receipt schemas

#### Scenario: Public entrypoint appears only in live inventory
- **WHEN** live inventory names an extension entrypoint without receipt or root evidence
- **THEN** the manager reports `entrypoint_seen` and unverified protected integrity
- **AND** it does not automatically remember the extension as complete

#### Scenario: Live inventory covers ambient installations
- **WHEN** no declaration or complete managed project receipt establishes the extension
- **THEN** the manager passes the host-visible inventory to `internals classify-system-skill-inventory`
- **AND** complete inventory evidence can represent user-home, plugin, environment-owned, or other host-discovered installations

#### Scenario: Legacy flat names appear
- **WHEN** receipt or live inventory shows old top-level protected names
- **THEN** the manager reports a migration candidate and recommends managed upgrade to the owning public pack

#### Scenario: No evidence reports unknown
- **WHEN** all three evidence levels fail to establish an extension
- **THEN** the manager reports the extension as unknown or missing and offers its installation subcommand

### Requirement: System Skill Reconciliation Is Additive
The system-skill manager SHALL register complete receipt-backed or live-inventory extensions during authorized operator mutation workflows unless the user opts out.

#### Scenario: Reconciliation remembers complete extension
- **WHEN** `reconcile-extensions` finds a complete extension that the Project does not declare
- **THEN** it runs the idempotent Project extension registration primitive
- **AND** it reports the extension id and evidence basis used for registration

#### Scenario: Detection-only request does not mutate
- **WHEN** the user requests detection, status, help, or explicitly opts out of registration
- **THEN** the manager does not call Project extension registration
- **AND** it reports registration advice separately

#### Scenario: Missing current inventory never forgets declaration
- **WHEN** a declared extension is absent from the current agent's roots or live inventory
- **THEN** reconciliation preserves the declaration
- **AND** it does not infer that other operator environments lack the extension

### Requirement: System Skill Manager Selects Installation Scope Explicitly
The system-skill manager SHALL select a concrete host target and either `project` or `user` scope before invoking system-skill installation.

#### Scenario: Project Operator installation defaults to project scope
- **WHEN** a user authorizes extension installation from a Project Operator Session without requesting user-wide availability
- **THEN** the manager selects `project` scope anchored to the current working directory
- **AND** it states that the installation applies to the current agent-host project context

#### Scenario: User-wide installation requires explicit intent
- **WHEN** installation would use `user` scope
- **THEN** the manager requires an explicit user request or confirmation for user-wide installation
- **AND** it states that the installed skills can affect the selected host across Projects

#### Scenario: Unknown host target blocks installation
- **WHEN** the manager cannot identify a supported concrete target for the current host
- **THEN** it reports a blocker instead of guessing a target or arbitrary skill root
- **AND** it preserves Project declarations and existing skill projections

### Requirement: Operator-Managed Extension Installation Converges
The protected manager SHALL converge authorized extension setup on the canonical public pack and Project declaration without independently installing protected members.

#### Scenario: Extension is absent
- **WHEN** the user authorizes installation of `deepsci` or `kaoju`
- **THEN** the manager installs core plus the selected `isomer-ext-*-entrypoint` pack at explicit target and scope
- **AND** it verifies the v4 receipt and nested member inventory before remembering the Project declaration

#### Scenario: Successful scoped installation is registered
- **WHEN** `install-extension <extension-id>` installs a complete family with `system-skills install --target <host-known-target> --scope <selected-scope> --extension <extension-id>`
- **THEN** the manager reads the resolved skill root from the installation result and verifies it with safe explicit-root CLI primitives
- **AND** it remembers the extension in the selected Project unless the user opted out

#### Scenario: Registration failure is partial
- **WHEN** scoped installation succeeds but Project registration fails
- **THEN** the manager reports a non-success partial outcome that distinguishes installed files from missing registration
- **AND** a retry can complete registration without reinstalling the extension

#### Scenario: Legacy flat extension is present
- **WHEN** a supported receipt tracks a flat installation for the requested extension
- **THEN** the manager uses managed upgrade and reports stale-path cleanup
- **AND** it does not delete untracked skill directories

#### Scenario: Host refresh is pending
- **WHEN** a pack install or upgrade succeeds
- **THEN** the manager reports that the current agent session may cache old discovery
- **AND** it directs the user to refresh the host or start a new session before claiming live usability

#### Scenario: Custom destination request is not translated to home override
- **WHEN** a user requests installation into an arbitrary plugin, extra, or custom skill directory
- **THEN** the manager explains that the scoped installer supports only target-defined `user` and `project` roots
- **AND** it does not reconstruct the removed `--home` behavior through path guessing

### Requirement: System Skill Manager Validation
Repository validation SHALL enforce the system-skill manager's owner boundary and required workflow material.

#### Scenario: Validator accepts complete manager
- **WHEN** operator and packaged-skill validation run against a complete system-skill manager bundle
- **THEN** validation accepts its frontmatter, interface metadata, local references, subcommands, trust order, mutation rules, and global `isomer-cli` guidance

#### Scenario: Validator rejects provider path hard-coding
- **WHEN** manager workflow text treats one provider-specific project or user-home path as universal discovery authority
- **THEN** validation reports a missing provider-neutral explicit-root or live-inventory boundary

