# Research Idea Recording

Use canonical Research Idea records when a durable research concept is created, selected, rejected, deferred, supported, refuted, followed up, merged, or subsumed. Record concept identity with `isomer-cli --print-json ext research ideas upsert`, link durable records with `isomer-cli --print-json ext research ideas realize`, and add idea-level relationships with `isomer-cli --print-json ext research ideas lineage add`.

Keep idea lineage separate from artifact lineage. Artifact lineage answers which records produced a record; idea lineage answers which concepts produced a concept.

Use stable semantic topic-scoped `idea_id` values such as `idea-combined-analytical-predictor`. Preserve source-local labels such as `R1`, `R8`, `C1`, or `C3` with `--alias` or realization metadata, not as the canonical id unless the label is itself durable and semantic.

Use `visibility=primary` only for user-facing top-level ideas that should appear in the default idea map. Use `visibility=supporting` or `visibility=hidden` for route decisions, implementation details, ablation terms, claims, and other material that should appear only after expansion or in a detail tab.

Every Idea Realization that points at a structured source record must use `--source-json-path` for one object-valued payload fragment that contains the idea itself. Do not point a Primary Idea realization at the whole payload, a list of ideas, rendered Markdown, route notes, filter notes, artifact lists, metrics, or other source-record context.

Use profile-aware idea sections as source paths: raw idea slate entries use `$.sections.raw_ideas[<index>]`, candidate frontiers use `$.sections.serious_candidates[<index>]` or `$.sections.candidate_ideas[<index>]`, rejected/deferred ideas use the matching rejected or deferred idea item, and selected/draft/outline records use the profile's single idea object under `$.sections` or a declared selected idea section. Source context such as `$.sections.filter_notes`, `$.sections.route_context`, `$.sections.rationale`, and `$.sections.collapse_rationale` may support provenance but must not be the source JSON path for the idea preview.

Before writing ideas from an existing source record, prefer `isomer-cli --print-json ext research ideas import-from-record <record-id>` to inspect the exact source paths. Use `isomer-cli --print-json ext research ideas validate` after manual writes, and use `isomer-cli --print-json ext research ideas repair` for source-path repair plans; only use `--update-payloads` when the user or task explicitly allows managed payload edits.

Use these idea lineage kinds:

- `derived_from`: a child idea follows from one parent idea.
- `selected_from`: a selected idea came from candidate ideas or drafts.
- `merged_from`: a child idea combines several parent ideas.
- `follow_up_to`: a child idea continues a prior idea after evidence, analysis, or route choice.
- `alternative_to`: an idea is an explicit alternative to another idea.
- `subsumes`: one idea intentionally covers another idea's mechanism, ablation, or test role.

Do not create idea-level `revision_of` edges. When accepted record revisions change wording, evidence, or detail without changing the concept, update the same Research Idea in place and add or refresh Idea Realizations.

When one pass produces sibling candidates, create one generation group with `ext research ideas generation upsert`, then attach child edges to that `generation_id`. A generation group does not imply `subsumes`; record `subsumes` only when the agent, operator, or decision record explicitly says one idea covers another.

Experiment and analysis evidence may show that an idea status is stale, supported, refuted, narrowed, or superseded, but status changes require an explicit idea write. Do not let query-index extraction, Markdown prose, or a result payload mutate idea status implicitly.
