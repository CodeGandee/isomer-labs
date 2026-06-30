# Operational Guidance

Use this reference when the scout route needs the longer tactical notes rather than the short control surface in `SKILL.md`.

## Planning note

Use quest or workspace planning files only when scouting becomes a real multi-step framing pass instead of a short clarification step.

## Durable-output note

When scout matters, leave behind just enough durable framing state to make the next anchor obvious rather than building a large documentation package by default.
If external search materially changed the frame, leave a literature scouting report rather than letting the survey live only in chat.
Prefer the structure in `references/literature-scout-template.md`.

## Thinking note

Keep scout conclusion-first and bounded: identify the minimum unknowns, resolve only the ones that change the next stage, then stop.

## Detailed workflow

### 1. Reconstruct the current frame

Summarize:

- current task
- current dataset and split understanding
- current metric contract
- current baseline status
- current blockers

If this can already be stated precisely, scouting may be complete immediately.

### 2. Identify the minimum unknowns

List only the unknowns that materially affect later stages, such as:

- unclear evaluation metric
- multiple conflicting dataset splits
- missing baseline candidate
- unclear repo or paper provenance
- missing source paper for a claimed baseline

Avoid collecting "nice to know" facts that do not change the next stage.

Also classify each unknown:

- blocks `baseline`
- blocks `idea`
- blocks both
- useful but non-blocking

### 2.1 Reuse durable state before broad new search

Before a fresh wide search, quickly reuse existing quest state and memory so scouting only fills real gaps instead of restarting from zero.

Stage-start requirement:

- begin every scout pass with `memory.list_recent(scope='quest', limit=5)`
- then run at least one scout-relevant `memory.search(...)` before broad new search
- if several lines already exist, narrow retrieval to the current task, benchmark, dataset, metric, split, and likely baselines

If the frame is already explicit after memory reuse, stop and record the next anchor.

### 3. Search the paper and repo neighborhood

Build a compact but sufficient neighborhood of references and implementations.

Use external search actively when local evidence is not enough.

For papers that survive triage and need real reading, switch from discovery to reading:

- use web search to find the paper
- then use `artifact.arxiv(paper_id=..., full_text=False)` to read or summarize it
- only switch to `full_text=True` or the raw PDF when the shorter view does not cover the needed detail

Search only the unresolved neighborhood that still changes framing, evaluation, or baseline choice.
Use a compact search ladder:

1. direct neighborhood:
   - same task, dataset, and metric
2. mechanism neighborhood:
   - same main lever, objective, or architectural trick
3. bottleneck neighborhood:
   - same failure mode, evaluation caveat, or boundary condition

For a more explicit search and triage method, read `references/paper-triage-playbook.md`.

### 4. Clarify the evaluation contract

Produce an explicit statement of:

- task
- dataset
- split or evaluation partition
- primary metric
- secondary metrics if necessary
- what counts as a useful improvement
- what comparisons will be considered fair

The evaluation contract should be strong enough that later `baseline`, `idea`, and `experiment` work do not need to keep re-deriving it.

If the evaluation contract is still ambiguous after local analysis, ask the user for a structured decision instead of guessing.

### 5. Produce a baseline shortlist

End scouting with a clear baseline direction.

For each serious candidate, score at least:

- trustworthiness of provenance
- metric and split compatibility
- implementation availability
- reproduction or import cost
- value as a downstream comparison reference

Each candidate should lead to one recommended route:

- attach an existing baseline
- import a reusable baseline package
- reproduce a baseline from source
- reject this candidate

For each serious candidate, also state:

- whether it is a direct baseline, a strong competitor, or only an adjacent reference
- whether the repo path or paper evidence is strong enough to trust the route
- the cheapest credible next action: attach, import, reproduce, or reject

Keep the shortlist small and decision-facing rather than turning it into a broad survey of every plausible baseline.

### 6. Recommend the next anchor

Do not stop with a list of possibilities.
Choose the most justified next anchor:

- `baseline`
- `idea`
- remain in `scout`

`idea` is only justified when the baseline is already durable and trustworthy enough.
If no usable baseline exists, prefer `baseline`.

### 7. Update quest continuity

If the frame changed, update:

- `brief.md`
- `plan.md`
- `status.md`

Then record a durable report or decision showing the recommended next anchor.

### 8. Stop on clarity, not exhaustion

The stage is done when the framing is decision-ready, not when every curiosity is satisfied.

Stop once all of the following are true:

- the task frame is explicit enough
- the evaluation contract is explicit enough
- the baseline direction is justified enough
- the next anchor is durable and obvious

## Search stop rules

Stop literature and repo search when:

- the strongest obvious local neighbors are mapped
- the evaluation contract no longer depends on unknown sources
- at least one baseline route is clearly better than the alternatives
- additional papers are no longer changing the next action

Continue searching only if:

- metric or split ambiguity remains
- the current shortlist is too weak or conflicting
- provenance of the likely baseline is still uncertain

Do not continue searching just to collect more papers after the next anchor is already clear.

## Memory note

Use memory to avoid repeating old scouting work and to preserve reusable framing conclusions, but do not let memory-writing become the stage's main output.

Stage-end requirement:

- if scouting produced a durable framing conclusion, literature scouting report, baseline-shortlist lesson, or metric-contract caveat, write at least one `memory.write(...)` before leaving the stage

## Artifact note

Record only the framing outputs that the next stage will actually consume, such as the evaluation contract, baseline direction, or next-anchor recommendation.
