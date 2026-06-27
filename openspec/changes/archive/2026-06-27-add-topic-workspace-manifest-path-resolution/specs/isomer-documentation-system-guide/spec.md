## ADDED Requirements

### Requirement: Semantic Workspace Path Documentation
The documentation SHALL explain that semantic surface labels are the workspace path contract and default directories are one layout profile.

#### Scenario: Topic Workspace Manifest is documented
- **WHEN** a reader opens Topic Workspace or runtime file documentation
- **THEN** the docs explain the Topic Workspace Manifest, its standard path, its topic-owned role, and its relationship to the Project Manifest

#### Scenario: Semantic labels are documented
- **WHEN** docs describe Topic Workspace and Agent Workspace paths
- **THEN** they name semantic labels such as `topic.main_repo`, `topic.records.artifacts`, `agent.workspace`, `agent.private_artifacts`, `agent.public_share`, and `agent.scratch`

#### Scenario: Default layout is described as a profile
- **WHEN** docs show `repos/topic-main`, `records/*`, `runtime/*`, or `agents/<agent-name>`
- **THEN** they describe those paths as the `isomer-default.v1` bindings rather than the only valid contract

#### Scenario: Directory meanings stay readable
- **WHEN** docs describe directory meanings for the default layout
- **THEN** they use Markdown nested lists or equivalent prose instead of relying on a table as the only representation

### Requirement: Semantic Path CLI Documentation
The documentation SHALL describe the CLI commands that query and materialize semantic paths.

#### Scenario: Path get is documented
- **WHEN** a reader opens the `isomer-cli` reference
- **THEN** it explains how to query one semantic label with `project paths get <semantic-label>`

#### Scenario: Path list is documented
- **WHEN** a reader opens the `isomer-cli` reference
- **THEN** it explains how to list known semantic labels and their resolution status with `project paths list`

#### Scenario: Materialization is documented as mutating
- **WHEN** docs describe default semantic directory creation
- **THEN** they document the explicit materialization command as mutating and keep read-only path queries separate

#### Scenario: Side effects remain explicit
- **WHEN** docs show path query commands
- **THEN** they state which commands are read-only and which commands can create manifests, directories, repositories, or worktrees

### Requirement: Cwd-derived Agent Context Documentation
The documentation SHALL explain when agent-scoped semantic path queries can omit Agent Name.

#### Scenario: Agent workspace cwd query is documented
- **WHEN** docs describe Agent Workspace operation
- **THEN** they show that an agent running inside its own Agent Workspace can query agent-scoped labels such as `agent.private_artifacts` without passing Agent Name

#### Scenario: Inference precedence is documented
- **WHEN** docs describe agent-scoped path queries
- **THEN** they explain the precedence of explicit selector, environment context, cwd-derived Agent Workspace match, and missing-context diagnostic

#### Scenario: Topic Main Repository does not infer agent
- **WHEN** docs describe cwd-derived agent inference
- **THEN** they state that cwd inside the Topic Main Repository owner checkout does not identify an Agent Workspace

#### Scenario: Inference is not access control
- **WHEN** docs describe cwd-derived agent context
- **THEN** they state that it is a convenience for path resolution and not filesystem-grade identity, isolation, or access control

### Requirement: Documentation Verification for Semantic Paths
The documentation verification path SHALL detect stale wording that treats default paths as the only workspace contract.

#### Scenario: Docs validation checks fixed-path-only wording
- **WHEN** docs validation runs
- **THEN** it reports selected stale wording that says agents or users must rely on fixed directory paths when a semantic label should be used

#### Scenario: Docs validation checks path query coverage
- **WHEN** docs validation runs
- **THEN** it checks that the CLI reference documents semantic path query and materialization command names

#### Scenario: Docs validation checks tmp layering note
- **WHEN** docs validation runs after this change
- **THEN** it allows the pending `tmp/` change only when docs describe `tmp/` as future or downstream semantic labels rather than a pre-manifest fixed-path-only contract

### Requirement: tmp Surfaces Are Documented as Downstream Labels
The documentation SHALL frame local `tmp/` surfaces as downstream semantic labels that inherit the manifest-backed path model.

#### Scenario: tmp is not introduced as fixed path only
- **WHEN** docs mention planned or implemented `tmp/` surfaces
- **THEN** they describe labels such as `topic.tmp`, `topic.main_repo.tmp`, or `agent.tmp` with default bindings rather than only hard-coded paths

#### Scenario: tmp semantics remain local-only
- **WHEN** docs describe future or implemented `tmp/` labels
- **THEN** they state that those labels are local, ignored, disposable, not shared, and not durable evidence
