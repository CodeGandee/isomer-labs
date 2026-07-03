## ADDED Requirements

### Requirement: Research Skills Resolve Worker Output Policy
Active v2 research-paradigm skills that write plain files SHALL resolve the current worker output policy through `isomer-cli` before choosing output paths.

#### Scenario: Plain file writing requires output policy
- **WHEN** a v2 research skill will write plain generated outputs such as JSON payload staging files, Markdown drafts, CSVs, figures, paper previews, paper builds, or local reports
- **THEN** the skill guidance tells the agent to resolve the worker output root and `commit_after_operation` preference through `isomer-cli`
- **AND** the skill does not direct the agent to write new generated files directly into the actor or agent workspace root

#### Scenario: Durable records still use record bindings
- **WHEN** a v2 research skill creates an accepted Artifact, Evidence Item, Run record, Decision Record, View Manifest, or other durable research record
- **THEN** the skill continues to use the applicable record binding or `topic.records.*` surface
- **AND** worker output roots are treated as plain output staging or worker-local material unless a promotion or record creation step accepts the material

#### Scenario: Operation outputs use operation sets
- **WHEN** a v2 research skill writes multiple plain outputs for one research operation
- **THEN** the skill guidance tells the agent to place them under one operation-specific child of the resolved worker output root
- **AND** the operation set name includes a discriminator that prevents repeated operations from overwriting each other

### Requirement: Research Skills Apply Post-Operation Commit Preference
Active v2 research-paradigm skills SHALL check the effective `commit_after_operation` preference after research operations that write files and apply it as a post-action step.

#### Scenario: Commit preference true triggers Git status and commit
- **WHEN** a research operation writes files and the resolved worker output policy reports `commit_after_operation=true`
- **THEN** the skill guidance tells the agent to inspect Git status after writing
- **AND** it tells the agent to commit committable changes according to normal Git behavior and the configured worker preference

#### Scenario: Commit preference false leaves workspace uncommitted
- **WHEN** a research operation writes files and the resolved worker output policy reports `commit_after_operation=false`
- **THEN** the skill guidance tells the agent not to commit merely because files were written
- **AND** it tells the agent to report the output location and any dirty workspace status relevant to the user

#### Scenario: Git ignore controls what can be committed
- **WHEN** a skill applies post-operation commit behavior
- **THEN** the skill guidance treats `.gitignore` and Git status as the authority for which output files are tracked, untracked, ignored, or committable
- **AND** it does not ask the agent to override ignore rules unless the user explicitly requests that change

### Requirement: Research Skill Validation Covers Output Policy Guidance
The research-paradigm validation harness SHALL report active v2 research skill entrypoints or references that write plain files without referencing worker output policy resolution.

#### Scenario: Missing output policy guidance is reported
- **WHEN** validation inspects an active v2 research skill that mentions plain file outputs but lacks output-policy resolution guidance
- **THEN** validation reports the skill and explains that generated plain outputs must use the worker output root resolved through `isomer-cli`

#### Scenario: Commit preference guidance is required
- **WHEN** validation inspects an active v2 research skill that performs research operations with file writes
- **THEN** validation confirms the skill includes post-operation guidance to check `commit_after_operation`

#### Scenario: Non-active material is exempt
- **WHEN** validation inspects migration notes, source-copy material under `org/`, passive templates, license files, or provenance material
- **THEN** validation does not require those files to include worker output policy guidance
