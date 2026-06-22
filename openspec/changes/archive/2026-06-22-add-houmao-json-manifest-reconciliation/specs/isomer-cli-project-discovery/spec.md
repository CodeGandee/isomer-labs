## ADDED Requirements

### Requirement: Houmao Adapter Manifest CLI Surface
The system SHALL expose deterministic CLI commands for Houmao adapter link export, integrity inspection, reconciliation, and adoption.

#### Scenario: Adapter link export is non-launching
- **WHEN** a user runs the adapter link export command for a Houmao-backed Agent Team Instance
- **THEN** the command writes or prints an `adapter-link.json` manifest and does not launch, stop, message, or inspect Houmao-managed agents

#### Scenario: Integrity inspection is read-only
- **WHEN** a user runs live inspection with integrity reporting for a Houmao-backed Agent Team Instance
- **THEN** the command reads Workspace Runtime refs, JSON manifests, and live Houmao state and emits deterministic output without recording adoption or changing launch state

#### Scenario: Reconcile records only when explicit
- **WHEN** a user runs the reconcile command for a Houmao-backed Agent Team Instance with recording enabled by the command contract
- **THEN** the command may write `adapter-runtime-manifest.json`, reconciliation records, diagnostics, and Provenance Records but does not start or stop Houmao-managed agents

#### Scenario: Adopt records external launch
- **WHEN** a user runs the adopt command for externally launched Houmao runtime state
- **THEN** the command validates mapping, paths, digests, and redaction before recording adopted adapter refs in Workspace Runtime

### Requirement: Houmao Manifest CLI Output
The system SHALL emit deterministic text and JSON output for Houmao adapter manifest and reconciliation commands.

#### Scenario: JSON output names generic refs
- **WHEN** a user requests JSON output from adapter link export, integrity inspection, reconcile, or adopt
- **THEN** the output names Project, Research Topic, Topic Workspace, Agent Team Instance, Agent Instance, Artifact, and Provenance refs plus opaque adapter refs and manifest paths

#### Scenario: Output reports reconciliation state
- **WHEN** a command observes linked, externally detected, adopted, drifted, conflicted, stale, or rejected state
- **THEN** the output includes the reconciliation state, mapping confidence, affected refs, and redacted diagnostics in stable field order
