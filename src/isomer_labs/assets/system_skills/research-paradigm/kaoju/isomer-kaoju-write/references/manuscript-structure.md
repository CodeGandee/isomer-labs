# MyST Manuscript Structure

The paper separates a reader-facing narrative from an auditable evidence view. Both are authored in canonical MyST and linked through typed roles, directives, citations, display refs, and source refs. Drafting resolves an explicitly named content template or content `main` and records its stable ref, state token, and observed tree digest. LaTeX presentation selection is separate and occurs only when TeX or PDF output is requested.

## Adaptive Profiles

Choose a structure for the accepted direction and evidence shape. A taxonomy survey may center categories and boundary cases; a system lineage may center mechanisms and transitions; an empirical comparison may center intent, fairness, and results. Every profile still covers motivation, scope, survey method, synthesis, limitations, and answers to the survey questions.

Record the profile id, rationale, section order, section jobs, required evidence roles, planned displays, and venue constraints in `KAOJU:PAPER-STRUCTURE-MYST`. Do not select a profile from venue convention alone.

## MyST Requirements

- Use one title and the profile's required heading hierarchy without authored numeric prefixes.
- Use checked citation roles tied to `KAOJU:CITATION-MAP`.
- Reference every figure and table as a separate file-backed Artifact through a typed display directive or placeholder.
- Bind claim-bearing text to accepted source or Run refs and keep supported, challenged, inconclusive, and limited evidence distinct.
- Keep abstract, acknowledgments, references, appendices, raw blocks, and venue-specific constructs explicit so conversion can diagnose them.

## Derivation Boundary

The content template can contain arbitrary MyST, configuration, includes, assets, and guidance. The agent interprets its tree and bounded authored metadata. Review Markdown is deterministic and non-canonical. TeX composition separately snapshots a named multi-file LaTeX template with a checked entrypoint and preamble, marker, or include contract. The presentation fingerprint depends on LaTeX stock and composition behavior, while the canonical MyST checksum remains separate lineage. Direct TeX inspection may repair paper-specific presentation and syntax, but content repair returns to canonical MyST and stock promotion requires an explicit LaTeX-template update.
