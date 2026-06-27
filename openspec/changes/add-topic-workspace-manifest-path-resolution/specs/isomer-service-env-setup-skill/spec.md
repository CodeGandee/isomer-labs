## ADDED Requirements

### Requirement: Service Setup Resolves Semantic Topic Surfaces
The service environment setup skill SHALL resolve setup paths through semantic Topic Workspace surfaces instead of assuming the default directory structure is authoritative.

#### Scenario: Topic Workspace root remains manifest-backed
- **WHEN** the service resolves the selected setup target
- **THEN** it uses Project Manifest-backed Topic Workspace selection before resolving topic-owned semantic labels inside that workspace

#### Scenario: Pixi manifest path is semantic
- **WHEN** the service needs the Topic Workspace Pixi manifest or Topic Workspace environment root
- **THEN** it resolves the corresponding semantic label or default-profile binding and reports the path source

#### Scenario: User intent gate path is semantic
- **WHEN** the service reads or writes environment gate material
- **THEN** it resolves the source and derived gate locations through semantic labels or default-profile bindings rather than assembling only hard-coded paths

#### Scenario: Required repository path is semantic
- **WHEN** the service needs a Topic Workspace repository location for setup
- **THEN** it resolves the repository root through the topic repository semantic surface and reports custom manifest-backed paths when present

### Requirement: Service Setup Preserves Custom Topic Layouts
The service environment setup skill SHALL accept safe manifest-backed Topic Workspace layout bindings that differ from the default layout.

#### Scenario: Custom repo root is accepted
- **WHEN** the Topic Workspace Manifest binds setup repositories to a safe project-local path that differs from `<topic-workspace>/repos/<repo-name>`
- **THEN** the service uses that binding for repository checks and setup evidence

#### Scenario: Custom gate root is accepted
- **WHEN** the Topic Workspace Manifest binds user intent gate surfaces to safe project-local paths
- **THEN** the service reads, derives, writes, and reports gate material through those bindings

#### Scenario: Unsafe custom binding blocks setup
- **WHEN** a required semantic binding resolves outside the Project root, inside `.isomer-labs/`, or into another Topic Workspace without an accepted policy
- **THEN** the service reports a blocker and does not mutate setup files at that path

### Requirement: Service Output Reports Semantic Evidence
The service environment setup skill SHALL report semantic labels and path sources in setup evidence.

#### Scenario: Setup evidence includes labels
- **WHEN** setup completes, defers, or blocks
- **THEN** the service output includes the semantic labels, resolved paths, path sources, changed files, commands run, readiness status, and blockers relevant to the setup

#### Scenario: Default paths are identified as defaults
- **WHEN** a setup path comes from `isomer-default.v1`
- **THEN** the output identifies the default profile source instead of implying the path was user-authored

#### Scenario: Custom paths are not blockers by themselves
- **WHEN** a setup path differs from the default layout but satisfies the required semantic label and safety checks
- **THEN** the service does not report the path difference as a blocker

### Requirement: Agent Workspace Environment Targets Require Explicit Scope
The service environment setup skill SHALL avoid implicit Agent Workspace setup unless the requested setup target includes explicit or inferred Effective Agent Context.

#### Scenario: Topic setup does not infer agent
- **WHEN** the service is preparing the Topic Workspace environment
- **THEN** it does not treat cwd inside an Agent Workspace as permission to mutate agent-specific environment files unless the requested setup target is agent-scoped

#### Scenario: Agent-scoped setup can use cwd inference
- **WHEN** a future accepted agent-scoped setup workflow requests an agent surface and cwd is inside a known Agent Workspace
- **THEN** the service may use Effective Agent Context inference to resolve agent-scoped semantic labels

#### Scenario: Cross-agent setup requires explicit selector
- **WHEN** service setup targets another agent's workspace surface
- **THEN** it requires an explicit Agent Name or Agent Instance selector rather than relying on the caller's cwd
