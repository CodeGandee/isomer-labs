# MyST As Canonical Paper Format

Status: accepted
Date: 2026-07-14
Related: ADR-0004, ADR-0005

UC-04 originally specified Markdown as the paper format, and ADR-0004 removed the Tectonic-first `.tex` constraint. The new UC-06 requires generating a PDF from the paper, which needs an intermediate LaTeX stage. The chosen canonical format is MyST: it is rich enough for structured survey papers, can be mechanically converted to Markdown for review, and can be converted to LaTeX for PDF production.

## Current Decision

- MyST is the **canonical paper format** for this feature.
- UC-04 produces `kaoju:paper-structure-myst` and `kaoju:paper-draft-myst`.
- A Markdown view `kaoju:paper-draft-md` can be derived automatically from MyST for human review.
- UC-06 converts the canonical MyST draft to LaTeX and compiles it to PDF.
- MyST-to-LaTeX conversion is hard; a script may initialize the `.tex` file, but the agent is expected to inspect and edit the `.tex` file directly to resolve directives, tables, citations, floats, and other conversion artifacts.
- UC-05's manual template export now exports the MyST template (as a `.md` file) and applies revisions back to `kaoju:paper-template-myst`.
- ADR-0004 is superseded by this decision.

## Affected Artifacts

- `feature-requirement.md`: updated functional and operational constraints to describe MyST-first paper production with derived Markdown and LaTeX/PDF views.
- `usecases/uc-04-write-paper-from-digested-materials.md`: changed canonical outputs from Markdown to MyST; added derived Markdown view.
- `usecases/uc-05-paper-template-manual-editing-and-apply.md`: updated to export and apply MyST templates.
- `usecases/uc-06-create-paper-pdf.md`: new use case describing MyST-to-LaTeX-to-PDF generation with agent-assisted TeX refinement.
- `usecases/README.md`: indexed UC-06.
- `README.md`: updated current-stage summary.

## Refinement History

### 2026-07-14 - Initial Decision

- Instruction: "now write the pdf version of the paper" / "create the paper pdf"; agent generates TeX template, TeX paper, and PDF; MyST chosen as canonical storage; MyST-to-Markdown is simple script conversion; MyST-to-LaTeX is hard, so scripted conversion is only for initialization (or can be skipped), and the agent handles the rest by direct file inspection and editing.
- Applied changes:
  - Created UC-06 with TeX template, TeX draft, and PDF compile actions.
  - Revised UC-04 to produce MyST drafts with optional derived Markdown.
  - Revised UC-05 to export and apply MyST templates.
  - Updated feature requirement to reflect MyST-first production.
  - Superseded ADR-0004 with ADR-0006.
