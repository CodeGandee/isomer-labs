# research-paradigm-skills Specification

## Purpose

See `openspec/specs/research-paradigm-skills/spec.md` for the full specification. This delta updates the canonical list of production DeepSci skill folders to include the new `isomer-deepsci-pipeline` skill.

## MODIFIED Requirements

### Requirement: Research Paradigm Skillset Layout

The project SHALL provide a reusable production DeepSci research-paradigm skillset under `skillset/research-paradigm/deepsci/` using Codex skill folder layout and the `isomer-deepsci-<purpose>` naming convention for research-stage method skills only.

#### Scenario: Production DeepSci skill folders exist

- **WHEN** the production DeepSci research-paradigm skillset is inspected
- **THEN** it contains `isomer-deepsci-shared` and folders for scout, baseline, idea, optimize, experiment, analysis, decision, finalize, science, write, review, rebuttal, paper-outline, paper-plot, figure-polish, nature-data, nature-figure, nature-paper2ppt, nature-polishing, workspace-mgr, and pipeline
