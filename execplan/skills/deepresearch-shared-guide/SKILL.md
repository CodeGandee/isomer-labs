---
name: deepresearch-shared-guide
description: Use when any deepresearch loop agent (orchestrator or specialist; any role) is about to read or write state, send or reply to mail, build a record_id, run GPU work, or close a round. Covers $HARNESS state/handoff/wakeup/record/email/gpu/plan/completeness/methodology usage, houmao-email-metadata blocks, schema_id/loop_id/handoff_id conventions, quest isolation, GPU operator-gating, ambiguity start-gate, research-quality gates.
---

# Shared Guide (all roles, deepresearch loop)

## Overview

Shared harness and comms conventions every deepresearch agent must apply before touching shared state. This is reference guidance other skills follow; it drives no turn of its own and changes no state. Consult it before any state read/write, mail send, reply, record_id construction, GPU run, or round close.

## When to Use

Use whenever, in the generated deepresearch loop, you are about to:
- read or write state (`$HARNESS state/handoff/wakeup/record ...`), or build any `record_id`;
- send, render, validate, or reply to mail (parse a `houmao-email-metadata` block);
- run GPU work (experiments, benchmarks, profiling, analyst ablations);
- record claims/decisions/analyses, render the plan, or close a round.

**When NOT to use:** this is not a turn-driving skill — do not invoke it to "do" a stage. It carries no role-specific procedure; the actual stage work lives in the role/event skill. Do not use it to justify touching another quest's data (quest isolation is absolute — see Common Mistakes) or to self-confirm a GPU allocation. Return to the calling skill after consulting.

## Inputs

- `$HARNESS` = the absolute harness path, exported as an env var on each launch profile (and recorded in `runs/prepared-workspace.md`). Invoke commands as `$HARNESS <group> <verb>`.
- The in-body `houmao-email-metadata` block of any received mail.
- Contracts: `specs/comms/templates.toml`, `specs/state/records/*.schema.json`, `specs/collab/topology/topology.toml`.

## Workflow

Ordered conventions to apply before any state read/write or mail action. Each is concise; gate-heavy details live in the named sections below.

1. **Read metadata first.** Parse the inbound mail's `houmao-email-metadata` block: `schema_id`, `loop_id` (= quest_id), `handoff_id`, `continuation_lane`, `round_index`, `from_role`, `to_role`. Reuse `loop_id` + `handoff_id` in every reply about that handoff.
2. **Dedup before working.** record_ids are deterministic so re-applying is a no-op; before doing work for an inbound handoff, dedup with `$HARNESS handoff query --seen <handoff_id>`.
3. **Touch state only via harness.** Read with `$HARNESS state query` / `$HARNESS handoff query` / `$HARNESS wakeup list`. Write records using the JSON-payload contract in [State writes](#state-writes-via-harness-only). Never read or edit `runs/state.sqlite` directly.
4. **Build record_ids exactly.** Composite-PK ids join PK components with `:` — see [record_id convention](#record_id-convention). The parser is strict.
5. **Respect quest isolation.** Read/write only your own quest's `runs/<this-quest-id>/` tree (and your assigned worktree). Never inspect, cite, or reuse another quest — see [Quest isolation](#quest-isolation-absolute).
6. **Check GPU gating before GPU work.** GPU use is operator-confirmed pre-loop; never self-confirm and never run outside the confirmed device set — see [GPU gating](#gpu-gating-operator-confirmed-pre-loop).
7. **Send mail through the flow.** TOML payload → `$HARNESS email validate` → `$HARNESS email render` → deliver via `houmao-agent-email-comms`; log lifecycle with `$HARNESS email apply` — see [Outgoing mail flow](#outgoing-mail-flow).
8. **Reply upstream (tree-loop).** Specialists always reply upstream to the orchestrator; never bypass it. The orchestrator owns the `handoff` ledger, `decision`/`finalize`, and the self-wakeup continuation.
9. **Stamp `--at`.** Every mutating command takes a caller-supplied ISO-8601 `--at` timestamp.
10. **Apply research-quality disciplines** when recording claims/decisions/analyses or closing a round — living plan map, claim roles, completeness audit, decisions-name-losers, frozen-objective/amendable-acceptance — see [Research-quality disciplines](#research-quality-disciplines).
11. **Apply binding methodology** for stage work: consult the stage's required pack and produce its typed record + validator before `status=done`. Read [`references/methodology.md`](references/methodology.md) before any stage work.

If the task does not map cleanly to these steps, use your native planning tool to build a plan from the commands and constraints in this skill, then execute it.

## State writes via harness only

Write records with a JSON payload:

```
$HARNESS record apply --json '{"record_type":"<rt>","record_id":"<id>","at":"<iso8601>", <fields>}'
```

Validate first with `$HARNESS record validate --json '{...}'`. **`record apply` takes ONLY `--json`/`--file`** — there is no `--type` or per-field flag.

**NOTATION:** throughout these skills a write shown as `record apply --type <rt> --<field> <val>` is shorthand for exactly that single JSON payload (the `--type` value is the `record_type` key; each `--field val` is a JSON key).

**Dedicated verbs** (`handoff`, `wakeup`, `gpu`, `experiment`, `lit`, `email`, `render`, `bo`, …) instead take their OWN typed flags — run `<verb> --help`; they do NOT accept `--record-id`. Examples:
- `handoff advance --quest-id <q> --handoff-id <h> --status <s>`
- `wakeup resolve --wakeup-id <id> --status <s>`

Never read or edit `runs/state.sqlite` directly.

## record_id convention

Composite-PK record_ids are PK components joined with `:`. The parser is strict; build them exactly:
- round = `<quest_id>:<round_index>`
- handoff = `<quest_id>:<handoff_id>`
- claim_evidence = `<claim_id>:<source_kind>:<source_ref>`

Because record_ids are deterministic, re-applying the same record is a no-op (idempotent).

## Outgoing mail flow

TOML payload → `$HARNESS email validate` → `$HARNESS email render` → deliver via `houmao-agent-email-comms`. Rendered mail carries the metadata block. Log lifecycle with `$HARNESS email apply` (bookkeeping only; **the harness never delivers mail** — delivery is the email-comms skill's job).

## GPU gating (operator-confirmed pre-loop)

**GPU-use is operator-gated, confirmed PRE-LOOP.** The operator confirms the allowed GPU devices during quest setup — a quest cannot reach `run_state=running` without a confirmed `gpu_allocation` (pre-loop start-gate). So during the live loop GPUs are already confirmed and the loop never re-prompts.

- GPU-using work — experiments, benchmarks, profiling, and analyst ablations — may only run on the confirmed devices.
- No `experiment`- OR `analysis`-stage handoff may open while unconfirmed (hard apply-time gate over both stages + invariant `experiment_requires_gpu_confirmation`). A single per-quest confirmation covers both stages.
- Only the operator confirms, via `$HARNESS gpu confirm` (operator-control).
- Prefer running GPU work through `$HARNESS experiment run --cmd ...`, which fails closed and injects `CUDA_VISIBLE_DEVICES=<confirmed devices>`; for direct runs, export the confirmed `devices`.
- Never use a GPU outside the confirmed set, and never self-confirm to unblock work.

## Ambiguity start-gate (pre-loop)

**Every quest passes a MANDATORY pre-launch ambiguity check.** Before a quest can reach `run_state=running` it must have a recorded `kind='clarification'` artifact (pre-loop start-gate, fail-closed) — the operator-facing setup reviewed the objective across 7 dimensions (objective, acceptance, GPU, domain, workspace, budget, domain constraints) and either found no blocking ambiguity or folded the operator's clarifications into the objective/acceptance brief. By the time agents run, the brief is operator-confirmed; the loop does not re-prompt for clarification.

## Quest isolation (absolute)

**TOTAL QUEST ISOLATION — never touch another quest.** Each quest is fully self-contained. You MUST NOT re-use, refer to, cite, or even inspect any artifact, data, finding, reference, code, or result from any other quest. Concretely:
- read/write only your own quest's `runs/<this-quest-id>/` tree (and your assigned worktree);
- never read a sibling `runs/<other-quest>/` or the q1-legacy `outputs/`;
- never pass another quest's `--quest-id` to a harness query and never use `findings query --all-quests` (operator-only).

`findings query`/`lit query` return only your quest's rows; references and findings are quest-owned by schema + invariants (`finding_quest_owned`, `reference_quest_owned`). Collect every datum fresh for THIS quest, even if the objective matches a prior quest's. Prior quests are invisible to you.

## Research-quality disciplines

Extended-lessons disciplines for all roles, applied when recording claims/decisions/analyses or closing a round:

- **Living plan map:** `runs/<q>/plan.md` is a **rendered DB projection** (`$HARNESS plan render`), never authoritative and never read back as state — the DB is canonical. `plan status` prints it; `plan validate` runs plan checks + decision lint. The orchestrator re-renders it at each round close.
- **Claim roles for completeness:** when recording a `claim.upsert`, set `kind` — `alternative`/`competing_hypothesis` for a rival explanation you intend to falsify, `limitation` for a documented scoped-out gap, else default `claim`. The analyst records ablation/mechanism `analysis` rows and names the competing hypothesis (so `$HARNESS completeness audit` can see them).
- **Research-completeness:** `$HARNESS completeness audit --quest-id <q>` = the 7 scientific-quality checks (evidence traceability, no orphan claims, mechanism explanation, named alternatives, ablation-or-documented-infeasibility, lit audit, unresolved-discrepancy handling). In `auto`+`publication` it HARD-gates `complete`; otherwise advisory. The reviewer blocks `revise` on a failing required item when the gate is hard.
- **Decisions name their losers:** a consequential `decision.record` chooses among ≥2 named candidates with non-winners marked + a Winner/Rejected-alternatives/Decisive-reason `rationale_ref`.
- **Frozen objective, amendable acceptance:** never edit `objective.md` post-launch (frozen) and never edit `acceptance.md` in place — acceptance changes only via the operator-confirmed, append-only `amend-acceptance` path (deepresearch-operator-control op 4b).

## Methodology references + binding usage audit

Loop-wide research/writing **craft** packs back every stage. Worker-stage methodology is **binding**: it must be applied through the stage's typed record + validator (`$HARNESS methodology check` resolves `methodology_used[].applied_as` to it), while orchestrator-internal stages (`decision`/`optimize`/`finalize`) use an advisory `artifact(kind='methodology-usage')` at round close.

The full pack catalog, the evidence-ladder + comparability-contract shared vocabulary, and the required-pack-by-stage binding table live in [`references/methodology.md`](references/methodology.md) — **read it before stage work.**

## Common Mistakes

- **Editing `runs/state.sqlite` directly.** All state goes through `$HARNESS`; the SQLite file is never a read or write surface.
- **Passing `--type`/per-field flags to `record apply`.** It takes ONLY `--json`/`--file`. The `--type ... --field val` notation is shorthand for one JSON payload.
- **Passing `--record-id` to a dedicated verb.** `handoff`/`wakeup`/`gpu`/`experiment`/… use their own typed flags — run `<verb> --help`.
- **Malformed record_ids.** Composite ids join PK components with `:` in exact order; the parser is strict.
- **Reusing/inspecting another quest.** Quest isolation is absolute — never read a sibling `runs/<other-quest>/`, the q1-legacy `outputs/`, pass another quest's `--quest-id`, or use `findings query --all-quests`. Collect fresh even if the objective matches.
- **Self-confirming GPUs or running off the confirmed set.** Only the operator confirms (`$HARNESS gpu confirm`); never self-confirm to unblock, never run outside the confirmed devices.
- **Specialist replying anywhere but upstream.** Specialists always reply to the orchestrator; never bypass the tree-loop.
- **Treating plan.md / methodology packs as authoritative state.** Both are projections/advisory craft; the DB is canonical. Record outcomes via `record apply`.
- **Editing `objective.md` (frozen) or `acceptance.md` in place.** Acceptance changes only via the append-only operator-confirmed `amend-acceptance` path.
- **Free-text methodology claims.** For worker stages, `applied_as` must resolve to the stage's validated typed record or `methodology check` rejects it; pure background reading goes in `methodology_consulted[]`.
- **Dropping `loop_id`/`handoff_id` or `--at`.** Reuse the inbound metadata ids on every reply; stamp ISO-8601 `--at` on every mutating command.

## Rationalizations vs. reality

| Rationalization | Reality |
|---|---|
| "A prior quest already answered this — I'll just cite/reuse it." | TOTAL quest isolation. Prior quests are invisible; collect fresh for THIS quest. Enforced by schema + invariants. |
| "GPUs are obviously free, I'll just run it / confirm it myself." | GPU use is operator-gated pre-loop. Only the operator confirms via `$HARNESS gpu confirm`; never self-confirm, never run off the confirmed set. |
| "I'll edit the SQLite / plan.md / acceptance.md directly, it's faster." | DB is canonical and reached only via `$HARNESS`; plan.md is a projection; acceptance changes only via the append-only `amend-acceptance` path; objective is frozen. |
| "I read the pack, that's enough to mark the stage done." | Worker stages bind methodology through the typed record + validator; reading goes in `methodology_consulted[]`, not `methodology_used[]`. |
| "I'll reply directly to the next specialist to save a hop." | Tree-loop: specialists reply upstream to the orchestrator, which owns the handoff ledger and continuation. |
| "Acceptance is a bit off — I'll just tweak it to pass." | Never amend acceptance to pass; interrogate the theory. Acceptance changes only via operator-confirmed op 4b. |
## Output / Stop

No state change of its own; this skill is reference guidance other skills follow. It is not a turn-driving skill — return to the calling skill.
