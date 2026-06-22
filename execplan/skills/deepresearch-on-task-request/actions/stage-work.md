# Per-stage bounded work (on-task-request step 3)

Do the work for YOUR role and the request's `stage`; record every durable row with `$HARNESS record apply`.
This is the depth behind step 3 of `SKILL.md`. The compact non-negotiable items per stage are in the
`SKILL.md` "Mandatory stage checklists"; this file is the full method per stage.

## intake-audit (scout-ideator)

Inventory + trust-rank the pre-existing assets under the quest repo (`quest.workspace_ref`); record one
`--type intake_asset.record` per asset (`trust` trusted|suspect|untrusted|rejected). For a trusted asset you
recommend adopting, set `adopt_as` and report it so the orchestrator adopts it (e.g. trusted baseline →
`baseline_gate`, trusted results → `result.record`). Report a recommended next anchor; the orchestrator records
the `decision`. Report a **current-board packet** (current mainline · incumbent · latest decisive result ·
active blocker · stale-routes-to-ignore · next-decision-scope) and, before recommending adoption of any
pre-existing paper/draft asset, separate its role (legacy / comparator / negative-evidence / appendix /
current) — do not adopt an old draft as current-method support. Don't confuse provenance (requests, branch
names, logs) with manuscript content.

## scope / baseline / idea (scout-ideator)

`--type idea.upsert`; for baseline, write the comparator+metric contract as an artifact
(`--type artifact.record`) **to the per-quest baseline path `runs/<q>/baseline/`** (canonical, read-only to the
experimenter thereafter — not the optional `shared/baseline/`) and report it. **Record a typed `baseline.contract`** — `baseline_id`, `baseline_name`, `comparison_policy`, `primary_metric_id`, `dataset`, `split`,
`eval_protocol`, `verification_verdict` (`verified_match`/`close_match`/`trusted_with_caveats`/`diverged`/`broken`,
or `waived`+`waiver_reason` if no baseline exists; metric_ids[]/validity_threats[] go in the `contract_ref`
artifact) via `$HARNESS record apply --type baseline.contract`. **Declare a `baseline_route`**
(`reproduced`|`imported`|`trusted`|`waived`) and the matching `evidence_ref`: `reproduced` → a baseline
`result_id` that has **validated provenance** (`result validate` → `provenance_ok=1`); `imported`/`trusted` → a
citation/source/note; `waived` → a `waiver_reason`. The orchestrator then runs **`$HARNESS baseline validate`**
(which computes the validator-owned `valid` flag) before setting `baseline_gate`: **`baseline_gate=passed` now
requires a VALIDATED contract (`valid=1`) on a real route, and `=waived` a validated waiver** — an
author-asserted `verification_verdict` alone no longer passes (the baseline-contract gate strengthens, not
replaces, the existing gate). May `$HARNESS lit search/fetch` → `--type reference.record`. **Use the `ideation-rubric` pack**
(`$HARNESS knowledge cards`): for `scope`, fill the **eval-contract** (task · dataset · split · official eval
path · primary metric + direction · fair-comparison rule · useful-improvement threshold) AND record it as a
typed **`scope.contract`** (objective · research_question · non_goals · primary_metric · metric_direction ·
dataset · split · eval_protocol · false_progress_signals · baseline_route_expectation · acceptance_criteria ·
constraints; defer a waivable field only via `contract.waivers{field: reason}`) — the orchestrator runs
**`$HARNESS scope validate`** (sets the validator-owned `valid`); a vague objective or missing metric/eval
plan is rejected, and **idea selection cannot proceed from an unvalidated scope contract** in bound mode. Then
compare baseline routes **attach / import / verify-local / reproduce / reject** (don't force one route) per
`comparability-contract`; for `idea`, run the **divergence→convergence** protocol (6–12 raw ideas across ≥2
mechanism families → 2–3 candidates), apply the **selection gate** (0/1/2 on
novelty/falsifiability/feasibility/evidence/fit; <7/10 ⇒ don't promote) and write a **pre-idea draft** + an
**objective contract** (primary objective · trusted proxies · **false-progress signals** · hard constraints)
before emitting a `selected` idea. Do a real related-work sweep (≥5 usable papers) and label novelty
`novel | incremental-but-valuable | not-differentiated`.

**Typed idea selection (MANDATORY — this is what gates idea → experiment; methodology usage is NOT
enough).** Write the typed selection to `runs/<q>/idea/select-<round>.json` — `objective_contract_ref`,
`baseline_contract_ref` (or an explicit waiver placeholder), `raw_slate[]` (each `candidate_id`/`title`/
`hypothesis`/`mechanism`/`expected_evidence`/`risk`), `challenge` (`strongest_rejection`,
`outside_family_alternative`, `why_retained_survives`), `novelty_risk` (`novelty_label`, `novelty_argument`,
`risk_notes`), `selection_gate[]` (per candidate 0/1/2 on novelty/falsifiability/feasibility/evidence_potential/
fit_to_objective + `total` + `verdict`), `rejected[]` (≥1, each with a concrete `reason`), and `retained`
(`candidate_id` from the slate, `hypothesis`, `mechanism`, `claim_candidate`, `mvp_experiment_plan`,
`expected_failure_mode`, `boundary_condition`) — then record `$HARNESS record apply --type idea.select`
(`select_ref`=that path) and **`$HARNESS idea validate --quest-id <q>`**. The validator enforces the
rigor floor (slate size + retained score) and rejects single-proposal / decorative (`not_differentiated`) /
below-floor / no-rejection / retained-not-in-slate / inconsistent-score selections. **The idea cannot advance
to an experiment handoff until `idea validate` passes** (the experiment-handoff idea gate reads the validator
flag, not the artifact's existence).

## experiment (experimenter, in YOUR isolated worktree)

**GPU gate FIRST** — run `$HARNESS gpu status --quest-id <q>`. If `confirmed=false`, you MUST NOT run anything
on a GPU: reply `status=failed` with `error="GPUs not operator-confirmed"` and stop (the orchestrator opening
this handoff is itself blocked apply-time, so this is a backstop). If confirmed, **restrict to the confirmed
devices** — prefer running every GPU command (kernel build/run, `ncu`, benchmark, any generated code)
**through** `$HARNESS experiment run --experiment-id <id> --quest-id <q> --cmd "<command>" [--cwd <worktree>]`,
which fails closed and injects `CUDA_VISIBLE_DEVICES=<confirmed devices>` for you; for direct runs,
`export CUDA_VISIBLE_DEVICES=<devices>` first. Never touch any GPU outside that set. `$HARNESS experiment run`
only EXECUTES the command (GPU-gated) and returns stdout/stderr — it writes no rows. YOU then record, via
`record apply`, `experiment.upsert` (status `done`, or `failed` on error — never `done` on failure),
`result.record`, `measurement.record` (mark the objective `is_primary`). If a BO point,
`experiment_param.record`. Then `$HARNESS git checkpoint`. Consult enabled domain knowledge with
`$HARNESS knowledge query` (e.g. the `science-scipkg` package-card catalog) when relevant.

**Method discipline (`research-method` pack):** lock a run contract before coding (hypothesis · baseline id ·
deciding metric keys · stop/abandon condition); climb the **evidence ladder** (minimum→solid→maximum,
significance testing whenever you claim superiority); never silently change a dataset/split/metric
definition/eval path; implement the *claimed* mechanism, not a shortcut. Record an `evaluation_summary`
(takeaway · claim_update · baseline_relation · comparability · failure_mode · next_action) in the result
artifact, and on failure classify it (data-contract / resource / numeric / implementation / evaluation /
direction). Stop re-running when a retry changes no hypothesis/code/command/evidence.

## analysis (analyst)

`--type analysis.record` (`confirms|blocks|inconclusive`); optional `$HARNESS claim link`. **When the result
space admits it, run an ablation / mechanism-isolation** (vary one factor — e.g. competing integration rules,
on/off of a component — holding constants fixed) and record it as its own `analysis.record` + a result table,
so the writer can present an ablation that *isolates the operative mechanism* (the single biggest rigor gap). **GPU gate applies to ablations too:** if an ablation re-runs anything on a GPU, the `analysis`
handoff is GPU-gated (same apply-time gate as `experiment`) — run `$HARNESS gpu status --quest-id <q>` first; if
`confirmed=false` do **not** touch a GPU (reply `status=failed`, `error="GPUs not operator-confirmed"`). When
confirmed, run GPU work through `$HARNESS experiment run --cmd ...` (injects `CUDA_VISIBLE_DEVICES`) or export
the confirmed `devices`; never use a device outside the confirmed set. Pure data-only analysis needs no GPU.

**Campaign discipline (`research-method` pack, campaign-design):** design slices in priority order
(claim-critical contradiction checks → robustness/sensitivity → failure-mode explanation → efficiency), vary
ONE factor at a time (don't change many and claim isolation), and **label** any slice that changes
dataset/split/protocol as generalization/stress-test (NOT apples-to-apples). Record a per-slice evidence
contract (research question · hypothesis · intervention · controls · metric · comparison target · stop
condition · comparability verdict · claim_update). Stop widening after two slices that don't move the claim
boundary; aim for ~5–10 paper-facing analysis groups for a mature paper.

**Tag evidence kind + PROOF (MANDATORY for coverage).** When you link evidence to a claim, set the typed
`evidence_kind` on `claim_evidence.link` — one of `baseline_comparison`/`main_result`/`ablation`/`robustness`/
`negative`/`efficiency`/`boundary`/`qualitative`/`significance`/`error_analysis` — AND attach structured
`evidence_proof`: a **label is not proof**. `campaign validate` will NOT count a kind without its required
proof keys: `main_result`/`baseline_comparison` {metric, direction}; `ablation` {changed_factor, controls,
delta, **parent_result** (a resolvable result_id)}; `robustness` {varied_condition, original_condition,
criterion}; `negative`/`boundary` {hypothesis, observed, implication}; `significance` {method, effect (test/
p-value/interval)}; `efficiency` {resource, metric, baseline}; `error_analysis` {error_category, subset,
implication}. Result-backed evidence ALSO needs `provenance_ok=1` (run `result validate`); `reference`/
`external` evidence needs an explicit `source`/`citation` and is never treated as local experimental proof.
Uncounted evidence is reported with a clear reason (e.g. `ablation evidence not counted: missing changed_factor`). **Analysis→paper bridge (MANDATORY — this is what gates
analysis → write; the Writer must NOT consume raw logs).** Write the typed bridge to
`runs/<q>/analysis/bridge-<round>.json` — `supported_claims`/`weakened_or_refuted_claims`,
`mechanism_interpretation`, `alternative_explanations`, `limitations`, `failure_modes`,
`recommended_claim_boundaries`, `figure_table_recommendations`, **`paper_facing_result_paragraphs`** (real
prose, not log dumps), `claim_to_evidence_map`, `evidence_to_section_recommendations` — record it with
`$HARNESS record apply --type analysis.bridge` (`bridge_ref`=that path) and **`$HARNESS campaign validate
--quest-id <q>`**. The validator checks the bridge is paper-facing AND that every main claim meets the rigor
coverage floor by `evidence_kind` (per-claim, not a global count). **The analysis cannot advance to an
outline/write handoff until `campaign validate` passes** (the gate reads the validator flag, not artifact
existence). This bridge is the writer's input and feeds the paper-spine (claim-evidence map, display plan,
weak points, follow-ups).

## outline (writer)

Build the paper outline — a **paper-view** (sectioned narrative: intro+contributions, method, setup, results,
ablation, analysis, related work, limitations) and an **evidence-view** (each planned claim → its supporting
analysis/result rows), with scoped claims, method abstraction, an evaluation/ablation plan, and evidence
boundaries. **Persist the typed paper-spine**: write `runs/<q>/paper/spine.json` (thesis,
core_contribution, central_mechanism, 1–3 `main_claims` each with `claim_id`/`scope`/`what_would_falsify_it`/
`evidence_needed`, `not_claiming`, `experiment_section_map` with a per-section thesis, `display_plan` linked to
claims, `reviewer_objections` mapped to evidence/follow-up, `weak_points`), then record it with
`$HARNESS record apply --type paper_spine.upsert` (`spine_ref`=that path) and **gate with `$HARNESS outline
validate --quest-id <q>`** (structural; it reads the spine row). **Fill the full
outline contract** (`paper-craft/references/outline-contract.md`): narrative_strategy, insight_ladder,
story_spine, positioning + novelty_boundary, 1–3 core claims each with **`what_would_falsify_it`**,
method_abstraction, an evaluation_plan + **4–8 analysis jobs**, **≥3 reviewer objections** each routed
(analysis/writing/claim_downgrade/limitation), and `evidence_grounding.must_not_claim`. Keep engineering detail
(worktrees, route decisions, batch arithmetic) OUT of paper_view.

## write (writer)

Produce a **publication-grade manuscript**, not a bare report. Target parity with a submittable systems paper
(abstract, intro + explicit contributions, background, method, setup, results, analysis/validation, related
work, limitations, conclusion, appendix). **Apply the `paper-craft` pack** (`$HARNESS knowledge cards`): the 20
oral-writing principles (write for reviewer cognition not compression; mandatory signposting; three-layer
results = pattern→anchor numbers→interpret, never just "which number is larger"; figures/tables carry values,
prose carries question+takeaway+mechanism), the **section-rewrite checklist**, and the evidence-budget rule
(spend main-text pages/displays where reviewer friction is highest; keep claim wording inside the
strongest-evidence zone). Never use polished language to conceal a missing result. Write the abstract last. To
compile against a real venue style, pass `--params '{"venue": "iclr2026"}'` to `render report` (see step 4;
default ML/AI venue is `iclr2026`). Steps:

1. **Figures** — for each headline result, emit a real figure from the recorded `result`/`measurement` data:
   write the series to a small CSV/JSON, then `$HARNESS render plot --input <data> --ref
   runs/<q>/figures/<name>.pdf --kind <scatter|bar|line>` (paper-plot → **matplotlib vector PDF** that embeds
   cleanly; **use `.pdf`, not `.svg`** — SVG needs an external converter at LaTeX time and silently drops the
   figure). At minimum a **predicted‑vs‑measured** figure (`--kind scatter`) and, when an ablation exists, an
   **ablation** figure (`--kind bar`). Reference them in the draft as `.pdf`. Each is an `artifact.record`
   (kind figure).
2. **Bibliography + related work (MANDATORY — scholarship bar, enforced at finalize).** Record **real external
   academic prior art** (papers / preprints / standards — not only tool/vendor docs) via
   `$HARNESS lit search`/`lit fetch` → `reference.record` (≥ the `min_refs` floor), then
   `$HARNESS lit bib --quest-id <q> --out runs/<q>/refs/references.bib`. Write a genuine **Related Work**
   section that *positions* this work against that prior art (how it differs/improves) — NOT an internal
   provenance note. Then **link ≥1 positioning claim to a reference** with `claim_evidence.link
   source_kind='reference'` (this is the enforced teeth). Self-check with `$HARNESS lit audit --quest-id <q>` —
   it must pass, or the finalize gate will reject `complete`. See `execplan/docs/publication-quality.md` for the
   bar.
3. **Assemble the Markdown draft** embedding the figures (`![](../figures/..pdf)`), result/ablation **tables**,
   and `\cite`/[@key] citations — asserting **only `supported` claims** (each traceable to a recorded
   analysis/result).
4. **Compile the paper** — `$HARNESS render report --input <draft.md> --ref runs/<q>/report/paper.pdf --bib
   runs/<q>/refs/references.bib --venue iclr2026` (paper-latex → LaTeX **+ compiled PDF**; `--bib` triggers a
   real **BibTeX** pass so `\cite` resolve into a numbered References section; `--venue` compiles against the
   venue style suite; figures referenced as `.pdf` embed via `\includegraphics`). Confirm the produced PDF
   actually embeds the figures + bibliography (size/pages should reflect them), not a text-only fallback. This
   replaces the old Markdown-only report.
4c. **Coverage gate (MANDATORY before reply/finalize).** Run `$HARNESS manuscript coverage --quest-id <q> --artifact-ref runs/<q>/report/paper.md --at <ts>`. It is **validator-computed** — you cannot self-certify readiness — and writes `submission_ready` onto the paper-spine. Resolve every reported gap (each main_claim linked to supporting evidence; no unmapped `result` rows; non-empty `not_claiming` + limitations/weak_points; each main claim stated in the prose; no process/draft traces). Finalize `complete` is **blocked** until this reports `submission_ready=true` (research-contract quests at standard/publication rigor).
4b. **Chinese edition (always produced)** — translate the assembled draft to Chinese as
   `runs/<q>/report/paper-zh.md`, **preserving** all tables, numbers, formulas, metric names, figure includes,
   file paths, citations, and keeping technical proper nouns in English (e.g. FlashAttention-4, Tensor-Core,
   B200, SASS/NCU). Then `$HARNESS render report --input runs/<q>/report/paper-zh.md --ref
   runs/<q>/report/paper-zh.pdf` — paper-latex auto-detects CJK and compiles with `ctexart`. Record both the EN
   and ZH PDFs via `artifact.record`. The deliverable is **bilingual** (`paper.pdf` + `paper-zh.pdf`).
5. Optional venue passes — `$HARNESS manuscript polish` (English) + `$HARNESS manuscript datastmt` (Data
   Availability); slides via `$HARNESS render slides`.
6. **Hygiene + bundle** — `$HARNESS manuscript validate` (language firewall), then `$HARNESS manuscript bundle
   --quest-id <q> --out-dir runs/<q>/report` to emit the evidence_ledger + claim_evidence_map +
   submission_checklist. Record every output via `artifact.record` (the compiled PDF as kind report). Report
   the `produced[]` set so the orchestrator's finalize gate can verify figures + compiled PDF + bib + bundle
   are present.

## review (reviewer)

Run `$HARNESS evidence validate` + `$HARNESS manuscript validate` (language hygiene: no
route/operator/worktree/prompt wording) + **`$HARNESS lit audit --quest-id <q>` (scholarship bar)**. Then a
**skeptical, adversarial pass**: write the review as **"objections raised → where answered"** (the strongest
3–5 objections a referee would make, each with the section/figure that answers it or a flagged gap), plus a
**reference audit** (every citation real, resolvable, and a genuine *external* academic source — not only
tool/vendor docs — with the Related Work *positioning* the work, not listing internal provenance) and a
**submission-checklist** confirmation (compiled PDF present, figures present, every supported claim has
evidence, no orphan claims — cross-check `runs/<q>/report/submission_checklist.md`). Record the review
(`--type artifact.record`, kind report, written to `runs/<q>/report/review/`); may flag a
`claim_evidence.resolve` / `claim.upsert` for the orchestrator to apply. **Apply the `review-craft` pack**
(`$HARNESS knowledge cards`): run the **Evidence Authenticity & Manuscript Coverage gate** (reconstruct an
experiment inventory from durable artifacts — not checklist labels; **recompute the real paper-facing result
count**; label each result current/stale/duplicate/failed/superseded and any fabrication risk: overclaim /
written-but-unsupported / contradiction); run the **literature-positioning benchmark** (a 3–8 paper comparator
set + novelty matrix); cover the **13 review dimensions**; and **route work correctly** — don't demand
experiments for a wording/positioning/claim-scope problem, don't demand rhetoric for a missing-evidence
problem. Produce the review-report / revision-log / experiment-todo artifacts (templates in the pack).
**Disposition** `accept` | `revise` | **`stop`/`branch` on a publishability or value collapse** (a low-quality
`stop` needs operator confirmation — flag a gated `decision`). **Block (`revise`, route to `write`) if `lit
audit` fails or scholarly positioning is missing**; `accept` only when the bundle is complete, `lit audit`
passes, and no supported claim is unsupported/contradicted.

**Typed verdict (MANDATORY — this is what binds finalize).** Write the typed verdict to
`runs/<q>/review/verdict-<round>.json` (`verdict` ∈ accept|borderline|reject, `summary`, and the flaw arrays
`fatal_flaws`/`missing_experiments`/`missing_analysis`/`overclaims`/`unsupported_claims`/`rewrite_requirements`,
`external_benchmark`, and **actionable** `experiment_todo`/`analysis_todo`/`rewrite_todo`, `routing_recommendation`),
then record `$HARNESS record apply --type review.verdict` (`verdict_ref`=that path). A borderline/reject verdict
**must** carry todos covering its flaws (missing_experiments→experiment_todo, missing_analysis→analysis_todo,
overclaims/unsupported_claims/rewrite_requirements→rewrite_todo) or the Orchestrator's `review validate` rejects
it as non-actionable. Finalize `complete` is **blocked** unless the latest verdict is a validated `accept`
(or operator-confirmed `borderline` at standard rigor) AND coverage is submission-ready.

## rebuttal (writer)

Map external-reviewer feedback into the smallest honest revision. **Apply the `rebuttal-craft` pack**
(`$HARNESS knowledge cards`): normalize the reviews into a **review-matrix** (atomic items with stable ids,
verbatim-clipped, classified + routed), an **action-plan** (per item: stance, route, why-sufficient,
MVP/Enhanced/fallback for experiment items), an **evidence-update**, and a **response-letter** written to the
letter **voice rules** (answer in the first 1–2 sentences; selectively concede/clarify/defend; 1–2 polished
paragraphs per item, no bullets inside responses; `[[AUTHOR TO FILL]]` placeholders, never invented results or
"we will add" promises). Manuscript deltas via `$HARNESS manuscript polish`; record the artifacts (`--type
artifact.record`, kind report) under `runs/<q>/report/rebuttal/`. Every supplementary run maps to a named
reviewer id — where reviewers demand new evidence, report it so the orchestrator records a `--type
decision.record` route to `experiment`/`analysis`.
