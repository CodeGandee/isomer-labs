## ADDED Requirements

### Requirement: Payload-file Research Record Guidance
Production DeepSci system skills SHALL teach agents to create durable structured records as JSON payload files managed by the research recording CLI.

#### Scenario: Skill workflow creates payload records
- **WHEN** a production DeepSci skill instructs an agent to create an accepted durable structured output
- **THEN** it tells the agent to draft JSON, validate the payload, call the record create or update command, and let Workspace Runtime snapshot the payload file into managed storage

#### Scenario: Skill workflow does not grow generated Markdown
- **WHEN** a production DeepSci skill describes repeated research rounds
- **THEN** it tells the agent to create new payload-backed records, snapshots, or revision links rather than appending to or overwriting generated Markdown files

#### Scenario: Skill workflow renders only for review
- **WHEN** a production DeepSci skill mentions Markdown review
- **THEN** it frames Markdown as on-demand display or explicit export from payload JSON, not as the accepted durable record itself

#### Scenario: Skill validation checks payload-file contract
- **WHEN** the research-paradigm validation harness scans active production DeepSci guidance
- **THEN** it reports instructions that make SQLite payload blobs or generated Markdown files the canonical accepted-output content for structured records
