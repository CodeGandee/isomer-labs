## ADDED Requirements

### Requirement: Centralized Step Dependency Contract
The Topic Team Specialization module skill SHALL centralize procedural step dependencies, recovery paths, produced artifacts, and blocker metadata in a machine-readable dependency manifest and SHALL provide a local script for querying that manifest.

#### Scenario: Dependency manifest and query script exist
- **WHEN** the `isomer-admin-topic-team-specialize` skill bundle is inspected
- **THEN** it contains `references/step-dependencies.json`
- **AND** it contains `scripts/query_step_dependencies.py`

#### Scenario: Manifest covers procedural subcommands
- **WHEN** `references/step-dependencies.json` is inspected
- **THEN** it records every public procedural subcommand in the Topic Team Specialization flow
- **AND** each recorded step includes a step id, display name, kind, required predecessor artifacts or inputs, produced artifacts or outputs, dependency edges or predecessor steps, recovery conditions, mutation notes, and unrecoverable blockers when applicable

#### Scenario: Query script validates graph
- **WHEN** `python skillset/operator/isomer-admin-topic-team-specialize/scripts/query_step_dependencies.py validate` runs from the repository root
- **THEN** it validates that all referenced step ids exist
- **AND** it validates that dependency paths are acyclic
- **AND** it reports an error for missing required fields, unknown targets, invalid edges, or malformed manifest data

#### Scenario: Query script returns targeted recovery paths
- **WHEN** an agent needs a targeted fast-forward recovery path for a selected subcommand
- **THEN** it can run `python skillset/operator/isomer-admin-topic-team-specialize/scripts/query_step_dependencies.py path --target <subcommand> --include-target`
- **AND** the output includes the canonical predecessor path plus the selected subcommand
- **AND** it can run the same command with `--exclude-target` to stop before the selected subcommand

#### Scenario: Query script answers local dependency questions
- **WHEN** an agent needs the prerequisites, produced artifacts, blockers, or explanation for one subcommand
- **THEN** it can query the script with `prereqs`, `produces`, `blockers`, or `explain`
- **AND** the script answers from `references/step-dependencies.json` without reading or mutating the Topic Workspace

#### Scenario: Skill prose delegates recovery paths to script
- **WHEN** the skill entrypoint, `fast-forward`, or procedural subcommand pages describe missing-prerequisite recovery
- **THEN** they instruct the agent to query `scripts/query_step_dependencies.py` for dependency paths
- **AND** they avoid duplicating long full recovery chains that are already represented in `references/step-dependencies.json`
- **AND** they preserve local prose for subcommand purpose, local evidence requirements, safety blockers, and information the agent must not invent

#### Scenario: Validation checks centralized contract
- **WHEN** `pixi run python scripts/validate_skillsets.py --scope operator` runs
- **THEN** it verifies that the dependency manifest and query script exist
- **AND** it verifies that the query script can validate the manifest
- **AND** it verifies that the manifest covers the topic-team procedural subcommands
- **AND** it does not require every procedural subcommand page to duplicate the full targeted fast-forward path in prose
