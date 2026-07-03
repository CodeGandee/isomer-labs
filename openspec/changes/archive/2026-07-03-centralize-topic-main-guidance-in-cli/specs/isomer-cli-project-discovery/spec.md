## ADDED Requirements

### Requirement: Topic Main Guidance CLI
The `isomer-cli project` command surface SHALL expose topic-main guidance rendering, inspection, and ensure commands backed by a packaged Jinja2 template asset.

#### Scenario: Guidance commands appear in command surface
- **WHEN** a user runs `isomer-cli --help` or `isomer-cli project --help`
- **THEN** the command surface includes `project topic-main-guidance render`, `project topic-main-guidance inspect`, and `project topic-main-guidance ensure`

#### Scenario: Render uses packaged template
- **WHEN** a user runs `isomer-cli project topic-main-guidance render`
- **THEN** the command renders the current Isomer topic-main guidance block from a packaged `.j2` template asset
- **AND** Python source code does not own the large guidance prose as a multiline string
- **AND** the rendered text includes the current begin marker, end marker, and `isomer-labs-topic-main-guidance` fenced block tag

#### Scenario: Render is topic independent
- **WHEN** `project topic-main-guidance render` runs from any directory
- **THEN** it does not require a selected Research Topic, Topic Workspace, Topic Main Development Repository, or Project Manifest
- **AND** it does not include resolved Research Topic ids, topic statements, Topic Workspace paths, Topic Actor names, Agent Names, runtime paths, credentials, external repository paths, resolved `manifest_path`, or resolved `pixi_environment`

#### Scenario: Inspect reports target statuses
- **WHEN** `isomer-cli --print-json project topic-main-guidance inspect --topic <topic>` runs with a resolvable `topic.repos.main`
- **THEN** the output reports one target entry for root `AGENTS.md` and one target entry for root `CLAUDE.md`
- **AND** each target reports a status such as `missing`, `current`, `stale`, `duplicate`, `malformed`, `unknown_version`, or `unsafe`
- **AND** the command does not create or modify files

#### Scenario: Ensure requires explicit write confirmation
- **WHEN** `project topic-main-guidance ensure` is invoked without `--yes`
- **THEN** the command reports a deterministic blocker or usage diagnostic
- **AND** it does not create or modify `AGENTS.md` or `CLAUDE.md`

#### Scenario: Ensure upserts guidance idempotently
- **WHEN** `isomer-cli --print-json project topic-main-guidance ensure --topic <topic> --yes` runs with a safe normal non-bare `topic.repos.main`
- **THEN** it creates missing root `AGENTS.md` or `CLAUDE.md`
- **AND** it appends the rendered guidance block when absent
- **AND** it updates a recognized stale block in place
- **AND** it preserves all content outside the Isomer-managed guidance block
- **AND** a second ensure run reports no changed files when the files are already current

#### Scenario: Ensure blocks unsafe repositories
- **WHEN** `project topic-main-guidance ensure --yes` resolves a missing, non-Git, bare, corrupt, ambiguous, or otherwise unsafe `topic.repos.main`
- **THEN** the command reports a blocker
- **AND** it does not create or repair `topic.repos.main`
- **AND** it directs repository preparation to the topic-main setup workflow

#### Scenario: JSON output includes guidance metadata
- **WHEN** any `project topic-main-guidance` command runs with `--print-json`
- **THEN** the payload includes guidance version, template resource id, begin marker, end marker, target file statuses when applicable, changed files when applicable, mutation status, and blockers or diagnostics
