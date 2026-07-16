# Research Idea Portfolio

The Research Idea portfolio is the canonical topic-scoped collection of durable research concepts. It answers which ideas were proposed, explored, selected, deferred, or closed, and how one idea derives from another. DeepSci hypotheses and Kaoju survey directions use the same model after acceptance; Project Web does not parse either extension's payload to construct authoritative ideas.

## Independent Facets

Each Research Idea has five independent facets. Exploration is `unknown`, `unexplored`, `exploring`, or `explored`. Decision is `unknown`, `open`, `shortlisted`, `selected`, `deferred`, or `closed`. Evidence is `unknown`, `unassessed`, `inconclusive`, `supported`, `mixed`, or `refuted`. Archive is `active` or `archived`. Visibility is `primary`, `supporting`, or `hidden`.

Do not collapse these facts into one status. An idea can be selected but unexplored, explored but deferred, or refuted but open. `unknown` preserves missing historical knowledge. `unassessed` means an actor explicitly recorded that no assessment has occurred. Compatibility `status` remains readable for older clients but is not the source for new predicates or mutations.

Closing an idea requires a rationale and one reason: `rejection`, `supersession`, `duplication`, `invalidation`, `user_closure`, `legacy_rejection`, `legacy_supersession`, or `other`. Evidence never closes an idea automatically.

## Recording Ideas and Decisions

Create or update canonical identity with known initial facets:

```bash
isomer-cli --print-json ext research ideas upsert \
  --project . --topic my-topic \
  --idea-id stage-pipeline-predictor \
  --title "Stage-pipeline predictor" \
  --summary "Predict runtime through stage-specific costs." \
  --exploration-state unexplored \
  --decision-state open \
  --evidence-state unassessed
```

Record later state changes as transitions. The actor, expected prior value, rationale, operation correlation, and applicable durable refs make concurrent and historical interpretation deterministic:

```bash
isomer-cli --print-json ext research ideas transition stage-pipeline-predictor \
  --project . --topic my-topic \
  --facet exploration_state \
  --expected-from unexplored \
  --to exploring \
  --actor topic-actor:lead \
  --rationale "Begin the bounded predictor validation task." \
  --research-task-id research-task-stage-pipeline
```

A Decision Record's option set is separate from an Idea Generation Group. Record every idea the decision actually considered, including non-selected options and their authored outcomes:

```bash
isomer-cli --print-json ext research ideas decision-options upsert \
  --project . --topic my-topic \
  --decision-record-id decision-route-1 \
  --idea-id stage-pipeline-predictor \
  --outcome selected \
  --actor topic-actor:lead \
  --ordinal 0 \
  --rationale "Best bounded explanation of the measured stage behavior." \
  --metadata-json '{"option_set_complete":true}'
```

Idea-bearing structured outputs should declare all promised idea, exact realization, generation, lineage, option, and transition effects in their structured payload. Record acceptance commits the research record and those effects in one transaction. Markdown alone is never proof that canonical effects exist.

## Read-only Inspection

These commands do not mutate Workspace Runtime:

```bash
isomer-cli --print-json ext research ideas query --project . --topic my-topic --decision-state selected
isomer-cli --print-json ext research ideas query --project . --topic my-topic --exploration-state unexplored --include-archived
isomer-cli --print-json ext research ideas decision-context --project . --topic my-topic --idea-id stage-pipeline-predictor
isomer-cli --print-json ext research ideas traverse --project . --topic my-topic --root-idea-id stage-pipeline-predictor --direction descendants --max-depth 8
isomer-cli --print-json ext research ideas validate --project . --topic my-topic
```

Project Web offers `current`, `all-proposed`, `open-for-exploration`, `unexplored`, `exploring`, `explored`, `selected`, `deferred`, `closed`, and `needs-classification` presets. Graph and timeline share the same predicate and counts but store filter state separately in the browser. Node selection, layout, focus, filters, decision review, detail loading, and ancestry or descendant traversal remain read-only.

Full source JSON, rendered records, decision bodies, and evidence bodies load only through detail routes. This keeps the initial portfolio response compact. An unprojected legacy idea-bearing record produces a diagnostic and repair route; the GUI does not parse it into transient canonical nodes.

## Kaoju Direction Sets

`KAOJU:DIRECTION-SET` is a Decision Record and generation context, not one Research Idea. Each durable proposal object realizes one Research Idea at its exact object path. The proposal's direction id remains an alias. Actor-authored selection, deferral, or closure becomes option membership and directly justified transitions. A non-selected proposal remains open unless the actor explicitly changes its disposition.

Reading-list sources, comparison candidates, claims, audit repair routes, paper sections, and output artifacts do not become ideas unless an actor explicitly promotes a distinct durable concept. A wording or boundary revision that preserves the concept adds a realization to the same `idea_id`; a concept-changing successor needs a new `idea_id` and justified Idea Lineage Edge.

## Legacy Migration and Repair

Migration is preview-first. Legacy status migration maps only meaning justified by the old value and leaves other facets `unknown`:

```bash
isomer-cli --print-json ext research ideas migrate-status --project . --topic my-topic
isomer-cli --print-json ext research ideas migrate-status --project . --topic my-topic --apply
```

Legacy Kaoju Direction Set migration creates one idea per durable proposal, preserves direction ids as aliases, records directly justified options, diagnoses missing dispositions or rationale, and invents no lineage:

```bash
isomer-cli --print-json ext research ideas migrate-kaoju-direction-set legacy-direction-set \
  --project . --topic my-topic
isomer-cli --print-json ext research ideas migrate-kaoju-direction-set legacy-direction-set \
  --project . --topic my-topic --apply
```

Review preview paths and stable concept ids before apply. Back up the topic `state.sqlite` for manual fixture repair, record the approved mapping in `context/migrations/`, apply exact transitions and edges, rebuild the query index, then run `ideas validate`, every relevant preset, decision context, and bounded traversal. Preserve unknown historical facts instead of guessing.

## Explicit Steering

`Explore this idea` sets the target exploration state to `exploring` without changing other decisions. `Explore instead` requires the exact selected idea ids being replaced, selects and explores the target, and defaults each replacement to `deferred`. A closed replacement needs a canonical closure reason. A closed or deferred target needs explicit reopening confirmation and rationale.

```bash
isomer-cli --print-json ext research ideas steer \
  --project . --topic my-topic \
  --action explore-instead \
  --target-idea-id stage-pipeline-predictor \
  --replace-idea-id current-selected-model \
  --actor project-operator:user \
  --idempotency-key user-route-20260717-1 \
  --expected-index-revision qidx:CURRENT \
  --rationale "Investigate the stage mechanism instead." \
  --prompt "Validate the idea on the accepted comparator set."
```

The application commits the Decision Record, option set, transitions, Research Inquiry, bounded Research Task, provenance, and planned handoff atomically. It then composes a Project Operator instruction with exact idea identity, latest Idea Realization refs, decision, inquiry, task, and user prompt. Houmao may deliver that instruction, but Houmao terms remain adapter details. Delivery failure leaves canonical acceptance durable and returns pending or blocked dispatch state plus a retry ref.

Use `--no-dispatch` when an operator wants to commit the canonical steering action and route the planned handoff separately. Expected revision and expected facets prevent stale confirmation. Reusing an idempotency key with equivalent input returns the original refs; using it for different input returns a conflict.
