## ADDED Requirements

### Requirement: V2 Skills Read Placeholder Bindings
Active v2 research skills SHALL read local placeholder binding pages before writing durable placeholder outputs.

#### Scenario: Skill entrypoint names binding page
- **WHEN** an active v2 research skill has placeholder definitions
- **THEN** its `SKILL.md` tells the agent that placeholder definitions live in `migrate/placeholders.md` and storage bindings live in `placeholder-bindings.md`

#### Scenario: Durable output uses binding page
- **WHEN** a v2 skill step produces a durable placeholder output
- **THEN** the skill instructs the agent to use the corresponding `placeholder-bindings.md` row rather than inventing a path or directly editing Workspace Runtime

#### Scenario: Compatibility fallback remains bounded
- **WHEN** a v2 skill still needs a source-shaped DeepScientist compatibility call
- **THEN** the skill allows `isomer-cli ext deepsci call ...` only as a compatibility fallback and still summarizes durable meaning through the placeholder binding

### Requirement: Binding Pages Preserve Workflow Flexibility
The v2 research skills SHALL keep placeholders in workflow prose and bind them through local binding pages.

#### Scenario: Workflow placeholders are not replaced
- **WHEN** placeholder binding pages are added to v2 skills
- **THEN** the existing workflow steps keep semantic placeholders such as `<MAIN_RUN_RECORD>` and `<NEXT_ROUTE_DECISION>` instead of replacing them with concrete paths or record ids

#### Scenario: Binding updates do not rewrite method prose
- **WHEN** a storage target changes from extension-backed CRUD to a future native command
- **THEN** the binding page can change without requiring workflow prose to rename the placeholder
