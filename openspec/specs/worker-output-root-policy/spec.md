# worker-output-root-policy Specification

## Purpose
Define how Topic Actors and Agents resolve worker-local output roots, organize operation output sets, rely on Git ignore state for tracking, and apply post-operation commit preference.
## Requirements
### Requirement: Worker Output Roots Are Configurable
The system SHALL provide a worker output root for each Topic Actor and Agent Workspace, with a default root under the worker's private workspace and optional user configuration through Isomer-owned configuration.

#### Scenario: Topic Actor output root defaults inside actor workspace
- **WHEN** a Topic Actor named `operator` has no configured output root
- **THEN** the system resolves its worker output root under the resolved `topic.actors.workspace`
- **AND** the default relative path includes `isomer-managed/worker-output/topic-actors/operator`

#### Scenario: Agent output root defaults inside agent workspace
- **WHEN** an Agent named `writer` has no configured output root
- **THEN** the system resolves its worker output root under the resolved `agent.workspace`
- **AND** the default relative path includes `isomer-managed/worker-output/agents/writer`

#### Scenario: User configured output root is relative to private workspace
- **WHEN** a user configures a worker output root for a Topic Actor or Agent
- **THEN** the configured value is interpreted as a path relative to that worker's private workspace
- **AND** the system rejects absolute paths, parent traversal, Project Config Directory targets, cross-topic targets, and paths outside the selected worker workspace

### Requirement: Worker Output Sets Avoid Merge Conflicts
The system SHALL organize default worker output roots and generated operation output sets so branches from multiple Topic Actors or Agents can merge without colliding on common generated filenames.

#### Scenario: Default roots include worker identity
- **WHEN** two different workers use default output roots
- **THEN** their resolved default paths differ by worker kind and worker name
- **AND** identical generated filenames under those roots do not occupy the same repository-relative path

#### Scenario: Operation outputs use unique child sets
- **WHEN** a research operation writes plain generated outputs
- **THEN** the operation writes into a unique child output set under the resolved worker output root
- **AND** the child path includes an operation discriminator such as timestamp, stage, operation name, or short id

#### Scenario: Output root is not a loose file namespace
- **WHEN** a skill writes generated payloads, Markdown summaries, figures, previews, paper builds, CSVs, or other plain outputs
- **THEN** it does not write those files directly into the worker workspace root
- **AND** it does not write unrelated loose files directly into the worker output root when an operation set is appropriate

### Requirement: Git Ignore Rules Control Tracking
The system SHALL treat generated `.gitignore` files and normal Git status as the authority for whether worker output files are tracked or untracked.

#### Scenario: CLI does not duplicate tracking policy
- **WHEN** an agent queries the worker output policy
- **THEN** the response does not require a separate Isomer tracked-versus-untracked policy to decide file tracking
- **AND** the response indicates that Git ignore rules and Git status control whether output files are committable

#### Scenario: User edits to ignore rules are respected
- **WHEN** a user changes the relevant `.gitignore` rules for a worker output root
- **THEN** post-operation commit behavior follows the resulting Git status
- **AND** Isomer does not override those ignore rules merely because the output root is configured

### Requirement: Post-Operation Commit Preference Is Queryable
The system SHALL expose a per-worker `commit_after_operation` preference that agents can query and apply after research operations that write files.

#### Scenario: Commit preference defaults to false
- **WHEN** no Topic Actor or Agent-specific commit preference is configured
- **THEN** the resolved worker output policy reports `commit_after_operation` as false

#### Scenario: Topic Actor commit preference is resolved
- **WHEN** a Topic Actor has `commit_after_operation` configured
- **THEN** the worker output policy query reports that value for the selected Topic Actor

#### Scenario: Agent commit preference is resolved
- **WHEN** an Agent has `commit_after_operation` configured through an Agent default or override
- **THEN** the worker output policy query reports the effective value for the selected Agent

#### Scenario: Agent commits only when preference is true
- **WHEN** a research operation writes files and the resolved `commit_after_operation` value is true
- **THEN** the agent performs a post-action Git status check and commits committable operation output according to normal Git behavior
- **AND** when the value is false, the agent leaves generated files uncommitted and reports the output location

### Requirement: Worker Output Policy Is Queried Through Isomer CLI
Agents SHALL use `isomer-cli` to resolve worker output roots and post-operation commit preference instead of hard-coding actor or agent workspace paths.

#### Scenario: Actor output policy is queried
- **WHEN** a Topic Actor-scoped skill needs to write plain generated outputs
- **THEN** the skill can query the selected actor's output root and `commit_after_operation` preference through `isomer-cli` using a Topic Actor selector or cwd-derived Topic Actor context

#### Scenario: Agent output policy is queried
- **WHEN** an Agent-scoped skill needs to write plain generated outputs
- **THEN** the skill can query the selected agent's output root and `commit_after_operation` preference through `isomer-cli` using an Agent selector or cwd-derived Agent context

#### Scenario: Plain outputs remain distinct from accepted records
- **WHEN** a skill writes plain outputs under the worker output root
- **THEN** those files are not treated as accepted Artifacts, Evidence Items, Run records, Decision Records, or View Manifests until a separate accepted record or promotion action records them under the appropriate topic-owned surface

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

