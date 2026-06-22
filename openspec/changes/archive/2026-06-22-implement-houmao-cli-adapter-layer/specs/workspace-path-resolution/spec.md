## ADDED Requirements

### Requirement: Houmao CLI adapter path plans
The system SHALL resolve and record path plans for Houmao CLI adapter material, command payloads, logs, and snapshots before those files are written or referenced.

#### Scenario: Adapter root is topic scoped
- **WHEN** the Houmao adapter prepares material for an Agent Team Instance
- **THEN** the adapter root resolves under the selected Topic Workspace runtime area or an accepted recorded Topic Workspace path plan and is linked to the Agent Team Instance

#### Scenario: Per-agent material is agent scoped
- **WHEN** the Houmao adapter writes per-Agent Instance launch material
- **THEN** the material resolves under the selected Agent Workspace path plan or an adapter path plan explicitly linked to that Agent Instance

#### Scenario: Command payload paths are durable
- **WHEN** the adapter writes command JSON payloads, sanitized outputs, launch logs, inspection snapshots, stop outcomes, or generated Houmao profile material
- **THEN** each path is recorded as durable adapter material before Workspace Runtime records depend on it

### Requirement: Houmao CLI adapter path validation
The system SHALL validate Houmao adapter paths against Project, Topic Workspace, and Agent Workspace ownership boundaries.

#### Scenario: Generated paths stay out of config and source checkouts
- **WHEN** the adapter generates launch material, command payloads, or logs
- **THEN** validation rejects writes into `.isomer-labs/`, the Houmao source checkout, another Topic Workspace, or untracked workspace-local team directories

#### Scenario: External direct Houmao refs remain explicit
- **WHEN** reconciliation or adoption references user-authored Houmao material outside Isomer-generated adapter paths
- **THEN** Workspace Runtime records the external ref source explicitly and validation reports missing or changed files without moving, rewriting, or deleting them

#### Scenario: Missing adapter files remain visible
- **WHEN** a recorded Houmao adapter material file, payload file, manifest, or snapshot is missing
- **THEN** runtime validation reports the missing durable path and preserves the referring adapter, Artifact, and Provenance refs
