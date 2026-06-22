## ADDED Requirements

### Requirement: Manifest Provenance Records
The system SHALL record Provenance Records for Houmao adapter JSON manifest creation, update, reconciliation, and adoption.

#### Scenario: Link manifest provenance is recorded
- **WHEN** Isomer writes or exports `adapter-link.json`
- **THEN** the system records or links Provenance Records naming the actor, Project, Research Topic, Topic Workspace, Agent Team Instance, Topic Agent Team Profile, Execution Adapter ref, manifest path, and creation timestamp

#### Scenario: Runtime manifest provenance is recorded
- **WHEN** Isomer writes or updates `adapter-runtime-manifest.json`
- **THEN** the system records or links Provenance Records naming the observation source, Houmao read-only command refs, affected Agent Team Instance or Agent Instance refs, adapter refs, manifest digest, and timestamp

### Requirement: Reconciliation Diagnostic Artifacts
The system SHALL record reconciliation diagnostics as durable Artifacts or adapter payload refs when they are needed to explain adoption, drift, conflict, stale state, or rejection.

#### Scenario: Drift diagnostic is recorded
- **WHEN** reconciliation detects drift between JSON manifests, referenced launch-material digests, Workspace Runtime records, and live Houmao state
- **THEN** the system records a diagnostic Artifact or adapter payload ref linked to the affected Agent Team Instance, Agent Instance refs when known, manifest refs, and Provenance Records

#### Scenario: Conflict diagnostic is redacted
- **WHEN** reconciliation detects a mapping conflict involving Houmao native payloads
- **THEN** the recorded diagnostic excludes credentials, tokens, passwords, API keys, raw private messages, and other secret material

#### Scenario: Adoption decision is auditable
- **WHEN** an externally launched Houmao-backed Agent Team Instance is adopted or rejected
- **THEN** the system records the adoption decision, mapping confidence, manifest refs, diagnostics, actor ref, timestamp, and Provenance Records
