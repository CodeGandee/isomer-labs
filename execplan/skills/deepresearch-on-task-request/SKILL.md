---
name: deepresearch-on-task-request
description: Use when a deepresearch specialist (scout-ideator, experimenter, analyst, writer, or reviewer) receives mail with schema_id "deepresearch.email.task-request". Covers parsing the task-request, handoff dedup, sending a deepresearch.email.receipt, doing one bounded stage of work (intake-audit, scope, baseline, idea, experiment, analysis, outline, write, review, rebuttal), GPU gate, typed records and validators, methodology_used reporting, and replying upstream with deepresearch.email.task-result.
---

# On Task Request (specialist, role-aware)

## Overview

This is the event-handler skill a deepresearch specialist runs when it receives a `deepresearch.email.task-request`. In one bounded turn you acknowledge the request, do the work for YOUR role and the request's `stage`, record durable rows, and reply upstream to the orchestrator with a `deepresearch.email.task-result`.

## When to Use

Use this skill when:
- You are a deepresearch **specialist** (scout-ideator, experimenter, analyst, writer, or reviewer), AND
- You received mail with `schema_id = "deepresearch.email.task-request"`.

Do **NOT** use this skill when:
- The mail is a different schema (e.g. `deepresearch.email.receipt`, `deepresearch.email.task-result`, a self-wakeup) — route to the matching handler instead.
- You are the **orchestrator**: result validation, gate-setting, best-result selection, and routing are the orchestrator's job (see `deepresearch-orchestrator-tick`); the orchestrator-internal stages `decision`/`optimize`/`finalize` are self-audited at round close, not here.
- The requested `stage` is not owned by your role (see the stage→role table below) — you should not silently do another role's work.
- The work would cross quest boundaries: TOTAL quest isolation applies. Operate only within the request's quest (`runs/<q>/...`); never reuse, refer to, or inspect another quest's artifacts/findings/refs.

## Inputs

- The task-request payload: `stage`, `instructions_ref`, optional `branch_id` / `idea_id` / `experiment_id` / `run_contract_ref` / `inputs`; metadata `loop_id` + `handoff_id`.

## Workflow

1. **Parse + dedup.** Parse the metadata block; confirm `schema_id`. Dedup: `$HARNESS handoff query --seen <handoff_id>` — if already `processed`, archive the mail and stop.
2. **Send a receipt.** Reuse `handoff_id`, set `reply_to_payload_id`; build the `deepresearch.email.receipt` payload (`accepted=true`), `$HARNESS email validate` → `render` → deliver to the orchestrator via `houmao-agent-email-comms`; `$HARNESS email apply` (out). If you cannot take it, send `accepted=false` + `reason` and stop.
3. **Do the bounded work for `stage`** (record every durable row with `$HARNESS record apply`). Find your stage in the **Stage → Owning Role** table, satisfy every item in the **Mandatory Stage Checklists** before `status=done`, and follow the full per-stage method in `references/stage-work.md`. The **GPU gate** (see Gates) is FIRST for `experiment` and applies to any `analysis` ablation that re-runs on a GPU.
3b. **Apply methodology** (MANDATORY before `status=done` for any stage with a required pack) — see the **Methodology Usage** section. Consult the required pack(s) via `$HARNESS knowledge cards`, produce the stage's typed record and pass its validator, and report `methodology_used[]`. Do not send `status=done` until your typed record validates and `methodology_used[]` resolves.
4. **Reply with a task-result.** Build `deepresearch.email.task-result` (reuse `handoff_id`): `status=done` with `produced[]` listing the rows you recorded **and `methodology_used[]`** (per step 3b), or `status=failed` + `error`. Validate → render → deliver to the orchestrator; `$HARNESS email apply` (out).
5. **Archive** the task-request on success.

If the task does not map cleanly to these steps, use your native planning tool to build a plan from the commands and constraints in this skill, then execute it.

## Stage → Owning Role

| Stage | Owner | One-line scope |
| --- | --- | --- |
| `intake-audit` | scout-ideator | inventory + trust-rank pre-existing assets; current-board packet |
| `scope` / `baseline` / `idea` | scout-ideator | eval-contract, baseline-route choice, divergence→convergence + selection gate |
| `experiment` | experimenter (in YOUR isolated worktree) | **GPU gate FIRST**; run contract, evidence ladder, `evaluation_summary` |
| `analysis` | analyst | ablation / mechanism-isolation (**GPU gate applies**); per-slice evidence contract |
| `outline` | writer | paper-view + evidence-view; `outline validate` |
| `write` | writer | publication-grade bilingual manuscript (figures, bib, compiled PDFs, bundle) |
| `review` | reviewer | adversarial pass, evidence-authenticity gate, scholarship bar; disposition accept/revise/stop |
| `rebuttal` | writer | review-matrix → action-plan → evidence-update → response-letter |

## Mandatory Stage Checklists (in-context; the pack holds the depth)

These are the **non-negotiable** items per stage — satisfy every one before `status=done`. They live here in the skill body so the core discipline is always loaded even if you never open the pack; the named pack (`$HARNESS knowledge cards`) and `references/stage-work.md` carry the full method, templates, and examples. Record the bound output as a durable row/artifact and cite it in `methodology_used[].applied_as` (per Methodology Usage).

- **intake-audit** (pack `intake-rubric`): ☐ trust-rank every pre-existing asset (`intake_asset.record`) ☐ separate legacy/comparator/negative/appendix/current role before adopting any paper asset ☐ adopt (`adopt_as`) only `trusted` ☐ report a current-board packet + recommended next anchor.
- **scope/baseline** (pack `ideation-rubric` + `research-method`): ☐ eval-contract (task·dataset·split·eval-path·metric+direction·fair-comparison·useful-improvement) ☐ compare baseline routes attach/import/verify-local/reproduce/reject ☐ comparability verdict usable/caveats/blocked.
- **idea** (pack `ideation-rubric`): ☐ ≥2 mechanism families diverged → 2–3 candidates ☐ selection-gate score (<7/10 ⇒ don't promote) ☐ objective contract incl. false-progress signals ☐ ≥5-paper related-work sweep + novelty label ☐ ≤1 `selected` idea.
- **experiment** (pack `research-method`): ☐ run contract before coding ☐ climb the evidence ladder (significance test when claiming superiority) ☐ no silent dataset/split/metric/eval-path change ☐ `evaluation_summary` in the result artifact ☐ classify any failure.
- **analysis** (pack `research-method`): ☐ vary ONE factor (no multi-change "isolation") ☐ label dataset/split/protocol changes as generalization/stress-test ☐ per-slice evidence contract ☐ stop after two slices that don't move the claim boundary.
- **outline** (pack `paper-craft`): ☐ paper-view + evidence-view ☐ 1–3 scoped claims each with `what_would_falsify_it` ☐ 4–8 analysis jobs ☐ ≥3 routed reviewer objections ☐ `outline validate` PASSES.
- **write** (pack `paper-craft`): ☐ three-layer results (pattern→numbers→interpret) + signposting ☐ assert only `supported` claims ☐ real Related Work + ≥1 reference-linked positioning claim (`lit audit` passes) ☐ `manuscript validate` PASSES ☐ bilingual EN+ZH PDFs.
- **review** (pack `review-craft`): ☐ evidence-authenticity gate (recompute the real result count; label fabrication risk) ☐ literature-positioning benchmark (3–8 comparators) ☐ route correctly (wording≠experiment) ☐ review-report + experiment-todo artifacts ☐ disposition accept/revise/stop.
- **rebuttal** (pack `rebuttal-craft`): ☐ review-matrix (atomic, verbatim-clipped, classified+routed) ☐ action-plan with MVP/Enhanced/fallback ☐ response-letter voice rules (answer first; no invented results/"we will add") ☐ every supplementary run maps to a named reviewer id.

## Methodology Usage (MANDATORY before `status=done`)

The required packs by worker stage are: `intake-audit` → `intake-rubric`; `scope`/`idea` → `ideation-rubric`; `baseline` → `ideation-rubric` + `research-method`; `experiment`/`analysis` → `research-method`; `outline`/`write` → `paper-craft`; `review` → `review-craft`; `rebuttal` → `rebuttal-craft`. (The orchestrator-internal stages `decision`/`optimize`/`finalize` also require `research-method` but are self-audited by the orchestrator at round close — see `deepresearch-orchestrator-tick` — not here.)

For your stage you MUST:
- **Consult** the pack(s) via `$HARNESS knowledge cards` (or `$HARNESS knowledge query`) and read the relevant card files.
- **Produce the stage's typed record** that embodies the methodology and pass its validator — this IS the binding application evidence (not a free-text note):
  - `idea` → `idea.select` + `$HARNESS idea validate`
  - `baseline` → `baseline.contract` (+ the orchestrator's baseline gate)
  - `analysis` → `analysis.bridge` + `$HARNESS campaign validate`
  - `outline`/`write` → `paper_spine.upsert` + `$HARNESS outline validate` / `$HARNESS manuscript coverage`
  - `review` → `review.verdict` + `$HARNESS review validate`
  - (`experiment` has no fold-time typed record — its evidence is tagged `evidence_kind` on `claim_evidence.link` and bound downstream by campaign coverage.)
- **Report `methodology_used[]`** in the task-result: one item per required pack `{pack, cards:[...], applied_as:<the typed record's id or ref>}`. The orchestrator runs `$HARNESS methodology check` and **rejects any item whose `applied_as` does not resolve** to that stage's validated typed record — so this is no longer free text. Pure background reading (no typed application) goes in `methodology_consulted[]`, which does not count as application.

Do not send `status=done` until your stage's typed record validates and `methodology_used[]` resolves; if you genuinely could not apply a pack, send `status=failed` + `error` explaining why.

## Gates

- **GPU gate (experiment, and analysis ablations that re-run on a GPU).** Run `$HARNESS gpu status --quest-id <q>` FIRST. If `confirmed=false` you MUST NOT run anything on a GPU: reply `status=failed` with `error="GPUs not operator-confirmed"` and stop (the orchestrator opening the handoff is itself blocked apply-time; this is a backstop). If confirmed, **restrict to the confirmed devices** — prefer running every GPU command through `$HARNESS experiment run --experiment-id <id> --quest-id <q> --cmd "<command>" [--cwd <worktree>]` (fails closed, injects `CUDA_VISIBLE_DEVICES=<confirmed devices>`); for direct runs `export CUDA_VISIBLE_DEVICES=<devices>` first. Never touch a device outside the confirmed set. Pure data-only analysis needs no GPU. Operator GPU confirmation is requested/managed by the `deepresearch-operator-control` path.
- **Validator gates** read validator-owned flags, not artifact existence: `$HARNESS idea validate` (idea→experiment), `$HARNESS baseline validate` / `$HARNESS scope validate`, `$HARNESS campaign validate` (analysis→write), `$HARNESS outline validate`, `$HARNESS manuscript coverage` (writes `submission_ready`), `$HARNESS review validate`. See `references/stage-work.md` for exactly what each enforces.
- **BO decision gate.** When ≥2 idea candidates are gate-eligible, the FINAL pick is the BO loop's, bound via `$HARNESS bo select --decision-kind idea-selection --bind`; the orchestrator's `bo_idea_decision` gate blocks idea→baseline until the BO winner is bound (a single eligible candidate may be skipped with `bo select --skip-reason`).

## Common Mistakes

- **Sending `status=done` without the typed record / resolving `methodology_used[]`.** The orchestrator runs `$HARNESS methodology check` and rejects unresolved `applied_as`. Produce and validate the typed record first; if you couldn't apply a pack, send `status=failed` + `error`.
- **Treating methodology consultation as application.** Reading a pack (`methodology_consulted[]`) is not the same as producing the validated typed record (`methodology_used[]`). Only the typed record gates the stage.
- **Touching a GPU before / despite the GPU gate.** Always `$HARNESS gpu status` first; never use a device outside the confirmed set; on `confirmed=false` reply `status=failed` and stop.
- **Recording `status=done` on a failed run.** `experiment.upsert` must be `failed` on error — never `done` on failure.
- **Self-certifying readiness or the BO winner in prose.** `manuscript coverage`/`submission_ready` is validator-computed; the idea winner is BO-bound. Don't assert either by hand.
- **Doing the orchestrator's job.** Result validation, gate-setting, best-result selection, and routing belong to the orchestrator. End your turn after one task-request.
- **Crossing quest boundaries.** Operate only within the request's quest; never reuse/refer-to/inspect another quest's artifacts, findings, or refs.
- **Doing a stage your role doesn't own.** Check the Stage → Owning Role table; if it isn't yours, don't silently do it.
- **A `label` without `evidence_proof`.** `campaign validate` will not count an `evidence_kind` missing its required proof keys; result-backed evidence also needs `provenance_ok=1`.
- **Silent dataset/split/metric/eval-path changes** during experiment/analysis. Never change them silently; label generalization/stress-test slices as such.
- **Polished language hiding a missing result.** Never use writing craft to conceal absent evidence; assert only `supported` claims.

## Rationalizations vs. Red Flags

If you catch yourself thinking any of these, STOP — they are the discipline this skill exists to enforce.

| Rationalization | Red flag — do this instead |
| --- | --- |
| "I read the pack, that's the methodology applied." | Reading is `methodology_consulted[]`. You still owe the validated typed record in `methodology_used[]`. |
| "The result is basically there; I'll mark `done`." | If the typed record/validator hasn't passed (`idea`/`campaign`/`outline`/`review`/coverage), it's not `done`. Validate or send `failed`. |
| "GPUs are obviously available, I'll just run it." | Run `$HARNESS gpu status` first; on `confirmed=false`, reply `status=failed` with `error="GPUs not operator-confirmed"` and stop. |
| "I'll pick the best idea candidate myself." | When ≥2 candidates are gate-eligible the BO loop binds the winner; produce a genuine multi-candidate slate and let `bo select --bind` decide. |
| "Coverage looks ready to me." | `submission_ready` is validator-computed via `$HARNESS manuscript coverage`; resolve every reported gap. |
| "I'll tighten the prose to cover the thin result." | Polished language must not conceal a missing result. Assert only `supported` claims; route the gap honestly. |
| "This other stage is easy, I'll just handle it too." | Stay in your role's stage; the orchestrator routes other stages to their owners. |
| "I can reuse that other quest's baseline/finding." | Quest isolation is absolute. Collect fresh within this quest only. |
## Output

- A receipt, then a task-result, to the orchestrator; durable rows recorded via `$HARNESS record apply`.

## Stop

- End the turn after one task-request. Result validation, gate-setting, best-result selection, and routing are the orchestrator's job.
