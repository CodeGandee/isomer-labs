# Markdown-First Paper Drafting

Status: superseded by ADR-0006
Date: 2026-07-14
Related: ADR-0003, ADR-0006

The feature requirement originally stated that paper production must be Tectonic-first `.tex`. The new UC-04 instead writes the paper in Markdown and focuses on content, leaving formatting to a separate workflow.

## Current Decision

- Paper production in this feature is **Markdown-first and content-focused**.
- The agent produces a `KAOJU:PAPER-STRUCTURE-MYST` artifact and then a `KAOJU:PAPER-DRAFT-MYST` artifact.
- LaTeX formatting, PDF rendering, typography, and citation styling are explicitly out of scope for UC-04 and for this feature's paper-writing workflow.
- The feature requirement and UC-04 are updated to reflect this decision.

## Affected Artifacts

- `feature-requirement.md`: updated functional requirement to describe a Markdown paper draft and updated operational constraint to allow Markdown-first output.
- `usecases/uc-04-write-paper-from-digested-materials.md`: new use case describing the two-stage structure-then-fill Markdown paper workflow.
- `usecases/README.md`: indexed UC-04.
- `README.md`: updated current-stage summary.

## Refinement History

### 2026-07-14 - Initial Decision

- Instruction: "now write a paper given currently digested materials", agent writes the paper in Markdown focusing on content, first producing a structure artifact with placeholders and then filling it.
- Applied changes:
  - Created UC-04 with supported actions for producing structure, filling structure, and reviewing the draft.
  - Replaced the Tectonic-first `.tex` operational constraint with a Markdown-first, content-focused constraint.
  - Added ADR-0004.
