## Context

Canonical Research Ideas already have stable identity, display keys, visibility, Idea Realizations, generation groups, and typed Idea Lineage Edges. Workspace Runtime, the `ext research ideas` CLI, graph read models, Project Web, and DeepSci skills all depend on that model. The current `status` field, however, combines several independent facts: whether an idea has been explored, whether it was selected, whether evidence supports it, and whether the idea is deferred, rejected, superseded, or archived.

That compression loses information and makes user-facing queries unreliable. A selected idea can still be unexplored, an explored idea can remain open, and a refuted idea can be reopened. Generation-group membership also does not prove that every member was considered in a particular selection decision. The GUI therefore needs canonical facets and explicit decision membership rather than more display-only status heuristics.

The design must preserve three existing boundaries. Research Idea lineage stays separate from record lineage. GUI browsing stays read-only. Houmao remains an execution adapter behind Project Operator routing rather than becoming canonical schema or GUI language.

## Goals / Non-Goals

**Goals:**

- Represent exploration progress, decision disposition, evidence assessment, visibility, and archival state independently.
- Preserve every meaningful state transition with rationale and durable refs.
- Make complete considered option sets and selection, deferral, closure, and reopening reasons queryable.
- Support portfolio presets, exact state filters, and bounded ancestor or descendant traversal in graph and timeline views.
- Let a user explore an idea alongside current work or explicitly replace current selected ideas through a provenance-backed Project Operator action.
- Teach idea-producing system skills and record-write conveniences to create canonical state and decision context when they accept an output.
- Migrate legacy data conservatively without hiding ambiguous ideas.

**Non-Goals:**

- Infer canonical state, lineage, or decisions from generated Markdown.
- Treat a Research Idea as a Research Inquiry, Research Task, Run, Artifact, or record lineage node.
- Make ordinary node selection, focus, layout, filtering, hover, or detail inspection mutate research state.
- Define a globally unique selected idea for a Research Topic; selections remain scoped by their Decision Records and affected idea set.
- Promote `Topic Lead`, Houmao sessions, or other adapter terms into canonical Isomer domain language.
- Automatically close an idea because evidence refutes it, or automatically mark an idea supported because an experiment mentions it.

## Decisions

### 1. Store Independent Canonical State Facets

Research Ideas gain four canonical state fields while retaining the existing visibility field.

| Facet | Values | Meaning |
| --- | --- | --- |
| `exploration_state` | `unknown`, `unexplored`, `exploring`, `explored` | Whether focused research work has investigated the idea |
| `decision_state` | `unknown`, `open`, `shortlisted`, `selected`, `deferred`, `closed` | The current portfolio disposition |
| `evidence_state` | `unknown`, `unassessed`, `inconclusive`, `supported`, `mixed`, `refuted` | The current evidence assessment |
| `archive_state` | `active`, `archived` | Whether the idea remains in the active canonical collection |
| `visibility` | `primary`, `supporting`, `hidden` | Whether and where the idea appears in user-facing views |

`unknown` means existing data does not justify a classification. `unassessed` is an explicit assertion that no evidence assessment has occurred. `closed` is the general decision disposition; a required reason code and rationale distinguish rejection, supersession, duplication, invalidation, user closure, and other closure causes.

The existing `status` field becomes a deprecated compatibility projection during the migration window. New code reads facets as the source of truth. Canonical writes update the compatibility projection deterministically and validation reports any projection conflict. This approach lets older clients continue to read familiar values while preventing the legacy field from making new decisions.

Alternatives considered:

- Expanding the single status enum was rejected because combinations such as selected plus unexplored or deferred plus supported remain impossible.
- Deriving facets at read time was rejected because inference would vary by client and would not preserve actor, rationale, or transition provenance.
- Replacing visibility with a lifecycle facet was rejected because Primary Idea is a presentation role, not a research decision.

### 2. Record Transitions and Decision Option Membership Explicitly

A `research_idea_state_transitions` relation records the idea, changed facet, previous value, next value, reason code, rationale, actor ref, timestamp, and optional Decision Record, Gate, Evidence Item, Artifact, Finding, Research Task, Run, and Provenance Record refs. Multi-facet changes share an operation id so readers can reconstruct one user or agent action.

A separate decision-option relation links a Decision Record to every Research Idea considered by that decision. Each row records the option role or outcome, ordering when meaningful, generation id when relevant, rationale, and consequence. Generation groups continue to mean that ideas came from one production pass; they do not imply that a later decision considered every sibling.

State transitions, option membership, and the Decision Record are written in one Workspace Runtime transaction. Actual external dispatch occurs after the transaction commits.

Alternatives considered:

- Storing considered alternatives only in Decision Record JSON was rejected because graph and CLI queries would need profile-specific payload parsing.
- Treating generation groups as decision sets was rejected because generation and selection are different events.
- Overwriting current state without transition rows was rejected because closure, deferral, reopening, and selection explanations would be lost.

### 3. Add Deterministic CLI Mutation, Query, and Migration Surfaces

`ext research ideas upsert` accepts initial facet values. A dedicated transition command changes one or more facets with actor, rationale, and durable refs. Query commands filter by any facet, decision id, generation id, visibility, and archive state. Traversal commands return bounded ancestors or descendants with relation-kind and depth controls. Decision-context queries return the selected option, all considered options, outcomes, rationale, and evidence refs.

Composite steering uses one application service exposed through both CLI and GUI Backend action APIs. Preview and apply modes remain distinct for migration and repair. Validation reports invalid values, incomplete transitions, conflicting compatibility status, missing decision options, stale refs, and ambiguous legacy rows without changing data.

### 4. Define Semantic Portfolio Presets Over Canonical Facets

The GUI Backend exposes fixed preset identifiers and applied predicates so Idea Graph and Idea Timeline use the same meanings.

| Preset | Predicate |
| --- | --- |
| `current` | Primary, active ideas whose decision state is `unknown`, `open`, `shortlisted`, or `selected` |
| `all-proposed` | All non-hidden Research Ideas, including archived ideas, with visibility clearly labeled |
| `open-for-exploration` | Active ideas whose decision state is `open`, `shortlisted`, or `selected` |
| `unexplored` | Ideas whose exploration state is `unexplored` |
| `exploring` | Ideas whose exploration state is `exploring` |
| `explored` | Ideas whose exploration state is `explored` |
| `selected` | Ideas whose decision state is `selected` |
| `deferred` | Ideas whose decision state is `deferred` |
| `closed` | Ideas whose decision state is `closed` |
| `needs-classification` | Non-hidden ideas with `unknown` in exploration, decision, or evidence state |

Users can compose explicit facet, visibility, relation-kind, and archive filters after choosing a preset. Responses include the applied predicate, facet counts for the unfiltered source scope, topology completeness, and diagnostics. The backend returns lightweight idea and edge data only. Heavy realization payloads, rendered Markdown, and supporting record details remain lazy.

For complete bounded graphs, Project Web may apply an equivalent local predicate for instant interaction. Shared contract fixtures must prove that the local result matches the backend predicate. For incomplete source graphs, Project Web requests a coherent filtered projection from the backend.

### 5. Reuse Canonical Lineage for Ancestor and Descendant Inspection

The existing N-hop projection remains available for interactive focus. A bounded transitive traversal adds explicit `ancestors` and `descendants` semantics, root idea ids, eligible Idea Lineage Edge kinds, optional maximum depth, and node or edge safety limits. Results report whether traversal is complete and never infer edges from records or prose.

The GUI exposes focused actions such as `Show all descendants` and `Show ancestry`. Selection highlights remain browser state and do not change backend decision state.

### 6. Separate Browsing From Explicit Steering

Project Web adds two user-facing actions:

- `Explore this idea` starts or resumes focused work on the target without changing other selected ideas. The action sets the target exploration state to `exploring`, reopens it when the user explicitly confirms a deferred or closed target, and creates or resolves an idea-focused Research Inquiry and bounded Research Task.
- `Explore instead` requires the target idea, the exact currently selected ideas being replaced, and a user rationale. It records a Decision Record and option set, marks the target `selected` and `exploring`, and moves the named prior selections to `deferred` unless the user explicitly chooses another disposition.

The action request carries the expected index revision and an idempotency key. The Workspace Runtime transaction creates the Decision Record, option links, state transitions, Research Inquiry or Research Task refs, and a planned handoff or dispatch request. A concurrent state mismatch returns a conflict before mutation.

After commit, the Project Operator composes an instruction with the target `idea_id`, display key, title, summary, exact latest Idea Realization refs, Decision Record ref, Research Inquiry ref, Research Task ref, and the user's prompt. It routes that instruction to the configured topic research actor. Adapter delivery failure leaves the decision and task durable, marks dispatch or handoff state pending or blocked, and returns actionable diagnostics; it does not roll back the user's recorded choice.

An explicit human action satisfies the ordinary choice boundary. If configured policy requires a Gate for reopening or replacing an idea, the service returns or resolves that Gate and performs no governed mutation before resolution.

### 7. Make Idea-producing Skills Responsible at Acceptance Time

The shared Research Idea Recording guidance becomes the owner contract for system skills. Idea-producing skills must submit canonical idea identity, exact realization paths, known facets, lineage, generation membership, decision options, and transition refs before declaring an idea-bearing output accepted. Skills use `unknown` plus diagnostics when source material cannot justify a facet; they do not guess or rely on a later import from Markdown.

Record-write conveniences use one transaction for the durable research record and promised canonical idea effects. A profile that declares canonical idea effects fails acceptance if those effects cannot be written. Profiles that are not idea-bearing can continue to omit idea metadata.

### 8. Keep Read Models Lightweight and Cacheable

Facet fields, counts, decision summaries, and traversal metadata are compact scalar data. Graph list responses include only brief decision summaries and refs. Full option rationale, transition history, realizations, source JSON, Markdown, evidence, and task details load from dedicated detail endpoints on demand.

Index revision changes whenever canonical idea state, decision membership, or lineage changes. Existing revision-aware refresh and stable-layout behavior then update visible data without resetting browser selection, layout, collapsed controls, or filter state unnecessarily.

## Risks / Trade-offs

- [Risk] Existing data cannot be classified exactly from the legacy status field. → Migration sets only facets directly justified by the old value, marks the rest `unknown`, preserves the original value, and exposes a Needs Classification preset.
- [Risk] Compatibility `status` and canonical facets can diverge. → One projection function owns compatibility writes, validation reports conflicts, and new mutation paths reject direct legacy-status updates unless invoked through migration compatibility mode.
- [Risk] More facets make skill authoring and CLI calls verbose. → Shared recording guidance, structured command arguments, profile defaults, and atomic record-write conveniences reduce repetition without hiding decisions.
- [Risk] `Explore instead` can create a durable decision even if the research actor is unavailable. → Commit the human decision and task first, record dispatch as pending or blocked, and support idempotent retry through the Project Operator.
- [Risk] Filtering can disconnect a graph or hide relevant parents. → Responses label filtered topology, preserve source counts, offer ancestry or descendant expansion, and show diagnostics for omitted cross-boundary edges.
- [Risk] Local and backend preset evaluation can drift. → Publish applied predicates in read metadata and run shared fixtures against Python and TypeScript implementations.
- [Risk] A general `closed` state can obscure why an idea ended. → Require reason codes, rationale, and Decision Record refs for new closure transitions and show them in detail views.

## Migration Plan

1. Add facet, transition, and decision-option storage through an additive Workspace Runtime schema migration. Keep the legacy `status` column readable.
2. Add compatibility projection, validation, CLI transition, decision-context, traversal, and preview migration commands.
3. Map only directly justified legacy meaning: `raw` establishes unexplored and open; `candidate` establishes open; `selected` establishes selected; `active` establishes exploring; `supported` and `refuted` establish evidence state; `deferred`, `rejected`, and `superseded` establish decision state; `archived` establishes archive state. Every unspecified facet becomes `unknown`.
4. Record migration provenance without inventing historical actors, rationales, or timestamps. Require explicit apply before changing existing rows.
5. Update record-write conveniences and system skills, then repair canonical fixtures including the flash-attention topic through explicit plans.
6. Update read models and Project Web to prefer facets while continuing to expose deprecated compatibility status for one release.
7. Enable steering actions after state, Decision Record, Research Inquiry, Research Task, handoff, and idempotency tests pass.
8. Remove direct legacy-status mutation in a later change after compatibility consumers have migrated.

Rollback keeps the additive tables and facet columns intact while an older application version reads the maintained compatibility status. No rollback step deletes new transition or decision history. If a release must disable steering, the action route can be disabled while all read-only portfolio views remain usable.

## Open Questions

- The release that removes the deprecated compatibility `status` field will be selected after downstream consumers have migrated; removal is outside this change.
- Promoting `Topic Lead` into canonical domain language, if desired, requires a separate domain-language change. This design uses existing actor refs and configured topic research actor roles.
