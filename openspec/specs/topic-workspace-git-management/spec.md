# topic-workspace-git-management Specification

## Purpose
TBD - created by archiving change add-topic-workspace-git-management. Update Purpose after archive.
## Requirements
### Requirement: Topic Workspace Git Operator Skill
The core operator pack SHALL provide protected logical capability `isomer-op-topic-workspace-git` as entrypoint member `topic-git` for optional local Topic Workspace tracking and optional remote publication.

#### Scenario: Topic Git terminology preserves canonical types
- **WHEN** the skill refers to the canonical Topic Workspace as the source of tracking or publication
- **THEN** Source Topic Workspace is interpreted as a contextual role of that Topic Workspace rather than a separate type
- **AND** Topic Publication Copy is interpreted as a derived projection rather than a Topic Workspace, Topic Actor Workspace, or Agent Workspace

#### Scenario: Protected skill bundle is installed
- **WHEN** the core system-skill pack is inspected
- **THEN** it contains `operator/isomer-op-entrypoint/subskills/isomer-op-topic-workspace-git/SKILL-MAIN.md`, matching `agents/openai.yaml`, and directly referenced operation pages
- **AND** the parent entrypoint exposes it as `isomer-op-entrypoint->topic-git`

#### Scenario: Git request selects the dedicated owner
- **WHEN** a user asks to initialize local Topic Workspace Git, choose local files to commit, update local ignore policy, prepare a sanitized remote publication, or synchronize a published topic
- **THEN** the entrypoint routes the request to `topic-git`
- **AND** Topic Manager does not duplicate the local-tracking or publication workflow

### Requirement: Isomer CLI Is a Read-Only Topic Git Query Plane
The Topic Git skill SHALL use Isomer CLI only to query Project, Research Topic, semantic-path, Topic Actor, Agent, and Workspace Runtime information and SHALL invoke Git directly after validating the returned task-dependent context.

#### Scenario: Topic Git resolves operation context
- **WHEN** a Topic Git operation needs the Source Topic Workspace, Topic Main, Topic Actor Workspace, Agent Workspace, or Workspace Runtime path
- **THEN** the skill obtains the value from an applicable `isomer-cli --print-json` read-only query with explicit selected-context arguments
- **AND** it canonicalizes and validates the returned path before using it

#### Scenario: Topic Git performs a Git operation
- **WHEN** an approved local or publication plan requires Git inspection or mutation
- **THEN** the agent invokes the Git executable directly with `git -C <validated-resolved-path> ...`
- **AND** it does not invoke an `isomer-cli project topic-git ...` command, Isomer CLI Git wrapper, Git-wrapping service, or Git-wrapping helper script

#### Scenario: Required Isomer information is unavailable
- **WHEN** read-only Isomer queries cannot resolve required selected-topic or worker topology
- **THEN** the operation reports a blocker without guessing from sibling directories or using an unvalidated path
- **AND** implementation may add only a read-only Isomer query surface for the missing information

### Requirement: Direct Git Execution Is Explicit and Path Scoped
The Topic Git skill SHALL teach low-freedom direct Git procedures that pin repositories, refs, and pathspecs and revalidate applicable state before mutation.

#### Scenario: Repository-scoped Git is invoked
- **WHEN** the skill inspects or mutates a repository
- **THEN** it uses `git -C` with the validated Source Topic Workspace, Topic Publication Copy, or sanitized component repository path
- **AND** it does not rely on ambient cwd to select the repository

#### Scenario: Exact files are staged
- **WHEN** an approved operation stages content
- **THEN** it uses explicit approved pathspecs after the index and working tree are rechecked
- **AND** it does not use `git add .` or `git add -A`

#### Scenario: Unsafe Git operation is proposed
- **WHEN** an operation would require pull, automatic merge, rebase, reset, clean, source history rewriting, an unapproved force-push, remote branch deletion, or implicit repair
- **THEN** the skill reports a blocker and does not run that operation

### Requirement: Topic Git State Respects Lifecycle Availability
The Topic Git skill SHALL require valid Workspace Runtime support for local mutations while allowing publication state to begin in the ignored Topic Publication Copy immediately after Topic Workspace registration.

#### Scenario: Local mutation needs state
- **WHEN** local init, ignore, or commit is requested
- **THEN** the skill requires an existing valid `topic.runtime` and writes only the applicable schema-validated file under `<topic.runtime>/topic-git/`
- **AND** it does not edit `state.sqlite` directly, initialize Workspace Runtime, or use an Isomer CLI mutation command

#### Scenario: Publication begins before runtime
- **WHEN** a Research Topic and Topic Workspace are registered but Workspace Runtime is unavailable
- **THEN** publish init, plan, and sync may persist schema-validated local state only in an ignored support root inside the Topic Publication Copy
- **AND** that support root is never eligible for a publication commit

#### Scenario: Runtime becomes available after publication
- **WHEN** a later approved publish init or sync observes a valid Workspace Runtime and matching copy-local or remote publication identity
- **THEN** it records the credential-safe binding and current publication state under `<topic.runtime>/topic-git/`
- **AND** read-only status alone does not perform that mutation

#### Scenario: Unpushed pre-runtime copy is lost
- **WHEN** the Topic Publication Copy is deleted before its first successful push and no runtime binding exists
- **THEN** the local publication plan is considered lost and must be prepared again

### Requirement: Topic Git Layers Are Disabled by Default
The system SHALL keep in-workspace local tracking and remote publication disabled until the user explicitly requests the applicable layer.

#### Scenario: Topic creation does not enable tracking
- **WHEN** Topic creation, Topic Environment Setup, Topic Actor setup, or Agent Environment Setup completes
- **THEN** it does not initialize a Source Topic Workspace root repository, create a Topic Publication Copy, configure a publication remote, or push any branch

#### Scenario: Status on an untracked topic is read-only
- **WHEN** overall Topic Git status runs for a topic with neither layer enabled
- **THEN** it reports local tracking as `disabled` and remote publication as `disabled`
- **AND** it performs no mutation

### Requirement: Local Tracking and Remote Publication Are Independent
The system SHALL support local tracking and remote publication as independent opt-in capabilities with no prerequisite, trigger, or implicit mutation relationship between them.

#### Scenario: Local-only operation is valid
- **WHEN** local tracking is enabled and remote publication is disabled
- **THEN** local status, planning, ignore maintenance, and commits operate normally without a publication binding or remote

#### Scenario: Publication-only operation is valid
- **WHEN** remote publication is enabled and local tracking is disabled
- **THEN** publication inventories the Source Topic Workspace filesystem and synchronizes through the Topic Publication Copy without initializing or requiring a root local repository

#### Scenario: Both layers can coexist
- **WHEN** both layers are enabled
- **THEN** each layer retains separate plans, state validation, operations, outcomes, and recovery behavior
- **AND** local Git status is diagnostic rather than publication authority

#### Scenario: Disabling one layer preserves the other
- **WHEN** one layer becomes disabled, invalid, missing, or blocked
- **THEN** the other layer remains usable when its own requirements are satisfied

### Requirement: Topic Git Operation Groups Express Layer Boundaries
The Topic Git skill SHALL expose overall `status`, local child operations `status`, `init`, `plan`, `ignore`, and `commit`, and publication child operations `status`, `init`, `plan`, and `sync`.

#### Scenario: Local invocation remains local
- **WHEN** the selected route is `isomer-op-entrypoint->topic-git->local()->commit()`
- **THEN** the skill loads the local operation page and shared local safety contract
- **AND** it does not load or invoke publication mutation procedures

#### Scenario: Publication invocation remains publication scoped
- **WHEN** the selected route is `isomer-op-entrypoint->topic-git->publish()->sync()`
- **THEN** the skill loads the publication operation page and shared publication safety contract
- **AND** it does not stage or commit the Source Topic Workspace root repository

#### Scenario: Vague tracking request starts with status
- **WHEN** a user asks to track a Topic Workspace without distinguishing local history from remote publication
- **THEN** the skill reports both layer states and explains the two choices before mutation

### Requirement: Topic Git Status Reports Layers Separately
Overall status SHALL report local tracking and remote publication as distinct state machines.

#### Scenario: Layer status is complete
- **WHEN** overall status runs
- **THEN** local tracking is reported as `disabled`, `enabled`, or `invalid`
- **AND** remote publication is reported as `disabled`, `prepared`, `synchronized`, `stale`, `copy-missing`, or `blocked`
- **AND** the output includes separate blockers and next actions for each layer

#### Scenario: Ancestor Project repository is not local enablement
- **WHEN** the Source Topic Workspace is nested inside a Project Git repository but is not itself that repository's top level
- **THEN** local tracking remains `disabled`

#### Scenario: Ancestor repository does not ignore the workspace
- **WHEN** any ancestor Git repository tracks a Source Topic Workspace path or does not effectively ignore the Source Topic Workspace
- **THEN** local init reports that ancestor repository and prerequisite as a blocker
- **AND** Topic Git does not edit the ancestor `.gitignore`, remove ancestor index entries, or initialize the local root repository

### Requirement: Topic Git Resolves Explicit Topic Context
Every Topic Git operation SHALL resolve the selected Project, Research Topic, and Source Topic Workspace through Project Manifest-backed read-only Isomer queries before inspection or mutation.

#### Scenario: Selected topic is unresolved
- **WHEN** the operation cannot resolve one selected initialized Research Topic and Source Topic Workspace
- **THEN** it reports a blocker and performs no Git, copy, ignore, runtime, or remote mutation

#### Scenario: Sibling directories are present
- **WHEN** other Topic Workspaces exist under the generated content root
- **THEN** the skill does not infer or switch the selected topic by scanning those directories
