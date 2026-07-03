## ADDED Requirements

### Requirement: Agent Self Query CLI Family
The CLI SHALL expose `project self` as a read-only Project command family whose subcommands return small, deterministic text and JSON responses for selected self-query concerns.

#### Scenario: Command surface includes self query subcommands
- **WHEN** a user runs `isomer-cli --help`, `isomer-cli project --help`, or `isomer-cli project self --help`
- **THEN** the command surface includes `project self show`, `project self identity`, `project self pixi`, `project self env`, `project self paths`, and `project self queries`
- **AND** the help text describes them as read-only agent self query commands

#### Scenario: Self show supports small JSON output
- **WHEN** a user runs `isomer-cli --print-json project self show`
- **THEN** the output is deterministic JSON with `command`, `output_schema_version`, `ok`, `mutated`, `summary`, `available_queries`, and `diagnostics` fields
- **AND** `mutated` is always `false`
- **AND** the output does not include detailed `identity`, `environment`, `semantic_paths`, `pixi`, or full query catalog fields

#### Scenario: Specific self subcommands support JSON output
- **WHEN** a user runs `isomer-cli --print-json project self identity`, `project self pixi`, `project self env`, `project self paths <label>...`, or `project self queries`
- **THEN** the output is deterministic JSON with `command`, `output_schema_version`, `ok`, `mutated=false`, the subcommand-specific payload field, and `diagnostics`
- **AND** each subcommand omits payload fields owned by the other self subcommands

#### Scenario: Self show supports concise text output
- **WHEN** a user runs `isomer-cli project self show`
- **THEN** the text output summarizes the selected Research Topic, Topic Workspace, Topic Actor or Agent headline when resolved, diagnostic count, and the available self subcommands
- **AND** it does not print a broad environment, path, Pixi, or query detail block

#### Scenario: Self subcommands accept existing selectors
- **WHEN** a user invokes any `project self` subcommand with existing topic, topic-workspace, lifecycle, agent-team-instance, agent-instance, topic-agent-team-profile, agent, or topic-actor selectors
- **THEN** the command applies the same selection and conflict rules used by Effective Topic Context, Effective Agent Context, and Topic Actor context resolution

#### Scenario: Self query commands are side-effect free
- **WHEN** any `project self` subcommand runs in text or JSON mode
- **THEN** it does not create or modify Topic Workspace directories, Workspace Runtime records, Path Plans, Topic Workspace Manifests, Project Manifests, Pixi manifests, lockfiles, agent guidance files, launch material, or external adapter state

### Requirement: Topic Main Guidance Recommends Progressive Self Queries
The topic-main guidance renderer SHALL direct coding agents to start with the small self summary and query only the self details they need.

#### Scenario: Rendered guidance includes self show first
- **WHEN** `isomer-cli project topic-main-guidance render` emits the guidance block
- **THEN** the first recommended Isomer query command is `isomer-cli --print-json project self show`
- **AND** the guidance says to query only the needed slice with commands such as `project self identity`, `project self pixi`, `project self env`, and `project self paths <semantic-label>`
- **AND** the lower-level `project context show`, `project paths get <semantic-label>`, and `project paths explain <semantic-label>` examples remain available

#### Scenario: Guidance avoids broad self dumps
- **WHEN** topic-main guidance is injected into `AGENTS.md` or `CLAUDE.md`
- **THEN** the guidance does not recommend a broad `project self --all`, `project self show --all`, or equivalent all-fields dump
- **AND** it does not embed a concrete Research Topic id, Topic Workspace path, Agent Name, Agent Instance id, manifest path, Pixi environment, credential, or external repository path
