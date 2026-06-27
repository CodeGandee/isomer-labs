## ADDED Requirements

### Requirement: Topic Env Setup Consumes Storage Contract
The service environment setup skill SHALL resolve setup file surfaces through Workspace Path Resolution before reading, writing, or reporting them.

#### Scenario: Setup repo uses resolved semantic label
- **WHEN** topic environment setup checks or mutates the setup repository surface
- **THEN** it uses the resolved semantic label for that surface, reports source metadata, and does not assume `repos/topic-main` or another default physical path

#### Scenario: Custom setup surface is accepted
- **WHEN** `env-gate.md`, setup notes, or operator input names a valid `custom.*` semantic label for setup material
- **THEN** the service resolves that label, validates safety and storage-profile-derived traits, and uses the resolved path for the dependent setup step

#### Scenario: Unknown setup label blocks mutation
- **WHEN** setup material names a semantic label that Workspace Path Resolution cannot resolve
- **THEN** the service reports a setup blocker and does not create a guessed path

### Requirement: Topic Env Setup Reports Durable and Disposable Surfaces Separately
The service environment setup skill SHALL use storage-profile-derived lifecycle traits to distinguish durable setup evidence from disposable local material.

#### Scenario: Disposable custom label is not durable evidence
- **WHEN** a custom semantic label uses a `storage_profile` with disposable lifecycle
- **THEN** the service omits files under that label from durable readiness evidence unless they are promoted to an accepted durable semantic surface

#### Scenario: Durable custom label may carry setup evidence
- **WHEN** a custom semantic label uses a `storage_profile` with durable lifecycle and passes safety validation
- **THEN** the service may report files under that label as changed files or setup evidence with semantic label and source metadata
