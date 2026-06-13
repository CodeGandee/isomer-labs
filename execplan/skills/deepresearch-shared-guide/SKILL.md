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
   Write only with `$HARNESS record apply --type <record_type> --at <iso8601> ...` (validate first with
   `$HARNESS record validate`). Never read or edit `runs/state.sqlite` directly.
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

## Output

- No state change of its own; this skill is reference guidance other skills follow.

## Stop

- Not a turn-driving skill; return to the calling skill.
