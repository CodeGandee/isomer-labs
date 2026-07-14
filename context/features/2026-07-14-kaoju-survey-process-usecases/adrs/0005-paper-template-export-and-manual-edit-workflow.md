# Paper Template Export And Manual Edit Workflow

Status: accepted
Date: 2026-07-14
Related: ADR-0004

UC-04 produces a Markdown paper structure and draft inside the agent chat workflow. Researchers often want to edit the template with their own editor, reorder sections, or add custom placeholders. A separate workflow is needed to export the template to the workspace filesystem, let the human edit it, and then apply the revised template back into the durable workflow.

## Current Decision

- UC-05 supports exporting the current paper template to a topic-workspace directory, with a manifest and a state-DB registration.
- The human edits the exported Markdown template with their own tools.
- When the human asks to apply the template, the agent reads it back, validates it, updates the durable `kaoju:paper-template` artifact, and regenerates `kaoju:paper-draft`.
- The export directory is either user-supplied or resolved through `isomer-cli`.

## Affected Artifacts

- `usecases/uc-05-paper-template-manual-editing-and-apply.md`: new use case describing export, manual edit, and apply actions.
- `usecases/README.md`: indexed UC-05.
- `README.md`: updated current-stage summary.

## Refinement History

### 2026-07-14 - Initial Decision

- Instruction: "get me the md template for inspection and revision", agent extracts template into a workspace directory with manifest and state-DB reference, user edits manually, then says "apply the template" or "update the paper with new template", agent reads back the template, updates durable template artifact, and regenerates the paper.
- Applied changes:
  - Created UC-05 with export, apply, and validation flows.
  - Defined `kaoju:paper-template-export`, `kaoju:paper-template-manifest`, and `kaoju:paper-template` durable outputs.
  - Added ADR-0005.
