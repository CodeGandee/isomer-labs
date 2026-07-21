## ADDED Requirements

### Requirement: Project Self Location and Context Check Commands
The CLI SHALL expose progressive read-only `project self location` and `project self check` commands for ambient workspace classification and intended-operation context alignment.

#### Scenario: Self command surface includes location and check
- **WHEN** a user inspects `isomer-cli project self --help` or `isomer-cli project self queries`
- **THEN** the output includes `project self location` and `project self check`
- **AND** it describes both commands as read-only progressive self queries

#### Scenario: Location JSON is ambient-only
- **WHEN** a user runs `isomer-cli --print-json project self location`
- **THEN** the output includes canonical cwd, matched workspace kind and root, owning topic or worker refs when cwd proves them, match source, diagnostics, and `mutated=false`
- **AND** it does not promote Project Manifest topic or actor defaults into the ambient-location payload

#### Scenario: Context check accepts operation scope and selectors
- **WHEN** a user runs `project self check --scope project|topic|topic-actor|agent` with applicable existing topic, Topic Workspace, lifecycle, Topic Actor, or Agent selectors
- **THEN** the command applies existing Effective Context selection and validation rules
- **AND** it returns the requested scope, selected target, selection sources, defaults considered, ambient location, expected worker cwd when applicable, alignment verdict, and diagnostics

#### Scenario: Context check text is concise
- **WHEN** a user runs `isomer-cli project self check` in text mode with a valid scope and target
- **THEN** the output summarizes the selected target, source, ambient workspace, alignment verdict, and next corrective selector or cwd action when needed
- **AND** it does not print unrelated environment, Pixi, runtime, or semantic path details

#### Scenario: New self commands are side-effect free
- **WHEN** `project self location` or `project self check` runs in text or JSON mode
- **THEN** it does not modify Project or Topic manifests, local context, Workspace Runtime, path plans, worker workspaces, skill files, templates, or external systems
