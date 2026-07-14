# MyST Manuscript Structure

The paper separates a reader-facing narrative from an auditable evidence view. Both are authored in canonical MyST and linked through typed roles, directives, citations, display refs, and source refs.

## Adaptive Profiles

Choose a structure for the accepted direction and evidence shape. A taxonomy survey may center categories and boundary cases; a system lineage may center mechanisms and transitions; an empirical comparison may center intent, fairness, and results. Every profile still covers motivation, scope, survey method, synthesis, limitations, and answers to the survey questions.

Record the profile id, rationale, section order, section jobs, required evidence roles, planned displays, and venue constraints in `kaoju:paper-structure-myst`. Do not select a profile from venue convention alone.

## MyST Requirements

- Use one title and the profile's required heading hierarchy without authored numeric prefixes.
- Use checked citation roles tied to `kaoju:citation-map`.
- Reference every figure and table as a separate file-backed Artifact through a typed display directive or placeholder.
- Bind claim-bearing text to accepted source or Run refs and keep supported, challenged, inconclusive, and limited evidence distinct.
- Keep abstract, acknowledgments, references, appendices, raw blocks, and venue-specific constructs explicit so conversion can diagnose them.

## Derivation Boundary

Review Markdown is deterministic and non-canonical. TeX initialization parses the accepted MyST revision, records unsupported constructs, and creates a compatibility fingerprint. Direct TeX inspection may repair presentation and TeX syntax, but a content repair returns to canonical MyST.
