# Pre-Idea Draft Template

Use this reference after bounded brainstorming and before formal idea submission.

Default durable path: `artifacts/idea/pre_idea_drafts/<candidate_id>.md`.

The goal is to force each serious candidate through one compact written stress test before it can be promoted.
This draft is not the final selected-idea submission.
It is the last place to expose hidden assumptions, local-optimum lock-in, and the strongest rejection case while the route is still cheap to discard.

## When to write it

Write a pre-idea draft for each serious surviving candidate.
Normally this means the top `1-3` candidates after the raw slate has been collapsed.

Do not spend this draft effort on every raw idea.
The purpose is to challenge the finalists, not to create paperwork for weak candidates that should already have been filtered out.
If a candidate survives multiple revisions in the same pass, keep updating the same durable draft path instead of scattering ad hoc filenames.

## Minimal fields

- `candidate_id`
- `candidate_family`
- `one-sentence claim`
- `targeted contradiction or bottleneck`
- `why_now`
- `dominant novelty type`
- `closest prior work`
- `hidden assumptions`
- `local_optimum_lock_in_risk`
- `outside_family_or_assumption_reversal_alternative`
- `strongest rejection case`
- `core hypothesis`
- `strongest falsification path`
- `minimal experiment`
- `abandonment condition`
- `promotion verdict`

## Questions the draft must answer

1. What exact contradiction, anomaly, or bottleneck is this candidate targeting?
2. Why is this candidate more than a decorative tweak?
3. What assumptions about the bottleneck, data, objective, evaluator, or systems boundary must hold for it to work?
4. Which of those assumptions is most fragile or least justified?
5. Are we favoring this candidate because it is actually best, or because it is familiar, already partially implemented, or easiest to ship?
6. What outside-family or assumption-reversal route would still be plausible if the current framing is wrong?
7. What is the strongest reason to reject this candidate right now?
8. What is the cheapest falsification path?
9. What result would immediately demote or kill this route?

## Recommended shape

```md
# Pre-Idea Draft: <candidate_id>

- candidate_family:
- one-sentence claim:
- targeted contradiction or bottleneck:
- why_now:
- dominant novelty type:

## Literature grounding

- closest prior work:
- what remains unresolved:
- why this is not just a local tweak:

## Hidden assumptions

- assumption 1:
- assumption 2:
- most fragile assumption:

## Local-optimum lock-in check

- why this route is currently attractive:
- what part of that attraction may just be convenience or incumbent inertia:
- outside-family or assumption-reversal alternative still worth keeping alive:

## Rejection case

- strongest reason to reject now:
- strongest competing alternative:
- what evidence would make that alternative preferable:

## Testability

- core hypothesis:
- strongest falsification path:
- minimal experiment:
- abandonment condition:

## Draft verdict

- promote / defer / reject:
- reason:
```

## Exit rule

Do not promote a candidate into the formal selected-idea package until this draft makes the route look stronger than:

- the incumbent continuation
- the easiest small tweak
- at least one outside-family or assumption-reversal alternative
