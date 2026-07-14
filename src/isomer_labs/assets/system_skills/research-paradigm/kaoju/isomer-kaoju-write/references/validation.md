# Validation

A successful build does not make a paper ready. A bound `kaoju:paper-validation-report` applies required checks from canonical MyST through derived TeX and PDF and records unavailable checks explicitly.

## Structural and Textual Checks

- canonical MyST revision, structure, citations, placeholders, display refs, and evidence boundaries
- derived TeX identity, conversion diagnostics, compatibility fingerprint, and included-file digests
- absence of authored section numbers
- citation resolution and bibliography consistency
- engine exit status, missing references, missing glyphs, overfull content, material warnings
- PDF media type, digest, page count, extractability, metadata
- outline or table-of-contents consistency
- broken URLs and suspicious duplicate or shifted section labels

## Survey-Content Quality Checks

Evaluate the survey-quality profile dimensions from the paper contract:
- protocol and scope coverage
- source identity integrity
- evidence adequacy
- comparative-study soundness
- traceability
- synthesis quality
- balance and limitations
- reader-facing reporting
- document integrity

## Visual Checks

When the paper contract requires publication-ready output:
- inspect the title or first page
- inspect the table of contents when present
- inspect every page containing figures, tables, or reported overflow risk
- check clipping, overlap, margins, readability, figure and table placement
- apply target-required accessibility checks

## Verdicts

- `ready`: all mandatory dimensions pass and no required check is unavailable.
- `ready-with-warnings`: warnings are named and explicitly permitted by the paper contract and applicable Gate.
- `not-ready`: a mandatory dimension fails or is unknown, a required check is unavailable, or a named defect is found.

## Compilation-Only is Insufficient

A PDF that exists but fails structural, textual, or visual validation yields `not-ready`. The publication bundle cannot be accepted from such a build.
