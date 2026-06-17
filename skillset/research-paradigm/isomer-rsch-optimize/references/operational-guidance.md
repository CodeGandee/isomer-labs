# Operational Guidance

Use this reference when the optimize route needs longer execution notes than the control surface in `SKILL.md`.

## Frontier Recovery

At the start of each meaningful optimize pass, refresh the frontier Artifact or View Manifest, recent Findings, current Research Task state, and exact durable wording when it matters. Do not create new candidates before the frontier, recent optimization lessons, and current execution references are checked.

## Submode Selection

Choose exactly one primary submode:

1. `fusion` when the frontier explicitly says fusion.
2. `debug` when a strategically valuable candidate failed for a concrete and likely fixable reason.
3. `rank` when several method briefs exist and promotion is unresolved.
4. `brief` when the candidate slate is too thin or too weak.
5. `seed` when a durable line exists but lacks a live implementation-attempt pool.
6. `loop` when a live pool or leading line already exists and bounded execution progress is needed.
7. `stop` when the remaining frontier is saturated or unjustified.

## Candidate Brief Protocol

Method briefs sit between idea intuition and implementation. They should answer what bottleneck is targeted, why the current line is limited, how the mechanism addresses it, and what must remain unchanged for comparability.

Preserve this discipline: clarify bottleneck, constraints, and comparability first; generate a small differentiated slate; recommend one approach with tradeoffs; self-check ambiguity, overlap, and weak justification before promotion.

## Promotion Protocol

Promote a method brief into a Research Branch only when it clearly dominates nearby alternatives, is top-ranked and sufficiently distinct, the Operator Agent requested it, or the frontier says it is the strongest next move.

Default promotion rule: promote one candidate when it clearly dominates, at most two or three when structural uncertainty remains, and at most one per mechanism family unless a documented override is justified.

Record a Decision Record explaining which briefs were compared, which one won, why promotion is justified now, and why others were held, fused, or rejected.

## Seed Protocol

Use seed mode after a durable line exists and before broad execution. Generate a small implementation-attempt pool, usually two or three candidates, with different mechanism, implementation path, or risk profile.

For each seed candidate, record candidate id, parent line, strategy, mechanism family, change layer, change plan, expected gain, keep-unchanged contract, first validation step, and archive condition.

Use validation-cost-aware seeding: if the first objective signal is expected in about twenty minutes or less, modestly wider quick checks may be justified; if it is slower or expensive enough that broad probing is wasteful, keep the pool narrow and require stronger reasons.

## Loop Protocol

Use loop mode when a durable line and implementation pool exist. Choose one primary action: smoke, promote to full evaluation, archive, record main result, switch to fusion, switch to debug, or stop.

Every loop pass should end with one updated candidate status, one updated next action, and one frontier-review trigger. If validation is fast, resolve uncertainty with evidence rather than over-arguing; if validation is slow, do not keep paying for frontier uncertainty that should have been reduced in brief or rank mode. Do not leave several half-started directions without a dominant next move.

## Execution Protocol

Execution belongs behind Capability Bindings and Execution Adapters. Record commands, logs, outputs, and metrics as Runs, Evidence Items, and Provenance Records. Use `[[tbd-surface:api-execution-command]]` for unsettled command surfaces and `[[tbd-surface:path-run-logs]]` for unsettled log layouts.

Prefer bounded smoke before full evaluation unless cheap direct validation is equally informative. Do not rerun the same unchanged candidate. If a candidate fails with a clear root cause, debug deliberately or archive it.

## Memory and Findings

Before broad new search, inspect relevant Findings and prior Evidence Items. Write a retrieval-friendly Finding when the pass produces a reusable success pattern, repeated failure pattern, fusion lesson, or explicit non-repeat rule. Do not write generic activity summaries.

## Stage Completion

This stage is complete only when a stronger line was promoted and the next anchor is clear, the current line produced a real measured result and the next route is recorded, the frontier says stop and the stop decision is recorded, or a blocker is durable.
