## ADDED Requirements

### Requirement: Topic Main Agent Guidance Injection
The service environment setup skill SHALL ensure Topic Main Development Repository agent rule guidance during `ensure-topic-main-repository`.

#### Scenario: Topic main setup creates missing rule files
- **WHEN** `ensure-topic-main-repository` prepares a newly initialized or safe empty `topic.repos.main`
- **THEN** it creates root-level `AGENTS.md` and `CLAUDE.md` when either file is missing
- **AND** each created file contains the Isomer-managed topic-main guidance block
- **AND** the files are eligible for normal Git tracking in topic-main

#### Scenario: Existing rule files are preserved
- **WHEN** `ensure-topic-main-repository` runs against an existing normal non-bare Topic Main Development Repository with an existing `AGENTS.md` or `CLAUDE.md`
- **THEN** it preserves existing user-authored content in those files
- **AND** it appends the Isomer-managed topic-main guidance block when the block is absent
- **AND** it updates the existing Isomer-managed block in place when the block is present but stale

#### Scenario: Guidance injection is bounded by mutation authorization
- **WHEN** `ensure-topic-main-repository` lacks direct Project Operator Session mutation confirmation or equivalent service authorization
- **THEN** it reports missing or stale topic-main guidance as a blocker or next action
- **AND** it does not create or modify `AGENTS.md` or `CLAUDE.md`

#### Scenario: Setup output reports guidance posture
- **WHEN** `ensure-topic-main-repository` creates, appends, updates, validates, or blocks agent guidance
- **THEN** it reports the posture of `AGENTS.md`, `CLAUDE.md`, the Isomer-managed block version, changed files, commands run, blockers, and next action

### Requirement: Topic Main Guidance Content
The service environment setup skill SHALL write topic-independent guidance that makes Pixi and Isomer CLI usage explicit.

#### Scenario: Guidance declares Pixi as primary
- **WHEN** the Isomer-managed topic-main guidance block is created or updated
- **THEN** the block states that the repository uses Pixi as the primary package manager and execution environment
- **AND** it states that Python should be invoked through Pixi with `pixi run --manifest-path <manifest_path> --environment <pixi_environment> python ...`
- **AND** it tells agents to avoid system Python, ambient virtualenvs, plain `python`, plain `pip`, shell activation, and local `.venv` environments as the source of truth for topic work

#### Scenario: Guidance prefers CLI queries over embedded facts
- **WHEN** the Isomer-managed topic-main guidance block is created or updated
- **THEN** the block tells agents to query topic-specific context, paths, and actor information with `isomer-cli`
- **AND** it includes read-only command forms for `project context show`, `project paths get <semantic-label>`, `project paths explain <semantic-label>`, `project topics list`, and `project topic-actors list`
- **AND** it tells agents not to hardcode or guess Research Topic ids, Topic Workspace paths, Topic Actor names, Agent Names, runtime paths, credentials, external repository paths, `manifest_path`, or `pixi_environment`

#### Scenario: Guidance names semantic labels without resolving them
- **WHEN** the Isomer-managed topic-main guidance block is created or updated
- **THEN** it may name semantic labels such as `topic.repos.main`, `topic.repos.main.isomer_managed`, `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, `topic.records`, `topic.runtime`, `topic.actors.workspace`, and `agent.workspace`
- **AND** it does not include resolved values for those labels
