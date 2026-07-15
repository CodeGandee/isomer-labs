## ADDED Requirements

### Requirement: Packaged System Skills Externalize Repository Acquisition
Every packaged system skill that obtains or updates a source repository SHALL keep repository command selection and execution outside Isomer APIs and SHALL use Isomer only for semantic target planning, post-verification registration, topology, policy, and durable records.

#### Scenario: Skill receives a user-supplied repository procedure
- **WHEN** a user names custom `git`, provider-CLI, local-copy, wrapper, authentication, checkout, sparse, partial, submodule, LFS, or history commands
- **THEN** the applicable skill preserves those commands within the user request and applicable Gate instead of replacing them with an Isomer acquisition command
- **AND** it registers the verified existing repository only after those commands succeed

#### Scenario: Skill chooses repository commands
- **WHEN** a repository is required and the user has not specified exact commands
- **THEN** the skill instructs the acting agent to choose commands suited to the source and task through its ordinary external command surface
- **AND** it does not invoke `project repos acquire`, a `repository_acquisition` extension point, or another Isomer API that executes source-control commands

#### Scenario: Skill records successful acquisition
- **WHEN** external acquisition and identity verification succeed
- **THEN** the skill uses the applicable non-executing semantic registration command and durable-record operations
- **AND** it distinguishes the Topic Workspace Manifest path binding from source identity, command evidence, access, license, relationship, and limitation provenance

#### Scenario: Skill encounters failed acquisition
- **WHEN** repository acquisition, identity verification, or post-acquisition registration fails
- **THEN** the skill reports a blocker or resumable checkpoint with sanitized evidence and the safe next action
- **AND** it does not claim a successful binding or ask Isomer to delete, move, reset, or repair the partial checkout

### Requirement: Packaged Skill Validation Enforces the Repository Boundary
System-skill validation SHALL reject active guidance that assigns repository acquisition commands to Isomer APIs or registers a new repository before external verification.

#### Scenario: Obsolete acquisition API appears in active guidance
- **WHEN** a packaged or source-mirrored system skill names `project repos acquire`, `repository_acquisition`, the removed Kaoju repository service, or an equivalent Isomer-owned Git execution route as active procedure
- **THEN** validation reports the skill, file, line when available, and violated external-acquisition boundary

#### Scenario: Acquire-then-register guidance is valid
- **WHEN** a skill uses a read-only semantic target query, authorized external repository commands, external identity verification, `project repos register`, and typed durable-record operations in that order
- **THEN** repository-boundary validation accepts the guidance
- **AND** family-specific validators continue to enforce their other owner, Gate, evidence, and command rules

#### Scenario: Registration precedes verification
- **WHEN** active skill guidance creates a successful non-main repository binding before external acquisition and identity verification complete
- **THEN** validation reports the ordering violation
- **AND** it directs the skill author to use a read-only default-path query before acquisition and semantic registration afterward
