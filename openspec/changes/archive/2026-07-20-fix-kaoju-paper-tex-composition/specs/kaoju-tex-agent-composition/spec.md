# kaoju-tex-agent-composition Specification

## Purpose
Defines the agent-mediated MyST-to-TeX composition contract for Kaoju papers. MyST is canonical and complete; TeX is a presentational projection produced by agent judgment against a real venue template, not by mechanical conversion.

## Requirements

## ADDED Requirements

### Requirement: MyST Contains All TeX Content
The canonical MyST draft SHALL contain all content that appears in the derived TeX version, or more. TeX SHALL never introduce content absent from MyST.

#### Scenario: TeX adds no new content
- **WHEN** a composed TeX tree is inspected against its source MyST revision
- **THEN** every claim, citation, table, figure reference, and section in the TeX traces to MyST content through the citation map or direct correspondence
- **AND** venue-mandated structural text (for example running heads or keywords formatting) is the only permitted addition

#### Scenario: MyST legitimately exceeds TeX
- **WHEN** MyST contains content the venue format cannot present (for example an internal evidence boundary note)
- **THEN** the composition report records the omission and its reason
- **AND** the omission does not count as drift

### Requirement: TeX Drift Is Presentation-Only
Differences between the canonical MyST and its derived TeX SHALL be limited to formatting requirements of the target venue.

#### Scenario: Formatting drift is acceptable
- **WHEN** the agent reflows a paragraph, converts a Markdown table to `booktabs`, or maps a MyST admonition to a venue environment
- **THEN** the wording, numbers, citation keys, and claim posture remain identical to MyST
- **AND** the change needs no evidence re-audit

#### Scenario: Content drift is rejected
- **WHEN** a TeX edit changes a claim, number, citation target, or section meaning relative to MyST
- **THEN** validation reports the drift as a content defect
- **AND** the correction is applied to MyST first and the TeX is recomposed

### Requirement: Composition Is an Agent Fill Against a Real Template
The system SHALL treat MyST-to-TeX composition as the agent reading the filled MyST and filling the actual venue template by content judgment. The CLI scaffolds the template tree and a fill contract; it SHALL NOT claim faithful automatic conversion.

#### Scenario: Scaffold hands the agent a fill contract
- **WHEN** `init-tex` runs against a MyST draft and an adopted venue template
- **THEN** it materializes the real template tree, writes a fill manifest naming the obligations (title and author block from frontmatter, abstract and keywords environments, section mapping, bibliography from the citation map, tables and floats, venue-specific constructs)
- **AND** it returns each obligation as pending rather than pretending conversion succeeded

#### Scenario: Agent completes the fill
- **WHEN** the write agent processes the fill manifest
- **THEN** it edits the TeX tree so every obligation is resolved against the MyST content, records what it decided and why in the composition report
- **AND** the build path requires this recorded fill, not mere file existence

#### Scenario: Mechanical pass-through is detected
- **WHEN** composed TeX still contains raw MyST frontmatter, the placeholder title, literal `Title` or `Abstract` sections, unresolved `\cite` keys without a bibliography, or repair-marker comments
- **THEN** validation reports each as an unfilled obligation with its file location
- **AND** the tree cannot be marked inspected or build-ready

### Requirement: Bibliography Is Materialized from the Citation Map
Composition SHALL produce a real bibliography for the venue from the accepted `kaoju:citation-map`, so no citation renders as an unresolved key.

#### Scenario: Citation map becomes bibliography
- **WHEN** the fill contract includes citations
- **THEN** the agent generates the venue bibliography (`.bib` or `thebibliography`) from citation-map entries with full reference metadata
- **AND** every `\cite` key in the TeX resolves to a bibliography entry

#### Scenario: Citation-map entry lacks reference metadata
- **WHEN** a cited source has no usable bibliographic record
- **THEN** the composition pauses and reports the affected keys
- **AND** the gap is recorded as a citation-map prerequisite, not silently dropped

## Relation to Existing Specs
- `kaoju-paper-production`: this capability supplies the composition contract that the init-tex and build requirements reference.
