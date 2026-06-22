## ADDED Requirements

### Requirement: Adapter Reconciliation Command Requests
The system SHALL route Houmao manifest reconciliation and adoption through provider-neutral Execution Adapter Command Requests.

#### Scenario: Reconcile request is created
- **WHEN** the system prepares to reconcile Houmao adapter manifests with Workspace Runtime and live Houmao state
- **THEN** it creates or validates an Execution Adapter Command Request with operation kind `adapter_reconcile`, selected Execution Adapter ref, Agent Team Instance ref, manifest refs, observation expectations, path validation expectations, and Provenance obligations

#### Scenario: Adopt request is created
- **WHEN** the system prepares to adopt externally launched Houmao runtime state
- **THEN** it creates or validates an Execution Adapter Command Request with operation kind `adapter_adopt`, target Agent Team Instance ref, proposed Agent Instance mappings, manifest refs, mapping confidence, Gate or approval refs when required, and Provenance obligations

#### Scenario: Reconciliation does not mutate Houmao
- **WHEN** an adapter reconciliation or adoption command request is executed
- **THEN** the adapter reads Houmao state and records Isomer-side outcomes without launching, stopping, or messaging Houmao-managed agents

### Requirement: Manifest Reconciliation Preflight
The system SHALL complete preflight before recording Houmao reconciliation or adoption outcomes.

#### Scenario: Reconciliation preflight validates inputs
- **WHEN** a Houmao reconciliation command is requested
- **THEN** preflight verifies current Workspace Runtime schema, selected Topic Workspace, selected Agent Team Instance, JSON manifest parseability, path-plan validity, redaction checks, and Houmao read-only inspection availability

#### Scenario: Failed preflight blocks recording
- **WHEN** reconciliation or adoption preflight fails
- **THEN** the system does not write reconciliation records, adoption records, or adapter-runtime manifests and returns deterministic diagnostics
