## ADDED Requirements

### Requirement: UC-01 Fixture Project
The system SHALL provide a repeatable UC-01 fixture Project for Explore a New Research Direction with one Research Topic, one Topic Workspace, one `deepsci-mini` Topic Agent Team Profile, explicit topic environment readiness binding, and a follow-up-inquiry Gate policy ref.

#### Scenario: Fixture validates before execution
- **WHEN** the UC-01 fixture Project is validated through the public CLI
- **THEN** validation succeeds without launching agents, creating Workspace Runtime state, or embedding runtime truth in Project config files

#### Scenario: Fixture declares expected workflow refs
- **WHEN** the UC-01 fixture Project is inspected
- **THEN** it exposes the selected Research Topic, Topic Workspace, Topic Agent Team Profile, expected Artifact refs or kinds, and follow-up-inquiry Gate policy ref through Project Manifest or Research Topic Config records

### Requirement: Headless UC-01 Runner
The system SHALL provide a deterministic headless UC-01 execution path that runs from Project discovery through follow-up inquiry Decision Record without requiring a GUI renderer.

#### Scenario: Simulated runner completes vertical slice
- **WHEN** the UC-01 runner executes in adapter-simulated mode for the fixture Project
- **THEN** it initializes Workspace Runtime, records readiness, creates an Agent Team Instance, launches or simulates the `deepsci-mini` team, dispatches scouting and synthesis-review handoffs, normalizes accepted outputs, records the follow-up inquiry decision, and exits successfully

#### Scenario: Runner is restart-safe
- **WHEN** the UC-01 runner completes and Workspace Runtime is reopened
- **THEN** the runtime can inspect the Research Inquiry graph, Research Tasks, Runs, handoffs, Artifacts, Evidence Items, Gate, Decision Record, View Manifests, and Provenance Records written by the run

### Requirement: UC-01 Durable Research Records
The system SHALL leave durable research records for the UC-01 path that are sufficient to inspect what was scouted, analyzed, reviewed, and selected.

#### Scenario: Research outputs are recorded
- **WHEN** UC-01 handoff results are accepted by Operator Agent normalization
- **THEN** Workspace Runtime records seed-source summaries, literature notes, claim candidates or Findings, Evidence Items, review notes, inquiry options, and linked Provenance Records as file-backed or runtime-backed records

#### Scenario: Candidate claims are not automatically supported
- **WHEN** a UC-01 handoff returns a claim candidate
- **THEN** the system records it as a candidate or Finding unless accepted Evidence Item links satisfy the Research Recording Contracts for a supported Research Claim

### Requirement: Follow-up Inquiry Closeout
The system SHALL close the UC-01 headless run by presenting follow-up Research Inquiry options, opening a follow-up-inquiry Gate, and recording the selected option through a Decision Record.

#### Scenario: Follow-up Gate is opened
- **WHEN** the UC-01 runner has candidate follow-up inquiry options
- **THEN** it records an open Gate that names the governed action, available options, affected Research Topic or Research Inquiry refs, and required Operator Agent decision context

#### Scenario: Decision selects follow-up inquiry
- **WHEN** the Operator Agent or deterministic simulated operator resolves the follow-up Gate
- **THEN** the system records a Decision Record, the selected follow-up Research Inquiry, rejected alternatives when material, rationale, and Provenance Records linking the decision to the UC-01 outputs

### Requirement: Minimal UC-01 View Manifests
The system SHALL emit minimal View Manifest records for literature matrix, claim graph, and inquiry comparison views as durable semantic records.

#### Scenario: View Manifests reference source records
- **WHEN** the UC-01 runner writes View Manifest records
- **THEN** each View Manifest references the underlying Artifacts, Evidence Items, Findings or claim candidates, Research Inquiries, Gate, Decision Record, and Provenance Records needed to reconstruct the view

#### Scenario: View Manifests do not require renderer
- **WHEN** the UC-01 runner completes in headless mode
- **THEN** the presence of View Manifest records does not require a GUI renderer, AG-UI event transport, screenshot, or generated visual asset

### Requirement: Simulated and Live Validation Modes
The system SHALL support deterministic adapter-simulated validation by default and live Houmao validation only behind an explicit live gate.

#### Scenario: Simulated validation is default
- **WHEN** the UC-01 integration or manual validation runs without a live Houmao gate
- **THEN** it uses deterministic adapter-simulated responses while writing the same generic UC-01 records expected from live mode

#### Scenario: Live validation is gated
- **WHEN** the UC-01 validation is requested against real Houmao
- **THEN** the system performs read-only capability checks before mutation, requires an explicit live-validation environment gate, reports skipped status when the gate is absent, and records cleanup status when live mutation occurs
