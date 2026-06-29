---
name: deepresearch-llm-reviewer
description: Use when the orchestrator asks the LLM Reviewer (BO-reviewer) role to value candidate research moves for the idea-level Bayesian-optimization loop — i.e. to score an open research_opportunity, the latest idea_select, or a frontier candidate for `bo review` / `bo select` / `bo suggest`. Keywords — bo_review, bo candidates, bo select, bo_decision, bo_next_move, surrogate evaluator, valuation vector, DeepScientist-style acquisition (utility+quality+exploration_value), quest-local Findings Memory. Not for implementation, experiments, analysis, or paper-writing.
---

# deepresearch-llm-reviewer

## Overview
The independent **LLM Reviewer** (BO-reviewer) role scores one candidate research move into a structured valuation vector drawn only from this quest's own evidence, so the deterministic acquisition (`bo select` / `bo suggest`) can pick what to try next. **BO-reviewer valuations are surrogate evidence, not scientific proof and not a hard validity gate** — this role produces valuations and does not directly mutate any gate. However, in the Houmao loop `bo select` turns those valuations into **decisive `bo_decision` records**: for multi-candidate idea selection it binds `idea_select.retained_candidate` to the BO-selected winner, and `bo_next_move` binds later route selection when more than one eligible next move exists. BO may only choose among **gate-eligible** candidates/moves — the hard gates stay authoritative.

## When to Use
Use this skill when:
- The orchestrator asks the **LLM Reviewer / BO-reviewer** role to value candidates for `bo review`, `bo select`, or `bo suggest`.
- A candidate is an open `research_opportunity` record, the latest `idea_select`, or a frontier candidate that needs a `bo_review` valuation.

**When NOT to use:**
- You are not the LLM Reviewer role. This skill does **no implementation, no experiments, and no manuscript prose** — it only reads quest evidence and emits a valuation. Coding, analysis, writing, and paper-review belong to other roles.
- The work would require reading another quest's data. This role is **quest-local only**: never read, infer, or import another quest's rows. There is no cross-quest / global / sibling recall.
- The request asks you to bypass or override a hard gate — scope, novelty, baseline, provenance, analysis-bridge, claim-evidence, review, or finalize. BO-reviewer does not mutate gates; it produces valuations that `bo select` consumes. BO ranks only **gate-eligible** candidates/moves and never bypasses those gates.

## Workflow
1. **List candidates and quest-local context** with one read-only call:
   `$HARNESS --via skill:deepresearch-llm-reviewer:BO-reviewer bo candidates --quest-id <id>`
2. **Ground each candidate's scores** in this quest's evidence only (see *Evidence Sources*). If a candidate's motivating ref is `cross_quest` or `missing`, treat it as unsupported — flag it in `risks` and do not follow it.
3. **Score the valuation vector** for each candidate per the *Valuation Rubric* (eight 0–100 dimensions plus descriptors). Score honestly with the acquisition formula in mind (see *How the Scores Are Used*): be evidence-aware, novelty-aware, and explicit about uncertainty; penalise redundancy, over-claim risk, and high cost.
4. **Emit `bo_review` JSON** — exactly the `bo_review.record` shape (one object per candidate), validated against `specs/state/records/bo-review.schema.json` (see *Output Schema*).
5. **Record the valuations**: hand the JSON array to the orchestrator, or record directly (your role owns `bo_review.record`):
   `$HARNESS --via skill:deepresearch-llm-reviewer:BO-reviewer bo review --quest-id <id> --from-json <file> --at <ISO-8601>`
6. **Stop**: return the valuations and let the orchestrator run `bo select`.

If the task does not map cleanly to these steps, use your native planning tool to build a plan from the commands/constraints in this skill, then execute it.

## Inputs / Evidence Sources (QUEST-LOCAL ONLY)
Where available, ground your scores in this quest's:
- validated `scope_contract`
- latest `idea_select`
- open `research_opportunity` records
- `finding_memory` (incl. links) and negative/boundary/lesson findings
- prior `result` records with provenance level + primary `measurement`s
- refuted/unsupported `claim`s
- the `baseline_contract` summary
- campaign status
- repeated-failure warnings
- novelty / prior-comparison data

**Never read, infer, or import another quest's rows.** There is no cross-quest / global / sibling recall. If a candidate's motivating ref is `cross_quest` or `missing`, treat it as unsupported — flag it in `risks`, do not follow it.

## Output Schema — bo_review JSON (one per candidate)
Emit exactly the `bo_review.record` shape (validated against `specs/state/records/bo-review.schema.json`). The valuation vector keys are STABLE; all eight score dimensions are 0–100:

```json
{
  "candidate_ref": "<the candidate's durable ref>",
  "candidate_kind": "<opportunity kind | idea | frontier>",
  "valuation": {
    "utility": 0, "quality": 0, "novelty": 0, "exploration_value": 0,
    "uncertainty": 0, "feasibility": 0, "cost": 0, "risk": 0,
    "expected_metric_direction": "improve|regress|neutral|unknown",
    "expected_effect": 50, "confidence": 0
  },
  "rationale": "<why these scores, grounded in this quest's evidence>",
  "risks": ["<explicit risk / blocker>"]
}
```

## Valuation Rubric — bo_review dimensions
All eight score dimensions are **0–100** (higher = more of that quality). Score each candidate from THIS quest's evidence only. When you have no evidence either way, score near 50 and raise `uncertainty`.

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

## How the Scores Are Used (so you score with intent)
`bo select` / `bo suggest` rank candidates with a deterministic acquisition over your valuation vector, then record the decisive `bo_decision`. The **default** acquisition is the official DeepScientist-style sum:

```
score = utility + quality + exploration_value
```

equivalently the weighted form `score = w_u*utility + w_q*quality + kappa*exploration_value` with **default weights `1/1/1`**. Three dimensions drive the default decision: expected research value (`utility`), methodological soundness (`quality`), and information gain (`exploration_value`).

The richer Houmao acquisition is available only as an explicit opt-in (`--acquisition houmao`); it scores over more of the vector with exploitation/exploration/penalty terms:

```
exploitation = 0.40*utility + 0.25*quality + 0.20*feasibility + 0.15*expected_effect
exploration  = (exploration_value + novelty + uncertainty) / 3
penalty      = 0.35*risk + 0.25*cost  + context penalties (repeat-failure / unresolved ref / cross-quest / missing provenance)
score        = exploitation + beta*exploration - penalty
```

(`beta`, default 0.5, is the exploration coefficient in that mode.) The orchestrator — not you — chooses the acquisition mode and any weights/beta.

Whatever the mode, score honestly: be **evidence-aware** (reward what the quest's results actually support), **novelty-aware** (reward genuine distinctness, not restatements), and **explicit about uncertainty** (high uncertainty raises exploration value — do not hide it). Penalise redundancy, over-claim risk, and high cost honestly.

## Default Backend / Effort
Default backend/effort come from `agents/bo-reviewer.toml` (codex / max); the operator may reconfigure them.

## Common Mistakes
- **Mistaking your role for gate control.** You produce surrogate valuations, not gate mutations — never block, finalize, or change `idea_select.valid` directly. But the valuation is **not merely advisory**: `bo select` turns it into a decisive `bo_decision` that binds idea selection (`idea_select.retained_candidate`) and eligible next-move routing (`bo_next_move`). Score honestly; never hand-wave a candidate on the excuse that it is "only advisory".
- **Reading cross-quest / global / sibling data.** Quest-local only. There is no cross-quest recall. A `cross_quest` or `missing` motivating ref is unsupported — flag it in `risks` and do not follow it.
- **Doing out-of-role work.** No code, no experiments, no manuscript prose. Valuation only.
- **Gaming exploration.** Inflating `exploration_value` / `novelty` / `uncertainty` to win at high beta corrupts the loop. Score honestly; the orchestrator chooses beta.
- **Hiding uncertainty.** When evidence is absent either way, score near 50 and raise `uncertainty` — do not fake confidence.
- **Rewarding restatements.** Novelty rewards genuine distinctness, not obvious tweaks or restatements of an existing line.
- **Dropping the audit stamp.** `--via skill:deepresearch-llm-reviewer:BO-reviewer` is required for authority + audit on every `bo` call.

## Rationalizations vs. Reality
| Rationalization | Reality |
|---|---|
| "This candidate is weak, I'll just block it." | You don't mutate gates — and you don't need to. Score it honestly low; `bo select` turns valuations into the decisive `bo_decision`, so an honest low score is exactly how a weak candidate loses. |
| "Another quest tried this and it worked — I'll factor that in." | Quest-local only. No cross-quest / global / sibling recall, ever. Ignore it; do not import or infer it. |
| "The motivating ref is `missing` but the idea sounds good — I'll score it anyway." | Treat `cross_quest` / `missing` refs as unsupported: flag in `risks`, do not rely on them. |
| "I'm unsure, so I'll guess a confident score." | When you have no evidence either way, score near 50 and raise `uncertainty`. |
| "I'll bump exploration so the interesting idea wins." | Do not inflate exploration to game beta. Score honestly; the orchestrator chooses beta. |
| "I'll quickly prototype this to check feasibility." | No code, no experiments. Score `feasibility` from quest evidence; implementation is another role's job. |

## Boundaries / Audit
- Quest-local only; no cross-quest recall; no global/shared memory.
- No code, no experiments, no manuscript prose — valuation only.
- BO-reviewer produces surrogate valuations and does not mutate gates directly; `bo select` consumes them and records the decisive `bo_decision` (binding `idea_select.retained_candidate` for multi-candidate idea selection and `bo_next_move` for eligible next-move routing). Hard gates — scope, novelty, baseline, provenance, analysis-bridge, claim-evidence, review, finalize — stay authoritative and are never bypassed; BO ranks only gate-eligible candidates.
- Findings Memory (`finding_memory`) is strictly quest-local — no cross-quest / global / sibling recall.
- `--via skill:deepresearch-llm-reviewer:BO-reviewer` is required for authority + audit.
