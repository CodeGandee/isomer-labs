# isomer-documentation-system-guide Specification

## Purpose
TBD - created by archiving change rewrite-docs-comprehensive-system-guide. Update Purpose after archive.
## Requirements

### Requirement: Documentation Information Architecture
The documentation SHALL include welcome-first onboarding paths for core Isomer, DeepSci, and Kaoju alongside informed-user entrypoint and CLI references.

#### Scenario: Documentation tree is inspected
- **WHEN** public documentation navigation is inspected
- **THEN** installation and quickstart pages link to packaged system-skill onboarding, core welcome, extension welcomes, entrypoint execution, and CLI reference
- **AND** newcomer guidance is not buried only inside the complete command reference

#### Scenario: Packaged skill guide is inspected
- **WHEN** docs explain the packaged public surface
- **THEN** they present each pack as a welcome and entrypoint pair
- **AND** they distinguish protected subskills from both public roles

#### Scenario: Required docs pages exist
- **WHEN** repository documentation is validated
- **THEN** the docs tree includes entry pages for index, tutorial quickstart, installation, first Project, first Research Topic, Project Web GUI, system-skill installation, manual CLI reference, Project lifecycle, Research Topics, Topic Workspace definition, Workspace Runtime, research records, Project Web, Houmao adapter, troubleshooting, developer architecture, storage, packaged system skills, UI contracts, release process, testing, and contributing to docs

#### Scenario: Pages use section-appropriate tone
- **WHEN** a current docs page is moved into the new layout
- **THEN** it is rewritten for tutorial, manual, developer, or UI contract use rather than copied unchanged

#### Scenario: README points to detailed docs
- **WHEN** a reader opens `README.md`
- **THEN** it gives a concise published-tool orientation and links to tutorial, manual, and developer docs rather than duplicating the full system guide

#### Scenario: Public install path is distinct from developer setup
- **WHEN** docs show how to install Isomer Labs for ordinary use
- **THEN** they recommend installing the published CLI with `uv tool install isomer-labs`
- **AND** they keep Pixi checkout setup in developer docs

#### Scenario: System skill install path is documented
- **WHEN** docs show how to install Isomer system skills for an agent
- **THEN** they recommend `npx skills add` examples and distinguish core skills from DeepSci extension skills
### Requirement: System Design Documentation
The system SHALL document the current Isomer Labs architecture using canonical domain language and explicit state ownership boundaries.

#### Scenario: Core state ownership is explained
- **WHEN** a reader opens the system design documentation
- **THEN** it explains how Project, Project Config Directory, Project Manifest, Research Topic Config, Topic Workspace, Topic Main Repository, `isomer-managed/`, Workspace Runtime, Agent Workspace, and adapter-generated files relate to each other

#### Scenario: Worker visibility boundary is explained
- **WHEN** a reader opens the system design documentation
- **THEN** it explains that worker agents normally operate from `agents/<agent-name>` and use Git branches, `isomer-managed/` shares or projections, and topic-owned Pixi tasks rather than browsing root owner-preserved directories as normal input

#### Scenario: Execution layers are separated
- **WHEN** a reader opens the system design documentation
- **THEN** it distinguishes Domain Agent Team Templates, Topic Agent Team Profiles, Agent Team Instances, Agent Instances, Operator Agent responsibilities, Execution Adapter behavior, and Houmao-specific implementation details

#### Scenario: Future work is not documented as current behavior
- **WHEN** docs mention roadmap features such as Operator Agent handoff normalization, GUI Backend, View Manifests, Service Requests, Gates, or full research records
- **THEN** the docs identify whether the feature is implemented, partially implemented, or planned

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

#### Scenario: Repository commands show the external boundary
- **WHEN** the command reference documents `project paths default`, `project repos create`, or `project repos register`
- **THEN** it states that default-path lookup is read-only, repository registration changes only the Topic Workspace Manifest, and repository-directory creation does not initialize or acquire a Git repository
- **AND** it explains that clone, fetch, checkout, copy, repair, and verification commands run outside Isomer APIs

#### Scenario: Removed repository acquisition command is absent
- **WHEN** the public CLI reference and examples are validated after this change
- **THEN** they contain no active `project repos acquire`, `repository_acquisition`, fixed depth-one clone, or Isomer-owned repository cleanup workflow

### Requirement: Intended Usage Workflows
The documentation SHALL show newcomer workflows that begin with welcome and informed-user workflows that begin directly with an execution entrypoint.

#### Scenario: First-time core user is guided
- **WHEN** a reader does not yet know Isomer task vocabulary or command ids
- **THEN** docs recommend `$isomer-op-welcome` to explore typical Project, Topic, topology, extension, GUI, and Toolbox patterns
- **AND** they show how welcome hands a selected task to `$isomer-op-entrypoint`

#### Scenario: First-time extension user is guided
- **WHEN** a reader wants to understand DeepSci or Kaoju before starting work
- **THEN** docs recommend the corresponding `$isomer-ext-<extension-id>-welcome`
- **AND** they show a representative exact execution request through `$isomer-ext-<extension-id>-entrypoint`

#### Scenario: Informed user has a concrete task
- **WHEN** a reader already knows the intended public command or can state a concrete task
- **THEN** docs allow direct entrypoint invocation without requiring a welcome step
- **AND** they explain that the entrypoint proceeds through protected owners and prerequisite recovery as applicable

#### Scenario: Routing cues are documented
- **WHEN** docs include representative user phrases or keywords
- **THEN** they label them as routing cues and pair them with deterministic public command forms
- **AND** they do not claim that natural-language routing depends on an undocumented exact keyword grammar

#### Scenario: Minimal project workflow is documented
- **WHEN** a new user follows the getting-started guide
- **THEN** the guide shows how to initialize a Project, inspect or validate it, resolve context, preview paths, initialize Workspace Runtime, prepare readiness, and create an Agent Team Instance without launching agents

#### Scenario: Houmao quick launch workflow is documented
- **WHEN** a user needs Isomer to launch a Houmao-backed Agent Team Instance
- **THEN** the docs explain the quick launch command sequence, preflight expectations, generated manifests, command payload records, live inspection, stop behavior, and validation checks

#### Scenario: Manual Houmao workflow is documented
- **WHEN** a user wants to inspect or edit Houmao launch material before invoking Houmao directly
- **THEN** the docs explain prepare-only materialization, manual `houmao-mgr` operation, direct edit drift detection, reconciliation, and explicit adoption

#### Scenario: External repository workflow is documented
- **WHEN** a user or agent needs a Canonical External Repository
- **THEN** the docs show how to query or choose a non-mutating target, run user-selected or task-appropriate repository commands outside `isomer-cli`, verify source identity, register the existing path, and record applicable provenance
- **AND** failure examples do not create a successful binding or imply that Isomer cleans partial filesystem content
### Requirement: Assumptions and Non-goals Documentation
The system SHALL document current assumptions, side-effect boundaries, security posture, adapter boundaries, and non-goals so readers do not infer unsupported guarantees.

#### Scenario: Filesystem and workspace assumptions are documented
- **WHEN** a reader opens assumptions documentation
- **THEN** it states that Agent Workspace, Workspace Boundary, Peer Read Access, `isomer-managed/` owner/reader split, and generated-link semantics are advisory and do not provide filesystem-grade isolation

#### Scenario: Houmao adapter assumptions are documented
- **WHEN** a reader opens assumptions documentation or Houmao adapter documentation
- **THEN** it states that Houmao is invoked through the public CLI JSON boundary and that Houmao internals remain adapter-specific unless accepted domain language promotes a term

#### Scenario: Repair and setup assumptions are documented
- **WHEN** docs discuss missing dependencies, failed readiness, or environment repair
- **THEN** they explain that repair should be explicit through Service Request-style work rather than hidden inside read-only diagnostics or runtime preparation

### Requirement: Runtime Files and Manifest Documentation
The system SHALL document durable runtime files, generated adapter files, manifests, payload refs, Isomer-managed worker-facing paths, and cache boundaries.

#### Scenario: Durable runtime paths are explained
- **WHEN** a reader opens runtime file documentation
- **THEN** it explains `state.sqlite`, root runtime directories, path plans, Agent Workspaces, `isomer-managed/` tracked and untracked worker-facing paths, adapter manifest directories, command payloads, inspection snapshots, stop outcomes, and which files are durable records

#### Scenario: Adapter manifests are explained
- **WHEN** a reader opens Houmao adapter documentation
- **THEN** it explains `adapter-link.json`, `launch-material-manifest.json`, `adapter-runtime-manifest.json`, their purpose, and how reconciliation uses them

#### Scenario: Cache is not implied
- **WHEN** docs describe launch material, command payloads, inspection snapshots, stop outcomes, adapter manifests, or untracked `isomer-managed/` shares
- **THEN** they state that these files are durable adapter records only when the relevant path plan, Artifact locator, or Provenance Record classifies them as durable rather than cache-like generated material

### Requirement: Documentation Verification
Documentation validation SHALL verify public welcome names, entrypoint names, role descriptions, and example command ids against the packaged manifest.

#### Scenario: Public pair drifts
- **WHEN** documentation omits a declared welcome, swaps welcome and entrypoint roles, or names a stale public skill
- **THEN** documentation validation reports the affected page and expected manifest identity

#### Scenario: Example command drifts
- **WHEN** a welcome or documentation example names a public entrypoint command absent from manifest v4
- **THEN** validation reports the stale command and owning entrypoint

#### Scenario: Protected direct invocation appears
- **WHEN** newcomer documentation tells users to invoke a protected logical id directly
- **THEN** validation reports the route and recommends the owning public entrypoint form

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

#### Scenario: Docs validation checks legacy workspace paths
- **WHEN** docs validation runs after this change
- **THEN** it reports `.isomer-agent/` and top-level `repos/topic-main/{shared,artifacts,tasks,runs,views,logs,tools}` guidance outside migration notes as stale workspace layout language

#### Scenario: Docs validation checks repository-acquisition ownership
- **WHEN** docs validation scans active documentation, tutorials, and system-skill explanations
- **THEN** it reports `project repos acquire`, `repository_acquisition`, the removed repository service, fixed Isomer-owned clone behavior, registration before verification, and claims that Isomer cleans partial external acquisitions
- **AND** it accepts direct repository commands only when nearby guidance identifies them as user-controlled or agent-controlled external operations followed by non-executing Isomer registration
### Requirement: Semantic Workspace Path Documentation
The documentation SHALL explain that semantic surface labels are the workspace path contract and default directories are one layout profile.

#### Scenario: Topic Workspace Manifest is documented
- **WHEN** a reader opens Topic Workspace or runtime file documentation
- **THEN** the docs explain the Topic Workspace Manifest, its standard path, its topic-owned role, and its relationship to the Project Manifest

#### Scenario: Semantic labels are documented
- **WHEN** docs describe Topic Workspace and Agent Workspace paths
- **THEN** they name semantic labels such as `topic.repos.main`, non-main `topic.repos.<group...>.<repo-name>`, `topic.records.artifacts`, `agent.workspace`, `agent.private_artifacts`, `agent.public_share`, and `agent.scratch`

#### Scenario: Default layout is described as a profile
- **WHEN** docs show `repos/topic-main`, `repos/extern/...`, `records/*`, `runtime/*`, or `agents/<agent-name>`
- **THEN** they describe those paths as the `isomer-default.v1` bindings or helper defaults rather than the only valid contract

#### Scenario: Directory meanings stay readable
- **WHEN** docs describe directory meanings for the default layout
- **THEN** they use Markdown nested lists or equivalent prose instead of relying on a table as the only representation

#### Scenario: Main and external repository roles are distinguished
- **WHEN** docs describe topic-level repositories
- **THEN** they identify `repos/topic-main` as the primary Topic Main Repository and Agent Workspace worktree source
- **AND** they identify helper-created non-main `topic.repos.*` repositories under `repos/extern/...` as supporting topic-local repositories that may be inspected or modified when authorized by the gate or user

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
The documentation verification path SHALL detect stale wording that treats default paths as the only workspace contract or treats tmp material as shared, durable, or evidence-ready.

#### Scenario: Docs validation rejects durable tmp wording
- **WHEN** docs validation scans documentation that mentions `tmp/`
- **THEN** it allows the wording only when the same document names semantic labels such as `topic.tmp`, `topic.repos.main.tmp`, or `agent.tmp`
- **AND** the document states that tmp material is local, ignored, disposable, not shared, and not durable evidence

#### Scenario: Docs validation rejects fixed tmp path authority
- **WHEN** docs validation scans documentation that describes `tmp/` as the only supported path contract
- **THEN** it reports that tmp path wording must be semantic-label-first and must identify default directories as `isomer-default.v1` bindings

### Requirement: tmp Surfaces Are Documented as Downstream Labels
The documentation SHALL frame local `tmp/` surfaces as semantic labels that inherit the manifest-backed path model.

#### Scenario: Topic Workspace definition lists implemented tmp labels
- **WHEN** a reader opens the Topic Workspace definition after this change is implemented
- **THEN** it lists `topic.tmp`, `topic.repos.main.tmp`, and `agent.tmp` as Local Tmp Surface labels with local disposable meanings
- **AND** default directories are described only as `isomer-default.v1` bindings

#### Scenario: Documentation no longer calls implemented labels planned
- **WHEN** documentation describes `topic.tmp`, `topic.repos.main.tmp`, or `agent.tmp` after the semantic surface catalog supports them
- **THEN** it describes them as implemented standard labels rather than planned or future labels

#### Scenario: Documentation distinguishes tmp from sharing
- **WHEN** documentation explains worker visibility and collaboration paths
- **THEN** it states that tmp is not Peer Read Access, not a generated-link target, not owner-preserved records, and not Git-tracked collaboration material

#### Scenario: Documentation distinguishes tmp from scratch
- **WHEN** documentation explains `agent.scratch` or `isomer-managed/agent-owned/scratch/`
- **THEN** it distinguishes agent-owned draft support from root tmp disposable material

### Requirement: Topic Workspace Definition Documentation
The system SHALL keep `docs/topic-workspace-definition.md` as the canonical documentation page for Topic Workspace and Agent Workspace filesystem structure.

#### Scenario: Standard layout shows isomer-managed namespace
- **WHEN** a reader opens `docs/topic-workspace-definition.md`
- **THEN** the standard layout shows `repos/topic-main/isomer-managed/` and the tracked, agent-owned, topic-owned, and generated-link subtrees with comments explaining their meanings

#### Scenario: Legacy support root is absent from current layout
- **WHEN** `docs/topic-workspace-definition.md` describes the current standard Agent Workspace internal layout
- **THEN** it does not present `.isomer-agent/` as the current support root

#### Scenario: Three sharing regimes are explained
- **WHEN** `docs/topic-workspace-definition.md` explains `isomer-managed/`
- **THEN** it distinguishes Git-tracked Isomer-injected material, untracked agent-owned material with owner/reader split, and untracked topic-owned material projected to agents

#### Scenario: Communication channels are updated
- **WHEN** `docs/topic-workspace-definition.md` describes Agent Communication Channels
- **THEN** it lists Git branch exchange as primary, `isomer-managed/` untracked shares and projections as secondary for large or temporary material, and topic-owned Pixi tasks as the structured tool/API channel

#### Scenario: Migration guidance is non-destructive
- **WHEN** `docs/topic-workspace-definition.md` mentions legacy `.isomer-agent/` or top-level `topic-main` Isomer directories
- **THEN** it frames them as migration diagnostics and states that Isomer must not delete or move user files without explicit operator instruction

### Requirement: Storage Contract Documentation
The documentation SHALL describe Workspace Path Resolution as the storage-layer contract for Topic Workspace and Agent Workspace file surfaces.

#### Scenario: Semantic labels are named as storage API
- **WHEN** docs describe where agents, services, or adapters read or write topic files
- **THEN** they present Semantic Workspace Surface Labels and `isomer-cli project paths get/list/preview/default` as the canonical path lookup interface

#### Scenario: Default directories are examples
- **WHEN** docs show directories such as `repos/topic-main`, `repos/extern/<repo-label-path>`, `records/artifacts`, `runtime`, or `agents/<agent-name>`
- **THEN** they identify those directories as `isomer-default.v1` bindings, helper defaults, or examples rather than the storage contract itself

#### Scenario: Custom binding example is documented
- **WHEN** docs explain the Topic Workspace Manifest
- **THEN** they include an example of rebinding a built-in label and declaring a custom `custom.*` label through `isomer-cli project paths register` with `label`, `path`, and `storage_profile`

#### Scenario: Binding lifecycle commands are documented
- **WHEN** docs describe semantic path binding management
- **THEN** they explain register, update, unregister, reset, and materialize behavior, including that unregistering or resetting a binding does not delete filesystem content or rewrite historical Path Plans

#### Scenario: Default path and materialization commands are documented
- **WHEN** docs describe reserved or valid grouped repository semantic labels with default paths
- **THEN** they document how to query the default path and, where supported, materialize a default filesystem target without treating the physical default path as the public contract

#### Scenario: Repository helper default is documented
- **WHEN** docs describe `project repos create`
- **THEN** they explain that bare non-main repository labels become `topic.repos.<group...>.<repo-name>` bindings with `storage_profile = "topic_repo"` and default paths under `repos/extern/...`

#### Scenario: Agents are told to query paths
- **WHEN** docs or skill references instruct an agent to use a Topic Workspace or Agent Workspace storage surface
- **THEN** they tell the agent to query the semantic label through `isomer-cli` or equivalent resolver output instead of remembering physical paths

#### Scenario: Repository helpers are documented
- **WHEN** docs describe `project repos create` or `project repos register`
- **THEN** they explain that bare non-main repository labels become `topic.repos.<group...>.<repo-name>` bindings with `storage_profile = "topic_repo"` and helper defaults under `repos/extern/...`
- **AND** they distinguish directory creation from registration of an existing externally acquired repository and state that neither helper executes Git commands

### Requirement: Documentation Validation Detects Default-path-only Guidance
Documentation validation SHALL report guidance that treats concrete default directories as authoritative without nearby semantic labels or default-profile framing.

#### Scenario: Default path without semantic label is reported
- **WHEN** docs mention a default storage path such as `repos/topic-main` or `agents/<agent-name>` as a command target without naming the related semantic label
- **THEN** documentation validation reports the path guidance as stale or incomplete

#### Scenario: Custom label docs are checked
- **WHEN** docs describe user-defined semantic paths
- **THEN** documentation validation requires accepted custom namespace examples and storage profile terms rather than repeated storage-profile-derived fields

### Requirement: Topic Workspace Documentation Explains Topic Main Development Repository
The documentation SHALL explain that the Topic Main Development Repository is the topic-owned development repository resolved by `topic.repos.main` and prepared by Topic Workspace environment setup.

#### Scenario: Topic workspace definition names ownership
- **WHEN** a reader opens Topic Workspace documentation
- **THEN** it states that `repos/topic-main` is the default Topic Main Development Repository
- **AND** it states that topic env setup creates, configures, and verifies it before Agent Workspace worktrees are created

#### Scenario: Existing user repo impact is explained
- **WHEN** documentation describes a custom or existing `topic.repos.main`
- **THEN** it explains that Isomer-created material belongs under `isomer-managed/`
- **AND** it does not instruct users to add top-level `extern/`, `shared/`, `tasks/`, `runs/`, or similar Isomer directories to the repository root

### Requirement: Documentation Explains External Repo Projections
The documentation SHALL distinguish canonical external repos under `repos/extern/...` from their Isomer-managed projections inside topic-main.

#### Scenario: Canonical external repo storage is documented
- **WHEN** documentation describes non-main `topic.repos.*` repositories
- **THEN** it states that their default canonical location is `repos/extern/<repo-label-path>`
- **AND** it states that these repositories are not Agent Workspace worktree anchors

#### Scenario: Projection roots are documented
- **WHEN** documentation describes how humans or agents access external repos from topic-main
- **THEN** it shows `isomer-managed/topic-owned/readonly/extern/...` for read-only projections
- **AND** it shows `isomer-managed/topic-owned/writable/extern/...` for writable projections
- **AND** it names `isomer-managed/tracked/manifests/extern-projections.toml` as the projection metadata file

### Requirement: Documentation States Breaking Recreate Policy
The documentation SHALL state that this Topic Workspace layout revision is breaking and that generated `isomer-content/` internals can be recreated instead of migrated.

#### Scenario: Old internals are not promised
- **WHEN** docs mention old generated paths, old topic-main setup responsibility, or old projection locations
- **THEN** they describe those conventions as replaced by the revised layout
- **AND** they do not promise compatibility for old generated Topic Workspace internals

#### Scenario: Validation docs prefer recreate
- **WHEN** docs describe validation failures caused by old generated `isomer-content/` internals
- **THEN** they name recreation under the revised layout as the accepted resolution

### Requirement: Canonical Domain Language Includes Topic Actor Workspace
The documentation system SHALL update canonical Isomer domain language so Topic Actor Workspace is a managed workspace type for human-orchestrated Topic Actors.

#### Scenario: Workspace taxonomy includes Topic Actor Workspaces
- **WHEN** canonical domain language describes Isomer-managed workspace types
- **THEN** it lists Topic Workspace, Agent Workspace, and Topic Actor Workspace as the managed workspace types
- **AND** it defines Topic Actor Workspace as the per-Topic Actor work area inside a Topic Workspace, separate from formal Agent Workspace identity

#### Scenario: Topic Actor Workspace remains separate from Agent Workspace
- **WHEN** documentation, schemas, CLI help, or skill prose describes manually controlled workers
- **THEN** it uses Topic Actor Workspace for their managed cwd surface
- **AND** it does not describe Topic Actor Workspaces as Agent Workspaces, Agent Instance ids, or Agent Team Instance membership
