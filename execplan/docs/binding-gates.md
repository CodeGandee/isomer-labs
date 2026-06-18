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
| Idea selection | `idea.select` (`idea_select`, `valid`) | `idea validate` | idea→experiment handoff (`_idea_gate`) | `idea_gate` |
| Baseline contract | `baseline.contract` (`baseline_contract`, `verification_verdict`) | (author-asserted verdict) | `quest.baseline_gate=passed/waived` (`_baseline_contract_gate`) | `baseline_contract` |
| Campaign coverage | claim evidence `evidence_kind` + `analysis.bridge` (`analysis_bridge`, `valid`) | `campaign validate` | analysis→outline/write handoff (`_analysis_bridge_gate`) | `campaign_coverage`, `analysis_bridge` |
| Paper spine / outline | `paper_spine.upsert` (`paper_spine`) | `outline validate` (structural) | (feeds manuscript coverage) | `paper_spine`, `outline_valid` |
| Manuscript coverage | `paper_spine` (`submission_ready`) | `manuscript coverage` | `finalize_outcome=complete` (`_finalize_coverage_gate`) | `manuscript_coverage` |
| Review verdict | `review.verdict` (`review_verdict`, `valid`) | `review validate` (+ `review confirm`, `review route`) | `finalize_outcome=complete` (`_finalize_review_gate`) | `review_verdict` |

Plus the pre-existing finalize guards (`_finalize_scholarship_gate`, `_finalize_authenticity_gate`,
`_finalize_completeness_gate`) and the GPU gate (`_gpu_gate`).

## Methodology resolution
`task-result.methodology_used[].applied_as` is **not free text**: the Orchestrator runs `methodology check
--quest-id <q> --stage <stage> --applied-as <ref>`, which resolves it to the stage's **validated** typed record
(idea.select / baseline.contract / analysis.bridge / paper_spine / review.verdict). The `experiment` stage and
the orchestrator-internal stages (decision/optimize/finalize) have no fold-time typed record — experiment is
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
| `DEEPRESEARCH_IDEA_GATE=0` | idea→experiment gate |
| `DEEPRESEARCH_BASELINE_CONTRACT_GATE=0` | baseline-contract gate |
| `DEEPRESEARCH_BRIDGE_GATE=0` | analysis→write bridge gate |
| `DEEPRESEARCH_COVERAGE_GATE=0` | finalize manuscript-coverage gate |
| `DEEPRESEARCH_REVIEW_GATE=0` | finalize review-verdict gate |
| `DEEPRESEARCH_IDEA_SLATE_MIN` / `DEEPRESEARCH_IDEA_SCORE_MIN` | idea-selection floors (per run) |
| `DEEPRESEARCH_IDEA_NOVELTY_WAIVER=1` | allow `novelty_label='not_differentiated'` |
| `DEEPRESEARCH_SCHOLARSHIP_MIN_REFS` / `_MIN_REF_CLAIMS` | scholarship bar |
| `DEEPRESEARCH_AUTHENTICITY_GATE=0` | finalize authenticity gate |
| `DEEPRESEARCH_COMPLETENESS_GATE_RIGOR=none` | finalize completeness checklist |

## Live-DB note
The gate tables (`idea_select`, `baseline_contract`, `analysis_bridge`, `paper_spine`, `review_verdict`) and
`claim_evidence.evidence_kind` are created by `state init` (and the additive column by the `db.py` migration).
On an un-reinited older DB a gate fails **safe** (advisory) if its table is absent.

## Regression
`python3 tests/binding/run_all.py` runs all gate suites (paper-spine/coverage, review verdict, idea selection,
baseline/campaign/bridge, gate status/methodology resolution).
