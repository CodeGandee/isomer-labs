---
name: deepresearch-on-task-request
description: Specialist on-event skill for the deepresearch loop. Trigger on received mail with schema_id "deepresearch.email.task-request". Acknowledge, do the bounded work for your role + the requested stage, record durable rows, and reply upstream to the orchestrator.
---

# On Task Request (specialist, role-aware)

**Trigger:** received mail, `schema_id = "deepresearch.email.task-request"`.

You are a specialist (scout-ideator, experimenter, analyst, writer, or reviewer). Do the work for YOUR role
and the request's `stage`, then reply to the orchestrator. One bounded turn. See `deepresearch-shared-guide`.

## Inputs

- The task-request payload: `stage`, `instructions_ref`, optional `branch_id` / `idea_id` /
  `experiment_id` / `run_contract_ref` / `inputs`; metadata `loop_id` + `handoff_id`.

## Procedure

1. Parse the metadata block; confirm `schema_id`. **Dedup:** `$HARNESS handoff query --seen <handoff_id>`
   — if already `processed`, archive the mail and stop.
2. **Send a receipt** (reuse `handoff_id`, set `reply_to_payload_id`): build the `deepresearch.email.receipt`
   payload (`accepted=true`), `$HARNESS email validate` → `render` → deliver to the orchestrator via
   houmao-agent-email-comms; `$HARNESS email apply` (out). If you cannot take it, send `accepted=false` +
   `reason` and stop.
3. **Do the bounded work for `stage`** (record every durable row with `$HARNESS record apply`). The full
   method per stage — including the GPU gate for `experiment`/`analysis` — is in **`actions/stage-work.md`**;
   the non-negotiable items are the "Mandatory stage checklists" below. Stage → owning role:
   - `intake-audit` (scout-ideator) — inventory + trust-rank pre-existing assets; current-board packet.
   - `scope` / `baseline` / `idea` (scout-ideator) — eval-contract, baseline-route choice, divergence→convergence + selection gate.
   - `experiment` (experimenter, in YOUR isolated worktree) — **GPU gate FIRST**; run contract, evidence ladder, `evaluation_summary`.
   - `analysis` (analyst) — ablation / mechanism-isolation (**GPU gate applies**); per-slice evidence contract.
   - `outline` (writer) — paper-view + evidence-view; `outline validate`.
   - `write` (writer) — publication-grade bilingual manuscript (figures, bib, compiled PDFs, bundle).
   - `review` (reviewer) — adversarial pass, evidence-authenticity gate, scholarship bar; disposition accept/revise/stop.
   - `rebuttal` (writer) — review-matrix → action-plan → evidence-update → response-letter.
3b. **Methodology usage (MANDATORY before `status=done` for any stage with a required pack).** The required
   packs by worker stage are: `intake-audit` → `intake-rubric`; `scope`/`idea` → `ideation-rubric`;
   `baseline` → `ideation-rubric` + `research-method`; `experiment`/`analysis` → `research-method`;
   `outline`/`write` → `paper-craft`; `review` → `review-craft`; `rebuttal` → `rebuttal-craft`. (The
   orchestrator-internal stages `decision`/`optimize`/`finalize` also require `research-method` but are
   self-audited by the orchestrator at round close — see `deepresearch-orchestrator-tick` — not here.)
   For your stage you MUST:
   - **Consult** the pack(s) via `$HARNESS knowledge cards` (or `knowledge query`) and read the relevant card files.
   - **Produce the stage's typed record** that embodies the methodology and pass its validator — this IS the
     binding application evidence (not a free-text note): `idea` → `idea.select` + `idea validate`;
     `baseline` → `baseline.contract` (+ the orchestrator's baseline gate); `analysis` → `analysis.bridge` +
     `campaign validate`; `outline`/`write` → `paper_spine.upsert` + `outline validate` / `manuscript coverage`;
     `review` → `review.verdict` + `review validate`. (`experiment` has no fold-time typed record — its evidence
     is tagged `evidence_kind` on `claim_evidence.link` and bound downstream by campaign coverage.)
   - **Report `methodology_used[]`** in the task-result: one item per required pack `{pack, cards:[...],
     applied_as:<the typed record's id or ref>}`. The orchestrator runs `$HARNESS methodology check` and
     **rejects any item whose `applied_as` does not resolve** to that stage's validated typed record — so this
     is no longer free text. Pure background reading (no typed application) goes in `methodology_consulted[]`,
     which does not count as application.
   Do not send `status=done` until your stage's typed record validates and `methodology_used[]` resolves; if
   you genuinely could not apply a pack, send `status=failed` + `error` explaining why.
4. **Reply with a task-result** (`deepresearch.email.task-result`, reuse `handoff_id`): `status=done` with
   `produced[]` listing the rows you recorded **and `methodology_used[]`** (per 3b), or `status=failed` +
   `error`. Validate → render → deliver to the orchestrator; `$HARNESS email apply` (out).
5. Archive the task-request on success.

## Mandatory stage checklists (in-context; the pack holds the depth)

These are the **non-negotiable** items per stage — satisfy every one before `status=done`. They live here in
the skill body so the core discipline is always loaded even if you never open the pack; the named pack
(`$HARNESS knowledge cards`) and `actions/stage-work.md` carry the full method, templates, and examples. Record
the bound output as a durable row/artifact and cite it in `methodology_used[].applied_as` (per 3b).

- **intake-audit** (pack `intake-rubric`): ☐ trust-rank every pre-existing asset (`intake_asset.record`)
  ☐ separate legacy/comparator/negative/appendix/current role before adopting any paper asset
  ☐ adopt (`adopt_as`) only `trusted` ☐ report a current-board packet + recommended next anchor.
- **scope/baseline** (pack `ideation-rubric` + `research-method`): ☐ eval-contract (task·dataset·split·eval-path·metric+direction·fair-comparison·useful-improvement)
  ☐ compare baseline routes attach/import/verify-local/reproduce/reject ☐ comparability verdict usable/caveats/blocked.
- **idea** (pack `ideation-rubric`): ☐ ≥2 mechanism families diverged → 2–3 candidates ☐ selection-gate score (<7/10 ⇒ don't promote)
  ☐ objective contract incl. false-progress signals ☐ ≥5-paper related-work sweep + novelty label ☐ ≤1 `selected` idea.
- **experiment** (pack `research-method`): ☐ run contract before coding ☐ climb the evidence ladder (significance test when claiming superiority)
  ☐ no silent dataset/split/metric/eval-path change ☐ `evaluation_summary` in the result artifact ☐ classify any failure.
- **analysis** (pack `research-method`): ☐ vary ONE factor (no multi-change "isolation") ☐ label dataset/split/protocol changes as generalization/stress-test
  ☐ per-slice evidence contract ☐ stop after two slices that don't move the claim boundary.
- **outline** (pack `paper-craft`): ☐ paper-view + evidence-view ☐ 1–3 scoped claims each with `what_would_falsify_it`
  ☐ 4–8 analysis jobs ☐ ≥3 routed reviewer objections ☐ `outline validate` PASSES.
- **write** (pack `paper-craft`): ☐ three-layer results (pattern→numbers→interpret) + signposting ☐ assert only `supported` claims
  ☐ real Related Work + ≥1 reference-linked positioning claim (`lit audit` passes) ☐ `manuscript validate` PASSES ☐ bilingual EN+ZH PDFs.
- **review** (pack `review-craft`): ☐ evidence-authenticity gate (recompute the real result count; label fabrication risk)
  ☐ literature-positioning benchmark (3–8 comparators) ☐ route correctly (wording≠experiment) ☐ review-report + experiment-todo artifacts ☐ disposition accept/revise/stop.
- **rebuttal** (pack `rebuttal-craft`): ☐ review-matrix (atomic, verbatim-clipped, classified+routed) ☐ action-plan with MVP/Enhanced/fallback
  ☐ response-letter voice rules (answer first; no invented results/"we will add") ☐ every supplementary run maps to a named reviewer id.

## Output

- A receipt, then a task-result, to the orchestrator; durable rows recorded via `$HARNESS record apply`.

## Stop

- End the turn after one task-request. Result validation, gate-setting, best-result selection, and routing
  are the orchestrator's job.
