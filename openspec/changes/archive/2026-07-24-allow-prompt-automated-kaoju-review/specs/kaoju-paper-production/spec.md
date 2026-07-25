## ADDED Requirements

### Requirement: Paper Review Defaults to Human and Supports Prompt Delegation
The Kaoju write workflow SHALL use human review by default for paper structure, draft acceptance, and bounded local build authorization and SHALL permit agent review only when the current prompt explicitly delegates the applicable review for a named paper target.

#### Scenario: Human paper review remains the default
- **WHEN** a paper structure, canonical MyST draft, or local PDF build plan is ready and the current prompt has not delegated its review
- **THEN** the write workflow presents the applicable structure, draft, or build plan for human revision or authorization
- **AND** it pauses before acceptance or build execution

#### Scenario: Prompt delegates structure and draft review
- **WHEN** the current prompt explicitly asks the agent to review and accept the paper structure and draft for a named paper target
- **THEN** the write skill may select and revise the adaptive structure, draft from accepted evidence, validate the canonical MyST, and accept the validated revision without another user turn
- **AND** it records the agent-review posture, prompt basis, structure rationale, revision rationale, evidence refs, validation result, and accepted paper refs

#### Scenario: Prompt delegates a bounded local PDF build
- **WHEN** the current prompt explicitly delegates local build-plan review and execution within the accepted template, toolchain, dependencies, resource boundary, and paper meaning
- **THEN** the write skill may authorize and execute the local build without another user turn after all TeX obligations and validation prerequisites pass
- **AND** it records the agent-review posture, build authorization basis, exact build Run, compile log, resource use, and validation result

#### Scenario: Material paper repair exceeds delegation
- **WHEN** a proposed repair changes canonical content meaning, evidence interpretation, dependencies, build profile, toolchain policy, or resources beyond the prompt-delegated boundary
- **THEN** the workflow pauses for a revised plan and the applicable authorization
- **AND** it does not apply the repair under prior agent review

#### Scenario: Publication checkpoint is reached
- **WHEN** a locally built paper reaches publication acceptance, external publication, or submission
- **THEN** generic paper-review delegation does not satisfy the configured publication Gate
- **AND** the workflow follows the existing publication authorization and provenance contract
