# Research-quality binding gates

The loop's research-quality bar is enforced by **binding gates**, not advisory prose. Every gate follows the
same shape:

> typed record / structured artifact → a **validator** computes a stored status flag → a **transition/finalize
> guard** in `records.py` consumes that flag (hard-blocks the write) → **`gate status`** exposes it →
> the Orchestrator routes on it.

A worker can never self-certify a validator-owned flag (the record schemas are `additionalProperties:false`
and force the flag to 0 on write; only the validator command sets it). `gate status` summarizes and guides
routing but does **not** replace the hard guards — they remain authoritative at the write path.

## The gates

| Gate | Typed record (table) | Validator command | Hard guard (records.py) — blocks | `gate status` key |
|---|---|---|---|---|
| Scope / eval contract | `scope.contract` (`scope_contract`, `valid`) | `scope validate` | idea selection requires it (via `idea validate`, bound) | `scope_contract` |
| Idea selection | `idea.select` (`idea_select`, `valid`) | `idea validate` (selection pressure + valid `scope.contract` + durable novelty grounding: `prior_comparison.closest_prior_refs` → `reference` rows, ≥2 at publication) | idea→experiment handoff (`_idea_gate`) | `idea_gate` |
| Baseline contract | `baseline.contract` (`baseline_contract`, `valid`) | `baseline validate` (route + eval contract + provenance-backed result) | `quest.baseline_gate=passed/waived` (`_baseline_contract_gate`) | `baseline_contract` |
| Campaign coverage | claim evidence `evidence_kind` + `analysis.bridge` (`analysis_bridge`, `valid`) | `campaign validate` | analysis→outline/write handoff (`_analysis_bridge_gate`) | `campaign_coverage`, `analysis_bridge` |
| Paper spine / outline | `paper_spine.upsert` (`paper_spine`) | `outline validate` (structural) | (feeds manuscript coverage) | `paper_spine`, `outline_valid` |
| Manuscript coverage | `paper_spine` (`submission_ready`) | `manuscript coverage` | `finalize_outcome=complete` (`_finalize_coverage_gate`) | `manuscript_coverage` |
| Review verdict | `review.verdict` (`review_verdict`, `valid`) | `review validate` (+ `review confirm`, `review route`) | `finalize_outcome=complete` (`_finalize_review_gate`) | `review_verdict` |

Plus the pre-existing finalize guards (`_finalize_scholarship_gate`, `_finalize_authenticity_gate`,
`_finalize_completeness_gate`) and the GPU gate (`_gpu_gate`).

## Result provenance strength
`result validate` computes both `provenance_ok` (the declared run-manifest holds up) and a
validator-owned `provenance_level` (author cannot self-certify):
- `declared` — an executed run-manifest only (command/code_revision/metric_source/run_status), nothing resolved;
- `artifact_backed` — a `log_ref`/`config_ref`/`output_artifacts` reference resolves to an `artifact` row AND
  `metric_source` is specified (any provided hash is hex-shaped). It does NOT verify metric-file contents;
- `external_trusted` — the `imported`/`trusted` route (a cited external result);
- `waived` — the `waived` route (an explicit, reasoned deferral);
- `reexecuted` — reserved (re-execution is not auto-performed; only via a trusted/manual route).

Campaign coverage counts a result's evidence at **standard** rigor on `provenance_ok=1` (declared is fine —
unchanged at standard rigor). At **publication** rigor a local result must be `>= artifact_backed` (external_trusted /
waived also pass); a declared-only result is **not counted** with the reason "provenance is declared only …",
unless `DEEPRESEARCH_ARTIFACT_PROVENANCE_GATE=0` waives it (surfaced in `gate status` `active_waivers`).
Re-run `result validate` after the run's log/config/output artifacts change.

## Discovery layer (advisory, quest-local — NOT a gate)
Separate from the binding gates, `gate status` also carries an **advisory** `data.discovery` block (open
`research_opportunity` rows + `recommended_next_actions`, refuted/unsupported claims, parked/abandoned routes,
a negative/boundary findings count). It NEVER blocks a transition or finalize and never appears in
`blocking_gates`. Agents record "what to try next and why" via `record apply --type opportunity.record`
(kinds: next_experiment / ablation / robustness / boundary / baseline_repair / new_idea / failure_followup),
citing this quest's finding/result/claim ids in `motivating_refs`; read it back with `opportunity list` or in
the `plan render` Discovery section. **Quest-local only — there is no cross-quest/global/shared discovery
memory.** (`bo status` reports a heuristic no-improvement streak, NOT Bayesian optimization; its
`objective_sense` is read from the validated scope contract's `metric_direction`.)

`opportunity.motivating_refs` and a finding's optional `links` (scope_contract/idea_select/experiment/
result/claim/claim_evidence/analysis_bridge/paper_spine/branch/artifact ids) are **resolved quest-locally**:
`opportunity list` / `opportunity check` / the `gate status` `data.discovery.opportunities_with_unresolved_refs`
flag any ref that is `missing` or owned by another quest (`cross_quest`), and `plan render` marks it
`!unresolved-refs`. This is **advisory** — unresolved refs never enter `blocking_gates` and never block a
transition or finalize. A cross-quest ref is flagged invalid, never followed (no cross-quest memory). Negative
/failed-path findings use `kind='lesson'`.

**Repeated-failure advisory (quest-local).** An optional `attempt_signature` (idea_key/method_key/dataset/
metric/parameter_key/baseline_id/condition/route/notes) on `opportunity.record` (and on idea-select content)
is compared — read-only — against this quest's prior FAILED signals: dropped opportunities (signature
overlap), refuted claims (cited or condition match), negative/boundary evidence (condition match), and
`lesson` findings (method/idea-key match). Surfaced via `opportunity check` (`repeated_failure` /
`no_repeat_risk`), `gate status` `data.discovery.repeated_failure_warnings`, and the `plan render`
"Repeated-failure advisory" line. **Advisory only** — never enters `blocking_gates`, never affects
`finalize_readiness`, never sets `idea_select.valid=0`, and needs no waiver. Repeating a failed path is
allowed; the agent should just explain what changed. Quest-local only (a matching attempt in another quest is
ignored — no cross-quest memory).

## Methodology resolution
`task-result.methodology_used[].applied_as` is **not free text**: the Orchestrator runs `methodology check
--quest-id <q> --stage <stage> --applied-as <ref>`, which resolves it to the stage's **validated** typed record
(scope.contract / idea.select / baseline.contract / analysis.bridge / paper_spine / review.verdict). The
`experiment` stage and the orchestrator-internal stages (decision/optimize/finalize) have no fold-time typed
record — experiment is
bound downstream by campaign coverage; the internal stages use an advisory `artifact(kind='methodology-usage')`
that `plan validate` warns about. Background-only reading goes in `methodology_consulted[]` (never counted).

## Rigor levels (`quest.rigor_level`)
All gates bind only for **research-contract** quests (a `kind='research-contract'` artifact) at rigor
`>= standard`:
- `scoping` → **advisory** (gates report `advisory`, never block).
- `standard` / `publication` → **binding** (publication uses stricter `[gate_floors]`).
- `strict` → reserved (floors defined in `seed.toml [gate_floors.strict]`; not yet in the `rigor_level` enum).

Configurable floors live in `seed.toml [gate_floors.<rigor>]` (idea slate/score; campaign required/baseline/
anyof/significance).

## `gate status`
`gate status --quest-id <q>` returns machine-readable JSON: per gate `{status (pass|fail|advisory|
not_applicable|missing), rigor_level, blocking, reason, latest_record_ref, route_target, required_next_action}`,
plus `finalize_readiness` and `blocking_gates[]`. The Orchestrator dispatches to the first blocking gate's
`route_target`; when nothing blocks (`finalize_readiness=pass`) it routes to finalize.

## Environment waivers (operator override; default = enforced)
| Env var | Waives |
|---|---|
| `DEEPRESEARCH_SCOPE_GATE=0` | scope/eval-contract requirement at idea selection |
| `DEEPRESEARCH_IDEA_GATE=0` | idea→experiment gate |
| `DEEPRESEARCH_BASELINE_CONTRACT_GATE=0` | baseline-contract gate |
| `DEEPRESEARCH_BRIDGE_GATE=0` | analysis→write bridge gate |
| `DEEPRESEARCH_COVERAGE_GATE=0` | finalize manuscript-coverage gate |
| `DEEPRESEARCH_REVIEW_GATE=0` | finalize review-verdict gate |
| `DEEPRESEARCH_IDEA_SLATE_MIN` / `DEEPRESEARCH_IDEA_SCORE_MIN` | idea-selection floors (per run) |
| `DEEPRESEARCH_IDEA_NOVELTY_WAIVER=1` | allow `not_differentiated` + waive durable novelty grounding (visible in `active_waivers`) |
| `DEEPRESEARCH_SCHOLARSHIP_MIN_REFS` / `_MIN_REF_CLAIMS` | scholarship bar |
| `DEEPRESEARCH_PROVENANCE_GATE=0` | result-provenance enforcement in campaign coverage |
| `DEEPRESEARCH_ARTIFACT_PROVENANCE_GATE=0` | publication-rigor artifact-backed-provenance requirement |
| `DEEPRESEARCH_EVIDENCE_PROOF_GATE=0` | evidence-kind proof enforcement in campaign coverage |
| `DEEPRESEARCH_FRESHNESS_GATE=0` | validator-freshness (stale computed-flag) checks |
| `DEEPRESEARCH_AUTHENTICITY_GATE=0` | finalize authenticity gate |
| `DEEPRESEARCH_COMPLETENESS_GATE_RIGOR=none` | finalize completeness checklist |

## Durable waivers + finalize acknowledgement
Env waivers are **visible** (`gate status` reports `status:"waived"`, `waiver_source`, and lists every active
override in `active_waivers`) but they are not silent passes for finalize. On a **bound** quest, finalize
`complete` is HARD-BLOCKED (`_finalize_waiver_ack_gate`, runs last) while any **finalize-sensitive** gate is
env-waived unless a durable **`quality_gate.waiver`** record (`finalize_ack=true` + a non-empty `reason`)
exists for that gate. The finalize-sensitive env→gate map:

| Env waiver | Acked gate name |
|---|---|
| `DEEPRESEARCH_BASELINE_CONTRACT_GATE=0` | `baseline_contract` |
| `DEEPRESEARCH_BRIDGE_GATE=0` | `analysis_bridge` |
| `DEEPRESEARCH_COVERAGE_GATE=0` | `manuscript_coverage` |
| `DEEPRESEARCH_REVIEW_GATE=0` | `review_verdict` |
| `DEEPRESEARCH_PROVENANCE_GATE=0` | `provenance` |
| `DEEPRESEARCH_EVIDENCE_PROOF_GATE=0` | `evidence_proof` |
| `DEEPRESEARCH_AUTHENTICITY_GATE=0` | `authenticity` |

Record an acknowledgement through the single write path:
`record apply --type quality_gate.waiver` with `gate`, `source` (`env|operator|record|scoping`), `reason`
(required), and `finalize_ack=true`. `reason` is schema-required, so a waiver with no reason is rejected.
`gate status` surfaces `durable_waivers`, `finalize_ack_present`, and `finalize_ack_missing`; the ack-gate is
the only escape (it is NOT itself env-bypassable). Scoping/advisory quests stay permissive but the waiver is
still shown. Read the audit trail with `gate waiver list --quest-id <q>`.

## Validator freshness (stale computed flags)
Validator-computed flags (`baseline_contract.valid`, `analysis_bridge.valid`, `paper_spine.submission_ready`,
`review_verdict.valid`) can go stale if their inputs change after validation. Each validator stamps a
**dependency fingerprint** (`validated_fingerprint`) — a signature of the records it validated over — onto its
row. The consuming gates + `gate status` recompute it and treat the flag as STALE when it no longer matches:
- baseline ← the contract's gate-relevant fields + the referenced result's `provenance_ok`;
- campaign/bridge ← the quest's claims + supporting claim_evidence (incl. evidence_proof + each result's
  `provenance_ok`) + `baseline_gate`;
- manuscript/spine and review ← the paper spine row + claims + supporting evidence.

A **bound** quest FAILS CLOSED on a stale flag at the hard transition/finalize (re-run the relevant validator).
`gate status` shows the per-gate stale reason and a top-level `stale_gates[]` list (computed even in
scoping/advisory mode, where the hard gates stay permissive — staleness is visible but non-blocking). The
fingerprint is **coarse**: any change to a tracked dependency invalidates the flag. A NULL fingerprint (legacy /
legacy / not-fingerprinted) is treated as not-checked (history-safe). `result.provenance_ok` is fresh-by-construction (a
`result.record` re-upsert force-resets it to 0). Waive all freshness checks with `DEEPRESEARCH_FRESHNESS_GATE=0`
(surfaced in `active_waivers`). **After changing evidence, results, claims, the paper spine, or the review
target, re-run the relevant validator** (`result validate` / `baseline validate` / `campaign validate` /
`manuscript coverage` / `review validate`).

## Live-DB note
The gate tables (`idea_select`, `baseline_contract`, `analysis_bridge`, `paper_spine`, `review_verdict`) and
`claim_evidence.evidence_kind` are created by `state init` (and the additive column by the `db.py` migration).
On an un-reinited older DB a gate fails **safe** (advisory) if its table is absent.

## Regression
`python3 tests/binding/run_all.py` runs all gate suites (paper-spine/coverage, review verdict, idea selection,
baseline/campaign/bridge, gate status/methodology resolution, waiver durability/finalize acknowledgement,
validator freshness/stale computed flags).
