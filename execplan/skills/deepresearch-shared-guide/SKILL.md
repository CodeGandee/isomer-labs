---
name: deepresearch-shared-guide
description: Shared harness/comms usage conventions for every deepresearch agent. Consult before any state read/write, mail send, or reply in the generated deepresearch loop.
---

# Shared Guide (all roles)

## Trigger

- A shared usage case: before any state access, record write, mail send, or reply in the loop.

## Inputs

- `$HARNESS` = the absolute harness path, exported as an env var on each launch profile (and recorded in
  `runs/prepared-workspace.md`). Invoke commands as `$HARNESS <group> <verb>`.
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
6. **Tree-loop.** Specialists always reply upstream to the orchestrator; never bypass it. The orchestrator
   owns the `handoff` ledger, `decision`/`finalize`, and the self-wakeup continuation.
7. **`--at` timestamps** are caller-supplied ISO-8601 on every mutating command.
8. **GPU-use is operator-gated, confirmed PRE-LOOP.** The operator confirms the allowed GPU devices during
   quest setup — a quest cannot reach `run_state=running` without a confirmed `gpu_allocation` (pre-loop
   start-gate). So during the live loop GPUs are already confirmed and the loop never re-prompts. GPU-using
   work — experiments, benchmarks, profiling, and analyst ablations — may only run on the confirmed devices;
   no `experiment`- OR `analysis`-stage handoff may open while unconfirmed (hard apply-time gate over both
   stages + invariant `experiment_requires_gpu_confirmation`). A single per-quest confirmation covers both
   stages. Only the operator confirms, via `$HARNESS gpu confirm` (operator-control). Prefer running GPU work
   through `$HARNESS experiment run --cmd ...`, which fails closed and injects
   `CUDA_VISIBLE_DEVICES=<confirmed devices>`; for direct runs, export the confirmed `devices`. Never use a GPU
   outside the confirmed set, and never self-confirm to unblock work.
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

## Research-quality disciplines (extended-lessons; all roles)

- **Living plan map:** `runs/<q>/plan.md` is a **rendered DB projection** (`$HARNESS plan render`),
  never authoritative and never read back as state — the DB is canonical. `plan status` prints it; `plan
  validate` runs plan checks + decision lint. The orchestrator re-renders it at each round close.
- **Claim roles for completeness:** when recording a `claim.upsert`, set `kind` —
  `alternative`/`competing_hypothesis` for a rival explanation you intend to falsify, `limitation` for a
  documented scoped-out gap, else default `claim`. The analyst records ablation/mechanism `analysis` rows and
  names the competing hypothesis (so `$HARNESS completeness audit` can see them).
- **Research-completeness:** `$HARNESS completeness audit --quest-id <q>` = the 7 scientific-quality
  checks (evidence traceability, no orphan claims, mechanism explanation, named alternatives, ablation-or-
  documented-infeasibility, lit audit, unresolved-discrepancy handling). In `auto`+`publication` it HARD-gates
  `complete`; otherwise advisory. The reviewer blocks `revise` on a failing required item when the gate is hard.
- **Decisions name their losers:** a consequential `decision.record` chooses among ≥2 named
  candidates with non-winners marked + a Winner/Rejected-alternatives/Decisive-reason `rationale_ref`.
- **Frozen objective, amendable acceptance:** never edit `objective.md` post-launch (frozen) and
  never edit `acceptance.md` in place — acceptance changes only via the operator-confirmed, append-only
  `amend-acceptance` path (deepresearch-operator-control op 4b).

## Methodology references + usage audit

Loop-wide research/writing **craft** packs
back every stage. Worker-stage methodology is **binding**: it must be applied through the stage's typed record +
validator (`methodology check` resolves `methodology_used[].applied_as` to it), while orchestrator-internal
stages use an advisory `methodology-usage` artifact. The full pack catalog, the evidence-ladder +
comparability-contract shared vocabulary, and the required-pack-by-stage binding table live in
**`reference/methodology.md`** — read it before stage work.

## Output

- No state change of its own; this skill is reference guidance other skills follow.

## Stop

- Not a turn-driving skill; return to the calling skill.
