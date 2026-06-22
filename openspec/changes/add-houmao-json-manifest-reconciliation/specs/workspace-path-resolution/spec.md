## ADDED Requirements

### Requirement: Houmao JSON Manifest Path Plans
The system SHALL resolve durable path plans for Houmao adapter JSON manifests before writing or relying on those manifests.

#### Scenario: Manifest path is topic scoped
- **WHEN** the adapter creates `adapter-link.json`, `launch-material-manifest.json`, or `adapter-runtime-manifest.json` for an Agent Team Instance
- **THEN** each manifest path resolves under the selected Topic Workspace or an accepted Topic Workspace path plan and is recorded as durable runtime evidence

#### Scenario: Manifest path is not cache-like
- **WHEN** a Houmao adapter JSON manifest is written or updated
- **THEN** the path plan or Artifact locator marks the file as durable adapter runtime evidence rather than disposable cache material

### Requirement: Direct Houmao Path References
The system SHALL validate and record referenced Houmao project overlay paths without treating them as Isomer-owned generated launch material.

#### Scenario: Direct material path is adopted
- **WHEN** a user adopts direct Houmao launch material from a project overlay path outside Isomer-generated launch-material paths
- **THEN** the system records the path as adapter-external or user-authored launch material with digest, source, diagnostics, and Provenance refs

#### Scenario: External path requires explicit adoption
- **WHEN** reconciliation discovers a Houmao launch-material path that is outside recorded Topic Workspace or Agent Workspace path plans
- **THEN** the system reports the path as externally detected and does not treat it as trusted launch material until an explicit adopt operation accepts it

#### Scenario: Missing referenced path is diagnostic
- **WHEN** a JSON manifest references a launch-material, native runtime, log, or snapshot path that no longer exists
- **THEN** runtime validation reports a missing durable path diagnostic without deleting adapter, Artifact, or Provenance refs
