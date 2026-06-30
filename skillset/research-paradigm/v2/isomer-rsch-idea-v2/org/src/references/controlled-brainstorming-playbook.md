# Controlled Brainstorming Playbook

Use this reference when the current route is not already obvious and `idea` needs a real divergence pass.

The goal is not open-ended ideation.
The goal is a bounded, differentiated slate that is broad enough to avoid premature convergence and narrow enough to remain auditable.

## 1. Enter only after framing

Before brainstorming, make sure both of these already exist:

- an objective contract
- a current board packet

If either is still fuzzy, do not widen yet.

## 2. Choose the family mix first

Decide which route families are allowed in this pass:

- `mechanism_family`
  - new algorithmic or modeling idea
- `objective_family`
  - change the training target, ranking target, or optimization target
- `measurement_family`
  - change the evaluator, validation lens, or what is being trusted
- `infrastructure_family`
  - change throughput, batching, staging, or other system constraints that affect useful iteration

Do not default to mechanism-family routes only.

## 3. Generate a bounded slate

Default target:

- `6-12` raw ideas
- collapse to a serious frontier of `2-3`, and at most `5`

Require visible differentiation:

- one local refinement of the incumbent
- one orthogonal alternative
- one route that changes the objective or measurement layer when that layer may be wrong
- one infrastructure or iteration-speed route when throughput itself is blocking progress

## 4. Filter aggressively

Discard or downgrade candidates that:

- only improve a surrogate without changing the real objective
- violate hard constraints
- are just within-family micro-variants
- reopen stale routes without new evidence
- have no cheap falsification path

## 5. Force `why now`

Every serious candidate must answer:

- what changed?
- why now?
- why this family instead of the current mainline?

If the answer is weak, the candidate should usually not survive.

## 6. End with a structured selection

The final serious candidates should each include:

- family type
- targeted limitation
- why now
- strongest prior-work overlap
- anti-win condition
- minimal validation
- abandonment condition

The selected route should beat the others on evidence-per-run, not just novelty theater.
