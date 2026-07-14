# kaoju-cli-services Specification

## Purpose
TBD - created by syncing change revise-kaoju-survey-process. Update Purpose after archive.

## Requirements
### Requirement: Project Artifact Commands Resolve Semantic Bindings
The CLI SHALL provide canonical `isomer-cli project artifacts` commands that resolve an exact semantic artifact id through the active binding registry.

#### Scenario: Binding is described
- **WHEN** a caller runs `project artifacts describe` for a registered Kaoju semantic id
- **THEN** the CLI returns the semantic meaning, record kind, profile ref, default semantic label, content mode, producer and consumer policy, revision mode, scope-key policy, and validation expectations
- **AND** it does not expose executable provider payloads as binding data

#### Scenario: Artifact is created from a file
- **WHEN** an authorized producer runs `project artifacts put` with a registered semantic id, content file, required scope, and relationship refs
- **THEN** the CLI infers the physical binding, validates the content, stores or registers it, creates the Artifact Core Record and links, and returns stable refs
- **AND** the caller does not need to supply record kind, profile ref, or physical records-root path

#### Scenario: Managed content path is allocated
- **WHEN** `put` or `revise` persists content under a managed `topic.records.*` surface
- **THEN** the artifact service allocates the internal path through its generic record-owned storage policy and returns the registered locator
- **AND** callers use stable Artifact refs and DB queries rather than treating the internal subpath shape as a public API

#### Scenario: Artifact is revised
- **WHEN** an authorized producer runs `project artifacts revise` for a current-state artifact
- **THEN** the CLI preserves the prior revision, validates the scope and base revision, creates explicit lineage, and advances the scoped current candidate
- **AND** a stale base or competing current candidate produces a deterministic conflict

#### Scenario: Binding cannot be resolved
- **WHEN** the semantic id, profile, label, scope policy, or producer authorization is missing or inconsistent
- **THEN** the command fails with a structured storage diagnostic
- **AND** it does not invent a path, profile, record kind, or fallback semantic id

### Requirement: Artifact Commands Support File and Directory Content
The project artifact service SHALL register structured files, ordinary files, directory manifests, external paths, and canonical repository references without embedding large content in state metadata.

#### Scenario: Structured payload is registered
- **WHEN** the binding selects structured-file content
- **THEN** the service validates the JSON schema and common identity and display fields and links the Artifact Core Record to the managed JSON file

#### Scenario: Ordinary file is registered
- **WHEN** the binding selects an ordinary MyST, Markdown, TeX, PDF, script, log, or downloaded file
- **THEN** the service records its locator kind, media type, checksum, size, status, and provenance
- **AND** the file remains the authoritative content

#### Scenario: Directory is registered
- **WHEN** the binding selects directory-manifest content
- **THEN** the service creates or validates a versioned manifest of member paths, checksums, media types, sizes, entry points, and external references
- **AND** the Artifact Core Record points to the manifest rather than embedding or scanning the directory tree during later discovery

#### Scenario: External content is registered
- **WHEN** the actor authorizes an external path or canonical repository locator
- **THEN** the service records the external locator posture, observed identity, digest or commit, access policy, and staleness policy
- **AND** it does not copy, move, rewrite, or delete externally owned content unless a separate authorized operation requires it

### Requirement: Artifact Queries Support Scoped Current State
The CLI SHALL provide `latest`, `list`, and `show` queries that use state-DB indexes and an optional binding-defined scope key.

#### Scenario: Scoped latest record is requested
- **WHEN** a caller requests the latest `kaoju:reading-list` for one direction scope
- **THEN** the CLI returns only the current candidate for that direction and its revision and conflict posture
- **AND** lists for other directions remain independently current

#### Scenario: Legacy unscoped records are queried
- **WHEN** a scoped query encounters only legacy records without a scope key
- **THEN** the CLI reports the migration or ambiguity posture and returns a deterministic result only when one compatible candidate can be established
- **AND** it does not silently choose among competing records by timestamp

#### Scenario: Content locator is stale
- **WHEN** `show` resolves a DB record whose referenced file is missing or whose checksum no longer matches
- **THEN** the CLI reports a stale or corrupt content diagnostic and the recovery route
- **AND** directory scanning does not substitute another file

### Requirement: Project Run Commands Persist Resumable Stages
The CLI SHALL provide `project runs begin`, `checkpoint`, `status`, and `complete` for bounded Research Task attempts.

#### Scenario: Run begins
- **WHEN** a pipeline procedure starts for a Research Task
- **THEN** `begin` records procedure id, control mode, actors, normalized input refs, expected output semantics, scheduler and Gate policy refs, and initial stage

#### Scenario: Run checkpoints
- **WHEN** a durable stage completes or pauses
- **THEN** `checkpoint` records stage id, output refs, pending Gate, blocker or Service Request refs, stage status, observations, and resume hint
- **AND** the update is visible through fresh Workspace Runtime state

#### Scenario: Run completes
- **WHEN** the bounded procedure reaches a terminal state
- **THEN** `complete` records `complete`, `paused`, or `blocked`, exact output refs, unresolved items, resource observations, and resume posture
- **AND** it does not start another macro procedure

### Requirement: Project Repository Acquisition Is Canonical and Atomic
The CLI SHALL provide `project repos acquire` for verified source acquisition into a semantic-label-resolved canonical external repository location.

#### Scenario: Shallow acquisition succeeds
- **WHEN** a verified remote URL and target repository identity pass preflight
- **THEN** the command clones with depth one by default, resolves the immutable commit, validates the checkout, and registers the canonical repository
- **AND** JSON output includes repository ref, semantic label, path, remote identity, commit, depth posture, and provenance refs

#### Scenario: Target or remote is ambiguous
- **WHEN** the remote identity, canonical target, or existing checkout relationship is ambiguous
- **THEN** the command fails before mutation with candidate and clarification data
- **AND** it does not merge unrelated repositories or overwrite an existing checkout

#### Scenario: Clone fails
- **WHEN** repository acquisition or post-clone validation fails
- **THEN** the command removes or records the staged recovery path and leaves canonical registration unchanged
- **AND** it returns a deterministic blocker suitable for `kaoju:source-access-blocker`

### Requirement: Project Service Request Commands Preserve Operational Ownership
The CLI SHALL provide `project service-requests create`, `dispatch`, and `status` without treating a Service Request as a Research Task or Workflow Stage.

#### Scenario: Request is created
- **WHEN** a Project Operator Session or Operator Agent requests environment support
- **THEN** the command records supported scope, task, expected support outputs, authorization scope, dispatch form, completion observation rules, related Research Task and Run refs, and provenance

#### Scenario: Request is dispatched
- **WHEN** the request is authorized and dispatchable
- **THEN** the CLI creates or references an Execution Adapter Command Request for dispatch, preflight, monitoring, and recording and waits for terminal completion or a configured timeout or interruption
- **AND** provider-specific or Houmao payloads remain outside the Service Request record

#### Scenario: Synchronous dispatch completes
- **WHEN** the Service Request reaches a normalized terminal state while `dispatch` is waiting
- **THEN** the command returns the stable Service Request ref, terminal state, completion observations, support Artifact refs, and command-request refs
- **AND** the first release does not require a separate status command for the successful interactive path

#### Scenario: Synchronous dispatch is interrupted or times out
- **WHEN** the caller is interrupted or the configured wait timeout expires before normalized terminal completion
- **THEN** the command returns the stable Service Request ref and latest observed non-terminal or unknown state without inventing completion
- **AND** `project service-requests status` can reconcile the durable request later

#### Scenario: Asynchronous dispatch is requested
- **WHEN** a first-release caller requests no-wait or asynchronous Service Request dispatch
- **THEN** the CLI reports that asynchronous dispatch is unsupported and identifies the synchronous `dispatch` and recovery `status` operations
- **AND** it does not silently change waiting behavior

#### Scenario: Request status is queried
- **WHEN** a caller checks Service Request status
- **THEN** the CLI returns lifecycle state, service actor refs when present, command-request refs, support Artifact refs, observations, blockers, and completion posture
- **AND** raw provider state is not represented as authoritative completion without normalization

### Requirement: Kaoju Paper Commands Are Deterministic Transformations
The CLI SHALL provide `ext kaoju paper` commands for template exchange, derived views, TeX initialization, and registered PDF builds while leaving authorship and TeX judgment to the write skill.

#### Scenario: Template is exported or applied
- **WHEN** `export-template` or `apply-template` runs
- **THEN** the CLI performs path resolution, manifest creation or validation, checksum and concurrency checks, structural validation, and Artifact registration
- **AND** the write skill remains responsible for selecting content and regenerating prose

#### Scenario: Markdown or TeX is derived
- **WHEN** `derive-markdown` or `init-tex` runs
- **THEN** the CLI records source revisions, converter identity, outputs, warnings, unsupported constructs, checksums, and lineage
- **AND** it does not declare mechanically initialized TeX ready without recorded agent inspection

#### Scenario: PDF is built
- **WHEN** `build-pdf` receives an inspected TeX artifact
- **THEN** it dispatches the document-build extension point, records the Run and compile log, validates the output, and registers the PDF
- **AND** it does not invoke an ambient compiler directly outside registered execution

### Requirement: Kaoju Wiki Commands Are Deterministic and Self-Contained
The CLI SHALL provide `ext kaoju wiki export`, `deploy`, and `start` backed only by package-owned Isomer code and assets.

#### Scenario: Wiki commands are discovered
- **WHEN** an installed-package caller inspects `ext kaoju wiki`
- **THEN** help and machine-readable command metadata describe required targets, selected artifact refs, update policies, outputs, and Gate posture
- **AND** no external skill checkout is required

#### Scenario: Export and deployment mutate explicit targets
- **WHEN** `export` or `deploy` is authorized
- **THEN** the command validates the explicit target, performs an idempotent operation, writes the applicable manifest, and registers the durable outputs
- **AND** it does not overwrite unrecognized files without an explicit decision

#### Scenario: Viewer start executes
- **WHEN** `start` receives a valid viewer deployment and port posture
- **THEN** it launches through command execution, records the Run and logs, and returns the local URL and stable refs

### Requirement: Executable CLI Operations Use Extension Points
Repository acquisition, package mutation, smoke runs, trials, document builds, and viewer launch SHALL use applicable Research Operation Extension Points and Execution Adapter Command Requests.

#### Scenario: Executable operation is dispatched
- **WHEN** a typed CLI service needs provider-backed or process execution
- **THEN** it constructs a provider-neutral command request with identity refs, Effective Topic Context metadata, capability and policy refs, semantic targets, expected inputs and outputs, monitoring policy, and provenance obligations
- **AND** provider command bodies, credentials, raw output, and live process state remain adapter-owned

#### Scenario: Required capability is unavailable
- **WHEN** no compatible binding satisfies the required extension point
- **THEN** preflight returns a capability blocker before execution
- **AND** the CLI does not fall back to ambient shell behavior

#### Scenario: Execution request is retried or repaired
- **WHEN** an approved operation fails
- **THEN** the execution service permits only identical bounded retries or binding-defined non-material repairs under the existing authorization
- **AND** a material change to dependencies, source, data, wrapper semantics, evaluator, metrics, resources, canonical content, or evidence interpretation requires a revised plan and Gate ref before dispatch

### Requirement: Legacy Research Commands Remain Explicit Compatibility Surfaces
The existing `ext research records` and `ext research templates` commands SHALL remain available during migration without becoming alternate canonical implementations.

#### Scenario: Legacy record command is used
- **WHEN** a caller uses a supported `ext research records` operation
- **THEN** it delegates to the same record and artifact services used by canonical project commands
- **AND** lineage, validation, query, and provenance meaning remain compatible

#### Scenario: Legacy template is inspected
- **WHEN** a caller lists, shows, compiles, or archives an existing `kaoju:writing-template`
- **THEN** the compatibility command preserves its legacy LaTeX meaning and reports that it is non-canonical for new paper content
- **AND** it does not silently promote the template to `kaoju:paper-template-myst`

#### Scenario: New canonical paper work is requested through the legacy group
- **WHEN** a caller attempts to create new canonical paper state through `ext research templates`
- **THEN** the CLI returns a deprecation diagnostic and the corresponding `ext kaoju paper` command
- **AND** it does not create ambiguous dual canonical state

### Requirement: Typed CLI Services Produce Stable Diagnostics and JSON
Every new CLI command SHALL provide deterministic human-readable errors and machine-readable JSON suitable for skill orchestration and tests.

#### Scenario: Command succeeds with JSON output
- **WHEN** a caller requests JSON output for a successful command
- **THEN** the result includes operation id, affected stable refs, resolved scope, status, diagnostics, and next allowed actions

#### Scenario: Command fails before mutation
- **WHEN** preflight detects invalid context, missing binding, stale input, ambiguity, unauthorized target, missing capability, or Gate requirement
- **THEN** the error identifies the command, stable error code, affected field or ref, mutation status, and recovery action
- **AND** it avoids a traceback for an expected user or state error
