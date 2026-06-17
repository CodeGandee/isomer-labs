# Method Brief

Use this template for a branchless candidate direction before it becomes a durable Research Branch.

## Template

```md
# Method Brief: <title>

## Bottleneck

What concrete bottleneck or limitation does this target?

## Why Current Line Is Limited

Why is the current best line or comparator not already solving this?

## Mechanism

What specific intervention or design change is proposed?

## Mechanism Family

Name the family explicitly, such as adapter, loss, architecture, augmentation, ensemble, retrieval, objective shift, evaluator repair, or infrastructure.

## Change Layer

- Tier1: local optimization or training detail.
- Tier2: representation or component change.
- Tier3: paradigm or system-level shift.

## Source Lens

- baseline refinement
- orthogonal mechanism
- failure repair
- cross-domain transfer
- objective shift
- search widening

## Keep Unchanged

What must remain stable for comparability?

## Expected Gain

What Evidence Item should improve if this works?

## Implementation Surface

- likely modules:
- likely change scope: local / moderate / broad

## Risks

- main failure mode:
- comparability risk:
- implementation risk:

## Foundation

- source Research Branch, Run, comparator, or Evidence Item:
- why this foundation is the right starting point:

## Promote Now

- yes / no:
- why:

## Next Target

Usually optimize or experiment.
```

## Promotion Rule

Do not promote a method brief into a Research Branch until expected value, differentiation, and execution path clarity justify the cost under `[[tbd-surface:policy-branching]]`.
