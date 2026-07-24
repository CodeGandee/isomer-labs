## ADDED Requirements

### Requirement: Kaoju Resolves Review Mode from Explicit Prompt Delegation
Kaoju SHALL default automatable review checkpoints to human review and SHALL use agent review only when the current prompt explicitly delegates the applicable checkpoint or a semantically clear set of checkpoints for a named target.

#### Scenario: Prompt is silent about review mode
- **WHEN** a Kaoju procedure reaches an automatable review checkpoint and the current prompt does not delegate that review
- **THEN** the procedure presents the candidate decision or artifact for human review
- **AND** it pauses before acceptance or the reviewed action

#### Scenario: Prompt explicitly delegates review
- **WHEN** the current prompt explicitly asks the agent to review and accept a named checkpoint or clearly delegates review checkpoints through a named target
- **THEN** the procedure may review, revise, narrow, reject, or accept the candidate without another user turn
- **AND** it records the agent-review posture, prompt-scoped basis, rationale, actor, affected refs, and terminal or resume posture through existing owner-supported provenance

#### Scenario: Run-to does not mention review delegation
- **WHEN** the user authorizes `run to <target>` or routine prerequisite automation without semantically delegating review
- **THEN** the run-to controller automates only the authorized routine closure
- **AND** human review remains the default at automatable review checkpoints

#### Scenario: Review delegation is ambiguous
- **WHEN** automation wording does not establish which target or review checkpoints it covers
- **THEN** the procedure asks for clarification or retains human review
- **AND** it does not infer session-wide or global approval

#### Scenario: Review delegation reaches its boundary
- **WHEN** the named target completes, the user changes the target, or a checkpoint lies outside the delegated set
- **THEN** the prompt-scoped agent-review posture expires for that work
- **AND** later checkpoints return to human review unless a current prompt explicitly delegates them

### Requirement: Kaoju Separates Automatable Review from Protected Authorization
Kaoju SHALL treat explore handoff, Direction Set review, Reading List review, Comparison Intent review, bounded trial-plan review, paper structure and draft review, and bounded local paper-build authorization as prompt-delegable review checkpoints while preserving protected authorization boundaries.

#### Scenario: Agent review remains inside accepted scope
- **WHEN** an explicitly delegated agent review can decide within accepted evidence, meaning, inputs, resources, attempt bounds, validation rules, and target scope
- **THEN** the focused owner may complete that review without a new human turn
- **AND** all ordinary audit, validation, ownership, recording, and evidence requirements remain in force

#### Scenario: Protected boundary is encountered
- **WHEN** continuation needs credentials, private or restricted data, a material license decision, a destructive or irreversible action, unexpected cost or resource expansion, public network exposure, publication acceptance, external publication, or submission
- **THEN** generic review delegation does not satisfy the applicable authorization
- **AND** the procedure pauses for the exact owner-specific decision or authorization

#### Scenario: Candidate fails validation
- **WHEN** an agent-reviewed candidate lacks required evidence, violates the contract, or fails validation
- **THEN** the agent rejects, revises, narrows, or pauses the candidate according to the focused owner contract
- **AND** it does not treat automated review as automatic acceptance

## MODIFIED Requirements

### Requirement: Kaoju Run-To Preserves Interaction and Gate Contracts
Kaoju run-to SHALL automate routine in-scope prerequisite routing and explicitly delegated review checkpoints while preserving nondelegable clarification, resource, publication, external-side-effect, and authorization contracts.

#### Scenario: Routine prerequisite is discovered
- **WHEN** a protected member or public procedure reports a routine producible prerequisite
- **THEN** the entrypoint may invoke its declared owner under active run-to authorization

#### Scenario: Prompt delegates an automatable review checkpoint
- **WHEN** active target-scoped run-to authorization includes semantically explicit delegation of an applicable Kaoju review checkpoint
- **THEN** the focused owner may perform and record that review without a new user turn
- **AND** the delegation does not transfer mutation authority or waive evidence and validation requirements

#### Scenario: Protected boundary is reached
- **WHEN** continuation requires an unresolved material choice outside delegated review, a nondelegable Gate, unauthorized resources, an external side effect, or a no-progress repeat
- **THEN** the entrypoint pauses with the current durable state and precise resume guidance
