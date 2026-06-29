---
name: deepresearch-research-method
description: Use when the experimenter, analyst, scout-ideator, or orchestrator judges evidence strength or comparability, chooses a baseline or next route, sizes an analysis campaign, responds to a plateau, or closes out a quest. Keywords evidence ladder (minimum/solid/maximum), comparability contract, comparison_ready, decision.record, route-selection, plateau, fusion, exploration-depth gate, publishability stop-loss, finalization checklist, resume packet. Read-only methodology lookup; changes no state.
---

# research-method

## Overview
Self-contained, cross-stage experimental-research methodology for the experimenter, analyst,
scout-ideator, and orchestrator across the loop's experimental stages (baseline, experiment,
analysis, decision, optimize, finalize). It is a read-only craft reference: it tells you how to
judge evidence, comparability, routes, campaigns, plateaus, and closure — it changes no state and
is never an authoritative state surface (the DB stays canonical).

## When to Use
Use this skill when you are:
- planning or running an experiment and need the run contract, preflight, diagnosis-mode, and
  recording discipline (see `references/execution-playbook.md`);
- judging whether a result is `minimum`, `solid`, or `maximum`, or whether a baseline is
  `comparison_ready` (Evidence Ladder, Comparability Contract);
- choosing a baseline route among attach / import / verify-local-existing / reproduce / repair;
- designing or sizing an analysis campaign, or judging slice value (Campaign Design,
  `references/analysis-quantity-and-operations.md`);
- backing a `decision.record` write: verdict, action, route, exploration-depth, publishability
  stop-loss (Decision Criteria);
- responding to a plateauing line or considering a fusion (Plateau / Fusion playbooks);
- closing, pausing, archiving, or handing off a quest (Finalization Checklist, Finalize Craft,
  Resume Packet).

When NOT to use:
- This is read-only. Do NOT finalize, mutate results, confirm GPU, or change quest state from
  here — route those through your role's real commands/skills.
- Do not use it to author authoritative state. Durable truth lives in `$HARNESS` records and
  `runs/<quest-id>/...` files plus the DB; this craft is advisory.
- Respect quest isolation: never reuse, refer to, or inspect another quest's artifacts/findings.

## Workflow
1. Stamp the read for traceability and (optionally) index the craft index. The audit stamp
   records no row:
   `$HARNESS --via skill:deepresearch-research-method:<your-role> knowledge cards --query evidence-ladder`
   (or `$HARNESS --via skill:deepresearch-research-method:<your-role> knowledge query --kind reference`).
2. Pick the method that matches your stage and read the matching section below (or the linked
   `references/` page for the long ones). Key entry points: Evidence Ladder, Comparability
   Contract, Route Selection, Campaign Design, Decision Criteria, Plateau / Fusion, Finalization.
3. Apply the method to the actual state. Choose the smallest action that genuinely resolves the
   current state; name tradeoffs and the rejected alternatives.
4. Do the stage work and record outcomes through your role's normal skill/commands (e.g.
   `$HARNESS record apply --type decision.record`, the durable main-experiment record, slice
   rows). Map any external tool names in the craft (`artifact.*`, `memory.*`, `bash_exec`) to the
   `$HARNESS` surface. The DB stays canonical.
5. Return the method to the calling task and continue. Do not change quest state from this skill.

If the task does not map cleanly to these steps, use your native planning tool to build a plan
from the commands/constraints in this skill, then execute it.

## Common Mistakes
- Treating this skill as a state surface: finalizing, mutating results, confirming GPU, or
  writing authoritative rows from here. It is read-only and advisory only.
- Confusing auxiliary/dev evidence with the main/test claim-carrying comparison.
- Polishing toward `maximum` before the line is even `solid` — first make it executable and
  comparable, then strong, then broad.
- Calling a baseline ready while later `experiment` work still has to guess the comparison
  contract. Make the core contract fields explicit first.
- Choosing a route because it sounds sophisticated or gives the illusion of motion, instead of
  attacking a real bottleneck.
- Drifting off `active_baseline_metric_contract_json` silently, or changing metric definitions /
  baseline recipe mid-run without recording it.
- Hiding a plateau under a sequence of tiny "one more tweak" edits, or rerunning an unchanged
  candidate; route through `decision` once retries stop adding interpretable delta.
- Finalizing dishonestly: erasing negative evidence, claiming success without claim statuses,
  omitting the package inventory, or relying on chat memory instead of durable files.
- Choosing `finalize` for a paper line when manuscript coverage is not `submission_ready=true`,
  or executing `stop` for a low-quality paper without first asking the user.

## Rationalizations vs. red flags
| If you catch yourself thinking… | The rule is… |
|---|---|
| "I'll just polish this to maximum first." | Move `minimum -> solid` before spending on `maximum` polish. |
| "The baseline is close enough, experiment can fill the gaps." | If experiment would keep guessing the comparison contract, the baseline is NOT ready. |
| "One more small tweak and it'll improve." | Repeated near-identical local tweaks = a plateau; name it and pick widen/promote/fuse/debug/stop. |
| "Let's fuse these two lines, we have several branches." | Fuse only when ≥2 lines have real, complementary strengths and one alone has stalled. |
| "Every attempt failed, so write the negative-result paper now." | Clear the exploration-depth gate first: ≥2 structurally distinct families, bottleneck-framing challenged, literature route checked, time budget weighed. |
| "Paper quality is low, just stop." | Ask the user with evidence + branch/narrow alternatives before executing `stop`. |
| "I'll reconstruct the run from memory at the end." | Record incrementally; preserve failed attempts and anomalies; durable files/DB first, not chat. |
| "An extra evaluator gives a nicer number." | Keep the canonical comparator; record any extra evaluator as supplementary, never as a replacement. |

## Inputs / authoritative truth sources
- `active_baseline_metric_contract_json` — when durable state exposes it, read it before planning
  commands or comparisons and treat it as the default authoritative baseline comparison contract
  unless you record a concrete reason to override.
- Durable frontier summary — for algorithm-first quests, read `$HARNESS state query frontier`
  (legacy: `artifact.get_optimization_frontier(...)`) and treat it as the primary optimize-state
  summary; only override with newer dominating durable evidence.
- `runs/<quest-id>/...` files plus the DB hold authoritative resume/closure state; memory cards
  are advisory continuity context.

## Evidence Ladder
Decide whether an experiment package is only minimally acceptable or strong enough to carry a
paper claim.

- `minimum`: basic executable result; comparable setup; enough to show the direction is not
  obviously broken.
- `solid`: main comparison is credible; baseline is strong and fair; results stable enough to
  support the main claim; significance testing present when superiority is claimed.
- `maximum`: the main claim is already credible; additional analysis now broadens confidence,
  interpretation, or scope.

Auxiliary vs main:
- `auxiliary/dev`: parameter effects, diagnostics, mechanism checks, setup clarification.
- `main/test`: claim-carrying comparison; the evidence likely to appear first in the paper.
Do not confuse auxiliary evidence with the main comparison.

Default policy: before spending heavily on `maximum` polish, first move the line from `minimum`
to `solid`. If still below `solid`, the next best action is usually to strengthen comparability,
repair a confounder, add significance testing, or run the most claim-critical follow-up
comparison.

## Comparability Contract
Decide whether a baseline is truly usable downstream.

Minimum/core contract — make these fields explicit: task identity; dataset identity; split
contract; evaluation script or path; required metric keys; metric directions; source commit or
package identity; known deviations. A core contract is enough for a `comparison_ready` baseline.
Expand to a fuller contract only when later paper claims, variant-heavy comparison, or
publication really need it.

Verdict logic: `usable now` / `usable with caveats` / `blocked`. If later `experiment` work would
have to keep guessing the comparison contract, the baseline is not ready.

## Route Selection (baseline stage)
Choose the route that gives the best trust per unit time and compute. Do not follow a fixed
ritual if another route reaches a cleaner comparison contract faster.
- `attach`: reuse an already published and trustworthy baseline.
- `import`: bring a reusable baseline package or bundle into the current quest.
- `verify-local-existing`: validate a local code path or service that already exists.
- `reproduce`: establish a baseline from source paper, repo, and evaluation path.
- `repair`: fix a bounded failure in an existing baseline line.

## Research Route Criteria (branches / ideas / groups / paper routes)
Core question: what exact insufficiency are we trying to resolve now? Do not choose a route only
because it sounds sophisticated or gives the illusion of motion.
Prefer routes that: attack a real bottleneck rather than a vague hope; stay compatible with the
existing architecture when possible; are implementable with bounded risk; can produce
interpretable evidence; are defensible in later writing, review, or rebuttal.
Name these tradeoffs explicitly: novelty vs feasibility; expected gain vs verification cost;
architectural fit vs rewrite burden; immediate progress vs long-term research value; elegant
mechanism vs brute-force scaling.
A good route decision records: winner; strongest alternatives; criteria; expected learnings; why
the rejected options lost.

## Campaign Design
A strong analysis campaign exists to strengthen writing-facing evidence, not to accumulate
miscellaneous extra runs. It should move the evidence boundary (fragile -> interpretable; minimum
-> solid; solid -> broader confidence) with the highest soundness gain that still fits the
current execution envelope. Do not treat every available follow-up as equally valuable.

Priority order: 1) claim-critical contradiction checks; 2) strongest robustness or sensitivity
checks; 3) failure-mode explanation; 4) efficiency or secondary support. Within a tier, prefer
the slice that is both runnable now and most likely to change the claim boundary.

Slice classes: `auxiliary` (settings/thresholds/mechanisms, not claim-carrying);
`claim-carrying` (directly affects whether the main narrative is justified); `supporting`
(broadens confidence after the main claim is credible).

Writing-facing policy: if tied to a selected outline, run claim-carrying slices first, then
supporting slices that deepen interpretation, then route back to `write` once evidence is strong
enough for the selected narrative.

Resource-aware design gate: before expanding a slice set, write down current practical limits
(machine class/devices; wall-clock budget; memory/storage; concurrency; environment/dependency
risk). Tag each candidate slice `runnable-now`, `runnable-with-downscope`, or
`blocked-by-resources`. When resources are tight, optimize for soundness-per-cost: prefer one
decisive runnable contradiction/robustness slice over several speculative expensive ones; use
narrower sweeps/fewer seeds/shorter horizons/smaller held-out subsets/cheaper diagnostics when
they still answer the question honestly; record blocked high-value slices explicitly instead of
letting them disappear.

For sizing targets, the full slice-evidence contract, campaign-artifact tactics, the resource
gate detail, and execution/monitoring tactics, read
`references/analysis-quantity-and-operations.md`.

## Execution
For the full experiment-execution checklist — run contract, preflight, diagnostic-mode trigger,
workspace confirmation, minimum-change discipline, long-running command protocol, output
validation, the durable main-experiment record and its six-field `evaluation_summary`, and the
end-of-stage next-move choice — read `references/execution-playbook.md`. The short control
surface: define the run contract, preflight against the metric contract, implement the minimum
hypothesis-bound change, run with auditable durable commands, validate comparability, record the
run durably, then choose an explicit next direction.

## Decision Criteria
Craft that backs a `decision.record` write. Houmao adaptation: durable decision rows are written
with `$HARNESS record apply --type decision.record`; frontier reads use
`$HARNESS state query frontier` (`artifact.get_optimization_frontier(...)`).

Required decision record makes clear: verdict; action; reason; evidence paths; next stage or next
direction. Keep the verdict simple and legible, and make the chosen action match the actual state
rather than sounding optimistic by default.

Canonical actions (choose the smallest that genuinely resolves the state): `continue`,
`launch_experiment`, `launch_analysis_campaign`, `branch`, `prepare_branch`, `activate_branch`,
`reuse_baseline`, `attach_baseline`, `publish_baseline`, `write`, `review`, `finalize`,
`iterate`, `reset`, `stop`, `request_user_decision`.

For paper-outline decisions, treat select-an-existing-candidate vs revise-the-selected-outline as
two distinct modes (legacy: `artifact.submit_paper_outline(mode='select'|'revise', ...)`). For
paper-bundle decisions, only close into a durable bundle when the draft/package state is durable
enough for that package type. When deciding whether a paper line can advance, judge method
fidelity and story coherence as well as metric coverage. Do not choose `finalize` for a paper
line unless manuscript coverage reports `submission_ready=true`; a draft checkpoint routes back
to `write`, a review package routes to `review`.

Publishability stop-loss rule (apply before choosing `write`, `review`, or `finalize` on paper
routes):
- If the line cannot plausibly become a useful and defensible paper, recommend stopping the paper
  objective or branching to a stronger route instead of another writing pass.
- Do not keep a paper route alive after a publishability stop-loss finding. If durable evidence
  shows novelty/evidence-sufficiency/reader-value has collapsed beyond reasonable narrowing,
  recommend `stop` or `branch`, and record any narrowed non-paper objective as the next direction
  rather than as a new action.
- If the proposed action is `stop` because paper quality is too low, first ask for a user
  decision with the evidence and the branch/narrow alternatives. Do not execute `stop` for a
  low-quality paper judgment without asking the user to confirm that route.
- If the user has given publication/scope/cost/non-paper preferences, consider them explicitly;
  if unclear and materially affecting the stop/branch choice, ask for a user decision.

Exploration-depth gate (all-negative-result papers): apply symmetrically before recommending
`close_round_write_paper` for an all-negative-result paper (every attempted idea falsified or
family-bounded, no positive lift survives). Before routing to `write`, answer all of these in the
decision record:
1. Have you tested at least two structurally distinct idea families (mechanism, objective,
   measurement, infrastructure, or model-architecture / ensemble / multi-agent), or only multiple
   variants inside one family?
2. Have you challenged the bottleneck framing itself — is "X is the locus of the residual gap" a
   conclusion or just an artefact of where you stopped looking?
3. Has the literature surfaced a structurally different route the current attempts did not cover
   (cross-domain mechanism transfer, different evaluator regime, different training-data
   composition, etc.)?
4. How much of the quest's `time_budget_hours` is unused, and could a third structurally distinct
   family fit inside the remainder?
If any answer is "no"/"unsure" and the time budget allows, route back to `idea` for a
re-ideation pass focused on a structurally different family before concluding. The negative-result
paper is still the right outcome when the gate is honestly cleared; this gate just prevents
premature closure. Positive-result papers are not blocked by this gate.

Decision-quality rules. Good decisions: are evidence-backed; name tradeoffs; say what happens
next; say why the alternative was not chosen; explicitly identify the winning candidate when
choosing among multiple packages; do not launch analysis campaigns unless expected information
gain clearly justifies the extra resource cost. Weak decisions: hide uncertainty; lack evidence
paths; give vague approvals; pretend blocked states are progress; choose a winner without naming
the rejected alternatives or criteria.

Algorithm-first truth source. When the quest is algorithm-first, before non-trivial route choices:
read the durable frontier summary (`$HARNESS state query frontier`); treat the frontier as the
primary optimize-state summary; only override it when newer durable evidence clearly dominates; if
the frontier says `explore`, do not collapse immediately to exploit unless the latest durable
result clearly changes the frontier; if it says `fusion`, judge whether complementary lines can be
merged before launching another isolated candidate. Compact mapping:
- frontier says `explore` -> widen or refine candidate briefs before new branch creation
- frontier says `exploit` -> keep the strongest line active and advance the best candidates
- frontier says `fusion` -> open at most one bounded fusion candidate
- frontier says `stop` -> record the stop decision and explicit reopen condition

Selection among candidate packages. Do not decide implicitly. Record candidates, criteria,
winner, and why the main alternatives lost. When paper-facing, prefer the option that best
preserves method fidelity, evidence support, story coherence, and experiment ordering that later
`write`/`finalize` can defend.

User-input note. Ask the user only when multiple options are all plausible; the choice depends on
preference/cost/scope; or the missing information cannot be derived locally. When asking, use a
structured decision request: a concise question; 1-3 concrete options; tradeoffs (main pros/cons
each); recommended option first; explicit reply format. Keep decision requests narrow.

Checkpoint memory on resume-changing decisions. For resume-changing route decisions, write one
compact checkpoint-style quest memory card (`type:checkpoint-memory`) so later turns know the
current active node, node history, what not to reopen by default, and the first files to read. In
Houmao, durable resume state lives in `runs/<quest-id>/...` files plus the DB; memory cards are
advisory continuity context, never the authoritative state surface.

## Plateau Response Playbook
Use when one line keeps producing non-improving results.
Plateau indicators: repeated non-improving results on the same line; repeated "small tweak"
proposals with no structural change; candidate queue filled with near-duplicate mechanisms.
Required response: 1) state that the line is plateauing; 2) identify the most likely root cause;
3) choose one of — widen search, promote a stronger alternative, fuse with another line, debug a
strategically valuable blocked candidate, or stop the line; 4) record one explicit non-repeat
rule so the next pass does not retry the same low-information move.
Do NOT: keep proposing near-identical local tweaks; rerun the same unchanged candidate; fuse
without a clear complementary mechanism; hide a plateau under a sequence of tiny "one more tweak"
edits.

## Fusion Playbook
Use fusion only when at least two lines have real strengths, the strengths are complementary, and
one line alone is no longer improving fast enough.
Before fusion, write down for each source line A and B: strongest mechanism; strongest evidence;
main weakness; what must survive the fusion.
Then answer: what exactly is being fused? why does this combination address a real bottleneck?
why are the source strengths complementary rather than redundant? what remains unchanged for
comparability? what evidence would prove the fusion was worth it? what bounded first validation
step should run before any broad rollout?
Do NOT fuse: two lines with the same mechanism under different names; two weak lines with no clear
strengths; merely because multiple branches exist.

## Finalization
Use before closing, pausing, archiving, or handing off a quest. The hard finalize gates
(manuscript coverage, outline validation, no-unmapped-analysis, bundle maturity, etc.) are
enforced at the write path in `records.py` — do not re-implement them here. Houmao adaptation:
durable closure rows are written with `$HARNESS record apply` (decision/report/quest rows); the
refreshed summary and resume packet live under `runs/<quest-id>/...`.

Core closure questions — confirm: what is genuinely supported; what is only partially supported;
what failed or was abandoned; what remains unresolved; what the recommended next action is.

Final report contents (a strong final report usually includes): executive state; strongest
supported findings; negative results worth preserving; limitations; packaging or bundle status;
recommendation; reopen conditions.

Belief-change log. For every important outcome classify it as `supported`, `partially supported`,
`unsupported`, or `deferred`. For each claim record: claim text/id; evidence paths; key caveats;
whether it is safe to surface in summaries or papers. If a claim was once believed and later
weakened, preserve that downgrade history rather than silently deleting it. Build a compact
belief-change log for the most important transitions (e.g. `supported -> partial`,
`partial -> unsupported`, `promising route -> abandoned`, `draft-ready -> evidence-gap`); for each
record what changed, which evidence caused the change, and what the new recommendation is.

Claim-ledger minimum. For each major claim: claim text/id; status (`supported`/`partial`/
`unsupported`/`deferred`); evidence paths; caveats; whether it is safe for summary/writing/
publication use.

Limitations taxonomy. A final limitations/failure section should include six categories: 1) data
or split limitations; 2) metric limitations; 3) implementation limitations; 4) robustness
limitations; 5) reproducibility risks; 6) claims intentionally not made. Also preserve: failed
branches that meaningfully changed direction; unresolved blocked items; confounders/comparability
issues that weaken confidence; handoff cautions for anyone resuming later.

Package inventory minimum. If code/experiments/writing outputs exist, identify: baseline package
location; decisive run/report locations; analysis campaign outputs; draft/outline/review/proofing
outputs; summary and status files.

Final recommendation structure. Choose the most honest next recommendation (stop and archive;
stop and publish; continue later with a targeted experiment; continue later with a targeted
analysis campaign; reset the current line and revisit ideation). Include: the chosen action; why
it is appropriate now; what evidence most strongly supports it; what would have to become true to
justify a different recommendation. When deciding publish-ready vs archive-ready, be explicit
about which writing/validation gates have actually passed.

Blocked-finalize states (diagnostic vocabulary for naming why finalize is premature; record one
explicitly and route back to the proper stage through `decision`): 1) `unresolved_major_claim`;
2) `unresolved_write_gate`; 3) `missing_proofing_or_submission_checks`; 4)
`unclear_final_recommendation`; 5) `missing_handoff_packet`; 6) `stale_summary_or_graph`; 7)
`unresolved_package_inventory`. For paper-like deliverables, do not finalize while any of these
remain true: required main-text outline items unresolved; completed analysis unmapped into the
paper contract; the active paper line still reports blocking open supplementary work; the paper
contract rows still fail to expose the main experiment or required analysis rows the manuscript
depends on; manuscript coverage does not report `submission_ready=true`; the academic-outline
validator does not pass for the selected outline; the manuscript-language validator reports
main-text wording blockers; the latest bundle is only a `draft_checkpoint` or `review_package`.

Required durable outputs (the finalize stage should usually leave behind): refreshed `SUMMARY.md`;
refreshed `status.md`; final report row; final decision row; refreshed Git graph; explicit
limitations and next-step recommendation; a final claim ledger or equivalent claim-status summary;
a compact resume packet or handoff packet when later continuation is plausible. Quest-specific
closure state belongs in files and DB rows first, not only in memory.

Finalization anti-patterns. Do not finalize by: erasing negative evidence; calling the quest
successful without claim statuses; omitting the package inventory; relying on chat memory instead
of durable files; overclaiming unresolved work; hiding failed branches; skipping limitations;
leaving no clear recommendation; claiming "done" without showing what is actually done; dropping
the package/file inventory; ignoring unmapped completed analysis that never entered the paper
contract.

## Resume / Handoff Packet
Use when the quest is pausing rather than ending permanently. Keep it short, high-signal, and
directly usable by a future agent turn. Recommended structure:
1. Current state — quest objective; present stage; final recommendation at pause time.
1A. Current node history — current active node; predecessor node(s); superseded node(s) or
   closure paths; why the current node is the authoritative resume point.
2. Accepted baseline — baseline id or path; status of reproducibility/comparability; key metric
   context.
3. Strongest evidence — top 2-3 results; supporting artifact paths; key caveats.
4. Open blockers — blocker; why it matters; what stage should resolve it.
5. Next action — the single best next step; why it dominates alternatives; what should be read
   first before acting.
6. Do-not-repeat notes — failed branches not worth retrying unchanged; misleading metrics or
   comparability traps; known environment or tooling pitfalls.
If later continuation remains plausible, also write/refresh one compact checkpoint-style quest
memory card mirroring this packet (`type:checkpoint-memory`).

## Audit / Boundaries
- `$HARNESS --via skill:deepresearch-research-method:<role>` is passed for traceability;
  read-only, so it records no row.
- Never finalize, mutate results, confirm GPU, or change quest state from here.
- Map any external tool names in the craft (`artifact.*`, `memory.*`, `bash_exec`) to the
  `$HARNESS` surface for your role. The DB stays canonical; this craft is advisory and never an
  authoritative state surface.

## Stage Templates (recover from your role's command surface)
This skill inlines the methodology. The original pack also ships fill-in templates the
craft references by name (plan, checklist, candidate-board/ranking, method-brief, strategic- and
debug-/frontier-response templates, optimization-memory, checkpoint-memory). When a section above
names a template (e.g. main-experiment plan/checklist, resume packet, checkpoint-memory card),
reproduce its structure from the corresponding section here, or recover the canonical template
through your role's normal command/skill surface. Do not depend on another skill's files for
content.
## Stop
Return the method to the calling task and continue.
