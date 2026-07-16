# kaoju-code-execution Specification

## Purpose
TBD - created by syncing change revise-kaoju-survey-process. Update Purpose after archive.

## Requirements

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

### Requirement: Repository Inspection Produces Source-Grounded Evidence
The system SHALL inspect acquired repositories locally and SHALL ground code-level findings in immutable source locations.

#### Scenario: Code behavior is described
- **WHEN** the examine skill records an implementation statement
- **THEN** the source digest cites repository ref, immutable commit, file path, line range, and inspection time
- **AND** it distinguishes direct code observation from documentation statements, paper claims, inferred behavior, and executed results

#### Scenario: Repository contains relevant dependencies or entry points
- **WHEN** inspection finds installation metadata, environment files, scripts, tests, examples, model or data download helpers, or task-critical entry points
- **THEN** the source digest records their locations and relevance for later environment planning
- **AND** inspection alone does not execute project code or mutate the topic environment

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

### Requirement: Environment Mutation Uses a Service Request
The system SHALL perform environment preparation through a recorded Service Request scoped to the active Research Task and Run.

#### Scenario: Service Request is dispatched
- **WHEN** the environment plan is ready and applicable authorization is present
- **THEN** the Project Operator Session or Operator Agent creates and dispatches a Service Request with the plan ref, target environment scope, expected artifacts, Gate refs, and completion observations
- **AND** the Kaoju skill consumes returned refs rather than invoking Pixi mutation directly

#### Scenario: No dedicated service agent is active
- **WHEN** the Project Operator Session must perform bounded Topic Service Master duties directly
- **THEN** the same Service Request, execution request, provenance, output, and completion contracts remain in force
- **AND** provider or Houmao details do not enter Kaoju artifacts

### Requirement: Pixi Environment Strategy Preserves Existing Environments
The environment service SHALL apply the accepted Pixi preference order and SHALL record both flexible intent constraints and exact derived resolution.

#### Scenario: Existing environment already satisfies requirements
- **WHEN** a registered Pixi environment passes dependency and task-critical preflight
- **THEN** the service reuses it without package mutation
- **AND** `kaoju:pixi-env-ref` records the environment, lock identity, exact resolved versions, and verification evidence

#### Scenario: Existing environment can accept packages safely
- **WHEN** no current environment satisfies requirements but an existing environment can accept compatible additions without breaking its declared consumers
- **THEN** the service prefers the `default` environment, adds `"*"` or compatible flexible constraints, resolves and locks the environment, and records before and after state
- **AND** exact resolved versions remain available in the derived environment ref

#### Scenario: Existing environments would be broken
- **WHEN** compatible additions would violate an existing environment's accepted constraints or consumers
- **THEN** the service creates a dedicated Pixi environment and records its purpose and binding
- **AND** it does not force incompatible packages into `default`

#### Scenario: Dependencies are unsatisfiable
- **WHEN** Pixi cannot resolve an authorized strategy after bounded attempts
- **THEN** the service records the solver evidence, attempted strategies, environment state, and blocker
- **AND** it does not report the code-run environment as prepared

### Requirement: Environment Preparation Includes a Smoke Run
The environment service SHALL create and execute a minimal smoke-run script that exercises the task-critical code path without performing the full UC-10 trial.

#### Scenario: Smoke run succeeds
- **WHEN** environment resolution completes
- **THEN** the service registers `kaoju:smoke-run-script`, dispatches it through command execution, and records `kaoju:smoke-run-result`
- **AND** it creates `kaoju:env-gate-revision` and an accepted `kaoju:pixi-env-ref` tied to the successful observation

#### Scenario: Smoke script becomes durable
- **WHEN** the service creates the smoke-run script
- **THEN** it registers the script as a file-backed Artifact under a resolved owner-preserved `topic.records.*` surface
- **AND** it does not treat a source-tree or Local Tmp Surface copy as canonical, although the Run may execute a disposable staged copy

#### Scenario: Smoke run fails
- **WHEN** import, initialization, minimal inference, compilation, or another task-critical smoke step fails
- **THEN** the result records command, environment, logs, exit status, observed failure, and bounded repair route
- **AND** the environment remains non-ready for UC-10

### Requirement: Code Trials Require Acquired Source and Prepared Environment
The system SHALL start UC-10 only with a verified registered source ref and accepted environment-preparation result.

#### Scenario: Trial prerequisites are ready
- **WHEN** `run-code-trial` resolves the registered repository semantic label, immutable commit or digest, accepted Pixi environment, and smoke result
- **THEN** it pins those exact refs as trial inputs

#### Scenario: Source or environment is missing
- **WHEN** a required source or environment ref is missing, stale, failed, or ambiguous
- **THEN** the procedure routes to the applicable source-code ingestion or preparation use case or reports a blocker
- **AND** it does not execute the trial in an ambient environment

### Requirement: Trial Execution Requires an Approved Plan
The system SHALL create `kaoju:method-trial-plan` and obtain a human Gate decision before implementing or executing the claim-bearing trial.

#### Scenario: Plan is presented
- **WHEN** trial prerequisites and the actor's selected data basis are known
- **THEN** the plan records source commit, environment ref, data path or generated-data contract, task, entry point, wrapper, metrics, expected outputs, resource boundary, adaptations, risks, and interpretation limit
- **AND** execution waits for the human Gate decision

#### Scenario: Actor requests plan changes
- **WHEN** the human Gate rejects or revises the plan
- **THEN** the system preserves the decision and plan revision history
- **AND** it does not execute until a later plan is approved

### Requirement: Trial Runs and Results Are Durable and Immutable
The system SHALL execute an approved minimal wrapper through registered command execution and SHALL record an immutable Run and result.

#### Scenario: Approved task has a compatible upstream command
- **WHEN** the paper or repository provides a command that fits the approved task, pinned source, prepared environment, selected data, and resource boundary
- **THEN** the durable wrapper invokes that command and records exact-command fidelity
- **AND** any necessary deviation is recorded as an adaptation rather than represented as exact-command reproduction

#### Scenario: Approved task needs an adapted entry point
- **WHEN** no upstream command fits the approved task and constraints
- **THEN** the durable wrapper implements the smallest necessary recorded adaptation
- **AND** the plan and result state the resulting fidelity and interpretation limit

#### Scenario: Trial completes
- **WHEN** the approved wrapper executes with selected data
- **THEN** `kaoju:method-trial-run` records exact inputs, source commit, environment and lock identity, wrapper, command request, logs, raw outputs, timing, resources, adaptations, exit status, and terminal state
- **AND** `kaoju:method-trial-result` records measurements, checks, evidence verdict, verification depth, limitations, and Run refs

#### Scenario: Trial has a transient failure
- **WHEN** an approved trial fails without requiring any change to its pinned source, environment, data, wrapper, evaluator, metrics, resources, or interpretation
- **THEN** the system may retry the identical request automatically within the recorded attempt bound
- **AND** each attempt remains a separate Run with its own logs, outputs, status, and lineage

#### Scenario: Trial repair would be material
- **WHEN** a failed trial would require a dependency or lock change, source patch or commit change, different data, changed wrapper semantics or entry point, changed evaluator or metrics, changed resource limits, or changed evidence interpretation
- **THEN** the system revises the trial plan and waits for the applicable human Gate before executing the repaired attempt
- **AND** the later Run does not overwrite the earlier failure, fidelity, or verdict

### Requirement: Random Data Trials Remain Capability Probes
The system SHALL record generated or random trial input as `kaoju:generated-dataset` and SHALL limit conclusions to the supported capability-probe scope.

#### Scenario: Actor selects random data
- **WHEN** the approved trial plan uses generated or random input
- **THEN** the generated dataset records generator, schema, size, seed, assumptions, checks, storage refs, and limitations
- **AND** trial results are labeled `capability-probe` at no stronger than executed verification depth

#### Scenario: Result is compared with a paper benchmark
- **WHEN** a generated-data result differs from or resembles a reported paper number
- **THEN** the system does not call the result a reproduction or benchmark validation
- **AND** it explains the input, environment, evaluator, and fidelity differences that limit comparison

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
