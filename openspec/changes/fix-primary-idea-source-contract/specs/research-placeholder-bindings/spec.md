## ADDED Requirements

### Requirement: Placeholder Bindings Declare Idea-bearing Payload Sections
Active production DeepSci placeholder binding pages SHALL declare exact idea-bearing payload sections for structured records that create, select, reject, defer, merge, subsume, or follow up Research Ideas.

#### Scenario: Idea-producing binding names source path pattern
- **WHEN** a `placeholder-bindings.md` row describes an idea-producing structured profile such as raw idea slate, candidate idea frontier, pre-idea draft, selected hypothesis, selected idea draft, rejected/deferred ideas, route decision, or paper-facing idea seed
- **THEN** the binding guidance names the payload section or path pattern that contains idea entries
- **AND** it distinguishes those entries from filter notes, report summaries, decision context, and provenance fields

#### Scenario: Binding command preserves exact source path
- **WHEN** a binding instructs an agent to record canonical Research Idea data for an idea-bearing record
- **THEN** the guidance tells the agent to pass exact item paths such as `$.sections.raw_ideas[0]` to `ext research ideas realize` or record-create idea convenience metadata
- **AND** it forbids collection paths, payload-root paths, generated Markdown paths, and context-only note paths as Primary Idea realization sources
- **AND** it treats executable profile-to-section mapping as owned by the shared CLI/runtime source-fragment registry rather than by free-form skill prose

### Requirement: Placeholder Binding Validation Checks Idea Source Contracts
The placeholder binding validation harness SHALL check active DeepSci idea-producing bindings for exact source-fragment guidance.

#### Scenario: Missing idea source guidance is reported
- **WHEN** validation inspects an active production DeepSci binding for an idea-producing structured profile and no idea-bearing section or source path pattern is documented
- **THEN** validation reports the skill, placeholder, and missing source-fragment guidance

#### Scenario: Broad path guidance is reported
- **WHEN** validation finds a binding that tells agents to realize Primary Ideas to a payload root, list path, generated Markdown file, or context-only section
- **THEN** validation reports the binding as violating the Primary Idea source contract
