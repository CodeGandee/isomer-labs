# Current Board Packet

Use this reference when the intake result must give the next skill one authoritative board surface instead of forcing it to merge stale summaries, conversation context, file state, and partial Artifacts again.

## Required Fields

- current mainline: the accepted research line or paper line that later stages should treat as active.
- incumbent: the accepted baseline, method, draft, report, or bundle currently defining comparison.
- latest decisive result: the most recent Evidence Item or Decision Record that changed the route.
- active blocker: the unresolved missing evidence, Gate, broken comparability, or unclear instruction that blocks progress.
- stale routes to ignore: routes, branches, drafts, or old claims that should not be reopened without new evidence.
- next decision scope: the narrow question the next skill should resolve.
- budget class: expected cost or risk class for the recommended next stage.
- trust summary: which assets are accepted, usable with verification, reference-only, stale, conflicting, or missing context.
- provenance note: where the main assets came from and why they are trusted enough for reuse.

## Decision-Facing Packet Shape

```md
# Current Board Packet

## Active Scope
- Research Inquiry or Research Task:
- current mainline:
- incumbent:
- recommended next Workflow Stage:

## Trusted Evidence
| Evidence Item or Artifact | Role | Why trusted | Caveat |
| --- | --- | --- | --- |

## Assets Needing Verification
| Asset | Required verification | Blocking stage | Owner or Gate |
| --- | --- | --- | --- |

## Stale or Conflicting Assets
| Asset | Why stale or conflicting | Do-not-reopen condition |
| --- | --- | --- |

## Next Decision Scope
- exact question:
- strongest support:
- strongest contradiction:
- budget class:
- expected next output:
```

## Handoff Rules

- Keep the packet compact enough that the next skill can read it before acting.
- Include negative, partial, failed, blocked, or contradictory evidence when it changes routing.
- Do not include every inspected file or note if it does not affect the next route.
- Do not call the board authoritative until unresolved conflicts and missing proof are named.
