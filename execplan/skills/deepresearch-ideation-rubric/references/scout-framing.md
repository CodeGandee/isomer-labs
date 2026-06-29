# Scout Framing (judgment narrative)

Scout framing craft. Use this reference when the quest does not
yet have a stable research frame and you need the full scouting judgment
narrative — the four framing layers, the baseline-route comparison, blocked-state
handling, the search ladder, and the stop-on-clarity discipline.

> Houmao tool-name mapping: where this file shows external tool calls
> (`artifact.*`, `memory.*`, `bash_exec(...)`), map them to the Houmao surface:
> durable framing records (evaluation contract, baseline direction, next-anchor)
> go through `$HARNESS record apply`; methodology lookups go through
> `$HARNESS knowledge cards` / `knowledge query`; quest/run state reads go
> through `$HARNESS state query`; any shell/CLI/git/repo inspection goes through
> your role's normal command surface. The DB stays canonical; this file is
> advisory craft. Durable paths shown as `artifacts/...` map to
> `runs/<quest-id>/...`.

## One-sentence summary

Resolve only the minimum framing unknowns that change the next anchor, then stop
once baseline or idea becomes durable and obvious. The right output is a durable
frame, not search exhaustion.

## The four framing layers

A scout pass should usually establish four layers. If one of the core layers is
still missing, say so explicitly instead of pretending the frame is complete.

1. **Task-definition layer.** What is the current task, who suffers from the
   open problem, and what is actually being asked? Make the task frame concrete
   enough that a heavier stage can start with confidence.
2. **Evaluation-contract layer.** The dataset, split/partition, primary metric,
   any secondary metrics, what counts as a useful improvement, and what
   comparisons will be considered fair.
3. **Literature and repo-neighborhood layer.** A compact but sufficient
   neighborhood of references and implementations — enough to know the strongest
   obvious neighbors, the closest competitors, and the provenance of any claimed
   baseline.
4. **Baseline-direction layer.** At least one justified baseline direction, with
   a recommended route (attach / import / reproduce / reject).

## Search for disconfirming evidence, not only supportive evidence

This is a non-negotiable rule. When checking whether a gap is real, a baseline
is trustworthy, or a novelty claim holds, actively look for evidence that would
**break** the current frame, not only evidence that confirms it. Do not inflate
novelty when the apparent gap is already closed by straightforward scaling,
standard engineering, or a strong recent paper. Other non-negotiables:

- Do not force a baseline route without comparing attach, import, and reproduce
  options.
- Do not rely on memory alone when primary sources or durable quest files exist.

## Truth sources (in order)

1. user-provided task description and explicit constraints
2. durable quest files and artifacts
3. codebase and repository docs
4. primary papers, official repos, and benchmark docs
5. existing reusable baselines and quest/global memory
6. web-search results, often including arXiv and adjacent sources, used to fill
   gaps, verify provenance, or update recency

Do not let the scout stage rest on vague recollection alone.

## Detailed workflow

### 1. Reconstruct the current frame

Summarize: current task, current dataset and split understanding, current metric
contract, current baseline status, current blockers. If this can already be
stated precisely, scouting may be complete immediately.

Before spending time scouting, first verify whether the current quest already
contains enough framing in `brief.md`, `plan.md`, `status.md`, `SUMMARY.md`,
baseline artifacts, and recent paper/knowledge memory cards. If the answer is
already clear, exit quickly and move to the correct next anchor.

### 2. Identify the minimum unknowns

List only the unknowns that materially affect later stages, such as: unclear
evaluation metric, multiple conflicting dataset splits, missing baseline
candidate, unclear repo or paper provenance, missing source paper for a claimed
baseline. Avoid collecting "nice to know" facts that do not change the next
stage. Classify each unknown:

- blocks `baseline`
- blocks `idea`
- blocks both
- useful but non-blocking

### 2.1 Reuse durable state before broad new search

Before a fresh wide search, quickly reuse existing quest state and memory so
scouting only fills real gaps instead of restarting from zero.

Stage-start requirement (surface; map to Houmao knowledge/state):

- begin every scout pass with `memory.list_recent(scope='quest', limit=5)`
- then run at least one scout-relevant `memory.search(...)` before broad new
  search
- if several lines already exist, narrow retrieval to the current task,
  benchmark, dataset, metric, split, and likely baselines

If the frame is already explicit after memory reuse, stop and record the next
anchor.

### 3. Search the paper and repo neighborhood

Build a compact but sufficient neighborhood of references and implementations.
Use external search actively when local evidence is not enough. For papers that
survive triage and need real reading, switch from discovery to reading:

- use web search to find the paper
- then use `artifact.arxiv(paper_id=..., full_text=False)` to read or summarize
  it
- only switch to `full_text=True` or the raw PDF when the shorter view does not
  cover the needed detail

Search only the unresolved neighborhood that still changes framing, evaluation,
or baseline choice. Use a compact search ladder:

1. direct neighborhood: same task, dataset, and metric
2. mechanism neighborhood: same main lever, objective, or architectural trick
3. bottleneck neighborhood: same failure mode, evaluation caveat, or boundary
   condition

### 4. Clarify the evaluation contract

Produce an explicit statement of: task, dataset, split or evaluation partition,
primary metric, secondary metrics if necessary, what counts as a useful
improvement, and what comparisons will be considered fair. The evaluation
contract should be strong enough that later `baseline`, `idea`, and `experiment`
work do not need to keep re-deriving it. If it is still ambiguous after local
analysis, ask the user for a structured decision instead of guessing.

### 5. Produce a baseline shortlist (attach / import / reproduce route comparison)

End scouting with a clear baseline direction. For each serious candidate, score
at least:

- trustworthiness of provenance
- metric and split compatibility
- implementation availability
- reproduction or import cost
- value as a downstream comparison reference

Each candidate should lead to one recommended route:

- **attach** an existing baseline
- **import** a reusable baseline package
- **reproduce** a baseline from source
- **reject** this candidate

For each serious candidate, also state:

- whether it is a direct baseline, a strong competitor, or only an adjacent
  reference
- whether the repo path or paper evidence is strong enough to trust the route
- the cheapest credible next action: attach, import, reproduce, or reject

Keep the shortlist small and decision-facing rather than turning it into a broad
survey of every plausible baseline.

### 6. Recommend the next anchor

Do not stop with a list of possibilities. Choose the most justified next anchor:

- `baseline`
- `idea`
- remain in `scout`

`idea` is only justified when the baseline is already durable and trustworthy
enough. If no usable baseline exists, prefer `baseline`.

### 7. Update quest continuity

If the frame changed, update `brief.md`, `plan.md`, `status.md`, then record a
durable report or decision showing the recommended next anchor.

### 8. Stop on clarity, not exhaustion

The stage is done when the framing is decision-ready, not when every curiosity
is satisfied. Stop once all of the following are true:

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

Do not continue searching just to collect more papers after the next anchor is
already clear.

## Blocked-state handling

Record a blocked state if scouting cannot proceed because:

- the quest objective is materially ambiguous
- the required code or paper source is missing
- multiple evaluation contracts conflict and the choice would change later
  conclusions
- all baseline candidates are too weak, broken, or poorly specified

A blocked scout result should state: what is missing, why it matters, which next
anchor is blocked, and what concrete user choice or source is needed. Do not
hide a blocked scout stage behind generic literature chatter.

## Planning, durable-output, memory, and artifact notes

- **Planning note.** Use quest or workspace planning files only when scouting
  becomes a real multi-step framing pass instead of a short clarification step.
- **Durable-output note.** When scout matters, leave behind just enough durable
  framing state to make the next anchor obvious rather than building a large
  documentation package by default. If external search materially changed the
  frame, leave a literature scouting report rather than letting the survey live
  only in chat.
- **Thinking note.** Keep scout conclusion-first and bounded: identify the
  minimum unknowns, resolve only the ones that change the next stage, then stop.
- **Memory note.** Use memory to avoid repeating old scouting work and to
  preserve reusable framing conclusions, but do not let memory-writing become the
  stage's main output. Stage-end requirement: if scouting produced a durable
  framing conclusion, literature scouting report, baseline-shortlist lesson, or
  metric-contract caveat, write at least one durable record before leaving the
  stage.
- **Artifact note.** Record only the framing outputs the next stage will
  actually consume, such as the evaluation contract, baseline direction, or
  next-anchor recommendation.

## Exit criteria

Exit the scout stage once the task frame is explicit, the evaluation contract is
explicit, at least one baseline direction is justified, and the next anchor is
obvious enough to record durably. If the stage relied on external search, the
literature scouting report must also be durable before exit. A good scout pass
makes the next anchor obvious or makes the blocker explicit enough that the
system stops guessing.
