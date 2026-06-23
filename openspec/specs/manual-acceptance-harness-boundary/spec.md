# manual-acceptance-harness-boundary Specification

## Purpose
TBD - created by archiving change move-uc01-acceptance-harness-out-of-src. Update Purpose after archive.
## Requirements
### Requirement: Manual Acceptance Harness Location
Use-case-specific acceptance implementations SHALL live outside `src/isomer_labs` unless a later accepted product spec explicitly promotes the use case into the core system.

#### Scenario: UC-01 harness lives in tests manual
- **WHEN** the UC-01 headless vertical slice is implemented as an acceptance path
- **THEN** its case-specific constants, deterministic fixture outputs, route choices, graph assertions, and runner entry point live under `tests/manual/uc01_headless_vertical_slice/`

#### Scenario: Source tree excludes named use-case orchestration
- **WHEN** source architecture tests scan `src/isomer_labs`
- **THEN** they fail if package modules such as `workflows/uc01.py`, `workflows/uc07.py`, or other named use-case orchestration modules appear without an accepted product spec

### Requirement: Harness Uses Generic Core Surfaces
Manual acceptance harnesses SHALL drive reusable Isomer platform APIs or generic CLI commands rather than depending on named use-case product commands.

#### Scenario: Harness drives generic commands
- **WHEN** the UC-01 manual harness prepares runtime state, creates or inspects Agent Team Instance records, dispatches or simulates handoffs, or validates output
- **THEN** it uses generic Isomer runtime, handoff, adapter, and validation surfaces rather than `isomer-cli uc01` commands

#### Scenario: Harness output is deterministic
- **WHEN** a manual acceptance harness completes in simulated mode
- **THEN** it prints or returns deterministic JSON containing `ok`, mode, selected route classification when applicable, key record refs or counts, diagnostics, and live-gate skipped status when live validation is not enabled

### Requirement: Harness Owns Case-Specific Truth
Manual acceptance harnesses SHALL own pinned use-case truth that would be inappropriate in core source modules.

#### Scenario: UC-01 pins fixture ids in harness
- **WHEN** UC-01 references Research Topic `flash-attention-gb10-peak-performance-optimization`, seed Research Inquiry `gb10-flash-attention-4-direction-selection`, or Research Task `map-gb10-flash-attention-optimization-directions`
- **THEN** those ids are declared in the UC-01 harness or fixture Project rather than in `src/isomer_labs`

#### Scenario: Fixture outputs remain test material
- **WHEN** UC-01 needs deterministic seed-source summaries, Flash Attention notes, GB10 feature notes, Evidence Items, Findings, View Manifest inputs, or follow-up inquiry options
- **THEN** that deterministic content is stored in the fixture Project or manual harness and is not embedded in core package modules

### Requirement: Core Extraction Requires Reuse
Behavior SHALL be promoted from a manual harness into `src/isomer_labs` only when it is reusable platform behavior rather than a single use-case workflow.

#### Scenario: Generic runtime helper is allowed
- **WHEN** UC-01 and future use cases need the same provider-neutral lifecycle record helper, runtime query helper, or validation helper
- **THEN** that helper may be implemented in an accepted core package with names that use Isomer domain language and no pinned use-case ids

#### Scenario: Single-use helper remains in harness
- **WHEN** a helper is only needed to generate UC-01 deterministic Artifacts or assert UC-01 route closeout
- **THEN** the helper remains in `tests/manual/uc01_headless_vertical_slice/` until reuse is demonstrated and specified

