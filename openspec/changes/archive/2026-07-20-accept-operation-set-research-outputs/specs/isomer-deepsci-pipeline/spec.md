## ADDED Requirements

### Requirement: DeepSci Pipeline Requires Accepted Stage Outputs
`isomer-deepsci-pipeline` SHALL advance between stages using verified durable record refs and operation-set closeout status rather than plain file paths.

#### Scenario: Stage with files hands off a complete receipt
- **WHEN** a pipeline stage produces material operation-set files and otherwise satisfies its continue condition
- **THEN** the pipeline verifies that stage's complete acceptance receipt and passes the resulting durable record refs to the next stage

#### Scenario: Stage without files declares closeout not applicable
- **WHEN** a stage opens no operation set and produces or consumes only durable records
- **THEN** the stage handoff records `closeout: not_applicable` with those durable refs and may continue

#### Scenario: Partial acceptance stops progression
- **WHEN** a stage has a missing, partial, stale, or unverifiable acceptance receipt
- **THEN** the pipeline does not start the next stage and emits a paused terminal report with the stage id and receipt recovery action

#### Scenario: File path is not an artifact handoff
- **WHEN** a stage reports only a worker output path or terminal prose for a produced artifact
- **THEN** the pipeline treats the artifact as unavailable until a durable record ref is accepted and verified

### Requirement: Pipeline Completion Reports Acceptance Evidence
The DeepSci pipeline SHALL include operation-set closeout evidence in its terminal report and SHALL reconcile any pipeline-level material files before reporting `status: complete`.

#### Scenario: Successful terminal report lists receipts
- **WHEN** every stage and the pipeline itself complete successfully
- **THEN** the terminal report lists each applicable acceptance receipt id, accepted durable record refs, any `not_applicable` closeouts, the final artifact ref, and the recommended next action

#### Scenario: Pipeline-level report file is reconciled
- **WHEN** the controller writes a pipeline-level report or other material file into its own operation set
- **THEN** it accepts and verifies that set before the terminal status becomes `complete`

#### Scenario: Terminal acceptance failure pauses pipeline
- **WHEN** pipeline-level closeout cannot complete after all research stages ran
- **THEN** the terminal report uses `status: paused`, preserves completed stage refs, and provides the acceptance resume point
