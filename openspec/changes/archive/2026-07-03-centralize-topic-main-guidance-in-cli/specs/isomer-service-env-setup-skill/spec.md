## ADDED Requirements

### Requirement: Service Uses CLI Topic Main Guidance Source
The service environment setup skill SHALL use `isomer-cli project topic-main-guidance` as the source of truth for topic-main agent guidance content and file mutation.

#### Scenario: Ensure topic main routes to CLI
- **WHEN** `ensure-topic-main-repository` needs to create, inspect, append, or update root `AGENTS.md` or `CLAUDE.md` guidance
- **THEN** the skill instructions route that operation through `isomer-cli --print-json project topic-main-guidance ensure --topic <topic> --yes` or an equivalent CLI-backed API
- **AND** the skill documentation does not include the full injected guidance body

#### Scenario: Service reports CLI output
- **WHEN** topic env setup carries topic-main guidance posture into predecessor evidence
- **THEN** it reports the CLI guidance version, target statuses, changed files, blockers, and next action returned by the guidance command

#### Scenario: Service does not duplicate template text
- **WHEN** service skillset validation inspects topic env setup documentation
- **THEN** it accepts concise references to the CLI command, marker names, and `.j2` template source of truth
- **AND** it reports diagnostics if the service docs reintroduce the full guidance block body as copied prose
