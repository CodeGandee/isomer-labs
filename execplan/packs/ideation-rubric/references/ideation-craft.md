# Ideation Craft (creative divergence, convergence, scoring)

Use this reference when the
idea stage needs the full divergence/convergence/refine craft, the lens
catalog, the failure-mode recovery taxonomy, the scoring rubric, and the
direction-shaping formats — not just the short playbooks.

> Houmao tool-name mapping: where this file shows external tool calls
> (`artifact.*`, `memory.*`, `bash_exec(...)`), map them to the Houmao surface:
> durable records and idea/decision submission go through `$HARNESS record apply`;
> methodology lookups go through `$HARNESS knowledge cards` / `knowledge query`;
> quest/run state reads go through `$HARNESS state query`; any shell/CLI/repo
> inspection goes through your role's normal command surface. The DB stays
> canonical; this file is advisory craft, never an authoritative state surface.
> Durable paths shown as `artifacts/idea/...` map to `runs/<quest-id>/...`.

## Stage purpose

The idea stage should not generate vague inspiration. It should produce
executable hypotheses tied to:

- the active baseline
- the current codebase
- the accepted evaluation contract
- the strongest relevant prior work

This stage is not just "brainstorming". It is a controlled brainstorming plus
route-selection stage. It still needs a bounded creative-divergence phase
before convergence. Do not collapse onto the first plausible route just because
it sounds implementable. Do not settle for a low-amplitude tweak when a
broader, still-feasible route remains live.

The output must survive three checks at once:

- novelty or at least clear research value
- feasibility in the current repo and resource budget
- manuscript defensibility if the line later becomes a paper claim

When multiple routes survive, prefer the most differentiated route that is
still falsifiable and executable in the current repo, rather than the easiest
tiny patch. At the direction level, prefer elegant algorithmic or theoretical
improvements over brute-force cost-for-performance tradeoffs whenever possible.

## Thinking protocol (MECE / SCQA / Pyramid discipline)

Use the old PI discipline. Your analysis should be:

- hypothesis-driven: viewpoint first, evidence second
- pyramid-shaped: conclusion first, then reasons, then action
- MECE where possible, across these buckets:
  - data
  - model
  - objective
  - optimization or training dynamics
  - inference
  - evaluation protocol
  - infrastructure
- SCQA-compatible:
  - situation
  - complication
  - research question
  - answer hypothesis plus `2-3` competing hypotheses

Do not dump disconnected observations. Turn them into a direction argument.

## Creative-divergence protocol: the lens catalog

Use deliberate ideation lenses before convergence when the route is not already
obvious from durable evidence. The point is not uncontrolled brainstorming. The
point is to widen the search just enough to avoid premature convergence onto the
first implementable idea.

This divergence protocol sits inside the main workflow after minimum grounding
already exists from memory reuse, initial literature sweep, baseline
reconstruction, and limitation analysis. If strong durable evidence already
narrows the route to one obvious serious option, you may abbreviate the full
widening pass, but you must record why a broader divergence pass was
unnecessary.

First classify the current entry frame:

- `problem-first`:
  - start from a concrete failure, bottleneck, or unmet need
  - confirm who suffers, how much it matters, and why the problem is still open
- `solution-first`:
  - start from a new capability, mechanism, or transfer idea
  - confirm at least two genuine problems it could solve and why this is not just
    a hammer looking for a nail

Then choose at least `2-4` ideation lenses that are actually relevant to the
current bottleneck. The default lens catalog:

- abstraction ladder:
  - move up to a broader principle
  - move down to an extreme constrained case
  - move sideways to an adjacent task with the same structure
- tension or contradiction hunting:
  - identify tradeoffs such as performance vs efficiency, safety vs capability,
    or generality vs specialization
- `why now` / `what changed`:
  - ask whether new compute, tooling, open models, benchmarks, failures, or
    regulations make an old direction newly viable
- analogy transfer:
  - borrow a structural mechanism from a nearby or distant field only when the
    mapping is causal, not metaphorical
- constraint manipulation:
  - list hard, soft, and hidden constraints, then relax, tighten, or replace the
    soft or hidden ones
- negation or inversion:
  - negate a widely assumed design rule and check whether the resulting system is
    coherent
- composition / decomposition:
  - combine two complementary components or separate a monolithic method into the
    real bottleneck pieces
- adjacent possible:
  - focus on directions that became feasible only because recent enablers now
    exist
- stakeholder rotation:
  - inspect the route from the end-user, developer, theorist, operator,
    regulator, or adversary perspective
- simplicity test:
  - ask whether the key contribution survives a simpler and cleaner mechanism

During this divergent phase:

- generate a compact but varied raw slate, usually `6-12` ideas
- do not score them too early
- force the slate to contain some diversity, usually:
  - one conservative route
  - one higher-upside route
  - one elegance-first or low-complexity route
- keep a parking-lot list for coherent rejects and odd-but-possible ideas

For each raw idea, capture at least:

- one-sentence hypothesis
- target limitation
- `why now` / `what changed`
- likely closest prior overlap or novelty risk
- whether it is conservative, higher-upside, or elegance-first

Only after this bounded widening step should you collapse into the shortlist
that will be scored seriously.

## Framework-selection dispatch table (situation → which lenses)

Do not use every ideation lens on every quest. Pick the smallest set that breaks
the current local optimum.

| Situation | Start with |
| --- | --- |
| area is important but the concrete route is still vague | tension hunting + `why now` / `what changed` |
| vague bottleneck but only incremental ideas | abstraction ladder + failure or boundary probing |
| a cool mechanism but no strong reason to care | `problem-first` check + stakeholder rotation |
| every candidate feels like a small benchmark tweak | constraint manipulation + negation or inversion |
| every candidate is a near-clone of the incumbent | analogy transfer + adjacent possible |
| stuck between two paradigms that seem opposed | contradiction hunting; look for synthesis, not compromise |
| route looks elegant but suspiciously complex | simplicity test; force the minimum viable mechanism |
| timing is the main uncertainty | `why now` audit + adjacent-possible check |

The goal is not to sound creative. The goal is to produce candidate mechanisms
that are genuinely different in logic, evidence burden, or timing rationale.

## Integrated ideation workflow: Phase A / B / C

Use this end-to-end pattern when the route is not already forced by durable
evidence. Treat it as a subroutine inside the main workflow, not as a
replacement for the main workflow order.

### Phase A. Diverge

Goal: create a compact but meaningfully varied slate before judging winners.

Precondition: minimum grounding already exists from quest memory, an initial
literature sweep, baseline reconstruction, and a current limitations map.

Recommended sequence:

1. classify the current entry as `problem-first` or `solution-first`
2. list the top bottlenecks, tensions, and what changed recently
3. probe one or two failure boundaries of the incumbent
4. apply `2-4` ideation lenses
5. generate `6-12` raw ideas and keep a parking-lot list for coherent rejects

During divergence:

- do not rank too early
- do not kill an idea only because it is unusual
- do kill ideas that are incoherent, outside scope, or impossible in the current
  repo

### Phase B. Converge

Goal: reduce the raw slate to a serious frontier that is usually `2-3`
candidates and at most `5`.

Apply these filters:

- explain-it test: can the idea be stated clearly in two sentences?
- problem-value test: does the problem matter to a real reader, user, or
  evaluator?
- `why now` test: is there a concrete reason this route is timely now rather
  than three years ago?
- simplicity test: is the mechanism doing real work, or is it ornamental
  complexity?
- feasibility test: can the current repo and resource budget test this honestly?
- novelty or value test: even if not novel, is the line still worth doing for
  transfer, negative-result, or infrastructure value?

If the shortlist is still homogeneous after convergence, return to Phase A with
different lenses once.

### Phase C. Refine

Goal: turn the winning candidate into a stable handoff contract for the
experiment stage.

Before promotion, force the winner to answer:

- what exact limitation it targets
- why current methods still fail here
- what changed or why this is timely now
- what the smallest credible implementation is
- what the cheapest falsification path is
- what the strongest likely objection is
- what the two-sentence pitch is

Only then move into the normal selection gate and the idea-submission flow
(`artifact.submit_idea(...)`; under Houmao, submit the selected
idea/decision through `$HARNESS record apply`).

## Common ideation failure modes and recovery moves

Watch for these predictable failures. Use the recovery moves early; do not wait
until the selection gate to discover the whole ideation pass was trapped in the
wrong mode.

- premature convergence:
  - symptom: the first plausible route becomes the winner before a real
    alternative set exists
  - recovery: reopen divergence with at least two different lenses
- novelty without value:
  - symptom: "nobody has tried this" is doing all the work
  - recovery: run the problem-value test and stakeholder rotation
- value without differentiation:
  - symptom: the route matters, but close prior work already did most of it
  - recovery: tighten the related-work map or route back to `scout`
- complexity worship:
  - symptom: the candidate has many moving parts but weak causal justification
  - recovery: run the simplicity test and reduce to the smallest mechanism that
    could still work
- analogy by metaphor:
  - symptom: a cross-domain import sounds clever but the mechanism does not
    really map
  - recovery: rewrite the analogy in causal language and reject it if the
    structure does not survive
- stale assumptions:
  - symptom: the team dismisses a route only because it failed under old
    constraints
  - recovery: run the `what changed` audit explicitly
- false binary:
  - symptom: discussion gets stuck on choosing A or B
  - recovery: ask whether the conflict is fundamental or an artifact of current
    formulations
- adjacent-but-impossible:
  - symptom: the route is interesting but needs assets or capabilities the
    current system does not have
  - recovery: redesign around current constraints or reject honestly instead of
    hand-waving feasibility

## Contribution-type frame and success target

Before generating ideas, state:

- the primary metric and whether higher or lower is better
- the strongest baseline number with source path
- the expected contribution type:
  - `Insight`
  - `Performance`
  - `Capability`
- the problem importance in one sentence
- the main challenge or bottleneck in one sentence
- whether the direction is emerging, stable, or late relative to the current
  literature wave
- the risk that the direction is valuable but may still be under-recognized
- one sentence for the intended increment over the strongest baseline
- what new knowledge the reader would gain if this line works

If the metric, baseline value, or contribution frame is unclear, stop and
clarify before ideation.

## Baseline reconstruction and improvement-potential rating

State clearly what the baseline does, what assumptions it depends on, where it
appears to fail, which metrics matter most, and what resource or repository
constraints matter. Identify concrete code touchpoints: train/eval entrypoints,
dataset loaders and preprocessing, model/loss/metric code, and where a future
method difference would actually land.

For each serious baseline method, also rate improvement potential as:

- `HIGH`
- `MEDIUM`
- `LOW`

and justify the rating from:

- algorithmic flexibility
- implementation complexity
- coupling or maintainability constraints
- room for principled extension

## Two-layer direction format (conceptual thrust + first-principles rationale)

When possible, make the direction-generation step explicitly two-layered:

1. abstract direction:
   - the core conceptual thrust
   - the first-principles rationale
   - why it is more elegant than brute-force scaling
2. repo-grounded translation:
   - where it could land in the current codebase
   - what the smallest meaningful implementation would be
   - what evidence would falsify it quickly

When the quest needs a stronger strategist-style ideation pass, prefer a fuller
two-layer direct-agent framing for each direction:

1. conceptual thrust
   - one memorable abstract phrase
2. first-principles rationale
   - why the direction should work from mathematical, algorithmic, or logical
     reasoning
3. path to an elegant solution
   - why it is better than brute-force scaling or expensive engineering
4. innovation factor
   - what appears genuinely unexplored or underexplored
5. research value justification
   - why the direction should score well on usefulness, quality, or exploration
     value
6. optional cross-domain inspiration
   - where the idea borrows its structural intuition, if relevant

Derive exactly five actionable research directions whenever the space is not
already tiny, ranked from higher to lower expected return on investment, then
reduce to a compact `2-5` candidate set for actual selection. When the search
space is not tiny, try to preserve diversity in the final candidate set: one
conservative or low-risk line, one higher-upside line, and one elegance-first
line with low engineering burden. If all surviving candidates are minor variants
of the same mechanism family, widen the search once before converging.

## Candidate scoring rubric (the axes)

Score each candidate along explicit axes:

- relevance to the limitation
- feasibility in the current codebase
- expected upside
- clarity of the two-sentence pitch
- falsifiability
- implementation cost
- evaluation clarity
- risk of confounding
- novelty headroom
- research value even if not fully novel
- expected information gain
- reusability as a platform capability
- `why now` credibility

Also keep a compact strategist-style score lens when useful:

- `utility_score`
- `quality_score`
- `exploration_score`

If these are used, explain the scores in prose rather than treating them as
magic numbers. Use them as a secondary decision lens, not as a substitute for
evidence-backed reasoning. Avoid "best sounding" choices; prefer the
best-explained choice. If a candidate scores weakly on novelty but strongly on
research value, label that explicitly instead of pretending it is novel.

For each candidate idea, specify: mechanism, expected gain, main risk, required
files or components, likely metric effect, cheapest falsification path,
strongest competing hypothesis, closest prior work and novelty / value verdict,
and whether it overlaps too much with prior quest ideas or prior failed
findings. Treat each serious candidate as a compact decision package, not a
slogan.

## Draft-before-submit SOP

Before a direction is formally submitted as the selected idea, write a compact
pre-idea draft or equivalent durable challenge memo for each serious surviving
candidate.

The default rule is:

- raw brainstorming can widen the frontier
- pre-idea drafts narrow and stress-test the frontier
- only then can a final selected idea be submitted

The pre-idea draft exists to stop three failure modes:

- local-optimum lock-in around the current mainline
- hidden assumptions staying implicit
- attractive ideas being promoted before the strongest rejection case is written
  down

Unless there is already an up-to-date equivalent artifact, do not formally
submit the final idea until at least one pre-idea draft has:

- been written for the likely winner
- been compared against the incumbent and at least one outside-family or
  assumption-reversal alternative
- been revised, rejected, or promoted based on that comparison

Default durable path rules (`artifacts/idea/...`; under Houmao map
to `runs/<quest-id>/...`):

- objective contract: `artifacts/idea/objective_contract.md`
- current board packet: `artifacts/idea/current_board_packet.md`
- candidate frontier summary: `artifacts/idea/candidates.md`
- pre-idea draft per serious candidate: `artifacts/idea/pre_idea_drafts/<candidate_id>.md`
- final selected idea: `artifacts/idea/selected_idea.md`

When a candidate is promoted, the final selected-idea artifact should point back
to the winning pre-idea draft path instead of losing that lineage in prose only.

## Memory / search reuse discipline

Every fresh idea build or refinement pass should begin with a memory sweep plus
an external literature sweep (or a clear, recorded reason the existing survey is
already sufficient). Separate generation from evaluation: generate first, judge
second. Before opening a broad new search, check quest and global memory
(`memory.search(...)` / `memory.list_recent(...)`; under Houmao
use `$HARNESS knowledge cards` / `knowledge query` plus your role's recorded
quest state) and reuse existing paper notes, idea notes, and knowledge cards.
Every new external query should close one explicit gap: a missing paper bucket,
a newer-than-last-survey refresh, an unresolved overlap with a candidate idea,
or verification of a paper that might block a novelty/value claim.
