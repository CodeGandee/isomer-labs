## ADDED Requirements

### Requirement: Project Manager Reconciles Operator Extensions After Initialization
The project-manager skill SHALL delegate additive system-extension reconciliation after successful operator-controlled Project initialization unless the user opts out.

#### Scenario: Operator-controlled init reconciles extensions
- **WHEN** `init-project` successfully runs direct `isomer-cli project init` from an active Project Operator Session
- **THEN** the project manager delegates to `isomer-op-system-skill-mgr reconcile-extensions`
- **AND** complete receipt-backed or live-inventory extensions are remembered in the new Project Manifest

#### Scenario: User opts out
- **WHEN** the user instructs the project manager not to register detected extensions
- **THEN** `init-project` skips mutating reconciliation
- **AND** it may report read-only extension observations and later registration advice

#### Scenario: Direct CLI init remains separate
- **WHEN** guidance distinguishes operator-controlled initialization from a user directly invoking `isomer-cli project init`
- **THEN** it explains that direct CLI initialization does not know the active agent inventory and does not register extensions automatically

#### Scenario: Reconciliation failure does not hide initialized Project
- **WHEN** Project initialization succeeds but delegated extension reconciliation fails
- **THEN** the project manager reports the Project as initialized and extension reconciliation as a distinct partial outcome
- **AND** it provides a retry route through the system-skill manager
