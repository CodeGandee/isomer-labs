## ADDED Requirements

### Requirement: Placeholder Bindings Use Payload-file Records
Active production DeepSci placeholder binding pages SHALL describe accepted structured outputs as payload-file records rather than durable generated Markdown files.

#### Scenario: Binding names payload file write
- **WHEN** `placeholder-bindings.md` describes a structured placeholder output
- **THEN** the binding tells the agent to draft a JSON payload file, validate it, and create or update the durable record through `isomer-cli ext research records` so the runtime snapshots the payload into managed record storage

#### Scenario: Binding omits default durable Markdown
- **WHEN** a binding gives the normal accepted-output create or update command
- **THEN** the command does not request default durable Markdown materialization for the structured record

#### Scenario: Binding describes on-demand rendering
- **WHEN** a binding mentions human review of a structured record
- **THEN** it points to an on-demand show, render, query, or explicit export command rather than a normally generated Markdown file path

#### Scenario: Binding validation rejects Markdown state
- **WHEN** the validation harness inspects active production DeepSci placeholder bindings
- **THEN** it reports guidance that treats generated Markdown as canonical structured state, expects generated Markdown to grow across rounds, or requires later agents to parse generated Markdown for structured fields
