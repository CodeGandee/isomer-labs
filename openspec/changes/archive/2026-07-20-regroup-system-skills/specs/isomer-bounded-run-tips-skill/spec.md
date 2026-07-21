## ADDED Requirements

### Requirement: Bounded Run Tips Is Protected Shared Support
The core public pack SHALL preserve logical capability `isomer-misc-bounded-run-tips` as protected shared member `bounded-run`.

#### Scenario: Protected bundle exists
- **WHEN** core pack assets are inspected
- **THEN** `operator/isomer-op-entrypoint/subskills/isomer-misc-bounded-run-tips/SKILL.md` exists
- **AND** its logical identity and release version remain valid

#### Scenario: Owning workflow requests bounded guidance
- **WHEN** a protected operator, service, or extension capability classifies a resource-heavy operation
- **THEN** it invokes `isomer-op-entrypoint->bounded-run` or includes the logical id through declared dependency closure
- **AND** the bounded-run capability preserves its existing risk classification and execution guidance

#### Scenario: Helper is not top-level
- **WHEN** ordinary host discovery runs
- **THEN** it does not list `isomer-misc-bounded-run-tips` as an independent user skill
