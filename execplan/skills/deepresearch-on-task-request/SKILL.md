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
     `result.record`). Report a recommended next anchor; the Orchestrator records the `decision`.
   - `scope` / `baseline` / `idea` (Scout/Ideator): `--type idea.upsert`; for baseline, write the
     comparator+metric contract as an artifact (`--type artifact.record`) **to the per-quest baseline path
     `runs/<q>/baseline/`** (canonical, read-only to the Experimenter thereafter — not the optional
     `shared/baseline/`) and report it (the Orchestrator sets `baseline_gate`). May `$HARNESS lit search/fetch`
     → `--type reference.record`.
   - `experiment` (Experimenter, in YOUR isolated worktree): **GPU gate FIRST** — run
     `$HARNESS gpu status --quest-id <q>`. If `confirmed=false`, you MUST NOT run anything on a GPU:
     reply `status=failed` with `error="GPUs not operator-confirmed"` and stop (the Orchestrator opening
     this handoff is itself blocked apply-time, so this is a backstop). If confirmed, **restrict to the
     confirmed devices** — prefer running every GPU command (kernel build/run, `ncu`, benchmark, any
     generated code) **through** `$HARNESS experiment run --experiment-id <id> --quest-id <q> --cmd "<command>"
     [--cwd <worktree>]`, which fails closed and injects `CUDA_VISIBLE_DEVICES=<confirmed devices>` for you;
     for direct runs, `export CUDA_VISIBLE_DEVICES=<devices>` first. Never touch any GPU outside that set.
     `$HARNESS experiment run` also records
     `--type experiment.upsert` (status `done`, or `failed` on error — never `done` on failure),
     `--type result.record`, `--type measurement.record` (mark the objective `is_primary`). If a BO point,
     `--type experiment_param.record`. Then `$HARNESS git checkpoint`. Consult enabled domain knowledge
     with `$HARNESS knowledge query` (e.g. the `science-scipkg` package-card catalog) when relevant.
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
   - `outline` (Writer): build the paper outline — a **paper-view** (sectioned narrative: intro+contributions,
     method, setup, results, ablation, analysis, related work, limitations) and an **evidence-view** (each
     planned claim → its supporting analysis/result rows), with scoped claims, method abstraction, an
     evaluation/ablation plan, and evidence boundaries → `--type artifact.record` (kind report); gate with
     `$HARNESS outline validate`.
   - `write` (Writer): produce a **publication-grade manuscript**, not a bare report. Target parity with a
     submittable systems paper (abstract, intro + explicit contributions, background, method, setup, results,
     analysis/validation, related work, limitations, conclusion, appendix). Steps:
     1. **Figures** — for each headline result, emit a real figure from the recorded `result`/`measurement`
        data: write the series to a small CSV/JSON, then `$HARNESS render plot --input <data> --ref
        runs/<q>/figures/<name>.svg` (paper-plot). At minimum a **predicted‑vs‑measured** figure and, when an
        ablation exists, an **ablation** figure. Each is an `artifact.record` (kind figure).
     2. **Bibliography + related work** — record prior art with `$HARNESS lit search`/`lit fetch` →
        `reference.record`, then `$HARNESS lit bib --quest-id <q> --out runs/<q>/refs/references.bib`. Write a
        Related Work section that cites them.
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
     no route/operator/worktree/prompt wording). Then a **skeptical, adversarial pass**: write the review as
     **"objections raised → where answered"** (the strongest 3–5 objections a referee would make, each with
     the section/figure that answers it or a flagged gap), plus a **reference audit** (every citation real &
     resolvable) and a **submission-checklist** confirmation (compiled PDF present, figures present, every
     supported claim has evidence, no orphan claims — cross-check `runs/<q>/report/submission_checklist.md`).
     Record the review (`--type artifact.record`, kind report, written to `runs/<q>/report/review/`); may flag a
     `claim_evidence.resolve` / `claim.upsert` for the Orchestrator to apply. Disposition accept only when the
     bundle is complete and no supported claim is unsupported/contradicted.
   - `rebuttal` (Writer): map external-reviewer feedback into the smallest honest revision — manuscript
     deltas (`$HARNESS manuscript polish`) + a response artifact (`--type artifact.record`, kind report);
     where reviewers demand new evidence, report it so the Orchestrator records a `--type decision.record`
     route to `experiment`/`analysis`.
4. **Reply with a task-result** (`deepresearch.email.task-result`, reuse `handoff_id`): `status=done` with
   `produced[]` listing the rows you recorded, or `status=failed` + `error`. Validate → render → deliver to
   the Orchestrator; `$HARNESS email apply` (out).
5. Archive the task-request on success.

## Output

- A receipt, then a task-result, to the Orchestrator; durable rows recorded via `$HARNESS record apply`.

## Stop

- End the turn after one task-request. Result validation, gate-setting, best-result selection, and routing
  are the Orchestrator's job.
