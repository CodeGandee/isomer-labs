---
name: deepresearch-on-task-result
description: "Use when the orchestrator receives mail with schema_id \"deepresearch.email.task-result\" in the deepresearch loop — a specialist returned a result (experiment/scope/baseline/analysis/write/review, status processed or failed) that must be deduped, folded into state, gated/validated, advanced past its handoff, and routed when the round's fan-out completes. Keywords: orchestrator on-event, handoff_id, loop_id, methodology_used, review.verdict, gate status, round.close, fan-out."
---

# On Task Result (orchestrator)

## Overview

This is the orchestrator's on-event handler for `deepresearch.email.task-result`. In one bounded turn it confirms a specialist's just-returned result, gates/validates it, advances the handoff to `processed`, and — only when the round's fan-out is complete — closes the round and routes the next stage off the hard gate status.

## When to Use

- You are the **orchestrator** and received mail whose metadata `schema_id = "deepresearch.email.task-result"`.
- A specialist has finished a stage (`experiment`, `scope`, `baseline`, `analysis`, `write`, `review`) and reported `status` (`processed` or `failed`) with `produced[]`, `methodology_used[]`, and (on failure) `error`.

### When NOT to use
- You are NOT the orchestrator role, or the mail is not `deepresearch.email.task-result` (e.g. a `task-request` belongs to `deepresearch-on-task-request`; a self-wakeup belongs to `deepresearch-on-self-wakeup`; an unprompted tick belongs to `deepresearch-orchestrator-tick`).
- The `handoff_id` is already settled (`processed`/`failed`) — this is a duplicate / late result; archive and stop without re-folding (see Workflow step 1).
- Anything that would read or reuse another quest's artifacts/findings/refs — total quest isolation applies; never cross the quest boundary.

## Inputs

- The task-result payload: metadata `loop_id` + `handoff_id`; `status`; `stage`; `produced[]`; `methodology_used[]`; `error`.

## Workflow

You are the orchestrator collecting a specialist's result. **One bounded turn.**

1. **Parse + dedup.** Parse metadata; confirm `schema_id`. Run dedup `$HARNESS handoff query --seen <handoff_id>`. If the handoff is already `processed` (or `failed`), this is a duplicate / late result for a settled handoff — **archive the mail and stop, recording nothing.** See *Dedup discipline* below.
2. **Fold in + gate** the produced rows by stage type. The specialist already wrote its rows; you confirm and gate them. See *Stage fold-and-gate matrix* below for the exact per-stage commands and gate rules.
3. **Review-verdict routing.** After a VALID review verdict, route deterministically by `route_target` from `$HARNESS review route --quest-id <q>`. See *Review-verdict routing* below.
4. **Methodology-resolution check (Tier-3 gate).** For each `methodology_used[]` item, verify it resolves to the stage's validated typed record. On an unresolved required pack, branch by `autonomy_mode`. See *Methodology-resolution (Tier-3) gate* below.
5. **Advance the handoff.** `$HARNESS handoff advance --quest-id <quest_id> --handoff-id <handoff_id> --status result_received --at <ts>` then `--status processed`. Update fan-out: `$HARNESS record apply --type round.update --received_handoffs <n>`.
6. **If the round's fan-out is complete** (`received_handoffs` ≥ expected, cross-checked via `$HARNESS handoff query --quest-id <q>`): close the round and route off the hard gate. See *Round close + gate routing* below. **If not complete:** stop and wait for the next worker's result.
7. **Settle the mail.** `$HARNESS email apply` (in); archive the mail on success.

If the task does not map cleanly to these steps, use your native planning tool to build a plan from the commands/constraints in this skill, then execute it.

## Stage fold-and-gate matrix

The specialist already wrote its rows; you confirm/gate:

- **`experiment` result** → `$HARNESS result validate` (sets `result.validity`); if a new valid best, `$HARNESS record apply --type quest.update --best_result_ref ...`.
- **`scope`** → `$HARNESS scope validate --quest-id <q>` (computes the validator-owned `valid` on the typed `scope.contract`: concrete objective + primary metric/direction + eval plan or explicit waivers). A vague or under-specified scope is rejected; idea selection (bound) cannot proceed until it passes.
- **`baseline`** → **first** `$HARNESS baseline validate --quest-id <q>` (computes the validator-owned `valid` flag from the contract's `baseline_route` + eval contract + route-specific verification), **then** set the gate: `$HARNESS record apply --type quest.update --baseline_gate passed|waived|blocked`. `passed`/`waived` now require `valid=1` — an author-asserted `verification_verdict` alone is rejected; if `baseline validate` fails, route back to `baseline` with its reasons rather than opening the gate.
- **`analysis`/`write`** → confirm the produced rows exist via `$HARNESS state query`.
- **`review`** → the Reviewer must have recorded a typed `review.verdict` (verdict + verdict_ref to the typed verdict.json). Run `$HARNESS review validate --quest-id <q>` (schema + actionability; sets `valid` + `route_target`) and `$HARNESS evidence validate`. **If `review validate` fails** (non-actionable verdict), treat it like the Tier-3 gap below (auto: re-dispatch the review handoff with a corrective note; assistant: `decision.record(requires_user_confirm=1)`) — a non-actionable verdict is NOT accepted.
- **`status=failed`** → record a `decision.record` (continue/branch/reset/stop) per the failure.

## Dedup discipline

`$HARNESS handoff query --seen <handoff_id>`. If status is `processed` (or `failed`), this is a **duplicate / late result for an already-settled handoff** — archive the mail and **stop**, recording nothing. A resend bumps `attempt_count` but keeps the same `handoff_id`, so a result that arrives after you already settled the round must never re-fold.

Belt-and-suspenders: even if a fold slipped through, `record apply` is idempotent on `record_id`, so produced rows would not duplicate; and the `handoff` transition guard rejects advancing a terminal handoff.

## Review-verdict routing

After a VALID review verdict, read `$HARNESS review route --quest-id <q>` and route deterministically by `route_target`:

- `reject`/`borderline` → open the next handoff to **experiment** (missing_experiments), **analysis** (missing_analysis), or **write** (overclaims / unsupported_claims / rewrite_requirements), carrying the verdict's `*_todo[]` as the task brief; do NOT route to finalize.
- `accept` → the review side permits finalize, but a `complete` finalize.record still requires `manuscript coverage` (`submission_ready=true`) — both gates are enforced at the write path.
- A `borderline` at standard rigor needs an operator `review confirm` before finalize (publication never permits borderline).

## Methodology-resolution (Tier-3) gate

For each `methodology_used[]` item, run `$HARNESS methodology check --quest-id <q> --stage <stage> --applied-as <item.applied_as>`. It must **resolve** (the ref points at the stage's validated typed record: scope.contract / idea.select / baseline.contract / analysis.bridge / paper_spine / review.verdict). `methodology_used` is NO LONGER free text — an item whose `applied_as` does not resolve is treated as missing (background-only reading belongs in `methodology_consulted`, which does not count).

If any required pack lacks a RESOLVING `methodology_used` item:

- **`autonomy_mode='auto'`:** do **not** advance to `processed`. Re-dispatch the same `handoff_id` (`$HARNESS handoff open ... bump_attempt`) with a corrective note ("produce + validate the stage's typed record so each `methodology_used[].applied_as` resolves"), re-deliver the task-request, arm continuation, stop.
- **`autonomy_mode='assistant'`:** record the gap as a `decision.record(requires_user_confirm=1)` + surface a clear BLOCKING warning to the operator (deepresearch-operator-control); do not silently accept.

(`$HARNESS plan validate` independently warns at round close; this fold-time check is the active gate.)

## Round close + gate routing

**If the round's fan-out is complete** (the round's `received_handoffs` ≥ expected, cross-checked via `$HARNESS handoff query --quest-id <q>`): close the round (`$HARNESS record apply --type round.close`) and **route via `$HARNESS gate status --quest-id <q>`** — do NOT route on prose/LLM discretion when a hard gate says fail.

Read `data.gates`: dispatch the next stage to the **first blocking gate's `route_target`**:

| Blocking gate | route_target |
| --- | --- |
| `scope_contract` | scope |
| `idea_gate` | idea |
| `baseline_contract` | baseline |
| `campaign_coverage` | experiment \| analysis |
| `analysis_bridge` | analysis |
| `paper_spine` / `outline_valid` | outline |
| `manuscript_coverage` | write |
| `review_verdict` | its `route_target` |

If `finalize_readiness=pass` (no blocking gates), route to **finalize**. Then arm the continuation (as in `deepresearch-orchestrator-tick`).

**If not complete:** stop and wait for the next worker's result.

## Output

- State folded + gated; handoff `processed`; next stage dispatched when the round is complete.

## Stop

- End the turn after one result (and at most one routing pass when the round completes).

## Common Mistakes

- **Re-folding a duplicate / late result.** A resend keeps the same `handoff_id` and only bumps `attempt_count`. If `handoff query --seen` shows `processed`/`failed`, archive and stop — do not re-fold.
- **Opening the baseline gate on an author assertion.** `passed`/`waived` require `valid=1` from `baseline validate`. An author-asserted `verification_verdict` alone is rejected; on failure, route back to `baseline` with its reasons.
- **Accepting a non-actionable review verdict.** If `review validate` fails, treat it like a Tier-3 gap (auto re-dispatch with corrective note; assistant `decision.record(requires_user_confirm=1)`) — never accept.
- **Treating `methodology_used` as free text.** An item whose `applied_as` does not resolve to the stage's validated typed record counts as missing; background-only reading belongs in `methodology_consulted`.
- **Routing on prose/LLM discretion when a hard gate says fail.** When a round completes, route off `gate status` / `review route` `route_target`, not on judgment.
- **Routing a `reject`/`borderline` review to finalize.** Those route back to experiment/analysis/write with the verdict's `*_todo[]`; only `accept` permits finalize (and still needs `manuscript_coverage` / `submission_ready=true`).
- **Advancing past Tier-3 gaps in `auto` mode.** Do not advance to `processed`; re-dispatch the same `handoff_id` with `bump_attempt` and a corrective note, then arm continuation and stop.
- **Crossing the quest boundary.** Never read or reuse another quest's artifacts/findings/refs.
- **Doing more than one bounded turn.** End after one result and at most one routing pass on round completion.

### Rationalization / red-flags table

| If you catch yourself thinking… | Stop — the rule is |
| --- | --- |
| "This result looks fine, I'll just re-fold it to be safe." | A settled `handoff_id` must never re-fold; archive and stop. |
| "The author asserted verification, so the baseline gate can pass." | `passed`/`waived` require `valid=1` from `baseline validate`; otherwise route back to `baseline`. |
| "The review verdict isn't actionable but it's close enough to accept." | A non-actionable verdict is NOT accepted; treat as a Tier-3 gap. |
| "They cited the pack in prose, so methodology is satisfied." | `methodology_used[].applied_as` must RESOLVE to the typed record; prose/consulted doesn't count. |
| "The gate says fail but my read of the result says proceed." | Route off the first blocking gate's `route_target`; never override a hard gate with prose. |
| "It's borderline but good — finalize it." | `borderline` routes back (or needs operator `review confirm` at standard rigor; publication never permits borderline). |
