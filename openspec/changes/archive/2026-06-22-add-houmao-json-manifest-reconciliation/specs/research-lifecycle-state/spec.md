## ADDED Requirements

### Requirement: Houmao Reconciliation Lifecycle Summary
The system SHALL represent Houmao reconciliation state through adapter-linked lifecycle summaries for Agent Team Instances and Agent Instances.

#### Scenario: External detection is not adopted lifecycle
- **WHEN** reconciliation detects live Houmao-managed agents that match an Isomer link manifest but have not been adopted
- **THEN** the Agent Team Instance summary reports externally detected adapter state without marking the generic launch lifecycle as launched by Isomer

#### Scenario: Adoption updates lifecycle summary
- **WHEN** adoption succeeds for externally launched Houmao runtime state
- **THEN** the Agent Team Instance and mapped Agent Instance summaries include adopted adapter state, mapping confidence, and Provenance refs

#### Scenario: Drift keeps previous lifecycle visible
- **WHEN** reconciliation reports material drift, missing native runtime paths, stale sessions, or conflicting mappings
- **THEN** the lifecycle summary keeps the previous launch or adoption state visible and adds drift, stale, or conflict diagnostics

### Requirement: Manual Operation Does Not Bypass Normalization
The system SHALL prevent direct Houmao operation from bypassing Isomer handoff and Run normalization requirements.

#### Scenario: Direct Houmao reply remains observation
- **WHEN** direct Houmao mail, gateway output, files, or inspection output indicates progress or candidate completion
- **THEN** the system records or reports Signal Observations and does not mark handoff, Run, or Workflow Stage Cursor completion accepted without Operator Agent normalization

#### Scenario: Adopted runtime keeps normalization boundary
- **WHEN** an externally launched Houmao-backed Agent Team Instance is adopted
- **THEN** existing and future handoff completion still requires the same Operator Agent normalization path as Isomer-launched runtime
