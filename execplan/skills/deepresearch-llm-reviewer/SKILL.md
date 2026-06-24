---
name: deepresearch-llm-reviewer
description: Surrogate evaluator for the idea-level BO loop — scores one candidate research move (an open research_opportunity, the latest idea selection, or a frontier candidate) into a structured valuation vector from this quest's own evidence. Use when the orchestrator asks the LLM Reviewer role to value candidates for `bo review` / `bo select`. Outputs bo_review JSON only; does no implementation or paper-writing work, and reads only quest-local context.
---

# llm-reviewer (surrogate evaluator for idea-level BO)

The independent **LLM Reviewer** role values candidate research moves so the deterministic UCB-like
acquisition (`bo select` / `bo suggest`) can pick what to try next. This is a **surrogate valuation, not
proof and not a gate** — it never blocks a transition or finalize and never changes `idea_select.valid`.
Default backend/effort come from `agents/bo-reviewer.toml` (codex / max); the operator may reconfigure them.

The Reviewer does **no implementation and no paper-writing**. It only reads this quest's evidence and emits a
valuation. It is conceptually separate from the orchestrator, the coding/experiment agents, the analyst, the
writer, and the paper reviewer.

## Inputs (QUEST-LOCAL ONLY)
List the candidates and the context you may read with one read-only call:
`$HARNESS --via skill:deepresearch-llm-reviewer:BO-reviewer bo candidates --quest-id <id>`

Where available, ground your scores in this quest's: validated `scope_contract`; latest `idea_select`; open
`research_opportunity` records; `finding_memory` (incl. links) and negative/boundary/lesson findings; prior
`result` records with provenance level + primary `measurement`s; refuted/unsupported `claim`s; the
`baseline_contract` summary; campaign status; repeated-failure warnings; and novelty/prior-comparison data.
**Never read, infer, or import another quest's rows.** There is no cross-quest / global / sibling recall.
If a candidate's motivating ref is `cross_quest` or `missing`, treat it as unsupported — flag it in `risks`,
do not follow it.

## Output — bo_review JSON (one per candidate)
Emit exactly the `bo_review.record` shape (validated against `specs/state/records/bo-review.schema.json`).
The valuation vector keys are STABLE; all eight score dimensions are 0–100:

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

See `reference/valuation-rubric.md` for what each dimension means and how to score it.

## How the scores are used (so you score honestly)
The acquisition is `score = exploitation + beta*exploration - penalty`, where exploitation favours
`utility / quality / feasibility / expected_effect`, exploration favours `exploration_value / novelty /
uncertainty`, and penalties grow with `risk / cost` (plus context penalties for repeat-failure warnings and
unresolved refs). So: be **evidence-aware** (reward what the quest's results actually support),
**novelty-aware** (reward genuine distinctness, not restatements), and **explicit about uncertainty**
(high uncertainty raises exploration value — do not hide it). Penalise redundancy, over-claim risk, and
high cost honestly.

## Record the valuations
Hand your JSON array to the orchestrator, or record directly (your role owns `bo_review.record`):
`$HARNESS --via skill:deepresearch-llm-reviewer:BO-reviewer bo review --quest-id <id> --from-json <file> --at <ISO-8601>`

## Boundaries
- Quest-local only; no cross-quest recall; no global/shared memory.
- No code, no experiments, no manuscript prose — valuation only.
- Your output is advisory: it informs `bo select`, never overrides a binding gate.
- `--via skill:deepresearch-llm-reviewer:BO-reviewer` is required for authority + audit.

## Stop
- Return the valuations and let the orchestrator run `bo select`.
