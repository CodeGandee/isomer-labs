---
name: deepresearch-orchestrator-tick
description: Orchestrator on-tick skill for the deepresearch loop. Invoked from a notifier/operator/self-wakeup prompt. Inspect quest+round state and perform one bounded reconciliation/dispatch/terminate pass, then arm the next durable self-wakeup.
---

# Orchestrator Tick (Orchestrator on-tick)

Invoked from a notifier/operator prompt with no new result mail, after folding a result, or as a
self-wakeup's `next_action`. Do **one** bounded pass, then stop. No sleeping/polling/in-chat waiting.

**Heartbeat-safe / idempotent:** re-read the cursor first and act only on persisted state. Deterministic
handoff ids + idempotent `record apply` mean a duplicate fire never double-dispatches or double-opens.

## Inputs

- `$HARNESS control status`, `$HARNESS state query <view>` (VIEW is **positional**, not a flag; available:
  `cursor`, `due-handoffs`, `best-result`, `frontier`, `bo-observations`, `open-claims`, `open-wakeups`,
  `branches`, `intake`), `$HARNESS control get-mode`. There is **no** `state query` fanout/convergence view:
  read fan-out completeness from the round (`received_handoffs` vs expected) / `$HARNESS handoff query`, and
  convergence posture from `$HARNESS bo status` (no-improvement streak) + `$HARNESS findings query`.

## Procedure

1. Read posture: `$HARNESS control status` + `$HARNESS state query cursor`. If `run_state` ∈
   {paused, stopped, completed, waiting_user}: stop. In `manual` mode, do one operator-prompted pass only.
2. **Reconcile handoffs (heartbeat-driven liveness):** this tick also fires on a periodic **heartbeat**
   (a repeating gateway reminder on the Orchestrator — see `deepresearch-operator-control`), so a stalled
   round is caught even when no result mail ever arrives. Run
   `$HARNESS handoff query --quest-id <q> --stalled --now <ts>` — it returns in-flight (`sent`/`acked`)
   handoffs past their `receipt_due_at`/`result_due_at` with an `action` per row:
   - `action="resend (reuse handoff_id, bump_attempt)"` (attempts remain) → `$HARNESS handoff open` with the
     **same `handoff_id`** + `bump_attempt=true`, then re-render + **re-deliver** the task-request mail. The
     re-delivery is new *unread* mail, which re-wakes an idle specialist whose `unread_only` notifier would
     otherwise never re-fire. Idempotent: the same `handoff_id` never double-opens and the worker dedups via
     `handoff query --seen`.
   - `action="fail+decision"` (`attempt_count >= max_attempts`) → `$HARNESS handoff advance --status failed`
     + `$HARNESS record apply --type decision.record` (route the failure: reassign / branch / stop).
   The `$HARNESS state query due-handoffs` view is handled identically for anything not surfaced by
   `--stalled`. **Never** re-dispatch a `processed`/`failed` handoff (the `handoff` transition guard rejects it).
3. **Wait gate:** if the round's fan-out is incomplete (the round's `received_handoffs` < expected,
   cross-checked via `$HARNESS handoff query --quest-id <q>`), stop (a result will wake you).
4. **Terminal checks** → finalize when any holds: `round_index >= max_rounds`; convergence (`$HARNESS bo
   status` no-improvement streak vs `convergence_patience`, and/or `$HARNESS findings query` shows no new
   admissible finding for `convergence_patience` rounds); acceptance criteria met.
   **Research-completeness + run mode (Phase 5; "technically satisfied ≠ scientifically done"):** before
   choosing `complete`, run `$HARNESS completeness audit --quest-id <q>` (the 7 scientific-quality checks:
   evidence traceability, no orphan claims, mechanism explanation, named alternatives, ablation-or-documented-
   infeasibility, lit audit, unresolved-discrepancy handling). Branch on `autonomy_mode` × `rigor_level`:
   - **`auto` + `rigor_level='publication'`:** completeness is a HARD gate (the harness `_finalize_completeness_gate`
     also blocks `complete`). If soft acceptance is met but the checklist is unmet → do **not** `complete`;
     instead `finalize.record outcome=park` with `reopen_conditions=<the unmet items verbatim>` (+ paired
     `quest.update run_state=parked`), or route back to `experiment`/`analysis`.
   - **`assistant` (any rigor) or `auto` + lower rigor:** completeness is ADVISORY — surface the unmet items
     and **recommend** `park`/`publish_and_continue` via `decision.record(route=..., requires_user_confirm=1)`,
     then **wait for `decision.confirm`** (the operator disposes). Do not self-finalize.
   Backstops (all modes): `round_index >= max_rounds` still terminates; `DEEPRESEARCH_COMPLETENESS_GATE_RIGOR=none`
   waives the hard gate. **Publication-quality
   gate (before `complete`):** a `complete` finalize REQUIRES the publication bundle to exist — verify via
   `$HARNESS state query` / the artifact rows + `runs/<q>/report/submission_checklist.md`: (i) a **compiled
   PDF** report artifact (`runs/<q>/report/paper.pdf`, not just Markdown); (ii) ≥1 **figure** artifact;
   (iii) a **bibliography** (`runs/<q>/refs/references.bib`); (iv) a clean **submission bundle** (evidence_ledger +
   claim_evidence_map + checklist) with **no orphan supported claims** and `evidence validate` clean;
   (v) the **Chinese edition** `runs/<q>/report/paper-zh.pdf` (bilingual output is expected); and (vi) the
   **scholarship bar** — `$HARNESS lit audit --quest-id <q>` passes (enough real references AND ≥1
   reference-backed positioning claim). If any
   are missing, do **not** complete — record a `decision.record` routing back to `write` (or `outline`) and
   dispatch it. Only when the gate passes record the outcome. **Note:** the harness *also* hard-blocks a
   `complete` finalize.record on the scholarship bar (apply-time gate), so finalizing without it will fail
   even if this check is skipped — route back to `write` rather than retry. **Finalize records a `--type finalize.record`
   outcome + the paired `quest.update` run_state:**
   - `complete` → `run_state completed`; `stop` → `run_state stopped` (a low-quality stop needs a
     `decision.record(requires_user_confirm=1)` then `decision.confirm` first).
   - `park` (park_and_continue_later) → `run_state parked`; `reopen_conditions` REQUIRED — populate it richly
     from `research-method/references/resume-packet-template.md` (strongest evidence · current baseline ·
     preferred next route · top blockers · read-first · do-not-repeat), not a bare string.
   - `publish_and_continue` (from a new incumbent) → record `published_ref` + `next_incumbent_ref`
     (a frontier incumbent / new branch); `run_state` stays `running` and the next round continues from
     that incumbent. Emit the operator completion/closure report.
   **Finalize honesty (`research-method` finalization-checklist):** the closure report must classify every
   outcome `supported | partially-supported | unsupported | deferred` with evidence paths, **preserve the
   belief-change history** of any claim that was downgraded (don't silently delete it), keep a Limitations
   section (data/metric/implementation/robustness/reproducibility + claims intentionally NOT made + failed
   branches that changed direction), and never hide a failed branch or leave a completed analysis unmapped
   into the paper.
5. **Else dispatch the next stage:** pick it from `state query cursor` (stage_catalog ordinal, or the last
   `decision`). `decision`/`finalize`/`optimize` you do yourself (orchestrator-internal); all other
   stages dispatch to the owning role:
   - **Decision discipline (Phase 4 — name your losers):** a consequential `decision.record`
     (route ∈ branch/reset/stop/finalize/idea/optimize) must choose among **≥2 named candidates** that round
     (`idea`/`frontier_entry` rows) with the **non-winners marked** (idea `status` rejected/exhausted;
     frontier `status` parked/rejected), and a `rationale_ref` artifact stating **Winner · Rejected
     alternatives (+ why each lost) · Decisive reason**. `$HARNESS plan validate --quest-id <q>` lints this
     (warns on <2 candidates / unmarked losers). Also **classify the bottleneck** in the rationale —
     `mechanism | objective-mismatch | measurement-evaluator | infrastructure` — and route from it. NOTE:
     `objective-mismatch` does NOT edit the objective (frozen); a *narrowed acceptance* goes through the
     operator-confirmed `amend-acceptance` path (deepresearch-operator-control), never an in-place edit.
     Prefer the **smallest action that genuinely resolves the current state**; record the next direction with
     explicit `success_criteria` + `abandonment_criteria` (see `research-method/references/strategic-decision-template.md`).
     **Exploration-depth gate before an all-negative / "we found nothing" paper:** before routing such a line
     to `write`/`finalize`, check four things — were **≥2 structurally distinct idea families** tried (not
     variants of one)? has the **bottleneck framing itself** been challenged? did the literature surface a
     structurally different route? is `time_budget`/`max_rounds` budget left? If any is "no/unsure" and budget
     remains, route back to `idea` instead. (Houmao's `completeness audit.named_alternatives` is an existence
     check, not this depth check.)
   - `optimize` (algorithm-first frontier mgmt): read `state query frontier` + `state query bo-observations`; rank candidates
     by primary `measurement`, set the `incumbent` and promote/park/fuse routes via `--type
     frontier.record` (+ `branch.record` for branch status). Then dispatch a new `experiment` for the next
     candidate (via the experiment route) or route to `decision`/`write` when the frontier plateaus.
     **Search discipline (`research-method` pack — brief-shaping/plateau/fusion playbooks):** keep a diverse
     promoted slate (≈1 incumbent-deepening + 1 orthogonal-mechanism + 1 paradigm/objective shift); promote
     only 1–3, and **don't let one mechanism family fill the slate**. **Family-shift trigger:** on a `bo status`
     plateau (no-improvement streak, or repeated same-family attempts), the next pass must NOT be another
     same-family tweak — switch to an orthogonal family / larger change-tier / fusion, or route to `decision`.
     Fuse only **complementary** (not redundant) lines; never fuse two weak or same-mechanism lines.
   - For `experiment` with a defined search space, `$HARNESS bo suggest`, then record `--type idea.upsert` +
     `--type experiment.upsert` (designed) + `--type experiment_param.record`.
   - **GPU gate (GPU-using stages — `experiment` AND `analysis`):** GPU use is confirmed **before the loop
     starts** (operator runs `gpu confirm` during quest setup; the quest cannot reach `run_state=running`
     without it — pre-loop start-gate). So in normal operation `$HARNESS gpu status --quest-id <q>` is
     **always** `confirmed=true` here, and you dispatch experiment/analysis handoffs directly. **Do NOT
     routinely route to operator-control for GPU confirmation** — that is reserved as a *safety fallback*
     only: if `gpu status` ever reports `confirmed=false` (a legacy or misconfigured quest that started
     before the gate), do not open the handoff (the harness blocks it apply-time anyway via `_gpu_gate`),
     record a `--type decision.record` (route to the blocked stage, `requires_user_confirm`), hand off to
     **deepresearch-operator-control**, arm the continuation, and stop. A single per-quest confirmation
     covers both stages. The Experimenter/Analyst restrict to the confirmed `devices` (and `experiment run`
     injects `CUDA_VISIBLE_DEVICES` + fails closed).
   - Open the round if needed (`--type round.open`); for each fan-out target (1..`fanout_default`, ≤
     `fanout_max=8` for experiment): mint a `handoff_id`, `$HARNESS handoff open` (schema_id
     `deepresearch.email.task-request`, set `receipt_due_at`/`result_due_at`), build → `$HARNESS email
     validate`/`render` → deliver the task-request to the role, `$HARNESS email apply` (out). Set
     `--type round.update --expected_handoffs <k>`.
5b. **Methodology self-audit for the orchestrator-internal stages you perform (`decision`/`optimize`/
   `finalize`).** Workers self-report `methodology_used` for their stages; YOU are the worker for these three,
   so when you close a `decision`/`optimize`/`finalize` round you MUST record the audit artifact yourself:
   `$HARNESS record apply --type artifact.record` with `kind='methodology-usage'`, `round_index=<r>`, and
   `ref=runs/<q>/methodology/r<r>-<stage>.md` citing **`research-method`** (the decision-route-criteria /
   optimize search / finalization-checklist cards you applied) + the bound output (the `decision`/`frontier`/
   `finalize_outcome` row). `finalize` additionally consults `paper-craft`/`review-craft` for the closure
   report. This is an audit overlay only — NOT authoritative over the DB rows. `$HARNESS plan validate` warns
   when a closed internal-stage round lacks this artifact.
6. **Arm continuation:** `$HARNESS wakeup arm` on lane `main` (next_stage, reason, next_action) → send the
   `deepresearch.email.self-wakeup` self-mail → `$HARNESS wakeup attach --message-ref <ref>`.
   **Re-render the plan map (Phase 2):** after closing a round (`round.close`), run `$HARNESS plan render
   --quest-id <q> --at <ts>` so `runs/<q>/plan.md` (a pure DB projection; never read back as truth) reflects
   the new node/route/revision state. The `plan_map_fresh` invariant flags a stale map if this is skipped.
   Record the internal-stage methodology-usage artifact (5b) BEFORE re-rendering so the plan map reflects it.
7. `$HARNESS state validate` opportunistically; on any violation, surface to the operator via
   **deepresearch-operator-control** instead of proceeding.

## Output

- One reconciliation/dispatch/terminate step recorded through the harness, plus an armed self-wakeup.

## Stop

- End the turn after one bounded pass.
