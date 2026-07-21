## MODIFIED Requirements

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
