## ADDED Requirements

### Requirement: Use-Case Source Boundary
The system SHALL keep named use-case acceptance orchestration out of `src/isomer_labs` unless a future accepted product spec explicitly promotes that use case into core Isomer behavior.

#### Scenario: Named use-case modules are rejected
- **WHEN** repository tests scan `src/isomer_labs`
- **THEN** they report named use-case orchestration modules or packages such as `uc01`, `uc07`, or `uc06` under source implementation paths unless the allowed package list has been deliberately updated by an accepted spec

#### Scenario: Core package names stay generic
- **WHEN** a new package is introduced under `src/isomer_labs`
- **THEN** its name describes a reusable Isomer platform boundary such as CLI, runtime, adapter, template, profile, validation, or another accepted domain concept rather than a use-case id

#### Scenario: Reusable helpers contain no pinned use-case ids
- **WHEN** code is promoted from a manual harness into `src/isomer_labs`
- **THEN** the promoted code does not hardcode pinned Research Topic ids, use-case names, deterministic fixture outputs, selected route classifications, or acceptance-only record ids

### Requirement: Manual Harnesses Are Not Architecture Violations
The architecture guardrail SHALL allow case-specific code under `tests/manual/<harness>/` while continuing to protect `src/isomer_labs`.

#### Scenario: Manual harness package is allowed
- **WHEN** a use-case acceptance harness is organized as Python modules under `tests/manual/uc01_headless_vertical_slice/`
- **THEN** source architecture tests do not treat that manual harness as a product package boundary

#### Scenario: Harness import direction is one-way
- **WHEN** source modules under `src/isomer_labs` are scanned
- **THEN** they do not import from `tests.manual`, fixture Projects, or use-case harness modules

### Requirement: Generic Core Additions Remain Allowed
The architecture boundary SHALL preserve reusable platform additions needed by acceptance harnesses.

#### Scenario: Generic lifecycle support stays in core
- **WHEN** the platform needs provider-neutral lifecycle record kinds, statuses, persistence, or validation that apply beyond one use case
- **THEN** that code may remain in `src/isomer_labs/runtime` or another accepted core package

#### Scenario: Built-in team templates stay in core registries
- **WHEN** a Domain Agent Team Template such as `deepsci-mini` is reusable across UC-01, UC-07, or later milestones
- **THEN** its built-in registration and validation support may remain in core template discovery code
