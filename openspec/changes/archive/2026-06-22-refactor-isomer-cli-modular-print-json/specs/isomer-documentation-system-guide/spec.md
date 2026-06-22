## MODIFIED Requirements

### Requirement: isomer-cli Command Reference
The system SHALL document every public `isomer-cli` command with purpose, prerequisites, side effects, common examples, and JSON/text output posture.

#### Scenario: CLI command coverage is checked
- **WHEN** documentation validation runs
- **THEN** every public command exposed by `isomer-cli --help` and documented command groups is represented in the CLI reference, or the validation reports the missing command

#### Scenario: Global JSON mode is documented
- **WHEN** a reader opens the CLI reference
- **THEN** it documents root-level `--print-json` as the canonical JSON output switch and does not present command-local `--json` or `--format json` as normal usage

#### Scenario: Side effects are explicit
- **WHEN** a documented command can mutate Project files, Workspace Runtime records, adapter manifests, generated launch material, or live Houmao-managed agents
- **THEN** the command reference states the mutation boundary before or alongside the command example

#### Scenario: Read-only commands are identified
- **WHEN** a documented command is read-only
- **THEN** the command reference states that it does not create Workspace Runtime state, Agent Workspaces, launch material, or live Houmao state

### Requirement: Documentation Verification
The system SHALL provide a repository-local documentation verification path that can be run during implementation and review.

#### Scenario: Docs validation command exists
- **WHEN** contributors inspect development commands
- **THEN** there is a documented command or script for validating documentation coverage and links

#### Scenario: Docs validation checks command coverage
- **WHEN** docs validation runs
- **THEN** it checks that the CLI reference includes current public command names and reports missing or stale command names

#### Scenario: Docs validation checks stale JSON examples
- **WHEN** docs validation runs after this change
- **THEN** it reports stale Isomer CLI examples that use command-local `--json` or `--format json` instead of root-level `--print-json`

#### Scenario: Docs validation checks canonical language posture
- **WHEN** docs validation runs
- **THEN** it checks selected docs for known stale or forbidden project terms and reports likely violations without replacing human review
