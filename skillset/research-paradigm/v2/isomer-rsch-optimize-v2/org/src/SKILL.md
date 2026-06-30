---
name: optimize
description: Use when an algorithm-first quest should manage candidate briefs, optimization frontier, branch promotion, or fusion-aware search instead of the paper-oriented default loop.
skill_role: stage
---

# Optimize

Use this skill for algorithm-first quests where the goal is the strongest justified optimization result rather than paper packaging.
The goal is to move the frontier by one justified step at a time, not to generate a large pile of low-information candidates.

## Match signals

Use `optimize` when:

- the quest is algorithm-first
- the baseline gate is already confirmed or waived
- the task has at least one plausible optimization direction
- multiple candidate directions exist and the system should rank them before promotion
- a durable line exists and the next step is to manage explore, exploit, fusion, debug, or stop

Do not use `optimize` when:

- the baseline gate is unresolved
- the main need is a paper draft, rebuttal, review, or finalize task
- the quest is still in broad literature scouting with no concrete optimization handle
- the real blocker is still idea-family selection rather than bounded optimization search inside an accepted family

## One-sentence summary

Recover the current frontier, choose one optimize submode, advance one justified move, then record the new frontier or explicit stop condition.

## Control workflow

1. Recover the current frontier and recent durable optimization state.
   Read the frontier, recent memory, and current quest state before creating or promoting anything.
2. Choose exactly one primary optimize submode for this pass.
   Keep the pass legible: one dominant optimize move, not several unrelated route changes.
3. Keep the candidate slate or active pool small and differentiated.
   If the direction is still fuzzy, shape and rank branchless candidate briefs; if a durable line already exists, manage a bounded implementation pool inside that line.
4. Promote or execute only bounded candidates with explicit evidence criteria.
   Promote only the strongest briefs into durable lines, and record implementation-level attempts separately from durable line creation.
5. Route from evidence to exactly one dominant next action.
   End in `explore`, `exploit`, `fusion`, `debug`, or `stop`, and record that route durably.

## AVOID / pitfalls

- Do not treat every patch or micro-attempt as a new durable idea line.
- Do not create a new Git branch or worktree for every implementation-level candidate.
- Do not create a new Git branch/worktree for every implementation-level candidate.
- Do not promote every plausible brief.
- Do not keep widening the frontier once a small serious slate already exists.
- Do not let one optimize pass mix multiple major route changes.
- Do not keep selecting the same familiar mechanism family after repeated non-improving results.
- Do not drift into paper-outline, bundle, or finalize work by default while this stage is active.
- Do not treat one candidate creation or one smoke pass as stage completion.

## Constraints

- Use these three object levels consistently:
  - candidate brief
  - durable optimization line
  - implementation-level candidate attempt
- Keep exactly one primary optimize submode active for the current meaningful pass.
- Keep only one bottom-layer optimize move truly in progress at a time.
- Before deciding the next route, call `artifact.get_optimization_frontier(...)` when available and use it as the primary optimization-state summary.
- Candidate briefs should use `artifact.submit_idea(..., submission_mode='candidate')`.
- Durable lines should use `artifact.submit_idea(..., submission_mode='line')`.
- Only promote a candidate brief into a durable line when it has enough expected value, differentiation, and execution path clarity to deserve branch/worktree state.
- Implementation-level candidate attempts inside one durable line should use `artifact.record(... report_type='optimization_candidate' ...)`.
- Real measured line results should use `artifact.record_main_experiment(...)`.
- All terminal work in this stage must go through `bash_exec(...)`.

## Validation

Before `optimize` can end, all applicable checks should be true:

- the frontier was refreshed
- the active optimize submode is explicit
- the candidate board and optimize checklist reflect the current state
- promoted lines are justified and bounded
- every live candidate has status and next action
- every major success, failure, promotion, or route change is durably recorded
- the pass ends with one durable next action or stop condition

## Interaction discipline

- Follow the shared interaction contract injected by the system prompt.
- For ordinary active work, prefer a concise progress update once work has crossed roughly 6 tool calls with a human-meaningful delta, and do not drift beyond roughly 12 tool calls or about 8 minutes without a user-visible update.
- Ordinary candidate creation, smoke checks, and route updates should stay concise.
- Use richer milestone updates only when a candidate is promoted, a strong run finishes, the frontier shifts materially, or a fusion/debug route becomes the new main path.
- When the user asks for the current optimization state, answer from the frontier and durable artifacts rather than from chat memory.
- Every terminal command in this stage must go through `bash_exec`; do not use any other terminal path for smoke checks, quick validations, long runs, Git, Python, package-manager, or file-inspection commands.

## Working surfaces

Before broad optimization search or candidate management becomes substantial, maintain these quest-visible control files:

- quest-root `plan.md` as the research map and loop tracker for the whole quest
- workspace `PLAN.md` as the active optimize-node contract
- `OPTIMIZE_CHECKLIST.md` as the optimize-specific execution frontier
- workspace `CHECKLIST.md` as a mirror of the immediate next move when it exists
- `CANDIDATE_BOARD.md` as the compact candidate ledger

Use these templates:

- `references/optimize-checklist-template.md`
- `references/candidate-board-template.md`

`optimize` is the looped search controller for algorithm-first quests, not a replacement for the quest-level roadmap.
When a result becomes the new incumbent, plateaus, or stops, update quest-root `plan.md` so the next loop edge is explicit.

## Core object model

Use these three object levels consistently:

1. candidate brief
   `artifact.submit_idea(mode='create', submission_mode='candidate', ...)`
   Record a possible direction or method brief without opening a branch yet.
2. durable optimization line
   `artifact.submit_idea(mode='create', submission_mode='line', ...)`
   Open a real branch or worktree and make it a formal optimization path.
3. implementation-level candidate attempt
   `artifact.record(payload={'kind': 'report', 'report_type': 'optimization_candidate', ...})`
   Record one within-line attempt such as one patch, one smoke candidate, one debug candidate, or one fusion candidate.

Use `artifact.record(payload={'kind': 'decision', ...})` when the frontier route changes, a line is promoted, a line is stopped, or the next optimize submode is selected.

## Optimize submodes

Treat `optimize` as one stable stage skill with six internal submodes:

- `brief`: turn loose directions into compact candidate briefs
- `rank`: compare briefs on one shared surface and choose promotion candidates
- `seed`: create a small implementation-level pool inside one durable line
- `loop`: advance one durable line with bounded smoke/full-eval/record actions
- `fusion`: combine complementary strengths from multiple lines
- `debug`: rescue a strategically valuable candidate blocked by a concrete failure mode

Do not treat these as separate public skills.
Treat them as internal execution modes inside one optimize workflow.

Default selection order:

1. `fusion` when the frontier explicitly says `fusion`
2. `debug` when a strategically valuable candidate failed for a concrete and likely fixable reason
3. `rank` when several candidate briefs already exist and promotion is the main unresolved question
4. `brief` when the candidate-brief slate is too thin or too weak
5. `seed` when a durable line exists but there is no live implementation-candidate pool
6. `loop` when a live candidate pool or leading durable line already exists and the main need is bounded execution progress

## Frontier route meanings

At meaningful route boundaries, choose exactly one dominant route meaning:

- `explore`: widen search with fresh candidate directions
- `exploit`: focus on the strongest current line
- `fusion`: merge insights from multiple successful or complementary lines
- `debug`: rescue a candidate or line blocked by a concrete failure mode
- `stop`: the current frontier is saturated or the remaining routes are not justified

Default heuristics:

- choose `explore` when no line is clearly dominant or the current lines are too similar
- choose `exploit` when one line clearly leads on evidence and comparability
- choose `fusion` when at least two lines have meaningful complementary strengths
- choose `debug` when a strategically valuable candidate failed for a concrete and likely fixable reason
- choose `stop` when the frontier is saturated or the remaining routes are low-value relative to cost

## Non-negotiable rules

- Keep all major optimization successes and failures durable through artifacts and memory.
- Do not convert ranking uncertainty into premature branch creation.
- Do not treat an implementation-level candidate report as a new durable optimization line.
- Before broad new search, inspect recent optimization memory and the same-line local attempt memory when relevant.
- If the same line stalls repeatedly, switch route instead of pretending more of the same is new evidence.
- Plateau is a route signal, not a reason to keep issuing tiny tweaks.

## Operational guidance

The main skill keeps the control surface in front.
For the longer playbooks, templates, and protocol details, read the references:

- `references/operational-guidance.md`
- `references/brief-shaping-playbook.md`
- `references/candidate-ranking-template.md`
- `references/frontier-review-template.md`
- `references/method-brief-template.md`
- `references/codegen-route-playbook.md`
- `references/debug-response-template.md`
- `references/fusion-playbook.md`
- `references/optimization-memory-template.md`
- `references/optimize-checklist-template.md`
- `references/plateau-response-playbook.md`
- `references/prompt-patterns.md`

Use them when:

- the candidate brief is still fuzzy
- explicit ranking or promotion notes are needed
- the frontier route is unclear
- implementation-route choice, debug, fusion, or plateau handling needs the full playbook
- memory writing, checklist maintenance, or prompt shaping materially affect the route

## Integrated reference appendix

Use these reference sections as needed without copying them into chat:

### optimize-checklist-template.md
### candidate-board-template.md
### method-brief-template.md
### brief-shaping-playbook.md
### candidate-ranking-template.md
### frontier-review-template.md
### optimization-memory-template.md
### fusion-playbook.md
### codegen-route-playbook.md
### debug-response-template.md
### prompt-patterns.md
### plateau-response-playbook.md

Codegen route choices should stay explicit: stepwise generation for incremental edits, diff / patch generation for contained changes, and full rewrite only when the old surface is genuinely the blocker.
Mandatory first-call sequence: refresh `artifact.get_optimization_frontier(...)`, recover quest state, then choose `brief`, `rank`, `seed`, `loop`, `fusion`, `debug`, or `stop`.
Use memory.search(...) for same-line local attempt memory before repeating a known failure or reopening stale frontier assumptions.

Stall-recovery protocol: if a line stops improving, decide whether the issue is mechanism family, change-layer diversity, validation-cost-aware seed policy, validation-cost-aware loop policy, or execution noise.
Internal submode selection should preserve a coverage contract and a distinct promotion policy for each route.
InternAgent maps most naturally to codegen-route and execution-surface optimization; MLEvolve maps most naturally to search-loop, mutation, and validation orchestration.

Brief shaping should clarify the bottleneck, constraints, and comparability boundary first, then generate a small differentiated slate, usually `2-3` serious approaches.
Recommend one approach with explicit tradeoffs against the alternatives, and self-check the winning brief for ambiguity, overlap, and weak justification before submission.
recommend one approach with explicit tradeoffs against the alternatives
Candidate briefs should expose `why_now`.

For seed mode, use a validation-cost-aware seed policy: if checks are under about `20` minutes, a separate smoke stage is optional; direct submission into quick parallel validation is acceptable.
Only skip smoke when the parallel quick validations are expected to produce distinguishable conclusions.
only skip smoke when the parallel quick validations are expected to produce distinguishable conclusions
Use smoke test or direct quick validation according to uncertainty, and you may skip a separate smoke stage and submit several quick validations in parallel when the hypotheses are separable.
For loop mode, use a validation-cost-aware loop policy; if the validation loop is slow, do not keep paying for frontier uncertainty that could have been reduced in `brief`.
Gate evolution on clear objective signal rather than small local preference.
gate evolution on clear objective signal

Family-shift trigger: when repeated same-family edits stall, revisit the mechanism family.
Task-category primer: prefer simple-first changes, one atomic improvement per pass, and bugfix-only passes when the failure is localized.

## Exit criteria

Exit `optimize` only when one of these is durably true:

- a stronger line was promoted and the next anchor is clear
- the current line produced a real measured result and the next route is recorded
- the optimization frontier says stop and that stop decision is durably recorded

Do not treat one candidate creation or one smoke pass as stage completion.
