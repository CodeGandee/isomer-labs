## Context

The Project Web GUI currently opens Idea Lineage with `includeSecondary: true`, so the graph includes route decisions, claims, and evidence detail alongside user-facing ideas. The Topic Graph API already marks nodes with `material_kind`; for the Flash Attention topic, the default backend request returns 13 idea nodes and no non-idea nodes, while the secondary request returns 103 nodes made of 13 ideas, 47 decisions, and 43 claims.

The user-facing interpretation is clear: titles such as "Precision-only throughput and exponential emulation correction" are ideas, while route decisions, launch-overhead claims, evidence records, and files are supporting details. The GUI should make that distinction visible in the interaction model.

## Goals / Non-Goals

**Goals:**
- Make Idea Lineage default to a clean overview of user-facing ideas.
- Keep route decisions, claims, evidence, files, diagnostics, and supporting records available through selected-idea drill-down.
- Preserve graph readability by projecting collapsed idea-to-idea edges where secondary records connect two ideas through an intermediate record path.
- Keep browsing read-only and general across topics.

**Non-Goals:**
- Do not delete or hide secondary data from the API.
- Do not mutate topic records, repair query-index rows, or rewrite existing Flash Attention artifacts as part of browsing.
- Do not build a full provenance explorer in the Idea Lineage overview.
- Do not require a topic-specific rule for Flash Attention filenames or record ids.

## Decisions

### Default Idea Lineage to Idea-only

The frontend should request Idea Lineage with `include_secondary=false` by default. This uses the backend's existing `material_kind="idea"` separation and immediately removes route decisions and claims from the first-level graph.

Alternative considered: filter secondary nodes only in the frontend. That would still fetch and layout unnecessary nodes, and it would leave API clients with a noisy default contract.

### Add Explicit Secondary Drill-down

When a user clicks an idea, the GUI should open the idea's record-detail Dockview tab as the first selected-idea detail surface. That tab can load the idea's source record, lineage, siblings, files, facets, diagnostics, and supporting decisions, claims, evidence, metrics, or files connected to the selected idea. A lightweight side inspector can be added later for quick context, but heavy Markdown, PDF, JSON, Mermaid, KaTeX, and graph detail work belongs to open tabs.

Alternative considered: keep secondary nodes visible but smaller. That still makes process details compete with ideas and does not match the user's "details below the idea" model.

### Project Collapsed Idea Edges

The backend should keep an idea-only overview connected where possible by projecting collapsed edges between idea nodes when canonical relationships or secondary paths imply an idea-to-idea relation. The API should preserve all accepted stable relation kinds, but the default overview should visually prioritize `derived_from`, `revision_of`, `selected_from`, `follow_up_to`, `alternative_to`, and `supersedes`. `supports` and `contradicts` may appear as idea-to-idea edges only when both endpoints are real ideas; evidence-style support stays in selected-idea detail. Projected edges should carry metadata such as `collapsed`, source relation ids or record ids, source classification, and diagnostics when projection is partial or ambiguous.

Alternative considered: accept an unconnected idea-only overview. That is cleaner but loses the core lineage purpose.

### Keep Secondary Mode as an Explicit Advanced Option

Secondary material should remain available through an explicit **Supporting Records** toggle or detail command, not as the default. When enabled, the UI should label it as supporting detail and avoid implying that route decisions or claims are peer ideas.

Alternative considered: remove secondary mode entirely. That would make debugging and provenance inspection harder.

### Use Topic Graph API as the Lineage Read Model

The frontend should use `/api/topics/{topic_id}/graphs/idea-lineage` as the idea-lineage read model. The backend can compose the response from existing export, record, lineage, sibling, file, and facet data, but the frontend should not reconstruct lineage from raw query-index rows.

Alternative considered: have the frontend call `records/export?view=ideas` and build the graph itself. That would duplicate backend relation policy in TypeScript and make read-model diagnostics harder to keep consistent.

### Normalize Only Common Statuses

The first normalized status set is `candidate`, `selected`, `rejected`, `superseded`, `deferred`, `unresolved`, and `stale`. Source values outside that set should stay visible as raw values or diagnostics; the GUI should not invent status meaning.

## Risks / Trade-offs

- Collapsed edge projection may overstate lineage if secondary paths are ambiguous. → Only project edges from canonical lineage or accepted relation kinds, attach source metadata, and emit diagnostics for ambiguous paths.
- Idea-only default may hide useful workflow context from advanced users. → Keep an explicit secondary detail mode and record detail tabs.
- Current query-index relationships may not always connect ideas directly. → Start with best-effort projection and unconnected groups; do not invent edges from Markdown prose.
- The selected-idea detail view could become heavy. → Lazy-load detail only after selection and reuse existing tab/resource policy.

## Migration Plan

No data migration is required. Existing query-index exports, idea rows, route rows, claim rows, lineage, sibling, file, and facet endpoints remain valid.

Implementation should update the backend graph projection and frontend defaults, rebuild the static bundle, and verify against the existing Flash Attention topic plus a minimal fixture. Rollback is to restore `includeSecondary: true` default and ignore collapsed edge metadata.

## Resolved Questions

- Selected idea details open as a Dockview record-detail tab first; a side inspector remains a later enhancement for lightweight context.
- The API supports accepted stable relation kinds, while the default overview visually prioritizes `derived_from`, `revision_of`, `selected_from`, `follow_up_to`, `alternative_to`, and `supersedes`.
- The advanced graph control is named **Supporting Records**.
- The first status normalization set is `candidate`, `selected`, `rejected`, `superseded`, `deferred`, `unresolved`, and `stale`.
- The dedicated idea-lineage graph API is the frontend-facing read model.
