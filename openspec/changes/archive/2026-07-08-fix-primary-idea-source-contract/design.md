## Context

The GUI now opens canonical Research Ideas through an idea detail tab, but the backend source resolver can fall back from an unresolved latest realization path to the whole structured record payload. In the flash-attention topic, this makes a single idea preview render the entire raw idea slate, including `filter_notes`, because the realization path points at `$.raw_ideas` while the managed payload stores the entries under `$.sections.raw_ideas`.

The domain model already distinguishes Research Idea, Primary Idea, Idea Realization, and source record provenance. The problem is that the current source path contract is too loose: it permits root payloads, collection paths, wrong paths, and record context to masquerade as the idea's own content.

## Goals / Non-Goals

**Goals:**

- Make the latest Primary Idea detail view resolve to one exact idea content fragment or to canonical idea metadata with diagnostics.
- Keep full record payloads available as source-record provenance, not as the main idea preview.
- Make `isomer-cli` validation, import, repair, and record write conveniences enforce exact source paths for Idea Realizations.
- Update DeepSci skill guidance so agents write idea-bearing payloads with clear idea entries, context notes, filter notes, and exact realization paths.
- Repair the flash-attention topic so its runtime idea metadata and managed payloads match the new standard.

**Non-Goals:**

- Do not remove raw idea slate, candidate frontier, rejected/deferred, or route-decision records; those are valid source artifacts.
- Do not infer authoritative idea content from generated Markdown.
- Do not build a full idea editor or change ordinary record detail rendering.
- Do not make every route note, filter note, claim, or ablation detail a Primary Idea.

## Decisions

### Treat idea content and source record context as separate API concepts

The idea detail endpoint should return explicit `idea_content` for the main preview and `source_provenance` for source-record links, payload digests, rendered-record refs, and diagnostics. Keep the existing `source` object as compatibility metadata for one release, but the frontend should render `idea_content` in the main panel and treat `source_provenance` as record context. The GUI action should be labeled `Open Source Record` and placed with provenance/context controls rather than beside idea copy actions.

Alternative considered: keep returning whatever source candidate resolves first. That preserves current behavior, but it makes a raw slate or candidate frontier indistinguishable from one idea.

### Forbid whole-payload fallback for the main idea preview

When `source_json_path` is unresolved, root-valued, or collection-valued for a Primary Idea realization, the backend should report diagnostics and fall back only to canonical Research Idea metadata for the main preview. It must not render the whole latest realization payload as the idea. Operators can still open the source record explicitly.

Invalid latest Primary Idea source paths are write-time errors for mutating commands. Read-only validation reports errors for invalid latest Primary Idea realizations and warnings for historical or supporting realizations that remain inspectable but do not power the default Primary Idea preview.

Alternative considered: silently prefer the Research Idea `source_json_path` after the latest realization path fails. That can hide stale realization metadata and still gives no warning that the latest link is broken.

### Centralize source path resolution in the CLI/runtime layer

Move the JSON path resolver and validation policy out of web-only helpers into shared record/idea code. Put the resolver and profile-aware idea source registry in a shared Python module such as `src/isomer_labs/records/idea_sources.py`, then have `isomer-cli ext research ideas validate`, `import-from-record`, `repair`, `realize`, record create conveniences, query-index export, and the web read model use it. Skills document the contract and source path patterns, but they do not own executable mappings.

Alternative considered: patch only the FastAPI resolver. That would make the GUI look better but leave future agents free to write misleading realization paths.

### Use profile-aware idea section mappings

DeepSci profile extractors and imports should know which payload sections contain idea entries and which contain context notes. For example, raw idea slates should map idea entries from `$.sections.raw_ideas[N]`, while `$.sections.filter_notes` remains record context. Candidate frontiers, pre-idea drafts, selected hypotheses, and selected idea drafts should have similar mappings.

Alternative considered: rely on generic key names such as `raw_ideas` anywhere in the payload. That caused the current miss and cannot distinguish idea entries from notes.

### Use a small source status vocabulary

Query-index export and API diagnostics should use a bounded source-fragment vocabulary. `source_fragment_status` starts with `exact`, `missing_payload`, `missing_path`, `unresolved_path`, `broad_path`, `non_object`, and `legacy_fallback`. `source_classification` starts with `canonical_idea_source`, `record_context`, and `legacy_heuristic`.

Alternative considered: return only ad hoc diagnostic codes. Diagnostics are still useful, but stable status values make GUI filtering, tests, and repair planning less brittle.

### Keep existing tables, tighten metadata and validation

The first implementation should reuse `research_ideas`, `research_idea_realizations`, `research_idea_lineage_edges`, and generation groups. Exact source path validity is derived by validation and query export rather than stored as authoritative state. If a later implementation needs a searchable `source_role` column, it can be added without changing this contract.

Alternative considered: add a new Primary Idea Content table. That duplicates Idea Realization and gives the system another place for stale content links.

### Migrate the flash-attention fixture as if generated by the new standard

The general `ideas repair` path should update runtime Research Idea rows and Idea Realizations by default, and should not mutate managed payload files unless the operator passes an explicit payload-update option such as `--update-payloads`. The flash-attention fixture migration may use that explicit path to enrich managed payload entries with human-facing fields such as canonical `idea_id`, source label, title or one-liner, status, visibility, family, concise rationale when available, and repair metadata. Runtime Idea Realizations should point to exact payload paths such as `$.sections.raw_ideas[0]`, each visible Primary Idea should have a coherent latest realization, and historical or supporting rows that cannot be repaired confidently should remain visible with diagnostics instead of invented content.

Alternative considered: only fix SQLite paths. That would stop the full-payload fallback, but the idea preview would still be too thin for a user-facing panel.

### Keep JSON path support intentionally small

Support the normalized subset already used by the system: `$`, `$.field`, nested dot paths, and numeric list indexes such as `$.sections.raw_ideas[0]`. Do not add filters, wildcards, recursive descent, or a full JSONPath dependency in this change.

Alternative considered: adopt a full JSONPath implementation now. That adds expressive power, but the current DeepSci payloads need deterministic item paths more than query expressions.

## Risks / Trade-offs

- Legacy topics may have no exact source paths → Keep canonical metadata fallback and diagnostics, plus import/repair commands that produce an apply plan.
- Profile-aware mappings can lag behind new payload shapes → Unknown profiles stay inspectable as records, but primary idea previews report unresolved source diagnostics until a mapping or explicit path is provided.
- Repairing fixture payloads changes example data → Preserve record ids and provenance metadata, and record repair metadata on changed idea entries and runtime rows.
- Generic JSON-to-Markdown previews may still be awkward for some idea fragments → Keep the source object focused and small now; schema-specific idea renderers can come later.

## Migration Plan

1. Add shared source-fragment resolver and diagnostics for structured payload paths.
2. Tighten Idea Realization validation and CLI import/repair behavior around exact object-valued paths.
3. Update query-index export and FastAPI read models to expose exact source status and avoid full-payload main-preview fallback.
4. Update GUI idea detail rendering to use the idea content object and show source-record context separately.
5. Update DeepSci shared idea-recording guidance, idea skill workflow text, placeholder bindings, packaged system skills, and validation checks.
6. Repair the flash-attention topic payloads, runtime idea rows, realization paths, latest flags, and query index.
7. Validate with CLI/unit tests, skill validation, topic runtime validation, query-index rebuild/validate, and a GUI smoke test against the idea-lineage view.

Rollback keeps the added fields and repaired payloads as harmless metadata: restore the previous web resolver behavior only if needed, while preserving explicit diagnostics and exact source paths for future reapplication.

## Open Questions

None currently recorded.
