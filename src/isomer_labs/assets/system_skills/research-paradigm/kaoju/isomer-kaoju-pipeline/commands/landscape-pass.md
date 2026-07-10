# Landscape Pass

## Workflow

1. **Frame**. Use `$isomer-kaoju-workspace-mgr` and `$isomer-kaoju-frame` to accept a Survey Contract with field boundary, five source classes, coverage date, depth, outputs, resources, and stop conditions.
2. **Discover**. Use `$isomer-kaoju-discover` for bounded queries, version families, query provenance, inclusion decisions, and type-aware links across papers, technical reports, source repositories, datasets, and models.
3. **Acquire selectively**. Use `$isomer-kaoju-acquire` only for materials needed to reach the accepted inspection depth.
4. **Examine**. Use `$isomer-kaoju-examine` to create Source Digests and Claim-Evidence Ledger entries at exact locators.
5. **Audit**. Use `$isomer-kaoju-audit` to check coverage, identity, provenance, depth, and claim traceability.
6. **Synthesize**. If the Audit Report is accepted, use `$isomer-kaoju-synthesize` to produce the Related-Work Catalog, Field Summary, Claim Status Table, and remaining frontier.
7. **Stop**. Return the pipeline terminal report without selecting another procedure.

If the request does not map cleanly to this recipe, use the native planning tool to build and execute a bounded stage plan from these skills while preserving audit before synthesis.

## Trigger

Use when the user wants a broad understanding of a field, problem, technique, or representative work, including a list of related works and a summary.

## Inputs

Require the survey question or seed, boundary or clarification mode, desired audience and depth, coverage date, resource envelope, and accepted prior refs. Papers and technical reports are primary related works; repositories, datasets, and models remain typed implementation or evidence links.

## Outputs

- Survey Contract and Discovery Ledger refs.
- Version-aware Related-Work Catalog with inclusion and exclusion evidence.
- Source Digests and Claim-Evidence Ledger refs for representative works.
- Accepted Audit Report, Field Summary, Claim Status Table, and Kaoju Dossier or bounded subset.
- `searched_through`, coverage limits, unresolved access blockers, and remaining frontier.

## Stop Conditions

Stop when the accepted coverage and representative-depth conditions are met, or return `paused` or `blocked` when access, resources, Gates, or material ambiguity prevents them. Never call the survey exhaustive unless the Survey Contract defines a finite, verifiable universe.

## Common Mistakes

- Letting code search replace literature search.
- Reading every candidate deeply before triage.
- Hiding excluded candidates or query provenance.
