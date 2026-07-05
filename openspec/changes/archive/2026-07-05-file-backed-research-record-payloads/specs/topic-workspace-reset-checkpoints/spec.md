## ADDED Requirements

### Requirement: File-backed Reset Payload Records
Topic-reset checkpoint, plan, and outcome records SHALL store durable payload content as managed JSON files and use Markdown only as on-demand display or explicit export.

#### Scenario: Reset payload is file-backed
- **WHEN** `isomer-cli project topic-reset checkpoint`, `update-checkpoint`, `plan`, or `apply` creates a structured reset record
- **THEN** it writes the checkpoint, plan, or outcome payload to a managed JSON payload file and records locator, digest, schema/profile refs, status, and provenance in Workspace Runtime

#### Scenario: Reset Markdown is on demand
- **WHEN** an operator asks to inspect a reset checkpoint, plan, or outcome as Markdown
- **THEN** the command renders Markdown from the managed JSON payload through the selected template without requiring a durable generated Markdown file

#### Scenario: Reset export is explicit
- **WHEN** an operator asks to export a reset checkpoint, plan, or outcome as Markdown
- **THEN** the system writes a generated artifact snapshot with source payload digest, template refs, output locator, output digest, and provenance

#### Scenario: Reset validation follows payload files
- **WHEN** reset validation checks checkpoint, plan, or outcome records
- **THEN** it validates managed payload JSON files and recorded digests rather than using generated Markdown as the source of reset decisions
