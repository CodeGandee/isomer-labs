---
name: deepresearch-shared-guide
description: Shared harness/comms usage conventions for every DeepResearch agent. Consult before any state read/write, mail send, or reply in the generated deepresearch loop.
---

# Shared Guide (all roles)

## Trigger

- A shared usage case: before any state access, record write, mail send, or reply in this loop.

## Inputs

- `$HARNESS` = the absolute harness path, exported as an env var on each launch profile (and recorded in `runs/prepared-workspace.md`). Invoke commands as `$HARNESS <group> <verb>`.
- The in-body `houmao-email-metadata` block of any received mail.
- Contracts: `specs/comms/templates.toml`, `specs/state/records/*.schema.json`, `specs/collab/topology/topology.toml`.

## Procedure (conventions)

1. **Read metadata first.** Parse the `houmao-email-metadata` block: `schema_id`, `loop_id` (= quest_id),
   `handoff_id`, `continuation_lane`, `round_index`, `from_role`, `to_role`. Reuse `loop_id` + `handoff_id`
   in every reply about that handoff.
2. **State only via harness.** Read with `$HARNESS state query` / `$HARNESS handoff query` / `$HARNESS wakeup list`.
   Write records with a JSON payload:
   `$HARNESS record apply --json '{"record_type":"<rt>","record_id":"<id>","at":"<iso8601>", <fields>}'`
   (validate first with `$HARNESS record validate --json '{...}'`). **`record apply` takes ONLY `--json`/`--file`**
   — there is no `--type` or per-field flag. NOTATION: throughout these skills a write shown as
   `record apply --type <rt> --<field> <val>` is shorthand for exactly that single JSON payload (the `--type`
   value is the `record_type` key; each `--field val` is a JSON key). **Dedicated verbs** (`handoff`, `wakeup`,
   `gpu`, `experiment`, `lit`, `email`, `render`, `bo`, …) instead take their OWN typed flags — run `<verb> --help`;
   they do NOT accept `--record-id` (e.g. `handoff advance --quest-id <q> --handoff-id <h> --status <s>`,
   `wakeup resolve --wakeup-id <id> --status <s>`). Never read or edit `runs/state.sqlite` directly.
3. **record_id convention.** Composite-PK record_ids are PK components joined with `:` (e.g. round =
   `<quest_id>:<round_index>`, handoff = `<quest_id>:<handoff_id>`, claim_evidence =
   `<claim_id>:<source_kind>:<source_ref>`). The parser is strict; build them exactly.
4. **Idempotency.** record_ids are deterministic, so re-applying the same record is a no-op. Before doing
   work for an inbound handoff, dedup with `$HARNESS handoff query --seen <handoff_id>`.
5. **Outgoing mail flow.** TOML payload → `$HARNESS email validate` → `$HARNESS email render` → deliver via
   `houmao-agent-email-comms`. Rendered mail carries the metadata block. Log lifecycle with
   `$HARNESS email apply` (bookkeeping only; the harness never delivers mail).
6. **Tree-loop.** Specialists always reply upstream to the Orchestrator; never bypass it. The Orchestrator
   owns the `handoff` ledger, `decision`/`finalize`, and the self-wakeup continuation.
7. **`--at` timestamps** are caller-supplied ISO-8601 on every mutating command.
8. **GPU-use is operator-gated, confirmed PRE-LOOP.** The operator confirms the allowed GPU devices during
   quest setup — a quest cannot reach `run_state=running` without a confirmed `gpu_allocation` (pre-loop
   start-gate). So during the live loop GPUs are already confirmed and the loop never re-prompts. GPU-using
   work — experiments, benchmarks, profiling, and analyst ablations — may only run on the confirmed devices;
   no `experiment`- OR `analysis`-stage handoff may open while unconfirmed (hard apply-time gate over both
   stages + invariant `experiment_requires_gpu_confirmation`). A single per-quest confirmation covers both
   stages. Only the operator confirms, via `$HARNESS gpu confirm`
   (operator-control). Prefer running GPU work through `$HARNESS experiment run --cmd ...`, which fails
   closed and injects `CUDA_VISIBLE_DEVICES=<confirmed devices>`; for direct runs, export the confirmed
   `devices`. Never use a GPU outside the confirmed set, and never self-confirm to unblock work.
9. **Every quest passes a MANDATORY pre-launch ambiguity check.** Before a quest can reach
   `run_state=running` it must have a recorded `kind='clarification'` artifact (pre-loop start-gate, fail-closed)
   — the operator-facing setup reviewed the objective across 7 dimensions (objective, acceptance, GPU, domain,
   workspace, budget, domain constraints) and either found no blocking ambiguity or folded the operator's
   clarifications into the objective/acceptance brief. By the time agents run, the brief is operator-confirmed;
   the loop does not re-prompt for clarification.
10. **TOTAL QUEST ISOLATION — never touch another quest.** Each quest is fully self-contained. You MUST NOT
    re-use, refer to, cite, or even inspect any artifact, data, finding, reference, code, or result from any
    other quest. Concretely: read/write only your own quest's `runs/<this-quest-id>/` tree (and your assigned
    worktree); never read a sibling `runs/<other-quest>/` or the q1-legacy `outputs/`; never pass another
    quest's `--quest-id` to a harness query and never use `findings query --all-quests` (operator-only).
    `findings query`/`lit query` return only your quest's rows; references and findings are quest-owned by
    schema + invariants (`finding_quest_owned`, `reference_quest_owned`). Collect every datum fresh for THIS
    quest, even if the objective matches a prior quest's. Prior quests are invisible to you.

## Research-quality disciplines (DeepScientist-lessons; all roles)

- **Living plan map (Phase 2):** `runs/<q>/plan.md` is a **rendered DB projection** (`$HARNESS plan render`),
  never authoritative and never read back as state — the DB is canonical. `plan status` prints it; `plan
  validate` runs plan checks + decision lint. The Orchestrator re-renders it at each round close.
- **Claim roles for completeness (Phase 5):** when recording a `claim.upsert`, set `kind` —
  `alternative`/`competing_hypothesis` for a rival explanation you intend to falsify, `limitation` for a
  documented scoped-out gap, else default `claim`. The Analyst records ablation/mechanism `analysis` rows and
  names the competing hypothesis (so `$HARNESS completeness audit` can see them).
- **Research-completeness (Phase 5):** `$HARNESS completeness audit --quest-id <q>` = the 7 scientific-quality
  checks (evidence traceability, no orphan claims, mechanism explanation, named alternatives, ablation-or-
  documented-infeasibility, lit audit, unresolved-discrepancy handling). In `auto`+`publication` it HARD-gates
  `complete`; otherwise advisory. The Reviewer blocks `revise` on a failing required item when the gate is hard.
- **Decisions name their losers (Phase 4):** a consequential `decision.record` chooses among ≥2 named
  candidates with non-winners marked + a Winner/Rejected-alternatives/Decisive-reason `rationale_ref`.
- **Frozen objective, amendable acceptance (Phase 6):** never edit `objective.md` post-launch (frozen) and
  never edit `acceptance.md` in place — acceptance changes only via the operator-confirmed, append-only
  `amend-acceptance` path (deepresearch-operator-control op 4b).

## Methodology references (ported from DeepScientist; read before stage work)

These are loop-wide research/writing **craft** packs (`kind='reference'`, enabled by default). Discover with
`$HARNESS knowledge query --kind reference` and list their files with `$HARNESS knowledge cards`; then READ
the named file under `execplan/packs/<pack>/references/...`. They are advisory craft, NEVER an authoritative
state surface (the DB stays canonical; record outcomes via `record apply`). Map any DeepScientist tool names
inside them (`artifact.*`, `bash_exec`, `memory.*`) to the `$HARNESS` surface.
- `ideation-rubric` — objective contract, selection gate, divergence/related-work playbooks, eval-contract + baseline-shortlist (scope/idea).
- `research-method` — evidence ladder, comparability contract, campaign design, decision/optimize/finalize methodology (baseline/experiment/analysis/decision).
- `paper-craft` — oral-writing principles, section-rewrite checklist, the paper-view/evidence-view outline contract (outline/write).
- `review-craft` — review dimensions, evidence-authenticity gate, literature benchmark, review templates (review).
- `rebuttal-craft` — review-matrix→action-plan→evidence-update→response-letter flow + voice rules (rebuttal).
- `intake-rubric` — trust-rank/reconcile pre-existing assets, current-board packet (intake-audit).

**Evidence ladder (shared vocabulary; from `research-method/references/evidence-ladder.md`).** Spend effort in
order, never out of order: `minimum` = the result is executable AND comparable to the baseline; `solid` = the
main comparison is credible — baseline strong + fair, results stable, and **significance testing is present
whenever superiority is claimed**; `maximum` = broaden/polish only AFTER the line is at least `solid`. Keep
`auxiliary/dev` evidence (params, diagnostics, mechanism) distinct from `main/test` (claim-carrying) evidence.

**Comparability contract (shared vocabulary; from `research-method/references/comparability-contract.md`).** A
comparison is trustworthy only when these are explicit: task identity · dataset identity · split contract ·
evaluation script/path · required metric keys · metric directions · source commit/package identity · known
deviations — with a verdict of `usable now | usable with caveats | blocked`. If downstream work would have to
*guess* the comparison contract, the baseline is not ready. Never silently change a dataset/split/metric
definition/eval path; a robustness slice that changes them must be LABELED generalization/stress-test, not
apples-to-apples.

## Methodology-usage audit (Tier-3; required, auditable)

Reading a pack is not optional for stages that have a **required pack**. Required packs by stage:

| stage | required pack(s) | cheap bound-output (Tier 4) | audited by |
|---|---|---|---|
| intake-audit | `intake-rubric` | trust-ranked intake_asset rows + current-board packet | worker |
| scope, idea | `ideation-rubric` | idea: a selection-gate score in the idea artifact | worker |
| baseline | `ideation-rubric` + `research-method` | comparability/eval-contract fields in the baseline artifact | worker |
| experiment, analysis | `research-method` | evaluation_summary / slice contract in the result/analysis artifact | worker |
| outline | `paper-craft` | `outline validate` passes | worker |
| write | `paper-craft` | `manuscript validate` passes | worker |
| review | `review-craft` | review-report + experiment-todo artifacts exist | worker |
| rebuttal | `rebuttal-craft` | response-letter artifact exists | worker |
| decision, optimize, finalize | `research-method` | the decision/frontier/finalize_outcome row | **Orchestrator (self-audit at round close)** |

EVERY stage now has a required pack. **Worker stages:** before replying `status=done` you MUST (1) consult the
pack via `$HARNESS knowledge cards`; (2) record an **`artifact(kind='methodology-usage')`** (quest-owned, with
`round_index`, `ref=runs/<q>/methodology/r<r>-<stage>.md`) naming the pack + cards applied and the bound
output; (3) report `methodology_used[]` `{pack, cards, applied_as}` in the task-result. **Orchestrator-internal
stages** (`decision`/`optimize`/`finalize`): the Orchestrator records the same methodology-usage artifact at
round close (no task-result — it is its own worker; see `deepresearch-orchestrator-tick` 5b). The compact
non-negotiable per-stage checklist lives in the **`deepresearch-on-task-request` body** ("Mandatory stage
checklists") so it is always in context even if the pack is never opened; the pack holds the depth. This is an
**audit overlay only — NOT authoritative over DB state** (the `result`/`claim`/`analysis` rows remain the
truth). The Orchestrator's on-task-result fold gates worker stages (re-dispatch in `auto`, operator-block in
`assistant`), and `$HARNESS plan validate` warns at round close when any closed required-pack round (worker OR
internal) has no methodology-usage artifact.

## Output

- No state change of its own; this skill is reference guidance other skills follow.

## Stop

- Not a turn-driving skill; return to the calling skill.
