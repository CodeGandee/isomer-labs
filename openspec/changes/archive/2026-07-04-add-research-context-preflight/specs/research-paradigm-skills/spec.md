## ADDED Requirements

### Requirement: V2 Skills Apply Latest Context Preflight
Active non-shared v2 research-paradigm skills with durable record bindings SHALL apply the shared latest-context preflight before accepted durable record writes, record refreshes, or durable stage decisions.

#### Scenario: Durable-record-writing skill entrypoints reference preflight
- **WHEN** an active non-shared v2 research skill `SKILL.md` with durable record bindings is inspected
- **THEN** its workflow or entry guidance references the shared latest-context preflight from `isomer-rsch-shared-v2`
- **AND** it places the preflight before accepted record writes, record refreshes, or durable stage decisions that select routes, accept comparator state, generate ideas, run experiments, analyze evidence, write claims, review manuscripts, create figures, polish prose, prepare data availability, rebut reviewers, or finalize a topic
- **AND** standalone source-only reading may skip the preflight until the skill writes or refreshes accepted Isomer records

#### Scenario: Shared skill owns the reference
- **WHEN** `isomer-rsch-shared-v2` is inspected
- **THEN** it contains the latest-context preflight reference and semantic registry entry
- **AND** other v2 skills reference that shared material instead of duplicating the full command ladder

#### Scenario: Stage context objects carry freshness verdicts
- **WHEN** a v2 skill creates or refreshes its first durable context object for a pass
- **THEN** the object includes a freshness verdict or an explicit pointer to the latest-context-snapshot content
- **AND** downstream stage work does not proceed when that verdict reports a blocking conflict, missing topic context, invalid runtime, or unresolved active-record ambiguity

### Requirement: V2 Skills Do Not Trust Remembered Research Context
Active non-shared v2 research-paradigm skills with durable record bindings SHALL prefer current Isomer context and durable records over prompt memory, chat memory, or older rendered prose when accepting durable record work.

#### Scenario: Prompt context is treated as input, not authority
- **WHEN** a user prompt includes a Research Topic, route, metric, paper state, or current result that will shape accepted durable record work
- **THEN** the invoked v2 skill treats that prompt as candidate context
- **AND** it checks the current Effective Topic Context and relevant durable records before treating the prompt as the active research context

#### Scenario: Older rendered records are not silently reused
- **WHEN** a v2 skill finds older rendered Markdown for a context object, contract, route, result, finding, paper state, or blocker
- **THEN** it checks record metadata, structured payload status, record status, updated timestamp, and active or supersession signals before using that record as current
- **AND** it routes to decision or blocker handling when the active version cannot be identified

#### Scenario: Scope changes are recorded or routed
- **WHEN** the preflight determines that the user changed the Research Topic scope, accepted dataset, comparator basis, metric contract, evaluation contract, paper target, or claim boundary
- **THEN** the invoked v2 skill records the scope-change implication in its context object or route decision
- **AND** it routes to scout, baseline, decision, paper-outline, workspace bootstrap, or blocker handling when the current stage is no longer ready

### Requirement: Research Skill Validation Covers Context Preflight
The research-paradigm validation harness SHALL check that active non-shared v2 skill entrypoints with durable record bindings include the shared latest-context preflight contract.

#### Scenario: Missing preflight is reported
- **WHEN** validation inspects an active non-shared v2 `SKILL.md` with durable record bindings that lacks a reference to the shared latest-context preflight
- **THEN** validation reports the skill and explains that v2 durable-record-writing entrypoints must resolve current topic context before accepted record work

#### Scenario: Shared and non-active material are not false positives
- **WHEN** validation inspects `isomer-rsch-shared-v2`, migration notes, source-copy material under `org/`, passive templates, or non-active provenance material
- **THEN** it does not require those files to consume the latest-context preflight as a stage entrypoint

#### Scenario: Validation accepts concise imports
- **WHEN** a v2 stage skill references the shared preflight and states that it must run before prompt memory or prior prose is trusted
- **THEN** validation accepts the entrypoint without requiring the full command ladder to be duplicated in that skill

#### Scenario: Worker output policy remains distinct
- **WHEN** validation inspects a v2 skill that already references worker output policy for plain generated files
- **THEN** that worker-output guidance does not satisfy the latest-context preflight requirement for accepted durable record work
- **AND** the latest-context preflight rule does not replace the worker-output-root policy, operation output set, or `commit_after_operation` requirements for plain file writes
