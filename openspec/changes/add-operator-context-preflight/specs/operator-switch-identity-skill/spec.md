## ADDED Requirements

### Requirement: Switched Posture Is Propagated as Session-Local Invocation Context
The identity-switch skill SHALL carry an active Topic Actor or Agent posture through downstream context checks, explicit command selectors, cwd discipline, and provenance without creating shared persistent identity state.

#### Scenario: Switch creates a complete posture envelope
- **WHEN** a one-task, `act-as`, or persistent switch resolves successfully
- **THEN** the operator session remembers target kind, Research Topic, worker name, resolved worker workspace, persistence mode, and provenance posture for the switch lifetime
- **AND** it does not infer any required field solely from workspace directory scanning or an unrelated manifest default

#### Scenario: Switched command pins selectors and cwd
- **WHEN** the operator executes a topic- or worker-scoped command under an active switch
- **THEN** it uses the switched worker workspace as default cwd and supplies explicit Research Topic and Topic Actor or Agent selectors when the command supports them
- **AND** it checks that the supplied target resolves to the remembered worker workspace before mutation

#### Scenario: Command outside switched cwd retains target
- **WHEN** a switched task requires a command from another resolved semantic path
- **THEN** the operator states why that cwd is required and retains explicit switched topic and worker selectors
- **AND** the cwd change does not reset or silently replace the active posture

#### Scenario: Manifest fallback does not activate switch
- **WHEN** `project self identity` reports a Topic Actor with source `manifest default` and no switch was requested
- **THEN** identity-switch status remains normal Project Operator posture
- **AND** the skill does not claim that the operator switched or that an independent Topic Actor performed work

#### Scenario: Persistent posture is not shared Project state
- **WHEN** the user requests a persistent switch
- **THEN** the posture remains available only to the current operator session until reset or replacement
- **AND** the skill does not write it to Project Manifest, local active context, Topic Workspace Manifest, Workspace Runtime, or another session-visible current-identity file

#### Scenario: Reset removes propagated posture
- **WHEN** the user resets a persistent switch
- **THEN** later plans stop applying the previous worker cwd and explicit worker selectors
- **AND** normal Project Operator provenance is restored without mutating worker topology or runtime identity records
