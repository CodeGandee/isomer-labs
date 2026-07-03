## ADDED Requirements

### Requirement: Tracked Topic Main Agent Rule Files
The system SHALL treat root-level `AGENTS.md` and `CLAUDE.md` in Topic Main Development Repository as tracked worker-facing guidance files.

#### Scenario: Topic main has rule files
- **WHEN** Topic Workspace environment setup prepares `topic.repos.main`
- **THEN** the repository contains root-level `AGENTS.md` and `CLAUDE.md`
- **AND** those files are normal topic-main files eligible for Git tracking
- **AND** they are not placed under `topic.repos.main.isomer_managed`, tmp paths, runtime paths, or external projection roots

#### Scenario: Existing repository content is not overwritten
- **WHEN** `topic.repos.main` already contains `AGENTS.md` or `CLAUDE.md`
- **THEN** Isomer preserves existing content outside the Isomer-managed guidance block
- **AND** Isomer does not reorder, normalize, delete, or rewrite unrelated rule-file sections

### Requirement: Isomer-Managed Topic Main Guidance Block
The system SHALL store Isomer-specific topic-main guidance in a fenced block with stable markers so the block can be updated idempotently.

#### Scenario: Guidance block uses stable boundaries
- **WHEN** Isomer writes topic-main guidance into `AGENTS.md` or `CLAUDE.md`
- **THEN** the guidance is bounded by `<!-- BEGIN isomer-labs-topic-main-guidance v1 -->` and `<!-- END isomer-labs-topic-main-guidance v1 -->`
- **AND** the guidance body is stored in a fenced block tagged `isomer-labs-topic-main-guidance`

#### Scenario: Guidance block is not duplicated
- **WHEN** Isomer updates `AGENTS.md` or `CLAUDE.md` and the file already contains a recognized Isomer-managed topic-main guidance block
- **THEN** Isomer updates the recognized block in place
- **AND** it does not append a duplicate block

#### Scenario: Guidance block avoids topic-specific values
- **WHEN** Isomer writes the topic-main guidance block
- **THEN** the block does not contain concrete Research Topic ids, topic statements, Topic Workspace paths, Topic Actor names, Agent Names, runtime file paths, credentials, external repository paths, resolved `manifest_path`, or resolved `pixi_environment`
- **AND** the block points agents to `isomer-cli` queries for those values
