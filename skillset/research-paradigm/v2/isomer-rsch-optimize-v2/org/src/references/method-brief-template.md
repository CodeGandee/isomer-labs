# Method Brief Template

## Title

One short line naming the candidate direction.

## Bottleneck

What concrete bottleneck or limitation does this target?

## Why Current Line Is Limited

Why is the current best line or baseline not already solving this?

## Mechanism

What specific intervention or design change is proposed?

## Mechanism Family

Name the family explicitly, for example `adapter`, `loss`, `architecture`, `augmentation`, `ensemble`, `retrieval`, `objective-shift`.

## Change Layer

One of:

- `Tier1`: local optimization / training detail
- `Tier2`: representation or component change
- `Tier3`: paradigm or system-level shift

## Source Lens

Where did this candidate come from?

- baseline_refinement
- orthogonal_mechanism
- failure_repair
- cross_domain_transfer
- objective_shift
- search_widening

## Keep Unchanged

What must remain stable for comparability?

## Expected Gain

What evidence should improve if this works?

## Implementation Surface

- main files or modules likely involved:
- likely change scope: local / moderate / broad

## Risks

- Main failure mode
- Comparability risk
- Implementation risk

## Foundation

- Source branch / run / baseline:
- Why this foundation is the right starting point:

## Promote Now

- yes / no
- why:

## Next Target

Usually `optimize` or `experiment`.
