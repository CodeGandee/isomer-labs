## ADDED Requirements

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
