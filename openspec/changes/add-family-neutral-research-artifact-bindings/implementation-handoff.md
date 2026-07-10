# Implementation Handoff

## Delivered Contract

- Registered `isomer.research.record-formats` beside the unchanged `isomer.deepsci.record-formats` provider. The neutral provider ships one common schema, one Markdown template, and 25 declarative Kaoju profiles.
- Added authored `semantic_id` lifecycle support, exact family and semantic queries, revision-aware latest selection, ambiguity diagnostics, profile-driven facets, SQLite migration, and generic Project Web record detail enrichment.
- Added 25 storage-neutral Kaoju semantic entries and 10 producer-local `artifact-bindings.md` authorities. Canonical accepted state is managed JSON; readable views are derived, and large materials remain referenced.
- Added binding-aware workspace bootstrap, reset-checkpoint guidance, deterministic survey and dataset management contracts, and family-aware research-paradigm validation.

## Verification Evidence

| Surface | Evidence |
| --- | --- |
| OpenSpec | `openspec validate add-family-neutral-research-artifact-bindings --type change --strict --no-interactive --json` passed with no issues. |
| Research skill contracts | `pixi run python scripts/validate_research_paradigm_skillset.py src/isomer_labs/assets/system_skills/research-paradigm` passed for packaged DeepSci and Kaoju roots. |
| Targeted behavior | 155 provider, record, query-index, lineage, reset, binding, package, installer, Project Web, validator, and integration tests passed. |
| Repository quality | `pixi run lint` passed; `pixi run typecheck` passed across 124 source files; `pixi run test` passed all 503 unit tests. |
| Temporary Topic | The integration smoke recorded a binding index and workspace readiness, created and revised a Survey Contract and Related-Work Catalog, selected explicit latest records, rendered an export, rebuilt the index, verified historical lineage, and included selected records in a reset checkpoint. |
| Package assets | Import-resource checks resolved the neutral catalog, schema, and template; system-skill materialization and installer tests preserved the semantic registry and binding pages. |

## Compatibility Evidence

- All 197 existing DeepSci catalog profiles, their schema and template refs, and generic v2 validation continue to resolve through `isomer.deepsci.record-formats`. No neutral alias or ref rewrite exists.
- Existing `--placeholder` create, list, show, update, archive, stored metadata, and index behavior remain supported. Generalized index identity derived from a placeholder is explicitly labeled `derived_placeholder`; the original placeholder remains unchanged.
- Existing DeepSci validator inventory, payload-first, display, latest-context, lineage, query-metadata, and profile diagnostics passed unchanged in the complete validator suite.
- Reset profiles keep their existing DeepSci refs. The neutral provider is additive to validation, rendering, record writes, runtime validation, reset inspection, and CLI resolution.

## Operational Boundary

Disabling the neutral provider and Kaoju binding guidance does not rewrite existing records. Neutral Kaoju records remain generic durable records addressable by stable record id and locator; DeepSci records and placeholder workflows remain independently addressable under their original refs.
