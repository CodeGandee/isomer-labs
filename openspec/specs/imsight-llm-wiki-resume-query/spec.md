# Purpose

Define the resume-query capability of `imsight-llm-wiki`, which lets a follow-up query load the most recent query output as context.

## Requirements

### Requirement: Query supports resume mode
The `query` subcommand SHALL support a `--resume` option that loads the most recent query output as context.

#### Scenario: User resumes the last query
- **WHEN** the user invokes `$imsight-llm-wiki use query to answer "<follow-up>" --resume`
- **THEN** the skill SHALL read the most recent `outputs/queries/*.md` file and treat it as context

### Requirement: Resume query identifies the prior question
The resume query workflow SHALL include the prior question and answer summary in the new answer.

#### Scenario: Follow-up answer generated
- **WHEN** a resume query produces an answer
- **THEN** the output SHALL reference the prior query slug and summarize the continuation

### Requirement: Resume query saves to a new file
The resume query workflow SHALL save the follow-up answer to a new `outputs/queries/<YYYY-MM-DD>-<follow-up-slug>.md` file.

#### Scenario: Resume query completes
- **WHEN** the follow-up answer is generated
- **THEN** it SHALL be saved as a new query output file

### Requirement: Resume query logs continuity
The resume query workflow SHALL append a log entry referencing the prior query.

#### Scenario: Resume query finishes
- **WHEN** a resume query completes
- **THEN** it SHALL append `## [HH:MM] query | <follow-up-slug> (resumed from <prior-slug>)`
