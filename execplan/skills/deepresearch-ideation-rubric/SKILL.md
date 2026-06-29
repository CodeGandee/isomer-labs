---
name: deepresearch-ideation-rubric
description: "Use when the scout-ideator is in the scope/idea stages — framing a quest, generating/scoping/selecting a research idea, or fixing its evaluation contract and baseline plan. Keywords: scout, ideation, divergence/convergence, selection gate, FINER, objective contract, eval contract, baseline shortlist (attach/import/reproduce/reject), candidate scoring, pre-idea draft, next-anchor, blocked scout, knowledge cards. Read-only methodology craft; changes no state."
---

# deepresearch-ideation-rubric

## Overview

Idea-and-scoping craft for the **scout-ideator** during the scope/idea stages of the research loop: it supplies the objective contract, the divergence-then-convergence-then-refine ideation workflow, candidate scoring, the selection gate, the evaluation contract, the baseline shortlist, and the scout framing narrative. This is a read-only methodology lookup — it indexes craft and makes no authoritative state change; the DB stays canonical.

## When to Use

Use when, acting as the **scout-ideator**, you are:

- framing a quest that does not yet have a stable research frame (task definition, evaluation contract, repo/literature neighborhood, baseline direction);
- generating, scoping, or selecting a research idea/direction;
- fixing an idea's evaluation contract or baseline plan;
- preparing the selection gate and the handoff record to the experiment stage.

**When NOT to use:**

- You are not the scout-ideator role, or the event is not a scope/idea stage trigger — defer to that role's own skill.
- You need to mutate state, finalize results, confirm GPU, or change quest state — this skill is advisory only and records no row.
- The work would cross quest-isolation bounds (reuse/refer-to/inspect another quest's artifacts/findings/refs) — collect fresh; never reach across quests.

## Workflow

1. **Index the methodology reference for the method you need** (read-only, traceable):
   `$HARNESS --via skill:deepresearch-ideation-rubric:<your-role> knowledge cards --query selection-gate`
   (or `knowledge query --kind reference`). Substitute the query for the stage you are in (e.g. `objective-contract`, `scout-framing`, `eval-contract`, `baseline-shortlist`).
2. **Scout framing first when the frame is not stable.** Establish the four framing layers, resolve only the minimum unknowns that change the next anchor, and recommend `baseline` / `idea` / remain-in-`scout`. Full narrative in `references/scout-framing.md` (search ladder, truth sources, blocked-state handling, stop-on-clarity rules).
3. **Set the objective contract** at the start of an idea pass whenever the real target may differ from the easiest surrogate. Use the template in **Objective Contract** below; do not widen the frontier until it distinguishes true progress / false progress / invalid routes.
4. **Run the ideation workflow: Diverge → Converge → Refine.** Classify problem-first vs solution-first, pick `2-4` lenses from the lens catalog, generate `6-12` raw ideas, converge to a `2-3` (max `5`) frontier, then refine the winner into a handoff contract. Full lens catalog, dispatch table, failure-mode-to-recovery taxonomy, scoring rubric, and draft-before-submit SOP in `references/ideation-craft.md`.
5. **Score candidates** along the explicit axes (see **Candidate Scoring** below and the rubric in `references/ideation-craft.md`); write a pre-idea draft for each serious surviving candidate before promotion.
6. **Clarify the evaluation contract and baseline shortlist** as durable framing outputs. Use the **Evaluation Contract** and **Baseline Shortlist** templates below; each shortlist ends with one recommended route (attach / import / reproduce / reject).
7. **Pass the selection gate** before promotion. Apply the value/feasibility screen, FINER screen, the `0/1/2` quality gate (promote only at total `>= 7/10`), honest novelty/value labels, and the mechanism/falsification gate. See **Selection Gate** below.
8. **Record outcomes through your role's normal skill/commands.** Map any external tool names in the references (`artifact.*`, `memory.*`, `bash_exec`) to the `$HARNESS` surface; durable idea/decision submission goes through `$HARNESS record apply`. Then return the method to the calling task and continue.

If the task does not map cleanly to these steps, use your native planning tool to build a plan from the commands/constraints in this skill, then execute it.

## Common Mistakes

- **Premature convergence.** Collapsing onto the first plausible/implementable route before a real alternative set exists. Reopen divergence with at least two different lenses.
- **Novelty without value / value without differentiation.** Letting "nobody has tried this" do all the work, or promoting a route that close prior work already dominates. Run the problem-value test and tighten the related-work map; route back to `scout` if needed.
- **Complexity worship / analogy by metaphor.** Promoting many moving parts with weak causal justification, or a cross-domain import whose mechanism does not really map. Run the simplicity test; rewrite the analogy in causal language and reject if the structure does not survive.
- **Forcing a baseline route.** Picking attach/import/reproduce without comparing the options, or trusting a baseline on memory alone when primary sources/durable quest files exist. Always compare routes; search for disconfirming evidence, not only supportive evidence.
- **Search exhaustion instead of stop-on-clarity.** Collecting "nice to know" papers after the next anchor is already clear. Stop once the task frame, eval contract, baseline direction, and next anchor are decision-ready.
- **Skipping the pre-idea draft or the quality gate.** Submitting a final idea without a durable challenge memo, or promoting below `7/10`. Both are hard gates.
- **Treating this as a state surface.** Never finalize, mutate results, confirm GPU, or change quest state from here. The `--via` stamp is read-only and records no row.

## Rationalizations and Red Flags

| Rationalization (do NOT accept) | Required behavior |
| --- | --- |
| "This route is implementable, let's just run it." | Run a bounded divergence pass first unless durable evidence already forces the route (and then record why a broader pass was unnecessary). |
| "It's novel — that's enough." | Novelty without a passing problem-value test is not promotable; label honestly. |
| "Close prior work is similar but ours is a bit different." | If `not sufficiently differentiated`, do not promote; only `novel` or `incremental but valuable` are eligible. |
| "The mechanism is complex because the problem is hard." | Run the simplicity test; reduce to the smallest mechanism that could still work. |
| "Memory says this baseline is fine." | Verify against primary sources / durable quest files; compare attach/import/reproduce. |
| "Score is 6/10 but it's exciting." | Hard gate: do not promote below `7/10`. |
| "I can just record the durable framing myself." | Record only through your role's normal commands / `$HARNESS record apply`; this skill changes no state. |

## Objective Contract

Use at the start of an `idea` pass whenever the real target might differ from the easiest available surrogate. The goal is to prevent ideation from drifting into "optimize what is measurable" when the real objective is narrower, more fragile, or more deployment-constrained.

Minimal fields:

- `primary_objective` — the real target the next route should improve
- `scoreboard_metric` — the single metric or ranking surface the quest is actually judged by
- `trusted_proxy_metrics` — the proxies that are allowed to influence direction choice
- `false_progress_signals` — local improvements that must not be mistaken for route health
- `hard_constraints` — constraints that invalidate a route even if metrics improve

Questions to answer:

1. What metric or region of behavior actually matters most?
2. Which proxies are trustworthy, and why?
3. Which proxies are only convenience signals rather than real progress?
4. What kind of apparent improvement would still count as failure?
5. Which leakage, deployment, submission-time, or comparability constraints must remain inviolable?

Example shape:

```md
# Objective Contract

- primary_objective:
  - Improve the real target metric, not just the easiest averaged surrogate.
- scoreboard_metric:
  - The metric or ranking surface that actually decides whether the route is better.
- trusted_proxy_metrics:
  - Proxy A because it tracks the head of the decision surface.
  - Proxy B because it reflects the main deployment tradeoff.
- false_progress_signals:
  - Lower average loss without improvement on the real decision region.
  - Better offline score using a feature that will not exist at deployment time.
- hard_constraints:
  - No submit-time unavailable features.
  - No leakage-prone labels or post-hoc ranking information in training.
```

Exit rule: do not widen the frontier until this contract is explicit enough to distinguish true progress, false progress, and invalid routes.

## Candidate Scoring

Score each candidate along explicit axes (full rubric in `references/ideation-craft.md`): relevance to the limitation, feasibility in the current codebase, expected upside, clarity of the two-sentence pitch, falsifiability, implementation cost, evaluation clarity, risk of confounding, novelty headroom, research value even if not fully novel, expected information gain, reusability as a platform capability, and `why now` credibility.

A compact strategist-style lens may supplement: `utility_score`, `quality_score`, `exploration_score` — explained in prose, used as a secondary decision lens, never as magic numbers. Prefer the best-explained choice over the best-sounding one. If a candidate scores weakly on novelty but strongly on research value, label that explicitly.

For each serious candidate, write a compact decision package: mechanism, expected gain, main risk, required files/components, likely metric effect, cheapest falsification path, strongest competing hypothesis, closest prior work and novelty/value verdict, and overlap with prior quest ideas or prior failed findings.

## Evaluation Contract

Use when the `scout` stage needs a durable evaluation contract.

```md
# Evaluation Contract

- task:
- dataset:
- dataset_version:
- split_contract:
- official_or_expected_eval_path:
- primary_metric:
- metric_direction:
- secondary_metrics:
- fair-comparison rule:
- useful-improvement threshold:

## Evidence
- paper paths:
- repo paths:
- benchmark docs:

## Known ambiguities
- ambiguity:

## Decision impact
- blocked_stage:
- why_it_matters:
```

The contract should be concise but explicit enough that `baseline`, `idea`, and `experiment` do not keep re-deriving it.

## Baseline Shortlist

Use when `scout` must recommend a concrete baseline route.

```md
# Baseline Shortlist

## Candidate 1
- name:
- source_paper_or_repo:
- route: attach | import | reproduce | reject
- provenance_trust:
- metric_split_match:
- implementation_availability:
- environment_risk:
- expected_cost:
- downstream_value:
- why_it_matters:
- main_risk:

## Candidate 2
- name:
- source_paper_or_repo:
- route:
- provenance_trust:
- metric_split_match:
- implementation_availability:
- environment_risk:
- expected_cost:
- downstream_value:
- why_it_matters:
- main_risk:

## Recommendation
- recommended_candidate:
- recommended_route:
- why_this_route_now:
- fallback_route:
```

The shortlist should end with one recommended route, not only a list of options.

## Selection Gate and Handoff

Use when choosing the final idea and preparing the handoff to `experiment`.

### 1. Value and feasibility screen

Before promotion, score each serious candidate on a compact `1-5` scale: importance, novelty, feasibility, verifiability, paper or report potential, failure value, breakthrough or boundary-changing potential.

Also check the FINER-style screen explicitly:

- `F` — feasible with current data, compute, codebase, and schedule
- `I` — interesting enough that the field would care
- `N` — novel in a meaningful sense relative to the strongest nearby work
- `E` — ethically acceptable and not obviously high-risk
- `R` — relevant to an important bottleneck rather than a decorative tweak

If the route scores poorly on both value and feasibility, do not promote it merely because it feels exciting. If the route is only a small local tweak, require an explicit justification for why a more differentiated route did not survive.

### 2. Lightweight quality gate

Score the final serious candidate on a `0/1/2` scale:

- novelty — `0` obvious tweak / `1` moderate variant / `2` clear non-trivial mechanism change
- falsifiability — `0` vague claim / `1` partially testable / `2` explicit metric, direction, and boundary condition
- feasibility — `0` unclear implementation path / `1` large refactor risk / `2` minimal touchpoints clearly identified
- evidence quality — `0` no credible citation / `1` weak or indirect support / `2` directly relevant papers plus baseline evidence
- constraint fit — `0` violates constraints / `1` uncertain fit / `2` fully compliant with dataset, protocol, and compute limits

If total `< 7/10`, do not promote the idea yet. Also treat these as hard gates before promotion:

- the literature survey must already durably cover at least `5` and usually `5-10` related and usable papers
- the survey must show both the strongest direct-field overlap and any adjacent-domain mechanisms that could plausibly subsume or outgrow the candidate
- a pre-idea draft or equivalent durable challenge memo must already exist for the serious surviving candidates, especially the likely winner
- that draft must explicitly surface hidden assumptions, local-optimum lock-in risk, strongest rejection case, and strongest outside-family alternative
- the closest-prior-work comparison must explain why the idea is still needed
- the selected route must be classified honestly as breakthrough-seeking, clearly differentiated, or incremental-with-justification; default rejection applies to decorative tweaks
- the final selected-idea draft must be ready to carry standard-format citations for the papers actually used

### 3. Honest novelty / value labels

- `novel`: closest prior work does not already make the same mechanism-plus-claim combination, and the route is materially more than a cosmetic delta from the baseline
- `incremental but valuable`: overlap exists, but the new setting, evidence package, or failure-mode resolution is still meaningful
- `not sufficiently differentiated`: closest prior work already dominates the idea

Only the first two are eligible for promotion. Even then, prefer `novel` when it remains feasible.

### 4. Mechanism and falsification gate

Before a candidate can be promoted, it should make explicit: core hypothesis, mechanism sketch, strongest falsification experiment. The mechanism sketch can be brief, but it must answer:

- why should this route work at all?
- what part of the current limitation does it change?
- for whom, where, or under what condition should it work or fail?

If the mechanism sketch or strongest falsification experiment is still vague, the route is not yet ready.

### 5. Handoff fields for experiment

The selected idea record should include: stable idea id; `motivation` in SCQA form; `reasoning` with main hypothesis plus `2-3` competing hypotheses near the top; `claim` as one falsifiable sentence tied to `metric_key`, expected direction, and boundary condition; `theory_and_method`; `code_level_plan`; `relation_to_literature`; `references` or `bibliography` in a standard citation format; and evidence or source pointers.

Inside the implementation handoff, also include: `metric_key`, `expected_direction`, `minimal_experiment`, `abandon_condition`, `strongest_alternative_hypothesis`.

### 6. Recommended presentation shape

Use a compact Pyramid structure: first line is the falsifiable claim plus metric focus plus boundary condition; then `3-6` bullets of reasoning and evidence pointers; then the minimal validation plan; then a short `References` or `Bibliography` section that cites the survey-stage papers actually used.

### 7. Promotion gate

Do not promote a candidate if any of these remain unclear: what exactly is being claimed; how the claim differs from closest prior work; what hidden assumption is carrying most of the route; whether the route only looks best because of incumbent inertia or implementation convenience; what minimal experiment can refute it; which code touchpoints are affected; what evidence package would later defend it in writing; which `5-10` surveyed papers actually support the motivation, mechanism, and claim boundary; whether the final idea draft includes proper citation markers plus a standard-format reference list; why this route deserves promotion over simpler but lower-value tweaks and over more ambitious but still feasible alternatives.

## Detail References (inside this skill)

- `references/ideation-craft.md` — full creative-divergence lens catalog, framework-selection dispatch table, Diverge/Converge/Refine workflow, failure-mode-to-recovery taxonomy, candidate scoring rubric, baseline-reconstruction + improvement-potential rating, two-layer direction format, draft-before-submit SOP, and memory/search reuse discipline. (Kept as a `references/` page because the source content exceeds ~200 lines.)
- `references/scout-framing.md` — full scouting judgment narrative: four framing layers, search-for-disconfirming-evidence rule, truth sources, the 8-step detailed workflow, search ladder + stop rules, blocked-state handling, and exit criteria. (Kept as a `references/` page for the same reason.)

## Audit / Boundaries

- `$HARNESS --via skill:deepresearch-ideation-rubric:<role>` is passed for traceability; it is read-only, so it records no row.
- Never finalize, mutate results, confirm GPU, or change quest state from here.
- Map any external tool names in the references (`artifact.*`, `memory.*`, `bash_exec`) to the `$HARNESS` surface; the DB stays canonical and this craft is advisory, never an authoritative state surface.
- Durable paths shown as `artifacts/...` map to `runs/<quest-id>/...`. Quest isolation is total: never reuse, refer to, or inspect another quest's artifacts/findings/refs.
