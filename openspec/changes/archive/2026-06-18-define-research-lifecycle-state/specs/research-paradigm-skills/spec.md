## MODIFIED Requirements

### Requirement: Generic Research Vocabulary
The extracted skills SHALL describe portable research behavior using established Isomer Labs concepts and without requiring DeepScientist workspace APIs or DeepScientist-specific runtime surfaces.

#### Scenario: DeepScientist API terms are mapped to Isomer concepts
- **WHEN** an extracted skill describes artifacts, memory, terminal execution, paper search, execution isolation, workflow progress, lifecycle state, or route branching
- **THEN** it uses Isomer concepts such as Research Topic, Research Inquiry, Research Inquiry Relationship, Research Task, Run, Topic Workspace, Workspace Runtime, Agent Workspace, Artifact, Evidence Item, Finding, Research Claim, Decision Record, Gate, Provenance Record, Workflow Stage Cursor, Operator Agent, Agent Role, Agent Instance, Agent Team Instance, Agent Team Instance lifecycle state, Capability Binding, Coordination Policy, and Execution Adapter

#### Scenario: Source-specific terms are bounded
- **WHEN** an extracted skill mentions a source-specific or stale term such as DeepScientist, `artifact.*`, `memory.*`, `bash_exec(...)`, DeepXiv, quest, Research Goal, Research Thread, Research Branch, Isomer Workspace, branch, worktree, `workspace_mode`, `continuation_policy`, `auto_continue`, or `wait_for_user_or_resume`
- **THEN** the mention is limited to provenance, adaptation notes, source-term mapping, or migration notes and is not a required runtime operation or active Isomer domain term

#### Scenario: Continuation policy is not ported
- **WHEN** an extracted skill preserves DeepScientist behavior about continuing, pausing, resuming, or monitoring long-running work
- **THEN** it describes the behavior through Agent Team Instance lifecycle state under Coordination Policy, paused waiting for Operator Agent instruction, Workflow Stage Cursor recommendations, Gates, Decision Records, Completion Watcher Contracts, or Signal Observations, and does not require an Isomer `continuation_policy` field

### Requirement: Unsettled Concrete Surfaces Are Explicit
The extracted skills SHALL mark unsettled commands, runtime APIs, providers, schemas, policies, storage roots, and generated layouts as `yet-to-be-determined` only when they are not settled by accepted Isomer designs such as Workspace Path Resolution, Research Recording Contracts, or Research Lifecycle State.

#### Scenario: Path surface is covered by workspace path resolution
- **WHEN** a skill needs an ordinary Topic Workspace, Workspace Runtime, Agent Workspace, Run log, experiment output, analysis output, paper output, figure output, or Artifact class location covered by the Workspace Path Resolution contract
- **THEN** the skill names the semantic workspace scope or Artifact kind and relies on the resolver instead of emitting a path TBD placeholder

#### Scenario: Recording surface is covered by research recording contracts
- **WHEN** a skill needs to record or query Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, or Gates covered by the Research Recording Contracts
- **THEN** the skill names the accepted record type or recording API instead of emitting `api-artifact-record`, `api-finding-query`, `api-gate`, `schema-decision-record`, `schema-evidence-item`, `schema-research-claim`, or `schema-gate` TBD placeholders

#### Scenario: Lifecycle surface is covered by research lifecycle state
- **WHEN** a skill needs Workflow Stage Cursor fields, Agent Team Instance lifecycle state, or Research Inquiry Relationship branching behavior covered by Research Lifecycle State
- **THEN** the skill names the accepted lifecycle object, state, relationship, or policy instead of emitting `schema-stage-cursor`, `schema-agent-team-state`, or `policy-branching` TBD placeholders

#### Scenario: Path surface remains unsettled outside the resolver
- **WHEN** a source skill uses a concrete path or filename that is not covered by the Workspace Path Resolution contract and no Isomer equivalent is settled by existing domain concepts or ADRs
- **THEN** the extracted skill marks that path or filename as `yet-to-be-determined` and states the missing design decision

#### Scenario: Runtime API is not settled
- **WHEN** a DeepScientist source skill depends on a command, tool wrapper, runner home, prompt injection mechanism, paper-search provider, scheduler behavior, Skill Binding, baseline-waiver policy, or cost/privacy policy with no settled Isomer equivalent
- **THEN** the extracted skill marks that surface as `yet-to-be-determined` and avoids inventing an implementation-specific default

## ADDED Requirements

### Requirement: Research Lifecycle State Consumption
The research-paradigm skillset SHALL consume Research Lifecycle State for execution levels, route relationships, Workflow Stage Cursor, Agent Team Instance lifecycle state, and branching policy.

#### Scenario: Shared registry reflects resolved lifecycle surfaces
- **WHEN** `isomer-rsch-shared/references/tbd-surface-registry.md` is inspected after this change
- **THEN** `schema-stage-cursor`, `schema-agent-team-state`, and `policy-branching` are removed as open TBDs or explicitly mapped to Research Lifecycle State

#### Scenario: Skill references use accepted lifecycle terms
- **WHEN** a research-stage skill needs Research Topic, Research Inquiry, Research Inquiry Relationship, Research Task, Run, Workflow Stage Cursor, or Agent Team Instance lifecycle state
- **THEN** the skill names those accepted lifecycle terms instead of stale terms or lifecycle TBD placeholders

#### Scenario: Research Inquiry is not parallel execution scope
- **WHEN** a research-stage skill describes parallel execution
- **THEN** it describes Topic-level parallelism across Agent Team Instances or Task-level parallelism across Agent Instances and does not assign parallel execution scope to Research Inquiry

#### Scenario: Local contract copies stay consistent
- **WHEN** a local `isomer-research-contract.md` copy is inspected in an `isomer-rsch-*` skill directory
- **THEN** its lifecycle guidance matches Research Lifecycle State and does not reintroduce Research Goal, Research Thread, Research Branch, Isomer Workspace, or resolved lifecycle TBD placeholders as active terms

#### Scenario: Non-lifecycle TBD surfaces remain explicit
- **WHEN** a research-stage skill needs unsettled command execution, scheduler behavior, literature provider, Skill Binding, baseline-waiver policy, cost/privacy Gate policy, or concrete Capability Binding behavior
- **THEN** the skill continues to use the appropriate TBD placeholder until that surface has its own accepted Isomer contract

#### Scenario: Validation checks stale and resolved lifecycle surfaces
- **WHEN** implementation validation runs
- **THEN** it confirms stale lifecycle terms are removed or confined to provenance and mapping notes, resolved lifecycle TBDs are removed or mapped to Research Lifecycle State, and remaining TBD placeholders are still registered
