## ADDED Requirements

### Requirement: DeepSci Skills Preserve Exact Idea Content
Production DeepSci skills SHALL teach agents to preserve Primary Idea content separately from slate/report context and to record exact Idea Realization source paths.

#### Scenario: Idea skill records exact source fragments
- **WHEN** `isomer-deepsci-idea` produces raw slates, candidate frontiers, pre-idea drafts, selected hypotheses, selected idea drafts, rejected/deferred ideas, route decisions, or paper-facing idea seeds
- **THEN** its workflow and directly linked research-idea recording guidance tell the agent to write canonical Research Ideas and Idea Realizations with exact object-valued source paths
- **AND** the guidance says that filter notes, summaries, and route context belong to the source record, not the Primary Idea main content

#### Scenario: Downstream skills update existing idea identity
- **WHEN** experiment, analysis, optimize, decision, write, review, rebuttal, or finalize skills support, refute, narrow, supersede, or follow up a Research Idea
- **THEN** their guidance tells the agent to update or realize the existing Research Idea when the concept is unchanged
- **AND** it tells the agent to create a new Research Idea only for a true follow-up or alternative concept with explicit lineage

### Requirement: Packaged DeepSci Skills Carry Source Contract Guidance
Packaged system-skill assets SHALL include the same Primary Idea source contract guidance as the repository skillset.

#### Scenario: Package skill mirrors are updated
- **WHEN** repository skill guidance or placeholder bindings are updated for exact idea source fragments
- **THEN** the corresponding files under `src/isomer_labs/assets/system_skills/research-paradigm/deepsci/` are updated consistently
- **AND** packaged skill validation does not route installed agents to stale broad-path guidance
