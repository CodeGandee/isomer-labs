## ADDED Requirements

### Requirement: Material Operation Sets Are Reconciled at Closeout
Research workflows SHALL reconcile material operation-set files through the Operation Set Acceptance contract before treating the operation as successfully complete.

#### Scenario: Material files require closeout
- **WHEN** a worker operation set contains any regular file outside the reserved coordinator control directory
- **THEN** the workflow obtains a complete acceptance receipt that maps every file to a durable record or an explicit disposable reason

#### Scenario: Git tracking does not satisfy closeout
- **WHEN** operation-set files are committed, ignored, untracked, or clean in Git
- **THEN** that Git state does not replace durable research-record acceptance or an explicit disposable disposition

#### Scenario: No operation set was opened
- **WHEN** a bounded research action writes no plain generated files and opens no operation set
- **THEN** its terminal result may record closeout as `not_applicable` without creating an empty acceptance receipt

#### Scenario: Incomplete closeout pauses completion
- **WHEN** a material file remains unclassified or a promised record, lineage edge, or Research Idea effect cannot be verified
- **THEN** the workflow reports a recoverable paused outcome with the manifest, diagnostics, and resume action instead of reporting success
