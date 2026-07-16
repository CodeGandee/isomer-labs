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
The CLI SHALL provide low-level `ext kaoju paper template` CRUD, exact named copy and replacement, export inspection, safe export, integrity validation, and state-token concurrency while leaving arbitrary template construction and merge decisions to Kaoju skills.

#### Scenario: Template is exported or applied
- **WHEN** `export-template` or `apply-template` runs
- **THEN** the CLI performs path resolution, manifest creation or validation, checksum and concurrency checks, structural validation, and Artifact registration
- **AND** the write skill remains responsible for selecting content and regenerating prose

#### Scenario: Markdown or TeX is derived
- **WHEN** `derive-markdown` or `init-tex` runs
- **THEN** the CLI records selected template name, stable ref, observed digest, converter identity, outputs, warnings, checksums, and lineage
- **AND** it does not declare mechanically initialized TeX ready without agent inspection

#### Scenario: PDF is built
- **WHEN** `build-pdf` receives inspected TeX state
- **THEN** it dispatches the document-build extension point, records the Run and compile log, validates output, and registers the PDF
- **AND** it does not invoke an ambient compiler outside registered execution

#### Scenario: Named templates are listed or shown
- **WHEN** `template list` or `template show` runs
- **THEN** the CLI queries the flat named-template namespace and returns stable ref, name, current tree digest, state token, status, authored metadata, and resolved default working path
- **AND** it exposes no snapshot classification or automatic revision history

#### Scenario: Template is created from prepared content
- **WHEN** `template create --name <name> --from <path>` receives a new path-safe name and integrity-valid prepared tree
- **THEN** it creates the stable named record, managed directory content, state token, and audit event
- **AND** it does not infer the tree's high-level template meaning

#### Scenario: Named template is copied explicitly
- **WHEN** `template create --name <new> --from-template <existing>` runs
- **THEN** the CLI creates an ordinary independent named template with exact source tree and allowed metadata
- **AND** it does not mark, list, retain, or manage the new name as a snapshot

#### Scenario: Prepared content updates mutable state
- **WHEN** `template update --name <name> --from <path> --expected-state <token>` receives valid low-level inputs
- **THEN** it atomically replaces current content in the stable named record and emits before-and-after digest provenance
- **AND** it does not create a superseding template-content record or preserve prior bytes by contract

#### Scenario: Known named template replaces target
- **WHEN** `template update --name <target> --from-template <source> --expected-state <token>` runs
- **THEN** the CLI copies exact source content and applicable metadata to the stable target and returns its new state token
- **AND** it performs no merge and leaves the source unchanged

#### Scenario: File and metadata CRUD remain low level
- **WHEN** `template file put`, `template file remove`, or `template metadata patch` receives a safe target, current token, and authorized input
- **THEN** the CLI atomically changes only the selected content or allowed authored metadata and recalculates managed state
- **AND** it rejects changes to service-controlled identity, scope, binding, digest, token, and audit fields

#### Scenario: Stale state is rejected
- **WHEN** any update, file edit, metadata patch, archive, or delete receives a stale state token
- **THEN** the CLI returns current-state diagnostics without mutation
- **AND** the caller must re-read before retrying

#### Scenario: Template removal is reference safe
- **WHEN** a caller archives or deletes a named template
- **THEN** the CLI applies the configured reference-safety and authorization policy and reports dependent paper state
- **AND** it does not silently remove a template still required by durable refs

#### Scenario: Registered exports are inspected or written
- **WHEN** `template exports` or `template export` runs
- **THEN** the CLI reports or writes stable working-copy metadata and tree digests through the resolved exchange surface
- **AND** it refuses to overwrite edited or unrecognized content

#### Scenario: High-level conversion is requested
- **WHEN** a caller asks the CLI to convert or merge an arbitrary user-edited directory into canonical template state
- **THEN** the CLI returns guidance to use the Kaoju agent to construct a candidate and then invoke low-level update
- **AND** canonical state remains unchanged

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
Package mutation, smoke runs, trials, document builds, and viewer launch SHALL use applicable Research Operation Extension Points and Execution Adapter Command Requests, while repository acquisition SHALL remain outside Isomer execution services.

#### Scenario: Executable operation is dispatched
- **WHEN** a typed CLI service other than repository acquisition needs provider-backed or process execution
- **THEN** it constructs a provider-neutral command request with identity refs, Effective Topic Context metadata, capability and policy refs, semantic targets, expected inputs and outputs, monitoring policy, and provenance obligations
- **AND** provider command bodies, credentials, raw output, and live process state remain adapter-owned

#### Scenario: Required capability is unavailable
- **WHEN** no compatible binding satisfies a required extension point for a remaining executable CLI operation
- **THEN** preflight returns a capability blocker before execution
- **AND** the CLI does not fall back to ambient shell behavior

#### Scenario: Execution request is retried or repaired
- **WHEN** an approved non-repository operation fails
- **THEN** the execution service permits only identical bounded retries or binding-defined non-material repairs under the existing authorization
- **AND** a material change to dependencies, source, data, wrapper semantics, evaluator, metrics, resources, canonical content, or evidence interpretation requires a revised plan and Gate ref before dispatch

#### Scenario: Repository acquisition is requested
- **WHEN** a user or skill needs to clone, fetch, copy, check out, deepen, repair, or otherwise acquire repository content
- **THEN** the acting user or agent selects and runs the commands outside typed Isomer CLI services and Execution Adapter Command Requests
- **AND** it invokes only non-executing Isomer path and registration commands after the external result is verified

### Requirement: Legacy Research Commands Remain Explicit Compatibility Surfaces
The existing `ext research records` commands SHALL remain available, while `ext research templates` SHALL stop owning or mutating the writing-template directory and direct new MyST work to the named Kaoju CRUD and agentic workflow.

#### Scenario: Legacy record command is used
- **WHEN** a caller uses a supported `ext research records` operation
- **THEN** it preserves existing record and provenance meaning
- **AND** it does not become an alternate implementation of named mutable templates

#### Scenario: Legacy template is inspected
- **WHEN** a caller lists, shows, compiles, or archives an existing `kaoju:writing-template`
- **THEN** the compatibility command preserves its legacy LaTeX meaning and reports that it is non-canonical for new paper content
- **AND** it does not silently promote the template to `kaoju:paper-template-myst`

#### Scenario: New canonical paper work is requested through the legacy group
- **WHEN** a caller attempts to create new canonical paper state through `ext research templates`
- **THEN** the CLI returns a deprecation diagnostic and the corresponding `ext kaoju paper` command
- **AND** it does not create ambiguous dual canonical state

#### Scenario: Legacy template record requires inspection
- **WHEN** a caller inspects an existing `kaoju:writing-template` record
- **THEN** generic record reads preserve access to its legacy LaTeX payload and lineage
- **AND** it is never treated as a named mutable `kaoju:paper-template-myst`

#### Scenario: Legacy template command is invoked
- **WHEN** a caller invokes `ext research templates`
- **THEN** the CLI returns migration guidance naming the applicable Kaoju template CRUD, export, or agentic update entrypoint
- **AND** it does not mutate `intent/derived/writing-template`

#### Scenario: Legacy directory conflicts with a MyST working path
- **WHEN** export finds a legacy LaTeX tree at its target
- **THEN** it reports non-destructive move or archive guidance
- **AND** it does not overwrite, reinterpret, or silently import the files

### Requirement: Typed CLI Services Produce Stable Diagnostics and JSON
Every new CLI command SHALL provide deterministic human-readable errors and machine-readable JSON suitable for skill orchestration and tests.

#### Scenario: Command succeeds with JSON output
- **WHEN** a caller requests JSON output for a successful command
- **THEN** the result includes operation id, affected stable refs, resolved scope, status, diagnostics, and next allowed actions

#### Scenario: Command fails before mutation
- **WHEN** preflight detects invalid context, missing binding, stale input, ambiguity, unauthorized target, missing capability, or Gate requirement
- **THEN** the error identifies the command, stable error code, affected field or ref, mutation status, and recovery action
- **AND** it avoids a traceback for an expected user or state error

### Requirement: Kaoju Shared Contract Commands Are Read-Only and Context-Free
The CLI SHALL expose package-owned Kaoju survey-process and binding resources through deterministic read-only commands under `isomer-cli ext kaoju` without requiring Effective Topic Context.

#### Scenario: Survey-process contract is shown
- **WHEN** a caller runs `isomer-cli --print-json ext kaoju process show`
- **THEN** the command returns a success envelope with `mutated: false`, the survey-process schema version, entry skill, ordered skill and command inventories, manager actions, aliases, and public policy decisions
- **AND** logical links to other shared resources use extension query commands rather than package or repository filesystem paths

#### Scenario: Binding inventory is listed
- **WHEN** a caller runs `isomer-cli --print-json ext kaoju bindings list`
- **THEN** the command returns a deterministic semantic-id-sorted summary with registry version, family, status, artifact type, producer, and consumers for every binding
- **AND** it does not require a Project, Research Topic, or Topic Workspace selection

#### Scenario: One binding is described
- **WHEN** a caller runs a command such as `isomer-cli --print-json ext kaoju bindings describe KAOJU:SURVEY-CONTRACT` for a registered id
- **THEN** the command returns the complete declarative binding and storage-neutral semantic meaning needed by active guidance
- **AND** the request and response preserve the exact canonical `KAOJU:WHAT` identifier without case conversion or placeholder translation
- **AND** it does not return an internal resource path or executable provider payload

#### Scenario: Unknown binding is requested
- **WHEN** `bindings describe` receives an unregistered, non-uppercase, or incompatible semantic id
- **THEN** the command returns a structured non-mutating diagnostic with the requested id and required uppercase grammar
- **AND** it does not select an alias, normalize case, derive another identifier, or choose a fallback binding

#### Scenario: Installed package serves shared contracts
- **WHEN** the commands run from an installed wheel without the source repository or system-skill family root
- **THEN** they load and validate resources from the package-owned Kaoju implementation
- **AND** malformed or missing resources produce deterministic diagnostics rather than a traceback or repository fallback

### Requirement: Kaoju Contract Queries and Artifact Operations Share One Loader
The `ext kaoju` contract queries and `project artifacts` operations SHALL resolve the same validated Kaoju contract and binding objects.

#### Scenario: Agent describes then writes an artifact
- **WHEN** an agent describes a semantic id through `ext kaoju bindings describe` and later invokes `project artifacts put` or `project artifacts revise` for that id
- **THEN** both surfaces report or enforce the same exact uppercase identifier, schema version, binding fields, producer policy, scope policy, and validation expectations
- **AND** no second registry copy or skill-local projection can override the package-owned registry

#### Scenario: Existing project artifact description remains available
- **WHEN** a caller uses `project artifacts describe` during topic-scoped artifact work
- **THEN** the command continues to describe the binding through the shared loader
- **AND** active skill guidance uses `ext kaoju` for context-free shared-resource discovery and `project artifacts` for topic-scoped artifact operations
