## ADDED Requirements

### Requirement: DeepSci Skills Record Research Idea Identity
Production DeepSci skills SHALL record stable Research Idea identity when producing idea-bearing durable records.

#### Scenario: Idea skill records candidate ideas
- **WHEN** `isomer-deepsci-idea` produces raw idea slates, candidate frontiers, pre-idea drafts, selected hypotheses, selected idea drafts, rejected ideas, or deferred ideas
- **THEN** the skill instructs the agent to record stable semantic topic-scoped Research Idea ids, source-local aliases, visibility, status, realization records, source JSON paths, sibling generation groups, and idea lineage where the relationship is known

#### Scenario: Experiment skill records explicit idea outcome
- **WHEN** `isomer-deepsci-experiment` records an experiment result that supports, refutes, narrows, or motivates a follow-up to a selected idea
- **THEN** the skill instructs the agent to explicitly update the relevant Research Idea status or create a follow-up Research Idea with canonical idea lineage and supporting evidence refs

#### Scenario: Experiment result does not auto-mutate idea
- **WHEN** `isomer-deepsci-experiment` records an experiment result without an explicit accepted idea status update
- **THEN** the skill guidance treats the result as evidence or a stale-status diagnostic and does not claim that the Research Idea status changed automatically

#### Scenario: Analysis skill records conceptual redirection
- **WHEN** `isomer-deepsci-analysis` concludes that the current line should continue, revise, split, merge, or return to ideation
- **THEN** the skill instructs the agent to record the affected Research Idea relationship, realization, status change, or follow-up idea before routing onward

### Requirement: DeepSci Skills Separate Idea Lineage from Record Lineage
Production DeepSci skills SHALL distinguish record lineage from idea lineage in active workflow guidance.

#### Scenario: Durable record has both lineage layers
- **WHEN** a DeepSci skill produces a durable record from prior durable records and the record also expresses an idea relationship
- **THEN** the skill instructs the agent to record record parents through `--parents-json` and idea parents through the Research Idea CLI/API or accepted idea metadata fields

#### Scenario: Siblings use generation group
- **WHEN** a DeepSci idea pass creates alternative serious candidates from the same parent context
- **THEN** the skill instructs the agent to use an idea generation group rather than pairwise sibling edges as the primary sibling representation

#### Scenario: Candidate collapse records subsumption
- **WHEN** a DeepSci idea pass concludes that one serious candidate subsumes another as an ablation, mechanism subset, or test role
- **THEN** the skill instructs the agent to record a canonical `subsumes` idea lineage edge in addition to the shared generation group

#### Scenario: Markdown is not authoritative lineage
- **WHEN** a DeepSci skill renders or writes Markdown for human review
- **THEN** the skill instructs the agent that Markdown prose does not replace canonical Research Idea rows, realizations, lineage edges, or generation groups

### Requirement: Skill Validation Covers Idea Recording Guidance
The research-paradigm skill validation harness SHALL detect missing or contradictory active guidance for Research Idea recording.

#### Scenario: Idea recording guidance is present
- **WHEN** the validation harness inspects active DeepSci idea, experiment, analysis, decision, optimize, and shared skill guidance
- **THEN** it confirms that idea-bearing workflows mention canonical Research Idea identity, realization, and lineage obligations where applicable

#### Scenario: Contradictory guidance is reported
- **WHEN** active skill guidance tells agents to infer authoritative idea lineage only from chat memory, generated Markdown, or record-lineage projection
- **THEN** validation reports the guidance as stale and directs the skill to use canonical Research Idea recording
