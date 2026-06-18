## MODIFIED Requirements

### Requirement: Research Topic Config Content
The system SHALL define Research Topic Config TOML as topic-specific configuration for defaults and refs, not as Workspace Runtime state.

#### Scenario: Topic config identifies its topic
- **WHEN** a Research Topic Config is loaded
- **THEN** the system requires its `research_topic_id` to match the Project Manifest Research Topic registration that referenced it

#### Scenario: Topic config can carry topic defaults
- **WHEN** a Research Topic Config is inspected
- **THEN** it may define topic statement text or refs, Measurable Objective text or refs, default Research Inquiry refs, default Topic Agent Team Profile refs, default Execution Adapter refs, default Control Mode, Capability Binding refs, Skill Binding projection refs, Research Operation Extension Point refs, Gate policy refs, scheduler policy refs, baseline-waiver policy refs, literature provider refs, Artifact Format Profile defaults, and Artifact Extension refs

#### Scenario: Topic statement can be inline and artifact-backed
- **WHEN** a Research Topic Config describes the Research Topic
- **THEN** it may include one short inline `topic_statement` for discovery, CLI previews, and human review, plus `topic_statement_artifact_refs` or other explicit Artifact refs for richer or evolving topic material

#### Scenario: Topic statement refs do not make config runtime state
- **WHEN** Research Topic Config references richer topic briefs, user notes, rationale, source notes, or objective material as Artifacts
- **THEN** the config stores only refs to those Artifacts and does not embed their rich content as authoritative Workspace Runtime state

#### Scenario: Topic config does not own runtime truth
- **WHEN** a Research Topic Config contains Run status, command outputs, live process ids, resolved command results, provider payloads, scheduler internals, Artifact contents, Evidence Items, Findings, Gates, Decision Records, or Provenance Records as authoritative state
- **THEN** validation reports the config as invalid and directs those facts to Workspace Runtime or file-backed Artifacts

#### Scenario: Topic config does not store secrets
- **WHEN** a Research Topic Config contains inline credentials, tokens, API keys, passwords, or secret material
- **THEN** validation reports the config as invalid and directs the value to a credential backend or a Capability Binding ref

#### Scenario: Topic config extension refs are declarative
- **WHEN** a Research Topic Config names Research Operation Extension Point refs, Capability Binding refs, Skill Binding projection refs, literature provider refs, baseline-waiver policy refs, scheduler policy refs, cost/privacy Gate policy refs, or Execution Adapter refs
- **THEN** validation treats those values as declarative refs for later command, provider, policy, and skill availability resolution and does not execute or dereference provider-specific implementation bodies while loading the config

#### Scenario: Topic config does not replace team profile binding
- **WHEN** a Research Topic Config names topic-level defaults for extension refs, provider refs, policy refs, or Execution Adapter refs
- **THEN** validation keeps role-scoped, Workflow Stage-scoped, skill-availability, and operation-authority details in Topic Agent Team Profile, Capability Binding, or Skill Binding projection material rather than treating Research Topic Config as the complete execution binding

### Requirement: Effective Topic Context
The system SHALL resolve an Effective Topic Context before `isomer-cli` performs a topic-scoped command.

#### Scenario: Effective context contains core refs
- **WHEN** `isomer-cli` resolves Effective Topic Context
- **THEN** the context includes Project root, Project Config Directory, Project Manifest path, Research Topic id, Research Topic Config path, Topic Workspace id, Topic Workspace path input, schema versions, and resolution source metadata

#### Scenario: Effective context carries optional lifecycle refs
- **WHEN** the user or environment selects a Research Inquiry, Research Task, Run, Agent Team Instance, Agent Instance, or Topic Agent Team Profile
- **THEN** the context carries those refs only after validating that they belong to the selected Research Topic and Topic Workspace

#### Scenario: Effective context carries defaults and extension refs
- **WHEN** Research Topic Config or Project Manifest defaults name Topic Agent Team Profiles, Execution Adapters, Capability Binding refs, Skill Binding projection refs, Research Operation Extension Point refs, Control Mode defaults, scheduler policy refs, baseline-waiver policy refs, literature provider refs, or Gate policy refs
- **THEN** the context exposes those values as refs for the current command without treating them as command outputs, runtime truth, credentials, provider payloads, or implementation bodies

#### Scenario: Effective context carries artifact format defaults
- **WHEN** Research Topic Config, Research Task expected outputs, or explicit command context names Artifact Format Profile defaults or Artifact Extension refs
- **THEN** the context exposes those refs for expected output planning and Artifact recording without making them mandatory core Artifact fields

#### Scenario: Effective context is process input
- **WHEN** Effective Topic Context is produced
- **THEN** the system treats it as a resolved process input for `isomer-cli`, Workspace Path Resolution, Run initialization, Execution Adapter Command Requests, and provider-backed extension operations, not as a replacement for Research Lifecycle State or Workspace Runtime records

#### Scenario: Run records store refs and resolution sources
- **WHEN** a Run, Run plan, Execution Adapter Command Request, or provider-backed extension operation consumes Effective Topic Context
- **THEN** the durable record stores validated refs, resolution source metadata, and consumed config or default versions instead of storing the full Effective Topic Context snapshot

#### Scenario: Stored context refs remain bounded
- **WHEN** the durable record stores context refs from Effective Topic Context
- **THEN** it may include selected Project, Research Topic, Research Topic Config, Topic Workspace, Research Inquiry, Research Task, Run, Topic Agent Team Profile, Agent Team Instance, Agent Instance, Execution Adapter, Capability Binding, Skill Binding projection, Research Operation Extension Point, scheduler policy, baseline-waiver policy, literature provider, Gate policy, Artifact Format Profile, and Artifact Extension refs that influenced the action

#### Scenario: Stored context sources are explainable
- **WHEN** a context ref or default is stored for audit
- **THEN** the record identifies whether it came from an explicit selector, current directory, supported environment variable, `.isomer-labs/local.toml`, Project Manifest default, Research Topic Config, Topic Agent Team Profile, Domain Agent Team Template, built-in default, Workspace Runtime record, or explicit command context

### Requirement: Topic Context Validation
The system SHALL validate Effective Topic Context before Run creation, Execution Adapter dispatch, provider-backed extension dispatch, or Workspace Runtime mutation.

#### Scenario: Topic refs are consistent
- **WHEN** Effective Topic Context includes Research Topic, Topic Workspace, Research Inquiry, Research Task, Run, Agent Team Instance, or Agent Instance refs
- **THEN** validation confirms those refs belong to the same Project and Research Topic or reports a context mismatch

#### Scenario: Topic config schema is checked
- **WHEN** a Research Topic Config is loaded
- **THEN** validation checks its schema version, required fields, allowed field classes, path bounds, ref consistency, and extension-ref field classes before the config can influence topic-scoped command behavior

#### Scenario: Missing references are reported
- **WHEN** Effective Topic Context references a missing Research Topic Config, Topic Workspace, Topic Agent Team Profile, Capability Binding ref, Skill Binding projection ref, Research Operation Extension Point ref, Gate policy ref, scheduler policy ref, baseline-waiver policy ref, literature provider ref, Research Task, Run, Agent Team Instance, or Agent Instance
- **THEN** validation reports the missing ref and blocks only the command behavior that depends on that ref

#### Scenario: Validation preserves provider-neutral boundaries
- **WHEN** Effective Topic Context names execution, scheduler, Skill Binding, baseline-waiver, cost/privacy, credential, literature provider, or data-export extension refs
- **THEN** validation confirms those refs are syntactically valid and leaves provider-specific implementation behavior to the accepted Research Execution and Extension Contract and selected provider or adapter

#### Scenario: Validation rejects inline implementation bodies
- **WHEN** Effective Topic Context or its source config includes inline provider-specific command bodies, credentials, tokens, API keys, live process state, command outputs, provider payloads, or scheduler internals
- **THEN** validation rejects those fields and directs them to the appropriate adapter payload ref, credential backend, Workspace Runtime record, Artifact, or Provenance Record

### Requirement: CLI Command Scope Boundaries
The system SHALL distinguish project-scoped, topic-scoped, run-scoped, and extension-backed `isomer-cli` command behavior in the first implementation.

#### Scenario: Project-scoped command families do not require topic
- **WHEN** a command validates or inspects the Project Manifest, lists registered Research Topics, lists Topic Workspaces, inspects built-in schemas, or checks project-level config without selecting one Research Topic
- **THEN** the command may run with Project context only and does not require Effective Topic Context

#### Scenario: Topic-scoped command families require topic context
- **WHEN** a command shows or validates Effective Topic Context, creates or inspects Research Inquiries, Research Tasks, Artifacts, Gates, Topic Agent Team Profiles, Agent Team Instance topic-participation records, topic-scoped views, or topic-specific path previews
- **THEN** the command resolves and validates Effective Topic Context before performing the action

#### Scenario: Run-scoped command families require run consistency
- **WHEN** a command inspects, resumes, cancels, records, or exports a Run
- **THEN** the command validates that the selected Run belongs to the selected Research Task, Research Inquiry, Research Topic, and Topic Workspace

#### Scenario: Workspace path commands use project or topic scope
- **WHEN** a command lists registered Topic Workspaces
- **THEN** the command remains project-scoped
- **AND WHEN** a command previews or resolves paths for one selected Topic Workspace
- **THEN** the command is topic-scoped and resolves Effective Topic Context

#### Scenario: Extension-backed commands use execution extension contract
- **WHEN** `isomer-cli` prepares to execute a shell command, package manager command, HPC job, notebook action, literature provider request, document build, figure render, service request, agent launch, baseline-waiver check, or other provider-backed operation
- **THEN** this contract supplies and validates Effective Topic Context while the Research Execution and Extension Contract defines the command request, extension refs, preflight, scheduler boundary, provider binding, and recording obligations
