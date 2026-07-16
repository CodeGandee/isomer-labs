## Why

Research Ideas currently use one overloaded `status` value to describe proposal maturity, exploration progress, selection outcome, evidence outcome, and archival state. This prevents the Idea Graph from answering basic portfolio questions reliably, such as which ideas remain unexplored, why one idea was selected, what descended from it, or why another idea was deferred or closed.

## What Changes

- Replace the overloaded Research Idea status model with independent exploration, decision, evidence, visibility, and archive facets, each with explicit transition provenance.
- Preserve decision context by linking each selection, deferral, closure, or reopening to the complete considered option set, rationale, actor, timestamp, and supporting Decision Record, Evidence Item, or Artifact refs.
- Extend Research Idea CLI and recording paths with deterministic facet updates, lineage traversal, decision-context queries, validation, and explicit preview/apply migration from legacy status values.
- Add user-facing Idea Graph and Idea Timeline portfolio presets for all proposed, open for exploration, unexplored, exploring, explored, selected, deferred, closed, and needs-classification ideas.
- Add focused ancestry and descendant exploration, plus detail views that explain why an idea was selected, deferred, closed, or reopened and which alternatives were considered.
- Add explicit `Explore this idea` and `Explore instead` steering actions. `Explore instead` records the user's choice and rationale, updates affected idea facets atomically, creates or updates the bounded Research Task, and routes an exact prompt through the Project Operator to the configured topic research actor.
- Keep ordinary GUI browsing read-only. Mutations occur only after an explicit steering action and remain separate from browser-local selection, focus, layout, and filter state.
- Update DeepSci and other idea-producing system-skill guidance so accepted operation outputs record canonical idea facets, lineage, decision context, and transition provenance at production time.
- Preserve legacy status reads during migration; ambiguous legacy values become `unknown` or `needs classification` instead of being guessed silently.

## Capabilities

### New Capabilities

- `research-idea-steering`: Defines explicit user steering actions that turn a selected Research Idea into provenance-backed Research Task and Project Operator instructions without making ordinary graph browsing mutating.

### Modified Capabilities

- `research-lifecycle-state`: Replaces the single Research Idea status vocabulary with independent exploration, decision, evidence, visibility, and archive facets plus durable transition history.
- `research-idea-lineage`: Extends canonical Research Ideas, generation groups, decision option membership, CLI queries, validation, and legacy migration for portfolio inspection.
- `research-recording-contracts`: Requires idea-producing record writes and system skills to persist canonical facets, decision context, lineage, and transition provenance atomically when enough intent is known.
- `topic-graph-read-api`: Adds portfolio facet metadata, semantic filters, decision context, and bounded ancestry or descendant traversal to renderer-neutral read models.
- `topic-idea-lineage-overview`: Adds portfolio presets, lifecycle-aware rendering, decision-rationale inspection, and closed or deferred idea review to the Idea Graph and Idea Timeline.
- `project-web-data-contracts`: Documents and validates the new idea facet, decision-context, traversal, preset, and steering-action payloads used by Project Web.

## Impact

The change affects Workspace Runtime Research Idea storage and migrations, runtime records, `ext research ideas` CLI commands, record-write conveniences, query-index projections, GUI Backend read and action APIs, Project Web Idea Graph and Idea Timeline state, idea detail panels, system-skill assets, topic fixtures, UI contracts, and unit, integration, and browser tests. Houmao remains an execution adapter behind Project Operator routing and does not become canonical Research Idea or GUI language.
