## 1. Runtime Schema and Store

- [ ] Add additive Workspace Runtime tables for `research_record_index`, `research_record_edges`, `research_record_files`, normalized facet tables, and generic JSON facts.
- [ ] Add typed store APIs to refresh one record, rebuild one Topic Workspace index, validate index state, clean stale or orphaned index rows, list indexed records, and export indexed records with facets.
- [ ] Centralize all query-index writes in Workspace Runtime record store and query-index service code; do not let agents, skills, or GUI clients write index tables directly.
- [ ] Ensure query-index refresh runs only from explicit mutating operations or explicit rebuild, and ensure list/show/validate/render/export paths do not mutate `state.sqlite`.
- [ ] Preserve canonical `lifecycle_records` and `structured_research_payloads` as the source of truth.

## 2. Extraction and Rebuild

- [ ] Implement profile-driven extractors for initial DeepSci payload families: raw ideas, selected hypotheses, route decisions, run records, result summaries, artifact manifests, and claim validation records.
- [ ] Index accepted operation-set files as record attachments with roles, semantic labels, locators, and existence status.
- [ ] Make rebuild idempotent and classify rows as authored, payload-derived, file-derived, or body-inferred.

## 3. Recording API and CLI

- [ ] Extend record create/update request models and CLI JSON input with optional relationship refs, file attachments, and index hints.
- [ ] Refresh or mark stale affected index rows after record create/update.
- [ ] Add `isomer-cli ext research records index rebuild`, `index validate`, and `index cleanup` commands with explicit read/write behavior.
- [ ] Add `isomer-cli ext research records query list`, `query export`, `query lineage`, `query files`, and `query facets` commands for read-only GUI and operator consumers.
- [ ] Make `index cleanup` preview by default and require `--apply` before it mutates query-index rows.

## 4. Validation

- [ ] Report stale rows, broken edges, missing files, cross-topic refs, unsupported relation kinds, extractor failures, and low-confidence claim support.
- [ ] Report cleanup diagnostics and affected-row summaries without deleting canonical records, payloads, rendered Markdown, operation-set files, or accepted artifacts.
- [ ] Keep diagnostics non-destructive and preserve canonical records for repair, supersession, or withdrawal.

## 5. DeepSci Skill Guidance

- [ ] Update production DeepSci `placeholder-bindings.md` pages with expected relationship, file, and GUI facet metadata.
- [ ] Keep payload-first structured record creation as the normal accepted-artifact path.
- [ ] Add or update validation coverage for the new binding guidance.

## 6. Verification

- [ ] Rebuild the query index for an existing FlashAttention topic workspace.
- [ ] Run index validation and cleanup preview for the rebuilt FlashAttention topic workspace.
- [ ] Verify exported JSON can show timeline records, idea slate, selected hypothesis, decision path, experiment files, metrics, and claims.
- [ ] Run `openspec validate add-research-record-graph-index --strict`.
