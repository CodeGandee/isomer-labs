# MyST Manuscript Structure

The paper separates a reader-facing narrative from an auditable evidence view. Both are authored in canonical MyST and linked through typed roles, directives, citations, display refs, and source refs. Drafting resolves an explicitly named content template or content `main` and records its stable ref, state token, and observed tree digest. LaTeX presentation selection is separate and occurs only when TeX or PDF output is requested.

## Adaptive Profiles

Choose a structure for the accepted direction and evidence shape. A taxonomy survey may center categories and boundary cases; a system lineage may center mechanisms and transitions; an empirical comparison may center intent, fairness, and results. Every profile still covers motivation, scope, survey method, synthesis, limitations, and answers to the survey questions.

Record the profile id, rationale, section order, section jobs, required evidence roles, planned displays, and venue constraints in `KAOJU:PAPER-STRUCTURE-MYST`. Do not select a profile from venue convention alone.

Reconcile the accepted Field Summary's lecture commitment basis before structure review. Give each active lecture-ready paper one dedicated named section with that paper as the primary subject. Record the section's paper identity, lecture Run, Source Digest, reader outcome, evidence boundary, equation and display jobs, limitations, and recovery posture. Preserve blocked commitments as unresolved structure obligations and explicit supersessions in paper lineage. A citation, list item, shared short paragraph, later non-lecture Run, or shorter treatment cannot discharge a lecture commitment.

## MyST Requirements

- Carry the paper title and authors in the MyST YAML frontmatter block, not in a `# Title` body heading; frontmatter is canonical content and feeds the venue title constructs at composition.
- Keep the abstract as a marked section (an `## Abstract` heading) so composition can lift it into the venue abstract environment; do not treat it as an ordinary numbered section.
- Use the profile's required heading hierarchy without authored numeric prefixes.
- Use checked citation roles tied to `KAOJU:CITATION-MAP`.
- Reference every figure and table as a separate file-backed Artifact through a typed display directive or placeholder.
- Bind claim-bearing text to accepted source or Run refs and keep supported, challenged, inconclusive, and limited evidence distinct.
- Record `lecture_sections` in canonical YAML frontmatter for every active accepted commitment. Each entry requires `run_ref`, `source_digest_ref`, `heading`, `section_job_kind: dedicated-detailed-section`, `reader_outcome`, accepted `evidence_refs`, `claim_refs`, `components`, `equation_jobs`, and `display_jobs`. The required component keys are `survey_role`, `problem_and_prerequisites`, `definitions_and_notation`, `method_intuition`, `method_walkthrough`, `worked_trace`, `equations`, `displays`, `results_and_evidence`, `comparison_and_positioning`, `limitations_and_failure_modes`, and `unresolved_boundaries`. Every component records status `covered` with a present `myst_locator` or status `not-applicable` with an evidence-backed rationale, plus `citation_map_refs`.
- Reconcile accepted equation and display jobs by exact source locator. A covered equation job records its MyST locator, symbol definitions, and Citation Map refs. A display job preserves its accepted handling posture; `reproduce`, `adapt`, and `redraw` record a file-backed `KAOJU:PAPER-DISPLAY` ref and typed placeholder, `describe` records a located textual treatment, and `omit` records `not-applicable` with rationale and Citation Map evidence.
- Teach each active lecture paper through its problem and prerequisites, definitions and notation, intuition, ordered method, applicable worked trace, essential equations and displays, results, comparison, limitations, failure modes, and unresolved boundaries. Do not impose an equation, figure, table, or trace when accepted evidence marks that component not applicable.
- Keep abstract, acknowledgments, references, appendices, raw blocks, and venue-specific constructs explicit so composition can map or diagnose them.

## Derivation Boundary

The content template can contain arbitrary MyST, configuration, includes, assets, and guidance. The agent interprets its tree and bounded authored metadata. Review Markdown is deterministic and non-canonical. TeX composition separately snapshots a named multi-file LaTeX template with a checked entrypoint and preamble, marker, or include contract. The presentation fingerprint depends on LaTeX stock and composition behavior, while the canonical MyST checksum remains separate lineage. Direct TeX inspection may repair paper-specific presentation and syntax, but content repair returns to canonical MyST and stock promotion requires an explicit LaTeX-template update.
