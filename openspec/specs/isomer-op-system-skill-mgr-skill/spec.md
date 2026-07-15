# isomer-op-system-skill-mgr-skill Specification

## Purpose
TBD - created by archiving change agent-guided-system-extension-reconciliation. Update Purpose after archive.

## Requirements

### Requirement: System Skill Manager Bundle
The repository SHALL provide a core operator skill named `isomer-op-system-skill-mgr` that owns working-agent system-skill detection, reconciliation, installation, status, and repair.

#### Scenario: Skill bundle is complete
- **WHEN** the packaged operator skillset is inspected
- **THEN** it contains `operator/isomer-op-system-skill-mgr/SKILL.md`, `agents/openai.yaml`, and directly linked local references needed to execute its workflow
- **AND** its frontmatter and interface metadata use the same skill name

#### Scenario: Owner subcommands are available
- **WHEN** the skill's help or local command index is inspected
- **THEN** it exposes `detect-extensions`, `reconcile-extensions`, `install-extension`, `status`, and `repair` subcommands
- **AND** each subcommand preserves read-only or mutation posture explicitly

### Requirement: System Skill Manager Uses Ordered Extension Evidence
The system-skill manager SHALL resolve optional extensions from Project declaration, explicit project-root receipt, and live inventory evidence in that order.

#### Scenario: Project declaration wins
- **WHEN** the Project Manifest declares an extension
- **THEN** the manager trusts that declaration and does not require receipt or inventory confirmation before routing
- **AND** it reports later load or execution failure as stale user-controlled state rather than silently removing the declaration

#### Scenario: Receipt-backed fallback uses host-known roots
- **WHEN** an undeclared extension may exist in a project-scope root known to the working agent
- **THEN** the manager passes that explicit root to `internals inspect-system-skill-root`
- **AND** it does not teach or guess provider-specific root names, receipt filenames, or receipt schemas

#### Scenario: Live inventory covers ambient installations
- **WHEN** no declaration or complete managed project receipt establishes the extension
- **THEN** the manager passes the host-visible inventory to `internals classify-system-skill-inventory`
- **AND** complete inventory evidence can represent user-home, plugin, environment-owned, or other host-discovered installations

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
The system-skill manager SHALL combine a user-authorized extension installation through an explicit target and scope with verification, Project registration, and activation guidance.

#### Scenario: Successful scoped installation is registered
- **WHEN** `install-extension <extension-id>` installs a complete family with `system-skills install --target <host-known-target> --scope <selected-scope> --extension <extension-id>`
- **THEN** the manager reads the resolved skill root from the installation result and verifies it with safe explicit-root CLI primitives
- **AND** it remembers the extension in the selected Project unless the user opted out

#### Scenario: Registration failure is partial
- **WHEN** scoped installation succeeds but Project registration fails
- **THEN** the manager reports a non-success partial outcome that distinguishes installed files from missing registration
- **AND** a retry can complete registration without reinstalling the extension

#### Scenario: New installation may require host refresh
- **WHEN** scoped installation succeeds but the extension is not observable in a refreshed live inventory
- **THEN** the manager reports `host_refresh_required`
- **AND** it advises a new turn, thread, or host-native refresh without claiming current-session availability

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
