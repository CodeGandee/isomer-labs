# Research-contract expansion (domain-neutral)

> **Status: ACTIVE.** This file defines the *rubric* for turning a minimal operator
> prompt into a deeper, operator-approved research contract **before** a quest is created. Enforcement is
> live: the pre-launch skill `deepresearch-research-contract` runs the expansion, and the harness
> **hard-gates** `not_started → running` on an approved `kind='research-contract'` artifact (a sibling of the
> clarification, GPU, and Claude-conditional effort-selection gates, in
> `execplan/harness/src/records.py::_contract_gate`). See
> `execplan/docs/start-runbook.md` (Step 3a) for the operational steps.

## Why this exists

The operator's new-quest template is intentionally minimal:

```
Objective: <one or two lines>
Acceptance: <one or two lines>
```

A minimal Objective/Acceptance tends to collapse into a **single shallow threshold** ("MAPE ≤ 10 %",
"accuracy ≥ 90 %", "p99 < 50 ms", "significant difference"). A loop pointed at a shallow gate will stop the
moment the number is cleared — producing a *correct-but-thin* result that explains little, isolates no
mechanism, rules out no alternative, and is not positioned against prior work. (This is the gap a side-by-side
with a stronger system surfaced: comparable headline accuracy, much weaker science.)

**Contract expansion** reads the minimal Objective/Acceptance and proposes a *deeper scientific done-bar* —
a falsifiable claim, a mechanism requirement, a baseline/ablation, an alternative to rule out, a scope
statement, scholarly positioning, and evidence traceability — then asks the operator to **approve, edit, or
trim** it before the quest is created. The goal: a weak prompt becomes a high-quality research contract, and
the loop optimizes *understanding*, not a number.

This rubric is **general-purpose and domain-neutral**. It assumes nothing about GPUs, kernels, or
performance modeling; it applies equally to ML, systems, wet-lab biology, and social-science-style studies.

## The expansion rubric (eight dimensions)

For each dimension: the *symptom* of a minimal prompt, and the *expanded done-condition* it should become.
Not every dimension is mandatory for every quest — see **Over-hardening** below. Treat this as a checklist to
*consider and consciously include or waive*, not a quota to fill.

1. **Question & falsifiable claim.**
   *Symptom:* an open verb ("improve", "test", "build a model of"). *Expanded:* a precise, falsifiable
   claim with a named subject, comparator, condition, and effect — phrased so it *could* come out false.
   "Method M raises <metric> by ≥ Δ over baseline B under fixed budget" beats "improve <metric>".

2. **Mechanism / explanation.**
   *Symptom:* the done-bar measures only *how much*. *Expanded:* require an account of *why* — the
   mechanism, the dominant factor, or the causal pathway — supported by evidence, not asserted.

3. **Baseline & fair comparison.**
   *Symptom:* a target number with nothing to compare against. *Expanded:* name a fair comparator (a
   standard/published baseline, the current production config, a control group/condition) and require the
   result to be reported *relative* to it.

4. **Ablation / factor isolation.**
   *Symptom:* the whole change is evaluated as a block. *Expanded:* isolate the operative factor — remove or
   vary the key component and show the effect tracks it. This is what separates "it works" from "this is
   *why* it works."

5. **Alternative-hypothesis falsification.**
   *Symptom:* one explanation is assumed. *Expanded:* name the leading competing explanation and a concrete
   way to rule it out. (E.g., "the gain is just more compute/data", "the effect is a confound", "decode is
   memory-latency-bound") — and a control or probe that would distinguish it. *When two models fit equally,
   the better science kills the alternative.*

6. **Scholarly positioning.**
   *Symptom:* no relation to prior work. *Expanded:* situate the contribution against external prior art —
   what others did, how this differs or improves — with real citations and a Related Work section. (See
   `execplan/docs/publication-quality.md` for the scholarship bar this becomes at finalize.)

7. **Scope & generalization boundaries.**
   *Symptom:* a single point or an unstated range. *Expanded:* state the conditions/coverage actually tested
   (the grid, population, regimes, sizes) and where the claim is *not* asserted — explicit boundaries beat
   silent over-generalization.

8. **Reproducibility & evidence traceability.**
   *Symptom:* a headline number with no trail. *Expanded:* every reported claim traces to recorded evidence
   (configs, seeds, repetitions, raw measurements, analysis rows); state any method constraints the domain
   requires (e.g. "no fitting", pre-registered analysis, n ≥ k replicates).

## How a minimal Objective/Acceptance is expanded

1. **Read** the operator's Objective + Acceptance verbatim.
2. **Draft** an expanded `objective.md` + `acceptance.md` that folds in the dimensions above that are
   *relevant and feasible* for this task and budget, plus a `contract.md` showing the original → expanded
   diff and a one-line rationale per added done-condition.
3. **Present** the expansion to the operator with **approve / edit / trim** per block (e.g. via the
   `AskUserQuestion` mechanism). The operator may drop any dimension, soften any threshold, or accept as-is.
4. **Fold** the approved edits back into `runs/<q>/objective/{objective,acceptance}.md` — these become the
   canonical brief the loop reads.
5. **Record** an approved `kind='research-contract'` artifact (`runs/<q>/objective/contract.md`) — the
   harness launch gate requires it before the quest can move to `running`.

The **acceptance** file is where the depth lands: a good expanded acceptance pairs the operator's metric
with mechanism, baseline/ablation, the ruled-out alternative, the scope, the scholarship requirement, and the
traceability constraint — each stated as a *checkable* done-condition.

## Cross-domain examples

Each shows a minimal prompt → the kind of expanded done-bar the rubric produces. These are illustrative, not
templates to copy verbatim.

### Machine learning
- **Minimal** — Objective: "Improve accuracy of model X on dataset Y." Acceptance: "Top-1 ≥ 90 %."
- **Expanded** — Claim: "Technique M raises top-1 by ≥ Δ over a strong baseline B at equal train compute
  and data." Mechanism: which component of M drives the gain. Baseline: a standard/published B, same
  protocol. Ablation: removing M's key component erases the gain. Alternative ruled out: the gain is not
  merely more compute/data/epochs (controlled). Scope: which data regimes/model sizes it holds for, and
  where it fails. Scholarship: positioned vs prior methods. Traceability: seeds, configs, eval protocol,
  variance. *Trim option:* operator may scope to one model size and record the rest as limitations.

### Systems / performance
- **Minimal** — Objective: "Make service S faster." Acceptance: "p99 < 50 ms."
- **Expanded** — Claim: "Change C reduces p99 by ≥ X % at fixed throughput vs the current config."
  Mechanism: which bottleneck C removes (profiled). Baseline: current production config. Ablation: reverting
  C returns the regression. Alternative ruled out: the gain is not warm-cache/measurement noise (repeated
  trials + confidence intervals). Scope: the load levels and payload sizes tested. Scholarship: related to
  known techniques for that bottleneck. Traceability: benchmark harness, repetition count, variance.

### Wet-lab biology
- **Minimal** — Objective: "Test whether compound K affects cell growth." Acceptance: "Significant
  difference."
- **Expanded** — Claim: "K reduces proliferation of line L vs vehicle control at dose D, effect size ≥ E."
  Mechanism: the proposed pathway + a marker/assay that supports it. Baseline/control: vehicle + a positive
  control. Ablation/dose-response: effect scales with dose; removing the target abolishes it. Alternative
  ruled out: the effect is not general cytotoxicity/confluence artifact (viability assay). Scope: which
  lines/doses; replicates n ≥ k. Scholarship: positioned vs literature on K and the pathway. Traceability:
  n, batches, the statistical test, a pre-specified analysis. *Trim option:* one cell line, dose-response
  deferred — recorded as a limitation.

### Social-science-style study
- **Minimal** — Objective: "Does intervention I improve outcome O?" Acceptance: "Positive effect."
- **Expanded** — Claim: "I increases O by effect size ≥ E vs a control group." Mechanism: the mediator /
  theory of change. Baseline/control: a control or comparison group; a pre-registered analysis. Ablation /
  dose: greater exposure to I yields a larger effect. Alternative ruled out: selection/confounding
  (randomization or covariate adjustment). Scope: the population and setting; external-validity boundaries.
  Scholarship: positioned vs prior studies. Traceability: sample, instruments, analysis plan, robustness
  checks.

## Over-hardening: keep it rigorous *and* achievable

A deeper done-bar is only useful if the quest can still finish. The central failure mode of contract
expansion is **over-hardening** — piling on required ablations, controls, and high thresholds until a
feasible study becomes impossible, or setting numeric bars no method can hit, or demanding data/infra that
isn't available. Guard against it:

- **Operator control is the primary safety valve.** The expansion is a *proposal*. The operator can
  **approve, edit, or trim** every block before launch, and should default to the *minimal sufficient* set
  for the task at hand.
- **Achievable & falsifiable, not merely hard.** Every done-condition must be checkable with the available
  budget and resources, and must be able to *fail informatively*. Prefer conditions that could come out
  false and teach something over arbitrarily high thresholds.
- **Proportional rigor.** Scale depth to stakes, scope, and budget (`max_rounds`, cost). A quick sanity
  check is not a flagship study; do not impose flagship rigor on a scoping quest.
- **Graceful degradation, not failure.** If a dimension turns out infeasible mid-quest, it downgrades to a
  *documented limitation* ("structural result + stated gap"), not a quest failure. Record the missing piece
  as future work. (This mirrors a healthy abandonment/downgrade clause: if a gap is only closable by
  fitting/fudging, downgrade and document rather than fake it.)
- **No moving goalposts.** Once the operator approves the contract, it is fixed for the run; changing it
  requires an explicit operator decision, so the loop cannot quietly soften its own bar to "pass".

The aim is a contract that is **demanding enough to force understanding, lenient enough to be finished, and
entirely under the operator's control before the loop starts.**
