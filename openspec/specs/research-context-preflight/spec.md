# research-context-preflight Specification

## Purpose
TBD - created by archiving change add-research-context-preflight. Update Purpose after archive.
## Requirements
### Requirement: Shared Latest Context Preflight
The research-paradigm v2 shared contract SHALL define a latest-context preflight that agents use before accepted durable research record work begins.

#### Scenario: Preflight resolves Effective Topic Context first
- **WHEN** an agent invokes a v2 research skill with durable record bindings and Project context available
- **THEN** the preflight tells the agent to resolve the current Effective Topic Context through `isomer-cli --print-json project context show`
- **AND** the preflight treats the resolved Research Topic id, Research Topic Config path, Topic Workspace path, resolution sources, and effective Topic Actor or Agent context as the starting context for the stage

#### Scenario: Preflight uses safe follow-up queries
- **WHEN** an agent needs additional context commands after resolving Effective Topic Context
- **THEN** the preflight tells the agent to use `isomer-cli --print-json project self queries` or documented shared query guidance to discover safe follow-up commands
- **AND** it does not tell the agent to infer topic identity from sibling directories, remembered context, or hard-coded paths

#### Scenario: Preflight inspects runtime before trusting old state
- **WHEN** the selected Research Topic has a Topic Workspace
- **THEN** the preflight tells the agent to inspect Workspace Runtime with `isomer-cli --print-json project runtime inspect --topic <topic>`
- **AND** it treats missing, invalid, stale, or contradictory runtime evidence as a blocker or route-to-bootstrap condition before accepted research records are written

### Requirement: Latest Relevant Records Are Checked
The latest-context preflight SHALL instruct agents to inspect the durable records relevant to the invoked stage before relying on prior stage prose or chat memory.

#### Scenario: Placeholder records are listed before use
- **WHEN** accepted durable record work depends on a prior context brief, contract, route decision, hypothesis, result, analysis finding, paper state, or blocker
- **THEN** the preflight tells the agent to list candidate records with `isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'`
- **AND** it tells the agent to use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-payload --include-rendered-body` when the payload or rendered body is needed

#### Scenario: Duplicate ready records require an active-record judgment
- **WHEN** record listing returns multiple ready records for the same placeholder or semantic object
- **THEN** the preflight treats the newest ready record as only the default candidate
- **AND** it requires the agent to prefer explicit active, supersession, route, or decision metadata when present
- **AND** it requires decision or blocker routing when competing ready records conflict and no active record can be identified responsibly

#### Scenario: Generated views are not the source of truth
- **WHEN** a listed record has a structured payload and a generated Markdown view
- **THEN** the preflight tells the agent to treat the structured payload and record metadata as authoritative for machine-readable fields
- **AND** it treats generated Markdown as review material unless the producing binding declares otherwise

### Requirement: Freshness Verdict Is Captured
The latest-context preflight SHALL produce or feed a stage-local freshness verdict before the stage accepts durable route, claim, context, evidence, result, or publication-facing records.

#### Scenario: Stage context records include freshness evidence
- **WHEN** a v2 stage creates or refreshes its first accepted durable context object
- **THEN** that object records which Effective Topic Context, Workspace Runtime inspection, and relevant record placeholders were checked
- **AND** it records whether prompt-provided context matched durable context, refined it, conflicted with it, or implied a Research Topic scope change

#### Scenario: Context conflict changes route
- **WHEN** prompt-provided context conflicts with durable Research Topic context, current route records, accepted comparator basis, metric contract, paper state, or blocker records
- **THEN** the preflight requires the agent to route to scout, decision, workspace bootstrap, or a blocker instead of continuing stage work from memory

#### Scenario: External freshness is stage-specific
- **WHEN** the preflight says to look up latest context
- **THEN** it means current Isomer topic, runtime, and record state by default
- **AND** it requires external web, literature, journal, package, repository, or benchmark freshness only when the invoked stage already depends on that external source class

#### Scenario: Plain worker outputs are not durable context
- **WHEN** a skill writes plain generated files under the worker output root
- **THEN** the preflight treats those files as worker-local outputs, not accepted durable research records
- **AND** the preflight applies before those files are promoted, recorded, or refreshed as accepted Artifacts, Evidence Items, Run records, Decision Records, View Manifests, context briefs, contracts, route decisions, or other durable research records

### Requirement: Preflight Remains Storage-Neutral
The latest-context preflight SHALL expose a semantic context snapshot without forcing a new storage binding for every stage.

#### Scenario: Shared semantic object is registered
- **WHEN** the v2 shared semantic-placeholder registry is inspected
- **THEN** it includes a semantic object for `latest-context-snapshot`
- **AND** that object names the selected topic refs, config source, runtime readiness, effective actor or agent context, checked record refs, and freshness verdict as required semantic content

#### Scenario: Existing stage objects may satisfy snapshot content
- **WHEN** a stage already creates a context brief, objective contract, experiment contract, paper control state, closure context, or similar first-stage object
- **THEN** that object may carry the latest-context-snapshot content
- **AND** the stage is not required to create a separate durable record solely for the snapshot unless another binding or user request requires it


### Requirement: Research Preflight Reconciles and Retains the Task Target
The latest-context preflight SHALL reconcile prompt-selected Research Topic and worker targets with ambient and Effective Context before durable research work and SHALL retain the reconciled target on subsequent commands.

#### Scenario: Prompt-selected topic is queried explicitly
- **WHEN** a research prompt names one Research Topic
- **THEN** preflight runs its context and self queries with an explicit selector for that Research Topic
- **AND** it does not allow Project-root cwd or Project Manifest defaults to replace the prompt-selected target

#### Scenario: Unnamed topic may use reported default
- **WHEN** a topic-scoped research prompt names no Research Topic and no stronger context source applies
- **THEN** preflight may accept a valid Project Manifest default
- **AND** the freshness evidence records that source before later commands pin the selected topic

#### Scenario: Prompt and resolved target conflict
- **WHEN** prompt-provided topic or worker context conflicts with active switch posture or validated explicit context
- **THEN** preflight records the conflicting sources and stops before accepted durable writes
- **AND** it requires a corrected selector, identity reset, or explicit scope decision rather than choosing from chat memory

#### Scenario: Subsequent record queries retain selected topic
- **WHEN** preflight resolves one Research Topic and continues to runtime inspection, record queries, template operations, TeX composition or PDF build operations, or accepted durable writes
- **THEN** every applicable CLI call carries the resolved `--topic` selector
- **AND** changing cwd during the stage does not change the Research Topic target

#### Scenario: Scope change requires renewed preflight
- **WHEN** the user or workflow intentionally changes Research Topic, Topic Actor, Agent, or operation scope after preflight
- **THEN** the stage reruns context alignment for the new target
- **AND** it does not reuse the prior target's freshness verdict as evidence for the new target
