# Paper Contract

The paper contract fixes the publication boundary before any manuscript drafting begins. It is a current-state record that can be revised when the publication target or evidence boundary changes, but a change to accepted evidence meaning must route back through audit and synthesis.

## Required Fields

- `target`: intended audience or venue
- `venue` or `paper_type`: submission target or paper category
- `survey_questions`: the questions the survey answers
- `scope`: included and excluded material, temporal cutoff, source classes
- `contribution_posture`: taxonomy, coverage, synthesis, comparative perspective, dataset, or gap-mapping contribution; novelty is optional
- `evidence_boundary`: accepted Audit Report, Field Summary, Claim Status Table, Related-Work Catalog, Source Digests or Claim-Evidence Ledger, dossier, comparison, Finding, and Run refs
- `template_ref`: ref to a generated or supplied LaTeX template
- `tex_entry`: `.tex` entry point relative to the template root
- `compiler_owned_numbering`: true; the compiler generates all section numbers
- `unnumbered_sections`: list of front and back matter handled by the template natively
- `citation_policy`: how citations are resolved and verified
- `display_expectations`: tables, figures, and their required question/takeaway framing
- `build_policy`: Tectonic-first, allowed LaTeX fallback, output form
- `quality_metrics`: survey-quality dimensions, thresholds, warning policy
- `validation_requirements`: structural, citation, compile, extracted-text, visual, and accessibility checks
- `gate_policy`: applicable publication-facing Gate policy ref

## Constraints

- The contract cannot strengthen verdicts, hide limitations, or add unsupported claims.
- A requested change that alters evidence meaning routes back to the owning Kaoju stage.
- Markdown-to-PDF conversion is never an accepted build path.
