# State Contract — DeepResearch

## Authority and boundaries

- Backend: **sqlite** (`harness state` owns init/validate/query; `harness record` owns apply). Stable
  entities with clear transitions → SQL is the right fit per contract defaults.
- **One platform-level database** `runs/state.sqlite` holds *all* quests (so single-active-quest is
  enforceable in SQL). **TOTAL QUEST ISOLATION:** every row carries a `quest_id` and every per-quest
  entity — findings, references, artifacts — is owned by exactly one quest; there is **no** cross-quest
  data reuse or inspection. A new quest never reads, refers to, or inspects another quest's findings,
  references, or artifacts (invariants `finding_quest_owned` + `reference_quest_owned`; the shared DB is a
  control plane, not a cross-quest data pool). Per-quest rich artifacts live under `runs/<quest-id>/`.
  Quests are created at runtime via `record apply`, not at platform init; `seed.toml` seeds only
  domain-neutral registries + role/default templates.
- This file is the **authority** for `schema.sql`. If the two disagree, this file is the intent and
  `schema.sql` must be reconciled to it.
- State stores compact control-plane facts: ids, refs, statuses, ownership, decisions, scalar gates,
  evidence links, transition audit, completion posture, and the continuation/comms ledgers.
- Rich material (idea memos, run logs, result blobs, rendered mail, reports, fetched literature,
  reflexion prose) lives as **artifacts** under `runs/<quest-id>/`; state stores their refs/paths.
- Participant agents reach state **only** through harness commands, never raw SQL. Direct edits are
  operator repair only: pause the loop first, then run `state validate`.
- Timestamps are ISO-8601 strings supplied by the caller (harness); the schema never generates them.

## Platform defaults (resolved)

- **Distinct specialists per role** (Orchestrator / Scout / Experimenter / Analyst / Writer /
  Reviewer); `participant.role` + `participant.tool` record the binding.
- **Findings isolated per quest** (enforced, not just default): every `finding_memory` row has
  `scope='quest'` and a `quest_id`; cross-quest/global findings are disallowed at the schema and by
  invariant `finding_quest_owned`. A new quest never reuses or inspects another quest's findings.
- **One active quest to start**: the loop operates a single `quest` in `run_state='running'` at a time.

## Entity families

Registries (extensibility):

- `stage_catalog` — the set of research stages. Seeded with the 13 built-in stages; a knowledge pack
  may `INSERT` domain stages (`is_builtin=0`) without schema edits. `round.stage`, `quest.current_stage`,
  `decision.from_stage/to_stage`, and `self_wakeup.next_stage` are soft references into it.
- `knowledge_pack` — pluggable domain knowledge: extra skills, references, templates, validators,
  metric vocabularies, and domain **adapters** for the pluggable harness commands (`kind` in
  `runner`/`compiler`/`validator`/`metric_vocab`). `enabled` toggles a pack; `priority` orders enabled
  adapters of the same `(domain, kind)` — **lowest priority is the primary** adapter, others are
  fallbacks. Priorities must be unique per `(domain, kind)` so resolution is deterministic.

Quest control plane:

- `quest` — one research run (= the `loop_id`). Holds config (objective/acceptance refs, workspace
  ref, budget knobs), the baseline gate, lifecycle (`run_state`), `execution_mode`, the cursor
  (`round_index`, `current_stage`, `active_branch_id`, `active_idea_id`), and the best-result pointer.
- `round` — one round: its `stage`, the branch in play, expected/received handoff counts (the fan-out
  gate), open/closed status, and a summary artifact ref.
- `participant` — instance id → role → tool binding → liveness (`last_seen`). Mirrors agent bindings.

Research structure:

- `intake_asset` — a pre-existing asset audited at quest entry (`intake-audit` stage): kind, source ref,
  `trust` rank, and optional `adopt_as` (the state row it was adopted into; trusted-only).
- `branch` — a research route as a real git branch + optional worktree. Failed routes move to
  `parked`/`abandoned`, never deleted (preserve-failed-routes). Supports parent/child forking.
- `idea` — a hypothesis/direction (short statement + route + memo artifact ref), with parent linkage
  for refinement chains and a lifecycle (`proposed→selected→rejected→exhausted`).
- `experiment` — one bounded experiment bound to an idea/branch, with a locked `run_contract_ref`,
  a baseline flag, lifecycle (`designed→running→done|failed|aborted`), and a log ref.
- `search_space` / `experiment_param` — the BO surface: a quest's tunable dimensions, and the concrete
  point each experiment evaluated (`proposed_by` records whether a point came from an agent, the BO
  refiner, the operator, or the seed).
- `frontier_entry` — the optimization frontier for the `optimize` stage: ranks candidate routes
  (branch/experiment/result) by their primary `score`, tracks the single `incumbent`, and records
  promotion/fusion (`status` candidate|incumbent|promoted|parked|dropped|fused).
- `result` — one validated outcome of an experiment, with a `validity` verdict and an artifact ref.
- `measurement` — schema-light, domain-neutral metric capture (`metric_name` + numeric/text value +
  unit); `is_primary` marks the objective's headline metric (the BO objective).
- `analysis` — a slice/ablation testing a `parent_claim`, with a `confirms|blocks|inconclusive` verdict.

Evidence, decisions, knowledge:

- `claim` — a research claim with status (`open→supported|refuted|withdrawn`).
- `claim_evidence` — the claim↔evidence map: links a claim to a `result`/`analysis`/`measurement`/
  `reference`/`external` source with a `supports|contradicts|contextualizes` relation. A `contradicts`
  link carries a `resolved` flag (+ `resolution_ref`/`resolved_at`): only **unresolved** contradictions
  block a claim from becoming `supported`; an acknowledged-and-rebutted one does not.
- `decision` — every state-machine transition / route judgment (from_stage→to_stage + route +
  rationale ref), including the operator-confirmation gate (`requires_user_confirm`/`confirmed`).
- `finalize_outcome` — one row per finalize event: `complete`/`stop` (terminal), `park`
  (+`reopen_conditions`), or `publish_and_continue` (+`published_ref`, `next_incumbent_ref`).
- `finding_memory` — durable findings + reflexion lessons, **quest-owned** (always `scope='quest'` with a
  `quest_id`; no cross-quest/global findings), grounded by a measurement/result ref.
- `reference` — external knowledge fetched by the literature harness (arxiv/web/doi), with cache ref.
- `artifact` — generic index of rendered outputs (reports, figures, drafts, bundles, logs).

Continuation + comms ledgers:

- `self_wakeup` — the durable backbone of the self-mail continuation spine (see lifecycle below).
  Grouped by `continuation_lane` (default `'main'`): each lane is a single-threaded continuation. The
  initial tree-loop uses one lane per quest; the model supports multiple lanes later with no schema
  change (only the `single_continuation_lane_per_quest` policy invariant would be dropped).
- `handoff` — the logical handoff ledger for idempotency/dedup (stable `handoff_id`, attempts, due
  times, status).
- `mail_log` — physical message lifecycle, referencing the logical `handoff_id`.
- `operator_intent_event` — pause/resume/stop/override/recover/set-mode/takeover/handback/confirm.
- `quirk` — append-only framework/system pitfalls (replaces DeepScientist's quirks files).

## Key transitions (reconstructable)

Each important transition records: changed entity, source actor/event, new state/decision,
evidence/artifact ref, and timestamp.

- `quest.run_state`: `not_started → running → (paused|recovering|waiting_user|parked)* →
  (completed|stopped)`. `parked` = park_and_continue_later (resumable); `publish_and_continue` keeps the
  quest `running` from a new incumbent rather than ending it.
- `quest.execution_mode`: `auto` (default; notifier wakeups drive turns) | `manual` (operator prompts).
- `round.stage`: ordered by `stage_catalog.ordinal` but the Orchestrator may re-route via a `decision`;
  default path `[intake-audit] → scope → baseline → idea → (optimize) → experiment → analysis →
  decision → [outline] → write → review → [rebuttal] → finalize` (intake-audit/optimize/outline/rebuttal
  are optional; outline/rebuttal are Writer-owned publication stages).
- `quest.baseline_gate`: `pending → (passed|waived|blocked)`. A result may not advance to `write`
  unless the gate is `passed` or `waived`.
- `idea.status`: `proposed → selected` (one active per branch) `→ rejected|exhausted`.
- `experiment.status`: `designed → running → done|failed|aborted`.
- `result.validity`: `unchecked → valid|invalid|incomparable` (set by the Validator command). Only
  `valid` results may back a `supported` claim or update `quest.best_result_ref`.
- `claim.status`: `open → supported` (when sufficient `supports` evidence exists and no blocking
  `contradicts`) `→ refuted|withdrawn`.
- `self_wakeup.status`: `armed → delivered → consumed` (or `superseded` when re-armed, `failed`).
- `handoff.status`: `pending → sent → acked → result_received → processed` (or `failed`).

## Lifecycle flows

### Self-wakeup (durable continuation spine)

The loop never waits in-chat. Each round ends by persisting state and arming the next turn via a
durable self-mail, mirrored in `self_wakeup`:

1. Orchestrator finishes a round: writes results/decisions through the harness.
2. It inserts a `self_wakeup` row (`status='armed'`) on the quest's continuation lane (`'main'` by
   default) capturing `next_stage`, `reason`, `next_action`, and a fresh `handoff_id`; then sends a
   `[self-wakeup]` self-mail and records its opaque `message_ref` back onto the row.
3. The mail-notifier wakes the loop; the Orchestrator reads the open self-mail, finds the matching
   `armed` row, sets it `delivered`, then acts.
4. On completion it sets the row `consumed` and archives the self-mail.
5. If a round re-plans before the previous wakeup fired, the stale row is set `superseded` (idempotent
   by `handoff_id`, so a late delivery is ignored).
6. **Recovery**: after any interruption, `state query --open-wakeups` returns rows in `armed`/
   `delivered`; `recover` rebuilds the next-step intent from them rather than from a fragile live turn.

Live gateway reminders are never used for the spine (they die on gateway restart). `self_wakeup` is the
only authority for "what the loop intends to do next".

### Handoff / dedup (idempotent dispatch)

Every dispatch between agents (or self) carries `loop_id` (= `quest_id`) + a stable `handoff_id`:

1. Sender inserts/updates a `handoff` row (`pending→sent`, `attempt_count++`), sets `receipt_due_at`
   and `result_due_at`, then sends the mail; the physical send is logged in `mail_log` with the same
   `handoff_id`.
2. Receiver, before acting, checks the `handoff` ledger: a `handoff_id` it has already `processed` is a
   duplicate and is acknowledged without re-doing work (dedup).
3. Normal progress: `sent → acked` (receipt mail) `→ result_received` (result mail) `→ processed`.
4. **Resend policy** (relay/edge-loop pattern): a supervisor resends *only* when downstream work
   cannot be observed and `now > receipt_due_at`/`result_due_at`, reusing the same `handoff_id` and
   incrementing `attempt_count`; at `attempt_count >= max_attempts` it marks `failed` and routes to a
   `decision` instead of looping forever.

### Bayesian-optimization refinement

When a quest declares a `search_space`, idea refinement can be delegated to the deterministic BO
refiner instead of (or alongside) the Orchestrator's heuristic selection:

1. Each evaluated experiment records its point in `experiment_param` and its objective in the
   `measurement` row flagged `is_primary` (with the objective sense declared in the quest/acceptance).
2. `bo suggest` reads `search_space` + all completed `(experiment_param, primary measurement)` pairs
   for the quest and returns the next candidate point(s).
3. The Orchestrator records each suggestion as a new `idea` (+ `experiment` with
   `experiment_param.proposed_by='bo'`) and dispatches it like any other experiment.
4. With no `search_space`, the refiner is skipped and the Ideator proposes from `finding_memory` +
   `analysis` verdicts — the platform stays fully general for non-tunable research.

### Literature / reference ingestion

1. Any stage may call `lit search`/`lit fetch` (arxiv/web). Fetched sources are cached as artifacts
   under `runs/<quest-id>/refs/` and recorded as `reference` rows (with `cite_key` when applicable).
2. A reference becomes evidence by inserting a `claim_evidence` row with `source_kind='reference'`,
   `source_ref=<reference_id>`, and a `supports|contradicts|contextualizes` relation.
3. Durable literature insight is additionally written to `finding_memory` (`kind='reference'`), scoped to
   the owning quest. References are **quest-owned** (`reference.quest_id` REQUIRED); there is **no**
   cross-quest cache reuse — each quest fetches and caches its own sources (invariant
   `reference_quest_owned`).

### Claim–evidence linkage

`claim` + `claim_evidence` are the findings-memory core that gates synthesis:

- A claim is `supported` only when it has sufficient `supports` evidence from `valid` results/analyses
  (and/or references) and no `contradicts` link with `resolved=0`. A contradiction can be acknowledged
  and later rebutted by setting `resolved=1` (+ `resolution_ref`), which unblocks support.
- The Writer may only assert claims that are `supported`; `review` audits the claim↔evidence map for
  coverage and for orphan assertions (claims with no evidence). `evidence validate` enforces this.

## Invariants

Named checks live in `invariants.toml`, run by `harness state validate`. At minimum:

- `single_open_round`: at most one `open` round per quest.
- `single_active_quest`: at most one quest in `run_state='running'` (default platform posture).
- `round_index_bounded`: `round_index <= max_rounds`.
- `baseline_gate_before_write`: no `round.stage='write'` while `baseline_gate='pending'|'blocked'`.
- `valid_backs_supported`: every `supports` `claim_evidence` from a `result` points at a `valid` result.
- `supported_claim_no_open_contradiction`: a `supported` claim has no `contradicts` link with
  `resolved=0` (resolved/rebutted contradictions are allowed).
- `best_result_is_valid`: `quest.best_result_ref` (when set) points at a `valid` result.
- `wakeup_handoff_unique`: at most one non-superseded/non-consumed `self_wakeup` per `handoff_id`.
- `single_open_wakeup_per_lane`: at most one open wakeup per `(quest, continuation_lane)` (durable).
- `single_continuation_lane_per_quest`: **initial policy** — one continuation lane per quest; drop this
  single check to enable multiple self-wakeup threads.
- `handoff_attempts_bounded`: no `handoff` with `attempt_count > max_attempts` left non-`failed`.
- `adapter_priority_unique`: enabled adapters of one `(domain, kind)` have unique `priority`.
- `gated_stop_confirmed`: a quest is not `stopped` on a gated stop `decision` left unconfirmed.
- `intake_adopt_trusted`: an `intake_asset` is adopted (`adopt_as` set) only when `trust='trusted'`.
- `single_incumbent_per_quest`: at most one `frontier_entry` with `status='incumbent'` per quest.
- `park_has_reopen` / `publish_has_incumbent`: a `park` finalize records `reopen_conditions`; a
  `publish_and_continue` records `next_incumbent_ref`.

## Scheduling queries (must be answerable)

- "current quest + round + stage" (drives the Orchestrator tick).
- "open self-wakeups for this quest" (continuation + recovery).
- "handoffs past their receipt/result due time with status not in (processed,failed)" (resend posture).
- "expected vs received handoffs for round N" (fan-out → collect gate).
- "valid results ordered by primary measurement" (best-result + plateau/convergence detection).
- "rounds since the last new admissible finding" (convergence vs `convergence_patience`).
- "open claims with insufficient evidence" (synthesis readiness).
- "active branch + its worktree ref; parked/abandoned branches" (route management + recovery).
- "evaluated points + primary objective for this search space" (BO refiner input).

## Non-state content

Idea/decision/analysis prose, run logs, result blobs, rendered mail bodies, report/figure outputs,
fetched literature content, and reflexion prose live as artifacts under `runs/<quest-id>/`, not as
columns. State stores their refs only.
