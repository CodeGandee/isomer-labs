# Claim Ledger

Use this reference when finalization must separate supported, partial, failed, refuted, deferred, and open claims.

## Claim Statuses

- supported: durable Evidence Items support the claim under the stated metric, dataset, protocol, and caveat boundary.
- partially supported: evidence supports a narrower or weaker claim than the draft or goal originally implied.
- unsupported: the evidence does not support the claim.
- refuted: durable evidence contradicts the claim or shows the route failed.
- deferred: the claim may be answerable later but was intentionally left out of the final recommendation.
- open: the claim remains unresolved and still matters for future work.

## Minimum Ledger Fields

| Claim or claim id | Status | Evidence Items | Caveats | Safe to surface | Reopen condition |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Belief-Change Log

Record major transitions such as supported to partial, partial to unsupported, promising route to abandoned, draft-ready to evidence-gap, or baseline-ready to comparator-blocked.

For each transition, record what changed, which Evidence Item or Decision Record caused the change, and what the new recommendation is.

## Writing and Publication Boundary

Only claims marked supported or carefully scoped partial should appear in final summaries, reports, or manuscript main text. Negative and refuted claims remain valuable evidence, but they need clear framing and should not be disguised as support.

If concrete Research Claim fields matter, use the accepted Research Claim fields.
