## ADDED Requirements

### Requirement: UC-01 Research Inquiry Graph
The system SHALL record the UC-01 headless path as a Research Inquiry graph under one Research Topic rather than as an unstructured run log.

#### Scenario: Seed inquiry is created
- **WHEN** the UC-01 runner starts work for the selected Research Topic
- **THEN** it records a seed Research Inquiry with source refs, status, scope notes, and Provenance Record refs

#### Scenario: Follow-up inquiry is linked
- **WHEN** the follow-up inquiry decision is resolved
- **THEN** the selected follow-up Research Inquiry is recorded and linked to the seed inquiry or Research Topic with a durable Research Inquiry Relationship

### Requirement: UC-01 Research Tasks and Runs
The system SHALL represent scouting, analysis, review, and closeout work as bounded Research Tasks and Runs.

#### Scenario: Handoff-backed tasks are recorded
- **WHEN** the runner delegates scouting, analysis, or review work to an Agent Instance
- **THEN** it records a Research Task and Run linked to the Research Inquiry, Agent Team Instance, target Agent Instance, handoff state, expected output refs, and Provenance Records

#### Scenario: Run completion follows normalization
- **WHEN** a UC-01 handoff produces a Signal Observation
- **THEN** the associated Run remains non-terminal until the Operator Agent records accepted normalization or another terminal normalization outcome

### Requirement: UC-01 Gate and Decision Lifecycle
The system SHALL represent follow-up inquiry selection as lifecycle state governed by a Gate and resolved by a Decision Record.

#### Scenario: Follow-up Gate blocks closeout action
- **WHEN** UC-01 follow-up inquiry options are ready but no selection has been recorded
- **THEN** the follow-up selection action is blocked by an open Gate while unrelated inspection remains allowed

#### Scenario: Gate resolution updates lifecycle refs
- **WHEN** the follow-up Gate is resolved
- **THEN** the seed Research Inquiry, selected follow-up Research Inquiry, closeout Run, and Workflow Stage Cursor refs point to the resolving Decision Record or Provenance Record

### Requirement: UC-01 Restart Recovery
The system SHALL recover UC-01 lifecycle state after process restart without requiring live Houmao inspection.

#### Scenario: Restart preserves route state
- **WHEN** the Workspace Runtime is reopened after a completed UC-01 simulated or live run
- **THEN** the Research Topic, Research Inquiries, Research Tasks, Runs, Gate, Decision Record, handoffs, Workflow Stage Cursors, and Agent Team Instance refs remain inspectable from persisted records

#### Scenario: Partial UC-01 run remains visible
- **WHEN** the runner stops after recording some but not all UC-01 lifecycle records
- **THEN** runtime validation reports missing or open lifecycle obligations without deleting completed records
