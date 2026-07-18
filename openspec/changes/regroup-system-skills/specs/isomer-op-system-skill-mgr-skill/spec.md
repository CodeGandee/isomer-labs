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

#### Scenario: Supported v4 receipt exists
- **WHEN** explicit-root inspection reports a current receipt and complete nested pack coverage
- **THEN** the manager treats it as verified managed installation evidence

#### Scenario: Public entrypoint appears only in live inventory
- **WHEN** live inventory names an extension entrypoint without receipt or root evidence
- **THEN** the manager reports `entrypoint_seen` and unverified protected integrity
- **AND** it does not automatically remember the extension as complete

#### Scenario: Legacy flat names appear
- **WHEN** receipt or live inventory shows old top-level protected names
- **THEN** the manager reports a migration candidate and recommends managed upgrade to the owning public pack

### Requirement: Operator-Managed Extension Installation Converges
The protected manager SHALL converge authorized extension setup on the canonical public pack and Project declaration without independently installing protected members.

#### Scenario: Extension is absent
- **WHEN** the user authorizes installation of `deepsci` or `kaoju`
- **THEN** the manager installs core plus the selected `isomer-ext-*-entrypoint` pack at explicit target and scope
- **AND** it verifies the v4 receipt and nested member inventory before remembering the Project declaration

#### Scenario: Legacy flat extension is present
- **WHEN** a supported receipt tracks a flat installation for the requested extension
- **THEN** the manager uses managed upgrade and reports stale-path cleanup
- **AND** it does not delete untracked skill directories

#### Scenario: Host refresh is pending
- **WHEN** a pack install or upgrade succeeds
- **THEN** the manager reports that the current agent session may cache old discovery
- **AND** it directs the user to refresh the host or start a new session before claiming live usability
