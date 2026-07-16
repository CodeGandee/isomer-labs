# Research Idea Portfolio Contract

The Research Idea portfolio contract is the shared source for Idea Graph and Idea Timeline. It projects every topic-scoped canonical Research Idea without inspecting the producing extension or parsing DeepSci or Kaoju payloads in the browser.

## Canonical Node Fields

A canonical portfolio node includes `idea_id`, `display_key`, `title`, `summary`, `exploration_state`, `decision_state`, `evidence_state`, `archive_state`, `visibility`, `needs_classification`, `backend_selected`, `decision_summary`, `transition_refs`, `decision_record_ids`, `generation_ids`, `steering_eligibility`, and lazy `detail_refs`. The five facets are independent:

| Facet | Values |
|---|---|
| `exploration_state` | `unknown`, `unexplored`, `exploring`, `explored` |
| `decision_state` | `unknown`, `open`, `shortlisted`, `selected`, `deferred`, `closed` |
| `evidence_state` | `unknown`, `unassessed`, `inconclusive`, `supported`, `mixed`, `refuted` |
| `archive_state` | `active`, `archived` |
| `visibility` | `primary`, `supporting`, `hidden` |

`unknown` is a canonical value, not permission to infer a value from `status`, prose, record kind, lineage, or timestamps. `needs_classification` lists each unknown exploration, decision, or evidence facet. The compatibility `status` field may remain present, but clients must not use it for portfolio predicates.

`CanonicalIdeaPortfolioNodeContract` requires all five facets. `TopicGraphNodeContract` remains permissive for explicitly diagnosed legacy fallback nodes. The backend must label fallback mode and must not silently omit canonical fields.

## Fixed Presets

| Preset | Canonical Predicate |
|---|---|
| `current` | Active Primary Ideas with decision `unknown`, `open`, `shortlisted`, or `selected` |
| `all-proposed` | Every non-hidden idea, including supporting and archived ideas |
| `open-for-exploration` | Active non-hidden ideas with decision `open`, `shortlisted`, or `selected` |
| `unexplored` | Non-hidden ideas with exploration `unexplored` |
| `exploring` | Non-hidden ideas with exploration `exploring` |
| `explored` | Non-hidden ideas with exploration `explored` |
| `selected` | Non-hidden ideas with decision `selected` |
| `deferred` | Non-hidden ideas with decision `deferred` |
| `closed` | Non-hidden ideas with decision `closed` |
| `needs-classification` | Non-hidden ideas with any unknown exploration, decision, or evidence facet |

Explicit exploration, decision, evidence, archive, visibility, generation, and Decision Record filters refine the preset with AND semantics. Multiple comma-separated values within one facet have OR semantics. Relation, text, and paging filters follow the order reported in `applied_predicate.composition_order`.

## Portfolio Metadata

`portfolio` includes the selected `preset`, `available_presets`, `explicit_filters`, `applied_predicate`, `source_counts`, `visible_counts`, `omitted_cross_boundary_edge_count`, and `source_topology_complete`. Source and visible counts include per-value counts for all five facets. Filtered edges remain only when both endpoints are visible.

Project Web may apply the same predicate locally only when it has a complete bounded source graph. The shared fixture at `tests/fixtures/research_idea_portfolio.json` proves Python and TypeScript parity for mixed-paradigm and Kaoju-only portfolios. Browser filter state is stored per topic and view; it is not canonical state and cannot change the topic index revision.

## Legacy and Lazy Boundaries

An idea-bearing legacy record without canonical projection produces `idea_bearing_record_unprojected` with previewable repair metadata. It does not produce transient payload-parsed idea nodes. Graph and timeline payloads omit full source JSON, rendered Markdown, record bodies, and transition rationale bodies. Clients load those through idea detail, decision context, record detail, and file routes.
