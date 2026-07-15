## MODIFIED Requirements

### Requirement: Executable CLI Operations Use Extension Points
Package mutation, smoke runs, trials, document builds, and viewer launch SHALL use applicable Research Operation Extension Points and Execution Adapter Command Requests, while repository acquisition SHALL remain outside Isomer execution services.

#### Scenario: Executable operation is dispatched
- **WHEN** a typed CLI service other than repository acquisition needs provider-backed or process execution
- **THEN** it constructs a provider-neutral command request with identity refs, Effective Topic Context metadata, capability and policy refs, semantic targets, expected inputs and outputs, monitoring policy, and provenance obligations
- **AND** provider command bodies, credentials, raw output, and live process state remain adapter-owned

#### Scenario: Repository acquisition is requested
- **WHEN** a user or skill needs to clone, fetch, copy, check out, deepen, repair, or otherwise acquire repository content
- **THEN** the acting user or agent selects and runs the commands outside typed Isomer CLI services and Execution Adapter Command Requests
- **AND** it invokes only non-executing Isomer path and registration commands after the external result is verified

#### Scenario: Required capability is unavailable
- **WHEN** no compatible binding satisfies a required extension point for a remaining executable CLI operation
- **THEN** preflight returns a capability blocker before execution
- **AND** the CLI does not fall back to ambient shell behavior

#### Scenario: Execution request is retried or repaired
- **WHEN** an approved non-repository operation fails
- **THEN** the execution service permits only identical bounded retries or binding-defined non-material repairs under the existing authorization
- **AND** a material change to dependencies, source, data, wrapper semantics, evaluator, metrics, resources, canonical content, or evidence interpretation requires a revised plan and Gate ref before dispatch

## REMOVED Requirements

### Requirement: Project Repository Acquisition Is Canonical and Atomic
**Reason**: `project repos acquire` fixes Git command shape, clone depth, staging, retries, and cleanup inside the Isomer API, which prevents user-specific or repository-specific acquisition procedures and assigns source-control execution to the wrong owner.

**Migration**: Remove the command, Kaoju repository service, and `repository_acquisition` extension point. Query or choose a safe target, run the required repository commands outside Isomer, verify the result, then register the existing path through `project repos register` and record research provenance through typed Artifact operations.
