## ADDED Requirements

### Requirement: Agent Self Query CLI Command
The CLI SHALL expose `project self show` as a read-only Project command that returns the caller's process-local Isomer self query packet in deterministic text and JSON forms.

#### Scenario: Command surface includes self show
- **WHEN** a user runs `isomer-cli --help` or inspects the Project command groups
- **THEN** the command surface includes `project self show`
- **AND** the help text describes it as a read-only agent self query command

#### Scenario: Self show supports JSON output
- **WHEN** a user runs `isomer-cli --print-json project self show`
- **THEN** the output is deterministic JSON with `command`, `output_schema_version`, `ok`, `mutated`, `context`, `identity`, `environment`, `semantic_paths`, `pixi`, `recommended_queries`, and `diagnostics` fields
- **AND** `mutated` is always `false`

#### Scenario: Self show supports text output
- **WHEN** a user runs `isomer-cli project self show`
- **THEN** the text output summarizes the selected Research Topic, Topic Workspace, Topic Actor identity when resolved, Agent identity when resolved, Pixi command hint when available, and the most important follow-up query commands

#### Scenario: Self show accepts existing selectors
- **WHEN** a user invokes `project self show` with existing topic, topic-workspace, lifecycle, agent-team-instance, agent-instance, topic-agent-team-profile, agent, or topic-actor selectors
- **THEN** the command applies the same selection and conflict rules used by Effective Topic Context, Effective Agent Context, and Topic Actor context resolution

#### Scenario: Self show is side-effect free
- **WHEN** `project self show` runs in text or JSON mode
- **THEN** it does not create or modify Topic Workspace directories, Workspace Runtime records, Path Plans, Topic Workspace Manifests, Project Manifests, Pixi manifests, lockfiles, agent guidance files, launch material, or external adapter state

### Requirement: Topic Main Guidance Recommends Self Query
The topic-main guidance renderer SHALL direct coding agents to start with `project self show` before using lower-level context, path, and topic actor queries.

#### Scenario: Rendered guidance includes self show first
- **WHEN** `isomer-cli project topic-main-guidance render` emits the guidance block
- **THEN** the first recommended Isomer query command is `isomer-cli --print-json project self show`
- **AND** the lower-level `project context show`, `project paths get <semantic-label>`, and `project paths explain <semantic-label>` examples remain available

#### Scenario: Guidance avoids hardcoded identity and Pixi values
- **WHEN** topic-main guidance is injected into `AGENTS.md` or `CLAUDE.md`
- **THEN** the guidance tells agents to query their own identity, `manifest_path`, `pixi_environment`, and semantic paths through `project self show` or lower-level `isomer-cli` commands
- **AND** it does not embed a concrete Research Topic id, Topic Workspace path, Agent Name, Agent Instance id, manifest path, Pixi environment, credential, or external repository path
