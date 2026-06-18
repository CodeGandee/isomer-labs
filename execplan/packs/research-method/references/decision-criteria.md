# Decision Criteria

Use this reference for the route-judgment craft that backs a `decision.record` write.
md`. Houmao adaptation: durable decision rows
are written with `$HARNESS record apply --type decision.record` (recorded the
same verdict through its artifact surface). Frontier reads use `$HARNESS state query frontier`
(`artifact.get_optimization_frontier(...)`).

## Required decision record

Every consequential decision should make clear:

- verdict
- action
- reason
- evidence paths
- next stage or next direction

Keep the verdict simple and legible, and make sure the chosen action matches the actual
state rather than sounding optimistic by default.

## Canonical actions

Use the following canonical actions. Choose the smallest action that genuinely resolves the
current state:

- `continue`
- `launch_experiment`
- `launch_analysis_campaign`
- `branch`
- `prepare_branch`
- `activate_branch`
- `reuse_baseline`
- `attach_baseline`
- `publish_baseline`
- `write`
- `review`
- `finalize`
- `iterate`
- `reset`
- `stop`
- `request_user_decision`

For paper-outline decisions, select an existing candidate vs. revise the selected outline as
two distinct modes (legacy call: `artifact.submit_paper_outline(mode='select'|'revise', ...)`).
For paper-bundle decisions, only close into a durable bundle when the draft or package state
is durable enough for that package type. When deciding whether a paper line can advance, judge
method fidelity and story coherence as well as metric coverage.

Do not choose `finalize` for a paper line unless manuscript coverage reports
`submission_ready=true`; a draft checkpoint routes back to `write`, and a review package routes
to `review`.

## Publishability stop-loss rule

For paper routes, apply the publishability stop-loss rule before choosing `write`, `review`, or
`finalize`:

- If the line cannot plausibly become a useful and defensible paper, recommend stopping the
  paper objective or branching to a stronger route instead of adding another writing pass.
- Do not keep a paper route alive after a publishability stop-loss finding. If durable evidence
  shows that novelty, evidence sufficiency, or reader value has collapsed beyond reasonable
  narrowing, recommend `stop` or `branch`, and record any narrowed non-paper objective as the
  next direction rather than as a new action.
- If the proposed action is `stop` because paper quality is too low, first ask for a user
  decision with the evidence and the branch/narrow alternatives. Do not execute `stop` for a
  low-quality paper judgment without asking the user to confirm that route.
- If the user has given publication, scope, cost, or non-paper preferences, consider them
  explicitly; if those preferences are unclear and materially affect the stop/branch choice,
  ask for a user decision.

## Exploration-depth gate (all-negative-result papers)

Apply the symmetric **exploration-depth gate before recommending `close_round_write_paper` for
an all-negative-result paper** (every attempted idea has been falsified or family-bounded, no
positive lift survives). Before routing to `write`, answer all of these in the decision record:

1. Have you tested at least two structurally distinct idea families (mechanism, objective,
   measurement, infrastructure, or model-architecture / ensemble / multi-agent), or only
   multiple variants inside one family?
2. Have you challenged the bottleneck framing itself — is "X is the locus of the residual gap"
   a conclusion or just an artefact of where you stopped looking?
3. Has the literature surfaced a structurally different route the current attempts did not
   cover (cross-domain mechanism transfer, different evaluator regime, different training-data
   composition, etc.)?
4. How much of the quest's `time_budget_hours` is unused, and could a third structurally
   distinct family fit inside the remainder?

If any answer is "no" or "unsure" and the time budget allows, route back to `idea` for a
re-ideation pass focused on a structurally different family before concluding. The
negative-result paper is still the right outcome when the gate is honestly cleared; this gate
just prevents premature closure when only one corner of the design space has been ruled out.
Positive-result papers are not blocked by this gate.

## Decision-quality rules

Good decisions:

- are evidence-backed
- name tradeoffs
- say what happens next
- say why the alternative was not chosen
- explicitly identify the winning candidate when choosing among multiple packages
- do not launch analysis campaigns unless the expected information gain clearly justifies the
  extra resource cost

Weak decisions:

- hide uncertainty
- lack evidence paths
- give vague approvals
- pretend blocked states are progress
- choose a winner without naming the rejected alternatives or criteria

## Algorithm-first truth source

When the quest is algorithm-first, add one extra truth-source rule before non-trivial route
choices:

- read the durable frontier summary (`$HARNESS state query frontier`)
- treat the frontier as the primary optimize-state summary
- only override it when newer durable evidence clearly dominates
- if the frontier says `explore`, do not collapse immediately to exploit unless the latest
  durable result clearly changes the frontier
- if the frontier says `fusion`, judge whether complementary lines can be merged before
  launching another isolated candidate

Compact algorithm-first mapping:

- frontier says `explore` -> widen or refine candidate briefs before new branch creation
- frontier says `exploit` -> keep the strongest line active and advance the best candidates
- frontier says `fusion` -> open at most one bounded fusion candidate
- frontier says `stop` -> record the stop decision and explicit reopen condition

## Selection among candidate packages

When choosing among multiple candidate outputs, do not decide implicitly. Record the
candidates, the criteria, the winner, and why the main alternatives lost.

When the choice is paper-facing, prefer the option that best preserves:

- method fidelity
- evidence support
- story coherence
- experiment ordering that later `write` or `finalize` can defend

## User-input note

Ask the user only when:

- multiple options are all plausible
- the choice depends on preference, cost, or scope
- the missing information cannot be derived locally

When asking, use a structured decision request with: a concise question; 1 to 3 concrete
options; tradeoffs (main pros and cons for each); recommended option first; explicit reply
format. Keep decision requests narrow.

## Checkpoint memory on resume-changing decisions

For resume-changing route decisions, write one compact checkpoint-style quest memory card so
later turns know the current active node, node history, what not to reopen by default, and the
first files to read. Use `references/checkpoint-memory-template.md` (tagged it
`type:checkpoint-memory`). In Houmao, durable resume state lives in `runs/<quest-id>/...` files
plus the DB; memory cards are advisory continuity context, never the authoritative state surface.
