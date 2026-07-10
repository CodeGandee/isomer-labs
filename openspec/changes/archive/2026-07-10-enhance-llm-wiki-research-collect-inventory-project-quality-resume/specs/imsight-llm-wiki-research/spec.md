## ADDED Requirements

### Requirement: Research subcommand discovers sources
The `imsight-llm-wiki` skill SHALL provide a `research` subcommand that accepts a topic string and discovers relevant web sources.

#### Scenario: User requests research on a topic
- **WHEN** the user invokes `$imsight-llm-wiki use research to research "<topic>"`
- **THEN** the skill SHALL search the web for sources related to the topic

### Requirement: Research results are ranked and filtered
The research workflow SHALL evaluate discovered sources for relevance and signal quality before ingestion.

#### Scenario: Low-quality sources are excluded
- **WHEN** the research workflow receives search results
- **THEN** it SHALL skip paywalled, duplicate, or low-relevance sources unless the user explicitly requests inclusion

### Requirement: Research ingests selected sources
The research workflow SHALL ingest high-signal sources through the same pipeline as the existing `ingest` subcommand.

#### Scenario: Selected sources become wiki pages
- **WHEN** the research workflow selects one or more sources
- **THEN** it SHALL create `raw/`, `wiki/summaries/`, and update `wiki/concepts/` and `wiki/index.md` following the existing ingest conventions

### Requirement: Research requires user confirmation for ingestion
The research workflow SHALL present the list of discovered sources and wait for user confirmation before ingesting, unless the user explicitly requests automatic ingestion.

#### Scenario: User confirms research results
- **WHEN** the research workflow presents discovered sources
- **THEN** it SHALL ingest only the sources the user approves

### Requirement: Research logs its operation
The research workflow SHALL append a log entry to the current day's `log/YYYYMMDD.md`.

#### Scenario: Research completes
- **WHEN** research ingestion finishes
- **THEN** it SHALL append `## [HH:MM] research | <topic> — ingested N sources (touched M pages)`
