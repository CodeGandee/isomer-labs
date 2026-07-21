## ADDED Requirements

### Requirement: Entrypoint Performs Context-Sensitive Preflight
The operator entrypoint SHALL classify operation scope, reconcile task-selected targets, and pin resolved context before executing a context-sensitive route.

#### Scenario: Prompt topic becomes explicit selector
- **WHEN** a concrete user task names one Research Topic and the entrypoint selects a topic-scoped owner, extension, or CLI route
- **THEN** the entrypoint supplies that Research Topic to self preflight as an explicit selector
- **AND** every downstream topic-scoped CLI call retains the resolved `--topic` selector even when cwd or Project Manifest defaults could also select a topic

#### Scenario: Project-scoped task ignores topic fallback
- **WHEN** the selected operation is Project-scoped
- **THEN** the entrypoint does not reinterpret the task as topic-scoped merely because Effective Topic Context can resolve a current-directory or Project Manifest default topic
- **AND** it uses topic context only if the selected Project operation explicitly requires a topic target

#### Scenario: Implicit default is visible and pinned
- **WHEN** a topic-scoped task names no Research Topic and preflight validly selects the Project Manifest default
- **THEN** the entrypoint reports that selection source
- **AND** it pins the resolved topic on subsequent routed commands so later cwd changes cannot change the target

#### Scenario: Worker-scoped task reconciles identity posture
- **WHEN** a route requires Topic Actor or Agent scope
- **THEN** the entrypoint requires an explicit worker target or active session switch posture, resolves its semantic workspace, and checks alignment
- **AND** it does not treat a sole manifest actor fallback as proof that the Project Operator is actively acting as that actor

#### Scenario: Context conflict stops before route mutation
- **WHEN** prompt target, active switch posture, explicit selectors, or unresolved implicit sources produce an incompatible context
- **THEN** the entrypoint stops before mutation and reports the conflicting sources and corrective selector, cwd, or reset action
- **AND** it does not choose a sibling topic, alternate worker, or alternate output directory as recovery

#### Scenario: Typed failure preserves original target
- **WHEN** the routed typed command fails after context has been pinned
- **THEN** the entrypoint preserves the original target while diagnosing or rerouting the failure
- **AND** it does not perform an unmanaged filesystem copy or change the output surface unless the user explicitly requests a separate operation
