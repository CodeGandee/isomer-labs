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
     comparator+metric contract as an artifact (`--type artifact.record`) and report it (the Orchestrator
     sets `baseline_gate`). May `$HARNESS lit search/fetch` → `--type reference.record`.
   - `experiment` (Experimenter, in YOUR isolated worktree): `$HARNESS experiment run` → it records
     `--type experiment.upsert` (status `done`, or `failed` on error — never `done` on failure),
     `--type result.record`, `--type measurement.record` (mark the objective `is_primary`). If a BO point,
     `--type experiment_param.record`. Then `$HARNESS git checkpoint`. Consult enabled domain knowledge
     with `$HARNESS knowledge query` (e.g. the `science-scipkg` package-card catalog) when relevant.
   - `analysis` (Analyst): `--type analysis.record` (`confirms|blocks|inconclusive`); optional
     `$HARNESS claim link`.
   - `outline` (Writer): build the paper outline (paper-view vs evidence-view, scoped claims, method
     abstraction, evaluation/analysis plan, evidence boundaries) → `--type artifact.record` (kind report);
     gate with `$HARNESS outline validate`.
   - `write` (Writer): draft from `supported` claims via `$HARNESS render report`; figures via
     `$HARNESS render plot` / `$HARNESS render polish`; optional venue prose via `$HARNESS manuscript polish`
     and a Data Availability statement via `$HARNESS manuscript datastmt`; slides via `$HARNESS render slides`.
     Check hygiene with `$HARNESS manuscript validate`. Records `--type artifact.record`; only assert `supported` claims.
   - `review` (Reviewer): `$HARNESS evidence validate` + `$HARNESS manuscript validate` (language hygiene:
     no route/operator/worktree/prompt wording); `--type artifact.record` (review notes); may flag a
     `claim_evidence.resolve` / `claim.upsert` for the Orchestrator to apply.
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
