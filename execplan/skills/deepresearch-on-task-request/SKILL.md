---
name: deepresearch-on-task-request
description: Specialist on-event skill for the deepresearch loop. Trigger on received mail with schema_id "deepresearch.email.task-request". Acknowledge, do the bounded work for your role + the requested stage, record durable rows, and reply upstream to the Orchestrator.
---

# On Task Request (specialist, role-aware)

**Trigger:** received mail, `schema_id = "deepresearch.email.task-request"`.

You are a specialist (Scout/Ideator, Experimenter, Analyst, Writer, or Reviewer). Do the work for YOUR
role and the request's `stage`, then reply to the Orchestrator. One bounded turn. See
`deepresearch-shared-guide`.

## Inputs

- The task-request payload: `stage`, `instructions_ref`, optional `branch_id` / `idea_id` /
  `experiment_id` / `run_contract_ref` / `inputs`; metadata `loop_id` + `handoff_id`.

## Procedure

1. Parse the metadata block; confirm `schema_id`. **Dedup:** `$HARNESS handoff query --seen <handoff_id>`
   — if already `processed`, archive the mail and stop.
2. **Send a receipt** (reuse `handoff_id`, set `reply_to_payload_id`): build the `deepresearch.email.receipt`
   payload (`accepted=true`), `$HARNESS email validate` → `render` → deliver to the Orchestrator via
   houmao-agent-email-comms; `$HARNESS email apply` (out). If you cannot take it, send `accepted=false` +
   `reason` and stop.
3. **Do the bounded work for `stage`** (record every durable row with `$HARNESS record apply`):
   - `intake-audit` (Scout/Ideator): inventory + trust-rank the pre-existing assets under the quest repo
     (`quest.workspace_ref`); record one `--type intake_asset.record` per asset (`trust`
     trusted|suspect|untrusted|rejected). For a trusted asset you recommend adopting, set `adopt_as` and
     report it so the Orchestrator adopts it (e.g. trusted baseline → `baseline_gate`, trusted results →
     `result.record`). Report a recommended next anchor; the Orchestrator records the `decision`. Report a
     **current-board packet** (current mainline · incumbent · latest decisive result · active blocker ·
     stale-routes-to-ignore · next-decision-scope) and, before recommending adoption of any pre-existing
     paper/draft asset, separate its role (legacy / comparator / negative-evidence / appendix / current) —
     do not adopt an old draft as current-method support. Don't confuse provenance (requests, branch names,
     logs) with manuscript content.
   - `scope` / `baseline` / `idea` (Scout/Ideator): `--type idea.upsert`; for baseline, write the
     comparator+metric contract as an artifact (`--type artifact.record`) **to the per-quest baseline path
     `runs/<q>/baseline/`** (canonical, read-only to the Experimenter thereafter — not the optional
     `shared/baseline/`) and report it (the Orchestrator sets `baseline_gate`). May `$HARNESS lit search/fetch`
     → `--type reference.record`. **Use the `ideation-rubric` pack** (`$HARNESS knowledge cards`): for `scope`,
     fill the **eval-contract** (task · dataset · split · official eval path · primary metric + direction ·
     fair-comparison rule · useful-improvement threshold) and compare baseline routes **attach / import /
     verify-local / reproduce / reject** (don't force one route) per `comparability-contract`; for `idea`, run
     the **divergence→convergence** protocol (6–12 raw ideas across ≥2 mechanism families → 2–3 candidates),
     apply the **selection gate** (0/1/2 on novelty/falsifiability/feasibility/evidence/fit; <7/10 ⇒ don't
     promote) and write a **pre-idea draft** + an **objective contract** (primary objective · trusted proxies ·
     **false-progress signals** · hard constraints) before emitting a `selected` idea. Do a real related-work
     sweep (≥5 usable papers) and label novelty `novel | incremental-but-valuable | not-differentiated`.
   - `experiment` (Experimenter, in YOUR isolated worktree): **GPU gate FIRST** — run
     `$HARNESS gpu status --quest-id <q>`. If `confirmed=false`, you MUST NOT run anything on a GPU:
     reply `status=failed` with `error="GPUs not operator-confirmed"` and stop (the Orchestrator opening
     this handoff is itself blocked apply-time, so this is a backstop). If confirmed, **restrict to the
     confirmed devices** — prefer running every GPU command (kernel build/run, `ncu`, benchmark, any
     generated code) **through** `$HARNESS experiment run --experiment-id <id> --quest-id <q> --cmd "<command>"
     [--cwd <worktree>]`, which fails closed and injects `CUDA_VISIBLE_DEVICES=<confirmed devices>` for you;
     for direct runs, `export CUDA_VISIBLE_DEVICES=<devices>` first. Never touch any GPU outside that set.
     `$HARNESS experiment run` only EXECUTES the command (GPU-gated) and returns stdout/stderr — it writes no
     rows. YOU then record, via `record apply`,
     `experiment.upsert` (status `done`, or `failed` on error — never `done` on failure),
     `result.record`, `measurement.record` (mark the objective `is_primary`). If a BO point,
     `experiment_param.record`. Then `$HARNESS git checkpoint`. Consult enabled domain knowledge
     with `$HARNESS knowledge query` (e.g. the `science-scipkg` package-card catalog) when relevant.
     **Method discipline (`research-method` pack):** lock a run contract before coding (hypothesis · baseline
     id · deciding metric keys · stop/abandon condition); climb the **evidence ladder** (minimum→solid→maximum,
     significance testing whenever you claim superiority); never silently change a dataset/split/metric
     definition/eval path; implement the *claimed* mechanism, not a shortcut. Record an `evaluation_summary`
     (takeaway · claim_update · baseline_relation · comparability · failure_mode · next_action) in the result
     artifact, and on failure classify it (data-contract / resource / numeric / implementation / evaluation /
     direction). Stop re-running when a retry changes no hypothesis/code/command/evidence.
   - `analysis` (Analyst): `--type analysis.record` (`confirms|blocks|inconclusive`); optional
     `$HARNESS claim link`. **When the result space admits it, run an ablation / mechanism-isolation**
     (vary one factor — e.g. competing integration rules, on/off of a component — holding constants fixed)
     and record it as its own `analysis.record` + a result table, so the Writer can present an ablation that
     *isolates the operative mechanism* (the single biggest rigor gap vs. DeepScientist). **GPU gate applies
     to ablations too:** if an ablation re-runs anything on a GPU, the `analysis` handoff is GPU-gated (same
     apply-time gate as `experiment`) — run `$HARNESS gpu status --quest-id <q>` first; if `confirmed=false`
     do **not** touch a GPU (reply `status=failed`, `error="GPUs not operator-confirmed"`). When confirmed,
     run GPU work through `$HARNESS experiment run --cmd ...` (injects `CUDA_VISIBLE_DEVICES`) or export the
     confirmed `devices`; never use a device outside the confirmed set. Pure data-only analysis needs no GPU.
     **Campaign discipline (`research-method` pack, campaign-design):** design slices in priority order
     (claim-critical contradiction checks → robustness/sensitivity → failure-mode explanation → efficiency),
     vary ONE factor at a time (don't change many and claim isolation), and **label** any slice that changes
     dataset/split/protocol as generalization/stress-test (NOT apples-to-apples). Record a per-slice evidence
     contract (research question · hypothesis · intervention · controls · metric · comparison target · stop
     condition · comparability verdict · claim_update). Stop widening after two slices that don't move the
     claim boundary; aim for ~5–10 paper-facing analysis groups for a mature paper.
   - `outline` (Writer): build the paper outline — a **paper-view** (sectioned narrative: intro+contributions,
     method, setup, results, ablation, analysis, related work, limitations) and an **evidence-view** (each
     planned claim → its supporting analysis/result rows), with scoped claims, method abstraction, an
     evaluation/ablation plan, and evidence boundaries → `--type artifact.record` (kind report); gate with
     `$HARNESS outline validate`. **Fill the full outline contract** (`paper-craft/references/outline-contract.md`):
     narrative_strategy, insight_ladder, story_spine, positioning + novelty_boundary, 1–3 core claims each with
     **`what_would_falsify_it`**, method_abstraction, an evaluation_plan + **4–8 analysis jobs**, **≥3 reviewer
     objections** each routed (analysis/writing/claim_downgrade/limitation), and `evidence_grounding.must_not_claim`.
     Keep engineering detail (worktrees, route decisions, batch arithmetic) OUT of paper_view.
   - `write` (Writer): produce a **publication-grade manuscript**, not a bare report. Target parity with a
     submittable systems paper (abstract, intro + explicit contributions, background, method, setup, results,
     analysis/validation, related work, limitations, conclusion, appendix). **Apply the `paper-craft` pack**
     (`$HARNESS knowledge cards`): the 20 oral-writing principles (write for reviewer cognition not compression;
     mandatory signposting; three-layer results = pattern→anchor numbers→interpret, never just "which number is
     larger"; figures/tables carry values, prose carries question+takeaway+mechanism), the **section-rewrite
     checklist**, and the evidence-budget rule (spend main-text pages/displays where reviewer friction is
     highest; keep claim wording inside the strongest-evidence zone). Never use polished language to conceal a
     missing result. Write the abstract last. To compile against a real venue style, pass `--params '{"venue":
     "iclr2026"}'` to `render report` (see step 4; default ML/AI venue is `iclr2026`). Steps:
     1. **Figures** — for each headline result, emit a real figure from the recorded `result`/`measurement`
        data: write the series to a small CSV/JSON, then `$HARNESS render plot --input <data> --ref
        runs/<q>/figures/<name>.svg` (paper-plot). At minimum a **predicted‑vs‑measured** figure and, when an
        ablation exists, an **ablation** figure. Each is an `artifact.record` (kind figure).
     2. **Bibliography + related work (MANDATORY — scholarship bar, enforced at finalize).** Record **real
        external academic prior art** (papers / preprints / standards — not only tool/vendor docs) via
        `$HARNESS lit search`/`lit fetch` → `reference.record` (≥ the `min_refs` floor), then
        `$HARNESS lit bib --quest-id <q> --out runs/<q>/refs/references.bib`. Write a genuine **Related Work**
        section that *positions* this work against that prior art (how it differs/improves) — NOT an internal
        provenance note. Then **link ≥1 positioning claim to a reference** with
        `claim_evidence.link source_kind='reference'` (this is the enforced teeth). Self-check with
        `$HARNESS lit audit --quest-id <q>` — it must pass, or the finalize gate will reject `complete`. See
        `execplan/docs/publication-quality.md` for the bar.
     3. **Assemble the Markdown draft** embedding the figures (`![](../figures/..svg)`), result/ablation
        **tables**, and `\cite`/[@key] citations — asserting **only `supported` claims** (each traceable to a
        recorded analysis/result).
     4. **Compile the paper** — `$HARNESS render report --input <draft.md> --ref runs/<q>/report/paper.pdf`
        (paper-latex → LaTeX **+ compiled PDF**; pass the bib via params when supported). This replaces the
        old Markdown-only report.
     4b. **Chinese edition (always produced)** — translate the assembled draft to Chinese as
        `runs/<q>/report/paper-zh.md`, **preserving** all tables, numbers, formulas, metric names, figure
        includes, file paths, citations, and keeping technical proper nouns in English (e.g. FlashAttention-4,
        Tensor-Core, B200, SASS/NCU). Then `$HARNESS render report --input runs/<q>/report/paper-zh.md --ref
        runs/<q>/report/paper-zh.pdf` — paper-latex auto-detects CJK and compiles with `ctexart`. Record both
        the EN and ZH PDFs via `artifact.record`. The deliverable is **bilingual** (`paper.pdf` + `paper-zh.pdf`).
     5. Optional venue passes — `$HARNESS manuscript polish` (English) + `$HARNESS manuscript datastmt`
        (Data Availability); slides via `$HARNESS render slides`.
     6. **Hygiene + bundle** — `$HARNESS manuscript validate` (language firewall), then
        `$HARNESS manuscript bundle --quest-id <q> --out-dir runs/<q>/report` to emit the
        evidence_ledger + claim_evidence_map + submission_checklist. Record every output via `artifact.record`
        (the compiled PDF as kind report). Report the `produced[]` set so the Orchestrator's finalize gate can
        verify figures + compiled PDF + bib + bundle are present.
   - `review` (Reviewer): run `$HARNESS evidence validate` + `$HARNESS manuscript validate` (language hygiene:
     no route/operator/worktree/prompt wording) + **`$HARNESS lit audit --quest-id <q>` (scholarship bar)**.
     Then a **skeptical, adversarial pass**: write the review as **"objections raised → where answered"** (the
     strongest 3–5 objections a referee would make, each with the section/figure that answers it or a flagged
     gap), plus a **reference audit** (every citation real, resolvable, and a genuine *external* academic
     source — not only tool/vendor docs — with the Related Work *positioning* the work, not listing internal
     provenance) and a **submission-checklist** confirmation (compiled PDF present, figures present, every
     supported claim has evidence, no orphan claims — cross-check `runs/<q>/report/submission_checklist.md`).
     Record the review (`--type artifact.record`, kind report, written to `runs/<q>/report/review/`); may flag a
     `claim_evidence.resolve` / `claim.upsert` for the Orchestrator to apply. **Apply the `review-craft` pack**
     (`$HARNESS knowledge cards`): run the **Evidence Authenticity & Manuscript Coverage gate** (reconstruct an
     experiment inventory from durable artifacts — not checklist labels; **recompute the real paper-facing result
     count**; label each result current/stale/duplicate/failed/superseded and any fabrication risk:
     overclaim / written-but-unsupported / contradiction); run the **literature-positioning benchmark** (a 3–8
     paper comparator set + novelty matrix); cover the **13 review dimensions**; and **route work correctly** —
     don't demand experiments for a wording/positioning/claim-scope problem, don't demand rhetoric for a
     missing-evidence problem. Produce the review-report / revision-log / experiment-todo artifacts (templates in
     the pack). **Disposition** `accept` | `revise` | **`stop`/`branch` on a publishability or value collapse**
     (a low-quality `stop` needs operator confirmation — flag a gated `decision`). **Block (`revise`, route to
     `write`) if `lit audit` fails or scholarly positioning is missing**; `accept` only when the bundle is
     complete, `lit audit` passes, and no supported claim is unsupported/contradicted.
   - `rebuttal` (Writer): map external-reviewer feedback into the smallest honest revision. **Apply the
     `rebuttal-craft` pack** (`$HARNESS knowledge cards`): normalize the reviews into a **review-matrix** (atomic
     items with stable ids, verbatim-clipped, classified + routed), an **action-plan** (per item: stance, route,
     why-sufficient, MVP/Enhanced/fallback for experiment items), an **evidence-update**, and a **response-letter**
     written to the letter **voice rules** (answer in the first 1–2 sentences; selectively concede/clarify/defend;
     1–2 polished paragraphs per item, no bullets inside responses; `[[AUTHOR TO FILL]]` placeholders, never
     invented results or "we will add" promises). Manuscript deltas via `$HARNESS manuscript polish`; record the
     artifacts (`--type artifact.record`, kind report) under `runs/<q>/report/rebuttal/`. Every supplementary run
     maps to a named reviewer id — where reviewers demand new evidence, report it so the Orchestrator records a
     `--type decision.record` route to `experiment`/`analysis`.
3b. **Methodology usage (MANDATORY before `status=done` for any stage with a required pack).** The required
   packs by worker stage are: `intake-audit` → `intake-rubric`; `scope`/`idea` → `ideation-rubric`;
   `baseline` → `ideation-rubric` + `research-method`; `experiment`/`analysis` → `research-method`;
   `outline`/`write` → `paper-craft`; `review` → `review-craft`; `rebuttal` → `rebuttal-craft`. (The
   orchestrator-internal stages `decision`/`optimize`/`finalize` also require `research-method` but are
   self-audited by the Orchestrator at round close — see `deepresearch-orchestrator-tick` — not here.)
   For your stage you MUST:
   - **Consult** the pack(s) via `$HARNESS knowledge cards` (or `knowledge query`) and read the relevant card files.
   - **Record an audit artifact**: `$HARNESS record apply --type artifact.record` with `kind='methodology-usage'`,
     `round_index=<r>`, and `ref=runs/<q>/methodology/r<r>-<stage>.md` — a short note listing the pack + card
     files you applied and the **bound output** (the durable row/artifact that embodies the methodology). This
     artifact is quest-owned and is an audit record only; it is NOT authoritative over the DB rows.
   - **Report `methodology_used[]`** in the task-result: one item per required pack `{pack, cards:[...],
     applied_as:<bound-output ref>}`.
   - **Bound-output (Tier 4) — produce the prescribed output, not just a citation:**
     `idea` → a selection-gate score recorded in the idea artifact (`applied_as` points at it);
     `outline` → `$HARNESS outline validate --artifact-ref <outline>` must PASS;
     `write` → `$HARNESS manuscript validate --artifact-ref <paper.md>` must PASS;
     `review` → the review-report + experiment-todo artifacts exist.
   Do not send `status=done` until the required methodology-usage artifact exists and `methodology_used[]` is
   populated; if you genuinely could not apply a pack, send `status=failed` + `error` explaining why.
4. **Reply with a task-result** (`deepresearch.email.task-result`, reuse `handoff_id`): `status=done` with
   `produced[]` listing the rows you recorded **and `methodology_used[]`** (per 3b), or `status=failed` +
   `error`. Validate → render → deliver to the Orchestrator; `$HARNESS email apply` (out).
5. Archive the task-request on success.

## Mandatory stage checklists (in-context; the pack holds the depth)

These are the **non-negotiable** items per stage — satisfy every one before `status=done`. They live here in
the skill body so the core discipline is always loaded even if you never open the pack; the named pack
(`$HARNESS knowledge cards`) carries the full method, templates, and examples. Record the bound output as a
durable row/artifact and cite it in `methodology_used[].applied_as` (per 3b).

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

- A receipt, then a task-result, to the Orchestrator; durable rows recorded via `$HARNESS record apply`.

## Stop

- End the turn after one task-request. Result validation, gate-setting, best-result selection, and routing
  are the Orchestrator's job.
