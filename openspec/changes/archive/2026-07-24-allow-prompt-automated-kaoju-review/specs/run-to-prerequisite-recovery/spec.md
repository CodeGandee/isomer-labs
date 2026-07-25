## MODIFIED Requirements

### Requirement: Run-To Stops at Nondelegable Boundaries
The system SHALL stop an authorized run-to traversal when continuation requires authority or information outside the target-scoped run-to grant and any explicit prompt-scoped review delegation.

#### Scenario: Automatable review is explicitly delegated
- **WHEN** continuation reaches a Kaoju review checkpoint that the current prompt explicitly delegates for the named run-to target
- **THEN** the focused owner may perform and record that review without pausing for another user turn
- **AND** it preserves validation, evidence, mutation ownership, Run, Gate, Artifact, and provenance boundaries

#### Scenario: Review checkpoint is not delegated
- **WHEN** continuation reaches an automatable Kaoju review checkpoint and the current prompt does not delegate that review
- **THEN** the system checkpoints completed work and pauses for the human review decision
- **AND** it presents the exact candidate, decision, accepted refs, and resume point

#### Scenario: Nondelegable Gate is reached
- **WHEN** continuation requires a material goal change outside delegated review, a destructive or irreversible action, credentials or restricted data, a material license decision, unexpected resource authorization, public exposure, publication acceptance, external publication, submission, or a materially ambiguous choice
- **THEN** the system checkpoints completed work and pauses at that boundary
- **AND** it presents the exact decision or authorization required to resume the same target

#### Scenario: User interrupts traversal
- **WHEN** the user asks the agent to stop, changes the target, or revokes run-to or review authorization
- **THEN** the system stops starting new prerequisite or review work
- **AND** it reports completed refs and the current resume point without applying the former authorization to the new target
