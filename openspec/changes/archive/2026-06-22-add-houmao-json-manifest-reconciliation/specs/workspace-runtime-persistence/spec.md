## ADDED Requirements

### Requirement: JSON Adapter Manifest Refs
The system SHALL persist Houmao adapter JSON manifest refs through opaque adapter payload refs linked to generic Workspace Runtime records.

#### Scenario: Manifest refs are adapter scoped
- **WHEN** Workspace Runtime stores refs to `adapter-link.json`, `launch-material-manifest.json`, or `adapter-runtime-manifest.json`
- **THEN** those refs are stored as adapter payload refs linked to Agent Team Instance, Agent Instance, Run, handoff, Artifact, path plan, and Provenance records without adding Houmao-specific generic fields

#### Scenario: Manifest refs survive restart
- **WHEN** a Houmao-backed Agent Team Instance is inspected after process restart
- **THEN** Workspace Runtime can resolve the stored JSON manifest refs and reconstruct the adapter state summary before optionally performing live Houmao inspection

### Requirement: Reconciliation Record Persistence
The system SHALL persist explicit reconciliation and adoption outcomes for Houmao-backed Agent Team Instances.

#### Scenario: Reconciliation is recorded
- **WHEN** a reconcile command records an outcome for a Houmao-backed Agent Team Instance
- **THEN** Workspace Runtime stores the reconciliation state, manifest digest summary, live observation summary, mapping confidence, diagnostics, timestamp, actor ref, and Provenance refs

#### Scenario: Adoption links external runtime
- **WHEN** an adopt command accepts externally launched Houmao runtime state
- **THEN** Workspace Runtime records the adopted adapter refs and Agent Instance mappings while preserving existing generic Agent Team Instance identity

#### Scenario: Drift does not delete records
- **WHEN** reconciliation reports drift, conflict, stale state, or rejection
- **THEN** Workspace Runtime preserves prior launch, manifest, adapter, Artifact, and Provenance refs and records the new diagnostic outcome separately

### Requirement: Generic Runtime Schema Boundary
The system SHALL keep Houmao manifest and runtime details out of generic Workspace Runtime schema fields.

#### Scenario: Generic inspection hides Houmao field names
- **WHEN** generic Isomer APIs inspect Agent Team Instance, Agent Instance, Run, handoff, or Artifact records linked to Houmao manifests
- **THEN** the records expose generic refs and adapter payload refs, not generic fields named after Houmao project profiles, gateways, mailboxes, managed agents, sessions, or native manifest paths
