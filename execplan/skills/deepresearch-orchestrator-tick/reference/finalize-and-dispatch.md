# Terminal checks, finalize, and dispatch discipline (orchestrator-tick steps 4–5)

Depth behind steps 4 (terminal/finalize) and 5 (dispatch) of `SKILL.md`.

## Step 4 — terminal checks → finalize

Finalize when any holds: `round_index >= max_rounds`; convergence (`$HARNESS bo status` no-improvement streak
vs `convergence_patience`, and/or `$HARNESS findings query` shows no new admissible finding for
`convergence_patience` rounds); acceptance criteria met.

**Research-completeness + run mode ("technically satisfied ≠ scientifically done"):** before choosing
`complete`, run `$HARNESS completeness audit --quest-id <q>` (the 7 scientific-quality checks: evidence
traceability, no orphan claims, mechanism explanation, named alternatives, ablation-or-documented-
infeasibility, lit audit, unresolved-discrepancy handling). Branch on `autonomy_mode` × `rigor_level`:
- **`auto` + `rigor_level='publication'`:** completeness is a HARD gate (the harness
  `_finalize_completeness_gate` also blocks `complete`). If soft acceptance is met but the checklist is unmet →
  do **not** `complete`; instead `finalize.record outcome=park` with `reopen_conditions=<the unmet items
  verbatim>` (+ paired `quest.update run_state=parked`), or route back to `experiment`/`analysis`.
- **`assistant` (any rigor) or `auto` + lower rigor:** completeness is ADVISORY — surface the unmet items and
  **recommend** `park`/`publish_and_continue` via `decision.record(route=..., requires_user_confirm=1)`, then
  **wait for `decision.confirm`** (the operator disposes). Do not self-finalize.

Backstops (all modes): `round_index >= max_rounds` still terminates;
`DEEPRESEARCH_COMPLETENESS_GATE_RIGOR=none` waives the hard gate.

**Publication-quality gate (before `complete`):** a `complete` finalize REQUIRES the publication bundle to
exist — verify via `$HARNESS state query` / the artifact rows + `runs/<q>/report/submission_checklist.md`:
(i) a **compiled PDF** report artifact (`runs/<q>/report/paper.pdf`, not just Markdown); (ii) ≥1 **figure**
artifact; (iii) a **bibliography** (`runs/<q>/refs/references.bib`); (iv) a clean **submission bundle**
(evidence_ledger + claim_evidence_map + checklist) with **no orphan supported claims** and `evidence validate`
clean; (v) the **Chinese edition** `runs/<q>/report/paper-zh.pdf` (bilingual output is expected); and (vi) the
**scholarship bar** — `$HARNESS lit audit --quest-id <q>` passes (enough real references AND ≥1
reference-backed positioning claim). If any are missing, do **not** complete — record a `decision.record`
routing back to `write` (or `outline`) and dispatch it. Only when the gate passes record the outcome. **Note:**
the harness *also* hard-blocks a `complete` finalize.record on the scholarship bar (apply-time gate), so
finalizing without it will fail even if this check is skipped — route back to `write` rather than retry.

**Finalize records a `--type finalize.record` outcome + the paired `quest.update` run_state:**
- `complete` → `run_state completed`; `stop` → `run_state stopped` (a low-quality stop needs a
  `decision.record(requires_user_confirm=1)` then `decision.confirm` first).
- `park` (park_and_continue_later) → `run_state parked`; `reopen_conditions` REQUIRED — populate it richly from
  `research-method/references/resume-packet-template.md` (strongest evidence · current baseline · preferred
  next route · top blockers · read-first · do-not-repeat), not a bare string.
- `publish_and_continue` (from a new incumbent) → record `published_ref` + `next_incumbent_ref` (a frontier
  incumbent / new branch); `run_state` stays `running` and the next round continues from that incumbent. Emit
  the operator completion/closure report.

**Finalize honesty (`research-method` finalization-checklist):** the closure report must classify every outcome
`supported | partially-supported | unsupported | deferred` with evidence paths, **preserve the belief-change
history** of any claim that was downgraded (don't silently delete it), keep a Limitations section
(data/metric/implementation/robustness/reproducibility + claims intentionally NOT made + failed branches that
changed direction), and never hide a failed branch or leave a completed analysis unmapped into the paper.

## Step 5 — dispatch the next stage

Pick the next stage from `state query cursor` (stage_catalog ordinal, or the last `decision`).
`decision`/`finalize`/`optimize` you do yourself (orchestrator-internal); all other stages dispatch to the
owning role.

**Decision discipline (name your losers):** a consequential `decision.record`
(route ∈ branch/reset/stop/finalize/idea/optimize) must choose among **≥2 named candidates** that round
(`idea`/`frontier_entry` rows) with the **non-winners marked** (idea `status` rejected/exhausted; frontier
`status` parked/rejected), and a `rationale_ref` artifact stating **Winner · Rejected alternatives (+ why each
lost) · Decisive reason**. `$HARNESS plan validate --quest-id <q>` lints this (warns on <2 candidates /
unmarked losers). Also **classify the bottleneck** in the rationale —
`mechanism | objective-mismatch | measurement-evaluator | infrastructure` — and route from it. NOTE:
`objective-mismatch` does NOT edit the objective (frozen); a *narrowed acceptance* goes through the
operator-confirmed `amend-acceptance` path (deepresearch-operator-control), never an in-place edit. Prefer the
**smallest action that genuinely resolves the current state**; record the next direction with explicit
`success_criteria` + `abandonment_criteria` (see
`research-method/references/strategic-decision-template.md`).
**Exploration-depth gate before an all-negative / "we found nothing" paper:** before routing such a line to
`write`/`finalize`, check four things — were **≥2 structurally distinct idea families** tried (not variants of
one)? has the **bottleneck framing itself** been challenged? did the literature surface a structurally
different route? is `time_budget`/`max_rounds` budget left? If any is "no/unsure" and budget remains, route back
to `idea` instead. (Houmao's `completeness audit.named_alternatives` is an existence check, not this depth
check.)

**`optimize`** (algorithm-first frontier mgmt): read `state query frontier` + `state query bo-observations`;
rank candidates by primary `measurement`, set the `incumbent` and promote/park/fuse routes via `--type
frontier.record` (+ `branch.record` for branch status). Then dispatch a new `experiment` for the next candidate
(via the experiment route) or route to `decision`/`write` when the frontier plateaus.
**Search discipline (`research-method` pack — brief-shaping/plateau/fusion playbooks):** keep a diverse promoted
slate (≈1 incumbent-deepening + 1 orthogonal-mechanism + 1 paradigm/objective shift); promote only 1–3, and
**don't let one mechanism family fill the slate**. **Family-shift trigger:** on a `bo status` plateau
(no-improvement streak, or repeated same-family attempts), the next pass must NOT be another same-family tweak
— switch to an orthogonal family / larger change-tier / fusion, or route to `decision`. Fuse only
**complementary** (not redundant) lines; never fuse two weak or same-mechanism lines.

For `experiment` with a defined search space, `$HARNESS bo suggest`, then record `--type idea.upsert` + `--type
experiment.upsert` (designed) + `--type experiment_param.record`.

**GPU gate (GPU-using stages — `experiment` AND `analysis`):** GPU use is confirmed **before the loop starts**
(operator runs `gpu confirm` during quest setup; the quest cannot reach `run_state=running` without it —
pre-loop start-gate). So in normal operation `$HARNESS gpu status --quest-id <q>` is **always** `confirmed=true`
here, and you dispatch experiment/analysis handoffs directly. **Do NOT routinely route to operator-control for
GPU confirmation** — that is reserved as a *safety fallback* only: if `gpu status` ever reports
`confirmed=false` (a legacy or misconfigured quest that started before the gate), do not open the handoff (the
harness blocks it apply-time anyway via `_gpu_gate`), record a `--type decision.record` (route to the blocked
stage, `requires_user_confirm`), hand off to **deepresearch-operator-control**, arm the continuation, and stop.
A single per-quest confirmation covers both stages. The experimenter/analyst restrict to the confirmed
`devices` (and `experiment run` injects `CUDA_VISIBLE_DEVICES` + fails closed).

Open the round if needed (`--type round.open`); for each fan-out target (1..`fanout_default`, ≤ `fanout_max=8`
for experiment): mint a `handoff_id`, `$HARNESS handoff open` (schema_id `deepresearch.email.task-request`, set
`receipt_due_at`/`result_due_at`), build → `$HARNESS email validate`/`render` → deliver the task-request to the
role, `$HARNESS email apply` (out). Set `--type round.update --expected_handoffs <k>`.
