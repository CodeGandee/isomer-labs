## Context

The project web GUI currently builds the `idea-lineage` view from query-index records, extracted `research_record_ideas` facets, and record-level lineage edges. That read model is useful for artifact provenance, but it cannot reliably answer the user-level question "which primary ideas led to which later primary ideas?"

The platform domain language has Research Topic, Research Inquiry, Research Task, Artifact, Decision Record, Finding, Research Claim, Evidence Item, and Provenance Record. It does not yet define a durable idea-level object. The DeepSci idea skill already asks selected idea records to include a stable idea id, but the CLI and runtime never promote that id into a canonical entity or DAG.

The implementation should keep existing record lineage intact. Record lineage answers "which durable records produced this record?" Idea lineage answers "which conceptual research ideas led to this idea?" These graphs overlap, but they are not the same graph.

## Goals / Non-Goals

**Goals:**

- Add Research Idea as a first-class topic-scoped concept with stable identity, status, primary visibility, and metadata.
- Add Idea Realization links from Research Ideas to the durable records that express them.
- Add idea-level lineage and generation groups so primary ideas form a validated DAG.
- Make `isomer-cli ext research ideas` the explicit maintenance and repair surface for idea data.
- Make the GUI's default idea-lineage view use canonical primary ideas when present.
- Update DeepSci skills so future records are written with idea identity and idea relationships instead of relying on later inference.
- Repair the existing flash-attention topic as a fixture that looks like it was produced by the new contract.

**Non-Goals:**

- Replace record lineage, record query export, or existing structured payload storage.
- Treat every extracted idea phrase, claim, route decision, or ablation term as a primary idea.
- Infer authoritative idea lineage from Markdown prose.
- Build a full interactive idea editor in this change.
- Change the research-paradigm method for selecting ideas, except for adding durable recording obligations.

## Decisions

### Decision: Use Research Idea as the core entity and Primary Idea as visibility

Research Idea is the durable conceptual node. Primary Idea is not a separate table; it is a visibility or role value that tells the GUI that this idea belongs in the default high-level map.

Alternative considered: name the entity Primary Idea. That makes the default GUI wording obvious, but it turns a presentation role into identity and gives no place to store supporting or raw ideas. A single Research Idea model with `visibility=primary|supporting|hidden` gives better repair and expansion behavior.

### Decision: Keep idea lineage separate from record lineage

The runtime should add idea-specific tables rather than projecting idea edges from `research_record_lineage_edges`. Record lineage remains canonical artifact provenance; idea lineage becomes canonical conceptual provenance.

Alternative considered: collapse record paths into idea edges in the graph backend. The current implementation already tries this conservatively and produces no edges for real topics when paths are ambiguous. Making this heuristic more aggressive would hide bad data instead of creating a durable contract.

### Decision: Model records as Idea Realizations

A Research Idea can be realized by many records over time: raw slate entry, candidate frontier entry, pre-idea draft, selected hypothesis, analysis follow-up, experiment result, or paper-facing claim. The GUI can open an idea tab that shows latest realization plus history.

Alternative considered: store one `record_id` directly on each idea. That works for first drafts but fails when the same idea appears in selected hypotheses, revisions, analysis summaries, and paper views.

### Decision: Update Research Ideas in place for revisions

Content-changing record revisions should update the same Research Idea in place and add or refresh Idea Realizations. A record revision must not introduce a new Research Idea unless a separate follow-up or alternative idea is explicitly created by the agent or operator.

Alternative considered: create a new Research Idea for every accepted `revision_of` record. That keeps revision history in the graph, but it makes the primary idea map noisy and turns ordinary content edits into user-facing ideas.

### Decision: Treat raw ideas as the chronological parent layer when they explain candidate branches

Raw idea slate entries can be primary Research Ideas when they are needed to explain how later candidate ideas branched. For the flash-attention fixture, R1-R8 form the earlier time layer and C1-C3 are candidate branches from selected raw parents.

Alternative considered: keep raw ideas supporting-only by default. That keeps the graph compact, but it hides the chronological parent layer the user expects to see when inspecting how candidates emerged.

### Decision: Use stable semantic topic-scoped idea ids

Canonical `idea_id` values should be stable semantic slugs scoped to one Research Topic, such as `idea-combined-analytical-predictor`. Source-local labels such as `R1`, `R8`, `C1`, or `C3` should be stored as aliases or realization metadata with source record refs and source JSON paths.

Alternative considered: use source-local labels directly as canonical ids. That is convenient for one idea pass, but labels can repeat across later passes and would make repair, query, and GUI links collision-prone.

### Decision: Use explicit CLI operations for idea repair and import

Add `isomer-cli ext research ideas upsert`, `realize`, `lineage add`, `generation upsert`, `query`, `graph`, `validate`, `import-from-record`, and `repair`. Record creation may get convenience options, but the dedicated idea command group is the maintenance authority.

Alternative considered: only extend `ext research records create` with more JSON fields. That helps producers but gives operators no clean way to inspect or repair idea lineage after the fact.

### Decision: Query index exports canonical idea DAG first and extracted facets second

The query-index export should include canonical ideas, idea realizations, idea edges, and idea generation groups. Existing extracted `research_record_ideas` rows remain available as fallback facets and diagnostics, but the GUI must prefer canonical idea data when it exists.

Alternative considered: remove extracted idea facets. Keeping them helps legacy topics, search, and repair diagnostics, and it avoids losing useful profile-derived snippets.

### Decision: Skills record idea identity during the workflow

DeepSci skills should create or update idea data at the same time they create durable records. The idea skill owns raw slates, candidate frontiers, pre-idea drafts, selected hypotheses, and route decisions. Experiment and analysis skills instruct the agent to explicitly update idea status or create follow-up ideas when results support, refute, narrow, or redirect the line.

Alternative considered: run a separate post-hoc indexer after agents write records. That remains useful for migration, but it cannot capture selection rationale, sibling groups, or confidence as well as the agent can at write time.

### Decision: Idea status updates are explicit writes

Experiment results, analysis findings, and query-index diagnostics may suggest that a Research Idea status is stale, supported, refuted, or superseded, but they must not mutate idea status automatically. Status changes require an explicit agent, operator, repair, or record-write action through the canonical idea store.

Alternative considered: automatically update idea status from experiment verdicts. That reduces manual work, but it can flip statuses from partial, noisy, or context-specific evidence before a research decision has been recorded.

### Decision: Use `subsumes` as a first-class idea lineage kind

Candidate collapse can be a user-visible conceptual relationship, not only grouping metadata. `subsumes` should be an accepted idea lineage kind for cases where one Research Idea intentionally covers another idea's mechanism, ablation, or test role.

Alternative considered: store subsumption only as metadata on `merged_from`, `selected_from`, or generation groups. That keeps the vocabulary smaller, but it makes a central branch relationship hard for the GUI and CLI to show directly.

## Runtime Data Shape

The Workspace Runtime should add these canonical objects:

- `research_ideas`: stable semantic topic-scoped idea identity, aliases, title, one-liner, family, status, visibility, source record/path, timestamps, and metadata.
- `research_idea_realizations`: links an idea to a record and source JSON path with stage, semantic id, latest flag, and metadata.
- `research_idea_lineage_edges`: typed parent-child DAG edges between ideas with lineage kind, parent role, generation id, decision record id, rationale, status, confidence, provenance refs, and metadata.
- `research_idea_generation_groups`: sibling or alternative candidate groups keyed by idea parent set digest, purpose, producer skill, decision record, and metadata.

The idea lineage vocabulary should start with `derived_from`, `selected_from`, `merged_from`, `follow_up_to`, `alternative_to`, and `subsumes`. Record-level `revision_of` remains part of artifact provenance, but idea revisions update the same Research Idea and are represented through realization history rather than idea-to-idea edges. Generation groups still represent sibling candidates from the same pass; `subsumes` is used only when one idea conceptually covers another.

## CLI and API Shape

The CLI should return deterministic `--print-json` payloads matching the existing extension command style.

Expected command group:

```text
isomer-cli ext research ideas upsert
isomer-cli ext research ideas realize
isomer-cli ext research ideas lineage add
isomer-cli ext research ideas generation upsert
isomer-cli ext research ideas query
isomer-cli ext research ideas graph
isomer-cli ext research ideas validate
isomer-cli ext research ideas import-from-record
isomer-cli ext research ideas repair
```

Record creation may accept `--realizes-idea-id`, `--idea-realizations-json`, `--idea-parents-json`, and `--primary-idea-json` as producer conveniences. These fields must create canonical idea rows through the same store API as the dedicated command group.

## GUI Read Model

The default idea-lineage graph should display only canonical ideas whose visibility is `primary`, unless the user enables supporting material. Primary ideas may include raw time-parent ideas when they explain visible candidate branches. Each node should open an idea detail tab, not just a record detail tab. That tab should show latest realization, realization history, status, incoming/outgoing idea edges, sibling generation group, and linked records.

When canonical idea data is absent, the backend may fall back to extracted record idea facets but must include diagnostics that the graph is heuristic. When canonical idea data is present, duplicate extracted facets such as repeated R1-R8 rows must not create duplicate graph nodes.

## Flash-Attention Fixture Repair

The existing topic should be repaired to expose this best-effort primary idea DAG:

```text
R1 occupancy correction ───────────────┬─derived_from──▶ C3 occupancy-only alternative
                                       └─merged_from──▶ C1 combined analytical predictor
R2 TMA/L2 bandwidth ─────────────────────merged_from──▶ C1 combined analytical predictor
R3 precision throughput ───────────────┬─derived_from──▶ C2 precision-only alternative
                                       └─merged_from──▶ C1 combined analytical predictor
R4 combined predictor ───────────────────merged_from──▶ C1 combined analytical predictor
R6 NCU bottleneck side output ───────────merged_from──▶ C1 combined analytical predictor

R5 symbolic-regression fallback, R7 metric switch, and R8 microbenchmark suite remain primary raw time-parent ideas with deferred or rejected status unless later reused.

C1 ─follow_up_to──▶ real-hardware validation
real-hardware validation ─follow_up_to──▶ launch-overhead / NCU calibration
launch-overhead / NCU calibration ─follow_up_to──▶ bottleneck-threshold calibration
bottleneck-threshold calibration ─follow_up_to──▶ bottleneck saturation predictability
```

R1-R8 should exist as primary raw time-parent ideas for this fixture, but their canonical ids should be semantic topic-scoped slugs with `R1` through `R8` preserved as source aliases. C1, C2, C3, real-hardware validation, launch-overhead / NCU calibration, bottleneck-threshold calibration, and bottleneck saturation predictability should also be primary. `C1` through `C3` should be preserved as source aliases for their semantic canonical ids. The two bottleneck-threshold calibration hypothesis records should be realizations of the same Research Idea, with the later record marked latest.

## Risks / Trade-offs

- Schema drift between record and idea lineage -> keep separate validation paths and test cross-topic, missing-ref, and cycle diagnostics.
- Agents may double-write inconsistent idea metadata -> route all record convenience flags through the same runtime store helpers as `ext research ideas`.
- Idea statuses may become stale when evidence accumulates -> surface diagnostics and skill reminders, but require explicit status-update writes.
- Legacy topics may lack canonical idea data -> keep extracted-facet fallback and add import/repair commands.
- The first migration is partly judgment-based -> store repair rationale and confidence metadata for inferred flash-attention idea edges.
- More graph data can make the UI noisy -> use `visibility=primary` only for ideas that explain the main branch structure, and keep implementation details, route decisions, claims, and ordinary ablation details behind expansion or filters.

## Migration Plan

1. Add domain language definitions and OpenSpec-backed requirements.
2. Add runtime models, SQLite schema migration, store methods, validation, and unit tests.
3. Add CLI commands and JSON output tests.
4. Extend record write paths and query-index export to carry canonical idea data.
5. Update backend graph/read APIs and frontend idea detail behavior to prefer canonical idea DAGs.
6. Update DeepSci skill instructions and validation expectations.
7. Run an explicit repair/import pass for `flash-attention-4-whitebox-runtime-model`.
8. Validate with `pixi run lint`, `pixi run typecheck`, `pixi run test`, and a targeted GUI/API smoke check.

Rollback is additive: keep old record lineage and query-index behavior, disable canonical idea graph preference if needed, and preserve repaired topic data as extra metadata rather than deleting existing records.

## Open Questions

None currently recorded.
