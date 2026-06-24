# Valuation rubric — bo_review dimensions

All eight score dimensions are **0–100** (higher = more of that quality). Score each candidate from THIS
quest's evidence only. When you have no evidence either way, score near 50 and raise `uncertainty`.

| Dimension | Meaning | Score high when… | Score low when… |
|---|---|---|---|
| `utility` | expected research value / impact toward the objective | directly advances the primary metric or core claim | tangential or marginal to the objective |
| `quality` | methodological soundness / expected evidence strength | clean comparison, strong expected evidence | confound-prone, weak or indirect evidence |
| `novelty` | distinctness from prior work and other candidates | clear non-trivial mechanism/claim not already covered | restatement or obvious tweak of an existing line |
| `exploration_value` | information gain — how much it reduces open uncertainty | resolves a live unknown / opens a new region | confirms what is already known |
| `uncertainty` | your uncertainty about the outcome | outcome genuinely unpredictable | outcome largely predictable |
| `feasibility` | implementable within this quest's repo/compute/protocol | minimal touchpoints, fits compute/protocol | large refactor, unclear path, over budget |
| `cost` | effort/compute cost (penalised) | cheap to run | expensive / long |
| `risk` | risk of redundancy, failure, or over-claim (penalised) | safe, well-grounded | likely redundant, fragile, or over-claims |

Descriptors (recorded, lightly used by acquisition):
- `expected_metric_direction`: `improve` | `regress` | `neutral` | `unknown` — expected effect on the primary metric.
- `expected_effect`: optional 0–100 normalised expected effect magnitude (absent ⇒ treated as 50).
- `confidence`: 0–100, your confidence in this valuation.

## Acquisition (so you score with intent)
```
exploitation = 0.40*utility + 0.25*quality + 0.20*feasibility + 0.15*expected_effect
exploration  = (exploration_value + novelty + uncertainty) / 3
penalty      = 0.35*risk + 0.25*cost  + context penalties (repeat-failure / unresolved ref / cross-quest / missing provenance)
score        = exploitation + beta*exploration - penalty
```
`beta` (default 0.5) is the exploration coefficient: at high beta a high-`exploration_value`/`novelty`/
`uncertainty` candidate can rightly beat a high-`utility` one. Do not inflate exploration to game this —
score honestly; the orchestrator chooses beta.

## Discipline
- Evidence-aware, novelty-aware, explicit about uncertainty.
- Quest-local only — never cite or infer another quest's results; flag `cross_quest`/`missing` motivating
  refs in `risks` and do not rely on them.
- This is an **LLM-reviewer surrogate**, not a probabilistic model and not full statistical Bayesian
  optimization. Your valuation is advisory input to a UCB-like rule, never proof.
