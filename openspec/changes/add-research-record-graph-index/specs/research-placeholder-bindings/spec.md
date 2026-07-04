## ADDED Requirements

### Requirement: Placeholder Bindings Describe Query-index Metadata
Active production DeepSci placeholder binding pages SHALL describe expected relationship, file, and GUI facet metadata for structured research records.

#### Scenario: Binding names expected relationship metadata
- **WHEN** a `placeholder-bindings.md` row describes a structured record profile that normally consumes, produces, routes to, supports, supersedes, summarizes, or cites other records
- **THEN** the binding guidance names the expected relationship intent and the record refs or payload fields an agent should preserve at write time

#### Scenario: Binding names expected file metadata
- **WHEN** a structured placeholder normally produces or cites durable files, operation-set outputs, rendered Markdown, figures, logs, configs, raw results, or manifests
- **THEN** the binding guidance names the expected file role, semantic label, and source payload field or output location pattern when known

#### Scenario: Binding names expected GUI facets
- **WHEN** a structured placeholder normally carries GUI-relevant ideas, route decisions, metrics, claims, artifact lists, or generic scalar facts
- **THEN** the binding guidance names those expected facets and the profile or payload section that drives extraction

#### Scenario: Skills are not required to hand-author every index row
- **WHEN** a binding describes query-index metadata for a structured profile
- **THEN** it can rely on profile-driven extractors for derived facet rows while still requiring agents to preserve explicit authored refs that only the producing skill knows
