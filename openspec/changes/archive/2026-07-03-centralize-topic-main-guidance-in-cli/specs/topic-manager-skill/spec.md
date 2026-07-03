## ADDED Requirements

### Requirement: Topic Manager Uses CLI Topic Main Guidance Source
The Topic Manager skill SHALL use `isomer-cli project topic-main-guidance` as the source of truth for topic-main agent guidance inspection and repair.

#### Scenario: Storage inspection routes guidance checks to CLI
- **WHEN** `storage-inspect-main` reports root `AGENTS.md` and `CLAUDE.md` guidance posture
- **THEN** it routes the read-only check through `isomer-cli --print-json project topic-main-guidance inspect --topic <topic>` or an equivalent CLI-backed API
- **AND** it reports target statuses, guidance version, blockers, and next action from that command

#### Scenario: Storage repair routes guidance mutation to CLI
- **WHEN** the operator explicitly requests topic-main agent guidance repair or refresh
- **THEN** the Topic Manager routes mutation through `isomer-cli --print-json project topic-main-guidance ensure --topic <topic> --yes` or an equivalent CLI-backed API
- **AND** it does not carry the full guidance body in the skill instructions

#### Scenario: Topic Manager does not duplicate template text
- **WHEN** operator skillset validation inspects Topic Manager documentation
- **THEN** it accepts concise references to the CLI command, marker names, and `.j2` template source of truth
- **AND** it reports diagnostics if Topic Manager docs reintroduce the full guidance block body as copied prose
