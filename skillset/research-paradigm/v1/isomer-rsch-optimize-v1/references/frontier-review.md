# Frontier Review

Use this reference at meaningful route boundaries.

## Template

```md
# Frontier Review

## Current Frontier

- mode:
- best_research_branch:
- best_run:
- stagnant_branches:
- candidate_backlog:
- fusion_candidates:

## Evidence Summary

- strongest_support:
- strongest_contradiction:
- biggest_unresolved_risk:

## Route Choice

- explore / exploit / fusion / debug / stop:
- why_this_is_the_best_next_move:

## Active Optimize Submode

- brief / rank / seed / loop / fusion / debug / stop:
- why_this_submode_is_dominant_now:

## Immediate Next Action

- exact_next_step:
- result_that_triggers_another_frontier_review:
- result_that_forces_a_different_mode:
```

## Route Meanings

- `explore`: widen search with fresh candidate directions.
- `exploit`: focus on the strongest current line.
- `fusion`: merge insights from complementary lines.
- `debug`: rescue a candidate or line blocked by a concrete failure mode.
- `stop`: remaining routes are saturated, redundant, or low value relative to cost.

## Heuristics

Choose explore when no line is clearly dominant or current lines are too similar. Choose exploit when one line leads on evidence and comparability. Choose fusion when at least two lines have complementary strengths. Choose debug when a strategically valuable candidate failed for a likely fixable reason. Choose stop when remaining routes are not justified.
