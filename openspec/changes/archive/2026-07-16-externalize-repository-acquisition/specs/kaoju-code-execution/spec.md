## ADDED Requirements

### Requirement: Source Repositories Use External Commands and Canonical Registration
The system SHALL let the acting user or agent acquire selected source code with prompt-sensitive external commands and SHALL register the verified result as a Canonical External Repository only afterward.

#### Scenario: User specifies repository commands
- **WHEN** the user supplies a clone, fetch, checkout, sparse, partial, submodule, LFS, local-copy, provider-CLI, credential-wrapper, or other repository procedure
- **THEN** the acting agent preserves that procedure within the applicable authorization and runs it outside `isomer-cli`
- **AND** it does not replace the procedure with a depth-one clone or an Isomer-owned command request

#### Scenario: Agent selects repository commands
- **WHEN** an accepted source identity is accessible and the user has not specified exact commands
- **THEN** the acquire skill selects commands that fit the source, desired revision, repository features, credentials, resource limits, and approved inspection needs
- **AND** it records why that method was selected without treating one Git sequence as the platform default

#### Scenario: Repository identity is verified and registered
- **WHEN** the external commands succeed at the intended target
- **THEN** the acquire and examine skills verify the resolved source locator, immutable commit or digest, target path, and relationship evidence through external checks
- **AND** they invoke `project repos register` for a new semantic binding and record the resulting semantic label and verified identity in `KAOJU:ASSOCIATED-SOURCE-CODE` and `KAOJU:ARTIFACT-LIBRARY`

#### Scenario: History or repository features are required
- **WHEN** identity resolution or approved inspection requires history, submodules, LFS objects, a sparse path set, a provider-specific checkout, or another repository feature
- **THEN** the acting agent runs the necessary external commands and records their rationale and resulting source posture
- **AND** no Isomer API chooses, limits, deepens, or repairs that repository state

#### Scenario: Repository may have an associated paper
- **WHEN** the actor supplies or selects a repository for ingestion
- **THEN** the acquire skill performs bounded associated-paper metadata discovery and records candidate relationships with their basis
- **AND** it does not grant a candidate paper evidentiary authority or ingest it in depth until the relationship is verified and the normal selection and approval path accepts it

#### Scenario: Acquisition or verification fails
- **WHEN** an external command fails, leaves partial content, or produces an ambiguous or unexpected identity
- **THEN** the acquire skill records `KAOJU:SOURCE-ACCESS-BLOCKER` with sanitized attempts, impact, filesystem posture, and resume condition
- **AND** it neither registers a successful Canonical External Repository nor asks Isomer to clean up or rewrite the external result

## MODIFIED Requirements

### Requirement: Source-Code References Are Resolved Before Acquisition
The system SHALL resolve a supplied repository URL, repository name, paper ref, or reading-item ref to an unambiguous Source Identity before executing external repository commands or registering associated source code.

#### Scenario: Actor supplies a repository URL
- **WHEN** the actor requests ingestion for an accessible repository URL
- **THEN** the system verifies the requested source identity, records the requested and resolved locators, and lets the acting agent select and execute the applicable external acquisition commands

#### Scenario: Actor supplies a name or paper reference
- **WHEN** the actor supplies a repository name, project name, paper ref, or reading-item ref without a verified URL
- **THEN** the system performs bounded repository discovery and presents or selects only candidates whose relationship evidence is recorded
- **AND** ambiguous or unverified candidates require clarification or produce a blocker before external acquisition or semantic registration

#### Scenario: Repository cannot be accessed
- **WHEN** the resolved repository is missing, private without authorization, or inaccessible after bounded attempts
- **THEN** the system records `KAOJU:SOURCE-ACCESS-BLOCKER` with sanitized attempts, impact, and resume condition
- **AND** it does not register a nonexistent or unverified checkout

### Requirement: Environment Preparation Has a Durable Plan
The system SHALL create `KAOJU:ENV-PREP-PLAN` before mutating or selecting a code-run environment.

#### Scenario: Preparation is planned
- **WHEN** the actor requests `prepare-code-run` for registered source
- **THEN** the plan records source and commit refs, dependency evidence, task-critical code path, candidate Pixi environments, compatibility risks, intended smoke check, required authorization, and expected outputs
- **AND** source-code ingestion through external acquisition, verification, semantic registration, and Artifact recording is routed first when no verified repository ref exists

#### Scenario: Dependency evidence is insufficient
- **WHEN** the repository does not establish enough dependency or entry-point information for a bounded setup
- **THEN** the plan records the missing evidence and returns a blocker or clarification request
- **AND** the system does not install speculative packages without rationale

### Requirement: Code Trials Require Acquired Source and Prepared Environment
The system SHALL start UC-10 only with a verified registered source ref and accepted environment-preparation result.

#### Scenario: Trial prerequisites are ready
- **WHEN** `run-code-trial` resolves the registered repository semantic label, immutable commit or digest, accepted Pixi environment, and smoke result
- **THEN** it pins those exact refs as trial inputs

#### Scenario: Source or environment is missing
- **WHEN** a required source or environment ref is missing, stale, failed, or ambiguous
- **THEN** the procedure routes to the applicable source-code ingestion or preparation use case or reports a blocker
- **AND** it does not execute the trial in an ambient environment

## REMOVED Requirements

### Requirement: Source Repositories Use Canonical Acquisition
**Reason**: A canonical Isomer acquisition service forces one Git workflow and makes the CLI own commands that must remain sensitive to user intent and repository-specific requirements.

**Migration**: Use the acting agent's external command surface for acquisition and verification, then use `project repos register` and typed Kaoju Artifact operations for canonical topology and provenance. No repository-acquisition service or extension-point compatibility path remains.
