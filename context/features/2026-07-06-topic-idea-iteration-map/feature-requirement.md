# Topic Idea Iteration Map Feature Requirement

## Goal

Show how proposed ideas evolve inside one Research Topic: what each idea is, where it came from, which ideas it supersedes or alternatives it opens, and what evidence or Decision Records changed its status. The view should help a user understand the exploration graph without reading raw payload JSON, generated Markdown, or SQLite rows.

## Non-Goals

- Do not create or edit ideas from the first version of this feature.
- Do not model idea evolution as Git branches, filesystem worktrees, or a strict tree; the canonical backing model is Research Inquiry, Research Inquiry Relationship, research records, and query-index edges/facets.
- Do not require topic-specific file names, fixed record counts, or special handling for the current `isomer-content/` sample topic.
- Do not infer authoritative relationships from generated Markdown prose when structured payloads, lifecycle metadata, or query-index relationships are missing.
- Do not auto-rebuild or repair query-index rows during read-only GUI browsing.

## Users And Workflows

- Project user: opens the local Project Web GUI, selects a Research Topic, and switches to an idea iteration view to see the current idea landscape.
- Project Operator Session: uses the view to decide whether to continue, revisit an older idea, compare alternatives, or ask for a new ideation pass.
- Research reviewer: inspects why an idea was selected, rejected, superseded, or split into alternatives before reading detailed evidence.

Primary workflow:

1. The user selects a Research Topic in the GUI.
2. The GUI loads proposed idea facets, query-index records, typed relationships, route decisions, evidence links, and record timestamps for that Topic Workspace.
3. The GUI renders an idea graph or lineage list where each idea node shows the concise idea text, status, source record, producer, timestamp, and key supporting or rejecting evidence.
4. The user selects an idea node to inspect predecessor ideas, alternative ideas, successor ideas, decision rationale, related experiments, findings, claims, and canonical record detail.
5. The user can filter by status, producer, route decision, time range, evidence state, or relationship kind without mutating Workspace Runtime.

## Functional Requirements

- The GUI shall provide an idea iteration view for the selected Research Topic using only project-discovered topics and topic-scoped APIs.
- The view shall show each proposed idea with a stable id, short title or one-liner, summary when available, status, source record id, producing skill or actor when available, and created/updated timestamps.
- The view shall show predecessor and successor links derived from typed query-index edges, Research Inquiry Relationships, route decisions, and explicit payload relationship metadata.
- The view shall distinguish relationship kinds such as `follows from`, `alternative to`, `supersedes`, `supports`, `contradicts`, `blocks`, and `derived from` when the source data provides them.
- The view shall support both graph and list/table presentation so large topics remain browsable when a dense graph is hard to read.
- The view shall show branching as a UI presentation of alternatives or derived inquiries, not as a durable domain object named Research Branch.
- The view shall show evidence summaries for each idea when linked Evidence Items, Research Claims, Findings, Runs, metrics, or Decision Records are available.
- The view shall identify selected, rejected, superseded, active, stale, or unresolved idea states using query-index facets and route records when available.
- The view shall let users open canonical record detail, rendered Markdown, lineage, files, and facets through existing read APIs.
- The view shall report missing, stale, unsupported, or ambiguous relationship data as diagnostics and maintenance hints rather than hiding the gap.
- The view shall remain useful when relationship data is partial by showing unlinked idea cards under an “unconnected ideas” group.
- The backend shall expose or derive a topic-scoped idea-lineage read model if existing `query export` and `facets` payloads are too coarse for efficient GUI rendering.

## System Boundaries

- Canonical data remains in Workspace Runtime lifecycle records, structured research payload files, and accepted relationship metadata.
- Query-index tables remain derived read models; the GUI reads them but does not treat them as canonical state.
- The frontend renders a topic-scoped view and keeps only live GUI selection, filters, and expansion state in browser memory.
- Any new API should live behind the Project Web GUI backend or existing research-record query API surface and should preserve read-only behavior for browsing.
- Relationship naming should align with Research Inquiry Relationship and query-index relation vocabulary; UI labels may be user-friendly but must map back to stable relation kinds.

## Operational Constraints

- The feature must work for any Project root served by `isomer-cli project web serve --root <Project>`.
- The feature must not assume that files referenced by payloads exist; it should rely on backend openability metadata before offering file actions.
- The feature must handle large topics by limiting initial payload size, supporting lazy detail loading, and preserving responsive layout on desktop, tablet, and mobile.
- The feature must keep cache behavior consistent with the local GUI service so refreshed frontend assets and API responses reflect the latest server state.
- Read endpoints must not trigger rebuild, cleanup, migration, or repair; maintenance remains explicit.

## Assumptions

- Proposed ideas are currently represented through structured payload facets, records with idea-like profiles, route decisions, Decision Records, or related query-index facts.
- Some historical topics will have incomplete relationship metadata, so the first implementation needs graceful degradation and diagnostics.
- A useful first version can derive from query-index `ideas`, `routes`, `edges`, `claims`, `metrics`, and record summaries before adding a dedicated lineage table.
- Users care about research meaning more than storage details, so the UI should emphasize idea text, evidence, status, and relationships rather than raw record ids.

## Open Questions

- Should the durable backing concept be strengthened around Research Inquiry and Research Inquiry Relationship, or should idea-specific payload profiles remain enough for the first version?
- What exact statuses should the UI normalize across idea records, route decisions, and Decision Records?
- Do we need a dedicated `query ideas lineage` API, or can `query export --view ideas` plus record detail endpoints support the first implementation?
- Should the graph show only idea-to-idea links by default, or include evidence, claims, decisions, and runs as secondary node types?
- How should users compare two sibling alternatives: side-by-side cards, a path comparison table, or a graph-focused interaction?
