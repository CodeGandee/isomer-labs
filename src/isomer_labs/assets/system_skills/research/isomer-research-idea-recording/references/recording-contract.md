# Canonical Recording Contract

## Durable-Concept Test

A Research Idea is a durable research concept that remains meaningful across records and workflow stages. Record it when a user may reasonably ask whether it was proposed, explored, selected, deferred, closed, reopened, supported, refuted, or derived from another concept.

Do not promote an object merely because a payload calls it an idea, candidate, direction, suggestion, or route. Sources, papers, repositories, datasets, models-as-assets, claims, findings, metrics, comparison rows, implementation patches, execution attempts, audit repairs, writing sections, and search queries retain their existing canonical types unless an actor explicitly promotes a distinct research concept.

## Canonical Facets

Treat these fields as independent sources of truth:

| Facet | Values | Meaning |
| --- | --- | --- |
| `exploration_state` | `unknown`, `unexplored`, `exploring`, `explored` | Focused research progress |
| `decision_state` | `unknown`, `open`, `shortlisted`, `selected`, `deferred`, `closed` | Portfolio disposition |
| `evidence_state` | `unknown`, `unassessed`, `inconclusive`, `supported`, `mixed`, `refuted` | Current evidence assessment |
| `archive_state` | `active`, `archived` | Active collection membership |
| `visibility` | `primary`, `supporting`, `hidden` | User-facing presentation role |

Use `unknown` when existing durable material does not establish a value. Use `unassessed` only when the actor explicitly establishes that no evidence assessment has occurred. Never infer selection from exploration, closure from refutation, or support from selection.

The legacy `status` field is a deprecated deterministic projection. New writes set facets and let the runtime project `status`; direct status mutation is migration compatibility only.

## Identity and Realizations

Choose a stable topic-scoped semantic `idea_id`. Preserve source-local ids such as `R1`, `C3`, or a Kaoju direction id as aliases. Reuse the same `idea_id` when a revision changes wording, boundary detail, evidence depth, or deliverables without changing the concept.

Every structured Idea Realization must name one exact object-valued JSON path, for example `$.sections.raw_ideas[0]` or `$.sections.proposals[2]`. The source object must carry the canonical `idea_id` or a retained alias. Never point a Primary Idea at `$`, an array, a context section, notes, rationale, metrics, rendered Markdown, or an entire record.

## Initial Writes and Later Transitions

Use `ext research ideas upsert` only for initial canonical state or concept-stable display and source updates. Supply all known facets explicitly:

```text
isomer-cli --print-json ext research ideas upsert --idea-id <idea-id> --title <title> --summary <summary> --exploration-state unexplored --decision-state open --evidence-state unassessed --archive-state active --visibility primary
```

Use `ext research ideas transition` for every later facet change. Supply expected current state, actor, rationale, and the applicable Decision Record, Gate, Evidence Item, Artifact, Finding, Research Task, Run, or Provenance Record refs. Correlate multi-facet changes with one operation id or idempotency key.

```text
isomer-cli --print-json ext research ideas transition <idea-id> --facet exploration_state --expected-from unexplored --to exploring --actor <actor-ref> --rationale <why> --research-task-id <task-ref>
```

Closing requires a supported reason code, a rationale, and a Decision Record or Provenance Record ref. Supported closure reasons are `rejection`, `supersession`, `duplication`, `invalidation`, `user_closure`, and `other`; legacy migration may preserve `legacy_rejection` or `legacy_supersession`. Reopening a deferred or closed idea is an explicit decision transition with recorded actor and rationale.

Evidence transitions cite the terminal result refs that justify the assessment. Evidence never changes decision state implicitly. Exploration completion cites the accepted task, run, artifact, finding, or evidence refs that establish completion.

## Decisions, Generations, and Lineage

Record every considered Research Idea as an option of the Decision Record. Use outcomes `considered`, `selected`, `not_selected`, `shortlisted`, `deferred`, `closed`, or `reopened`, with ordinal, generation id, rationale, consequence, actor, and supporting refs when available. An unselected option remains `open` unless the actor explicitly defers or closes it.

Generation groups describe concepts produced in one pass. Store exact member ids and parent ids. They do not prove consideration by a later decision; decision option membership is separate.

Use only justified concept lineage:

- `derived_from`: the child concept follows from a parent concept.
- `selected_from`: the selected concept was formed from candidate concepts rather than merely chosen unchanged.
- `merged_from`: the child combines multiple parent concepts.
- `follow_up_to`: the child continues a prior concept after evidence, analysis, or a route choice.
- `alternative_to`: the concepts are explicit alternatives.
- `subsumes`: one concept intentionally covers another concept's mechanism, ablation, or test role.

Do not create idea-level `revision_of`. Record-level revision lineage stays separate from Research Idea lineage.

## Atomic Idea-Bearing Record Acceptance

When a structured profile promises canonical idea recording, include one `research_idea_effects` object in the authoritative JSON payload. It must declare `atomic=true` and list every affected idea with exact source path and explicit current facets. Add generation groups, lineage edges, complete decision options, and justified transitions in the same object.

The record service must return all created or updated idea, realization, generation, lineage, decision-option, transition, and operation refs. Any invalid path, missing idea, stale expected state, invalid durable ref, incomplete promised component, or decision mismatch rejects the record and rolls back every effect.

Profiles that are not idea-bearing may omit `research_idea_effects`. Do not infer ideas from their content.

## Producer Mappings

Map extension-specific output fields into this contract without copying or renaming the canonical vocabulary. DeepSci raw slates, candidate frontiers, selected hypotheses, rejected or deferred ledgers, analysis follow-ups, and evidence results use their declared idea object paths. Kaoju Direction Set v2 maps each durable proposal object to one canonical Research Idea, retains the direction id as an alias, records the proposal generation and complete option set, and transitions only dispositions the actor explicitly changed.

Kaoju discovery candidates remain Source Identities or survey material. Comparison candidates remain works or methods unless promoted as distinct conceptual directions. Claims, audit repairs, paper structure, and outputs retain their own canonical types.

## Migration Posture

Preview legacy migration before applying it. Preserve the original status or direction id and migration provenance. Set only values directly justified by the old data; leave the rest `unknown`. Never invent historical rationale, option membership, closure reasons, or idea lineage.

Legacy Kaoju Direction Set migration creates one proposed canonical idea per durable proposal only after preview review. It preserves source-local direction ids as aliases, records selection outcomes only when the payload justifies them, and reports ambiguous dispositions rather than guessing.

## Accepted-Output Verification

Before reporting completion:

1. Confirm the record response contains the expected `idea_writes` refs and a committed operation.
2. Query every affected `idea_id` and compare all five facets with the authored current state.
3. Resolve each Idea Realization and confirm its JSON path returns one matching object.
4. Query the Decision Record context and confirm every considered option, outcome, rationale, actor, and supporting ref.
5. Query generations and lineage and confirm exact membership and edge direction.
6. Inspect transition history for expected previous and next values, rationale, actor, reason code, and terminal refs.
7. Run `isomer-cli --print-json ext research ideas validate` and stop on errors.

Completion requires durable refs and successful verification. Plain files, Markdown summaries, operation-set output, query-index extraction, or a chat statement do not satisfy this checklist.
