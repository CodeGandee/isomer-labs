# DeepSci Org Research Team Design

This document designs `deepsci-org` as a Domain Agent Team Template for Isomer Labs research work. It adapts the DeepScientist research approach into Isomer terms, installs the local `isomer-rsch-*` skill bundles, and keeps runtime concerns such as launch tooling, credentials, scheduler internals, mailbox routes, and concrete workspace paths outside the role design.

The key design choice is context reuse. DeepScientist has many Workflow Stages and companion skills, but a useful Agent Role should own a reusable working set, not a single step. This template therefore uses seven core Agent Roles: one `deepsci-org-master` root role, five specialist roles that preserve hot context across adjacent stages, and one independent review role. The master owns the whole team: it is the internal root of the Agent Team Instance, dispatches team Research Tasks, collects specialist handoffs, records route decisions, and closes the loop.

For the condensed five-role variant, see `teams/deepsci-lite/source/team-design.md`.

## Source Basis

The design is grounded in the local DeepScientist source and migration notes:

- `extern/orphan/DeepScientist/src/deepscientist/skills/registry.py` defines stage skills such as `scout`, `baseline`, `idea`, `optimize`, `experiment`, `analysis-campaign`, `write`, `finalize`, and `decision`, plus companion skills such as `paper-outline`, `paper-plot`, `figure-polish`, `intake-audit`, `review`, and `rebuttal`.
- `extern/orphan/DeepScientist/src/deepscientist/prompts/builder.py` groups stage memory differently for scouting, baselines, ideas, optimization, experiments, analysis, writing, finalization, and decisions. Those memory slices are the main evidence for grouping stages into roles.
- `context/explore/deepscientist-skill-analysis/write.md` shows that writing is not just prose generation. It refreshes paper contracts, validates outlines, plans figures, drafts bounded section jobs, validates manuscript support, and routes back to analysis, review, or finalization.
- `skillset/research-paradigm/README.md` provides the Isomer-native research skills and the migration rule: preserve DeepScientist research judgment while replacing source runtime APIs with Isomer concepts such as Research Topic, Research Inquiry, Research Task, Run, Artifact, Evidence Item, Decision Record, Gate, Capability Binding, Skill Binding projection, and Execution Adapter Command Request.

## Role Count

Use seven core Agent Roles for the full `deepsci-org` template:

| Agent Role | Why It Exists | Context Kept Hot |
| --- | --- | --- |
| `deepsci-org-master` | Owns the whole team, coordinates stages, handles Gates and Decision Records, and closes the research loop. | Research Topic state, Research Inquiries, Workflow Stage Cursor, Gates, Decisions, handoffs, completion signals. |
| `deepsci-org-framer` | Combines scout and baseline work because both need the same paper, benchmark, dataset, metric, and comparator context. | Literature neighborhood, dataset and split contract, metric contract, comparator candidates, baseline evidence. |
| `deepsci-org-designer` | Combines idea and optimize work because both reason over objective contracts, bottlenecks, candidate families, and frontiers. | Current board, accepted comparator, objective contract, candidate frontier, selected route, rejected alternatives. |
| `deepsci-org-experimenter` | Owns implementation and main evidence-bearing Runs. It may have multiple Agent Instances for task-level parallel execution. | Code, environment, commands, run contract, logs, outputs, metrics, reproducibility facts. |
| `deepsci-org-analyzer` | Owns follow-up evidence, claim slices, robustness, ablations, error analysis, and reusable result interpretation. | Parent result, parent claim, slice definitions, comparability verdicts, tables, analysis findings. |
| `deepsci-org-publisher` | Combines outline, writing, plotting, figure polish, data availability, and presentation work because these share the manuscript surface. | Paper contract, claim-evidence map, outline, draft, bibliography, figure inventory, bundle status. |
| `deepsci-org-reviewer` | Stays separate from publication to preserve an independent skeptical context for audit and rebuttal routing. | Draft, claim-evidence map, novelty benchmark, reviewer items, revision log, missing-evidence inventory. |

This is intentionally not a role-per-stage design. The Workflow Stages remain visible in the Coordination Policy, but role boundaries follow context locality.

```text
Research Topic
  |
  v
deepsci-org-master
  |------ deepsci-org-framer: scout + baseline
  |------ deepsci-org-designer: idea + optimize
  |------ deepsci-org-experimenter: experiment Runs
  |------ deepsci-org-analyzer: follow-up slices
  |------ deepsci-org-publisher: outline + write + figures + data + slides
  |------ deepsci-org-reviewer: skeptical audit + rebuttal routing
  |
  v
Decision Records, Gates, Artifacts, Evidence Items, Research Claims, final package
```

## Skill Binding Projection

Install `isomer-rsch-shared-v2` for every team role. It carries common evidence, handoff, terminology, provenance, and unsettled-surface rules.

| Agent Role | Required Skills | Optional Skills |
| --- | --- | --- |
| `deepsci-org-master` | `isomer-rsch-shared-v2`, `isomer-rsch-intake-v1`, `isomer-rsch-decision-v2`, `isomer-rsch-finalize-v2` | `isomer-rsch-review-v1` when the master must inspect a review handoff before opening a Gate. |
| `deepsci-org-framer` | `isomer-rsch-shared-v2`, `isomer-rsch-scout-v2`, `isomer-rsch-baseline-v2` | `isomer-rsch-science-v2` for domain package checks, `isomer-rsch-paper-outline-v1` when the framer must state paper evidence needs early. |
| `deepsci-org-designer` | `isomer-rsch-shared-v2`, `isomer-rsch-idea-v2`, `isomer-rsch-optimize-v2` | `isomer-rsch-scout-v2` for narrow literature checks that change idea selection. |
| `deepsci-org-experimenter` | `isomer-rsch-shared-v2`, `isomer-rsch-experiment-v2`, `isomer-rsch-science-v2` | `isomer-rsch-analysis-v2` for tiny post-run checks that do not justify a separate analysis handoff. |
| `deepsci-org-analyzer` | `isomer-rsch-shared-v2`, `isomer-rsch-analysis-v2`, `isomer-rsch-science-v2` | `isomer-rsch-paper-plot-v1`, `isomer-rsch-figure-polish-v1` for analysis-facing result displays. |
| `deepsci-org-publisher` | `isomer-rsch-shared-v2`, `isomer-rsch-paper-outline-v1`, `isomer-rsch-write-v1`, `isomer-rsch-paper-plot-v1`, `isomer-rsch-figure-polish-v1` | Source DeepScientist companions `nature-data`, `nature-figure`, `nature-paper2ppt`, and `nature-polishing`, or future Isomer equivalents, when those bundles are available in the active Skill Binding projection. |
| `deepsci-org-reviewer` | `isomer-rsch-shared-v2`, `isomer-rsch-review-v1`, `isomer-rsch-rebuttal-v1`, `isomer-rsch-analysis-v2` | `isomer-rsch-scout-v2` for novelty benchmarking and comparator-paper checks. |

The optional Nature-family companions should be bound only when the Topic Agent Team Profile needs that publication surface. They should not be installed as mandatory research capabilities for all topics.

## Role Responsibilities

### `deepsci-org-master`

The master is the root Agent Role of the `deepsci-org` team. It owns the team loop after the Agent Team Instance is launched: it interprets the Research Topic, plans the stage route, dispatches bounded Research Tasks to specialists, records team-level Decisions and Gates, and closes or parks the research package.

- Open or resume the Research Topic from the user prompt, Topic Workspace state, and any existing Artifacts.
- Use `isomer-rsch-intake-v1` when the Topic Workspace is not blank or when prior evidence needs trust ranking.
- Maintain the Workflow Stage Cursor, current Research Inquiry graph, Research Task routing, Gate state, and Decision Records.
- Dispatch bounded Research Tasks to specialist Agent Instances and define the Completion Watcher Contract for each handoff.
- Use `isomer-rsch-decision-v2` for go, stop, branch, write, finalize, reset, baseline waiver, and preference-sensitive choices.
- Use `isomer-rsch-finalize-v2` to consolidate claims, limitations, recommendations, resume packets, and closure state.
- Own the final team answer; specialists recommend routes, but the master records the team-level route authority.

### `deepsci-org-framer`

This role compresses the external and comparator context. It should leave later roles with a durable task frame and a trustworthy comparison contract instead of a pile of paper notes.

- Clarify task, dataset, split, metric ids, metric directions, evaluator, fair-comparison rules, and known constraints.
- Scout only the literature, benchmark, repository, or dataset neighborhood that can change the next route.
- Build a comparator shortlist and choose the lightest trustworthy route: attach, import, verify-local-existing, reproduce, repair, waive, block, or route-change.
- Record baseline evidence, metric contract, source identity, deviations, and comparability verdict.
- Hand off the accepted baseline, waiver, or blocker to `deepsci-org-master`.

### `deepsci-org-designer`

This role owns the intellectual route. It turns the accepted frame into a falsifiable direction and, for algorithm-first work, manages the optimization frontier.

- Build the objective contract, current board, false-progress signals, constraints, and strongest rejection cases.
- Use literature and research history only where they affect candidate selection.
- Generate a small differentiated set of candidate routes, stress-test them, and select one falsifiable route.
- Maintain candidate briefs, durable optimization lines, implementation attempts, frontier ranking, fusion ideas, debug routes, and stop conditions.
- Hand off a selected route or promoted candidate with experiment-ready metrics, expected outputs, stop rules, and abandonment criteria.

### `deepsci-org-experimenter`

This role owns main evidence-bearing implementation and measurement. It should be the most horizontally scalable role in the template.

- Recover selected route, accepted comparator or Baseline-Waiver Policy ref, metric contract, current code state, and expected outputs.
- Lock the Run contract before implementation: question, comparator, dataset, metrics, stop rule, abandonment rule, output schema, and comparability boundary.
- Implement the minimum hypothesis-bound change and avoid unrelated cleanup.
- Run smoke or pilot checks only when they reduce execution uncertainty, then run the evidence-bearing Run.
- Preserve commands, configs, logs, outputs, metric records, failure modes, and Provenance Records.
- Return measured results to `deepsci-org-master`; do not decide publication readiness independently.

### `deepsci-org-analyzer`

This role owns follow-up evidence after a main result. It protects the team from overgeneralizing one Run.

- Lock the parent object: main result, Research Claim, paper gap, reviewer item, failure mode, or route decision.
- Audit execution limits before planning slices.
- Define the smallest slice set that can confirm, weaken, change, or block the parent claim.
- Run claim-critical slices first and keep comparisons isolated.
- Record each slice with status, evidence path, claim update, comparability verdict, caveat, and next action.
- Aggregate only decision-relevant findings and route back to experiment, strategy, publication, review, decision, pause, or blocker.

### `deepsci-org-publisher`

This role owns communication artifacts, not research truth. It writes only from durable evidence and routes back when support is missing.

- Refresh the paper contract: outline, claim-evidence map, experiment matrix, analysis matrix, bibliography, figure and table status, bundle status, and unresolved Gates.
- Build or repair a paper-native outline with separate paper view and evidence view.
- Draft bounded section jobs from Evidence Items, verified citations, and supported Research Claims.
- Use `isomer-rsch-paper-plot-v1` for first-pass standard figures and `isomer-rsch-figure-polish-v1` for final render-inspect-revise work.
- Use Nature-family companions only for their bounded surfaces: data availability, submission-grade figures, presentation decks, or Nature-leaning language.
- Route back to the analyzer, framer, reviewer, or master decision when evidence, citations, or claim boundaries are insufficient.

### `deepsci-org-reviewer`

This role remains separate from publication so the team has a genuine audit surface. It should be skeptical, evidence-grounded, and route-aware.

- Rebuild the claim and experiment inventory from durable Artifacts, not from draft wording.
- Audit novelty, value, rigor, clarity, baseline support, analysis coverage, figure truth, and likely rejection routes.
- Produce a review report, revision log, and experiment TODOs only when new evidence is genuinely required.
- Normalize external reviewer feedback into stable reviewer items with affected claims, evidence anchors, action classes, and route recommendations.
- Route reviewer-linked evidence through analysis, manuscript changes through publication, comparator gaps through frame, and route choices through master decision.

## Manual Mode

In Manual Mode, `deepsci-org-master` drives the Agent Team Instance through explicit handoffs. The user does not need to talk directly to every Agent Instance.

```text
User
  |
  v
deepsci-org-master
  |  creates Research Tasks, opens Gates, records Decisions
  |
  +--> deepsci-org-framer ------+
  +--> deepsci-org-designer ----+
  +--> deepsci-org-experimenter --+--> durable handoffs --> deepsci-org-master
  +--> deepsci-org-analyzer ----+
  +--> deepsci-org-publisher ---+
  +--> deepsci-org-reviewer -----+
```

Manual Mode flow:

1. The user gives the Research Topic, constraints, and desired control level to `deepsci-org-master`.
2. The master creates or receives the Topic Agent Team Profile context and starts the team loop.
3. For each Research Task, the master writes a handoff with scope, expected inputs, expected outputs, Gate constraints, Skill Binding projection, Capability Binding refs, and Completion Watcher Contract.
4. A specialist Agent Instance works inside its Agent Workspace, records Agent Artifacts, and returns a handoff with promoted Artifacts, Evidence Items, Findings, Research Claims, Decision Record recommendations, caveats, and blockers.
5. The master normalizes the handoff into Workspace Runtime, advances or holds the Workflow Stage Cursor, and asks the user only for true Gates such as cost, credentials, privacy, data export, destructive mutation, baseline waiver, publication-facing finality, or scope preference.
6. The user can pause, inspect, redirect, or approve the next handoff at each Gate.

Manual Mode is best when the user wants close scientific control, when credentials or private data are involved, when the team is still tuning its Topic Agent Team Profile, or when an expensive Run needs approval before launch.

## Fully Automatic Mode

In fully automatic mode, `deepsci-org-master` remains authoritative inside the team, but a Scheduler Policy allows it to continue from durable state after each non-blocking milestone. This mirrors the useful part of DeepScientist auto-continue behavior without importing source continuation-policy fields into the Domain Agent Team Template.

```text
Scheduler Policy
  |
  v
deepsci-org-master
  |
  +--> dispatch task
  |      |
  |      v
  |   specialist Agent Instance
  |      |
  |      v
  |   Completion Watcher Contract
  |
  v
Decision Record or Gate preflight
  |
  +--> safe routine decision: continue automatically
  +--> governed decision: open Gate for user
```

Automatic mode flow:

1. The master performs intake, chooses the next Workflow Stage Cursor, and dispatches the smallest useful Research Task.
2. The Completion Watcher Contract observes candidate completion through agent replies, inspected Agent Artifacts, adapter events, file observations, validation rules, or staleness rules.
3. When a specialist completes, the master records the handoff, runs the required validation or decision skill, and dispatches the next Research Task if no Gate is required.
4. Routine route choices, such as moving from baseline to idea after a confirmed comparator, can proceed through `isomer-rsch-decision-v2` without user interruption.
5. Governed actions still open Gates. Automatic mode must not bypass cost, credential, privacy, data export, destructive change, long-compute, baseline-waiver, publication-facing, or final-completion Gates.
6. When the state is blocked, stale, contradictory, or repeatedly unchanged, the master records the blocker and parks the Agent Team Instance with a resume packet rather than looping.

Automatic mode is best for unattended progress on low-risk research tasks with available credentials, bounded compute, clear metrics, and accepted Gate policies.

## Stage-to-Role Routing

| Workflow Stage or Companion Work | Owning Role | Notes |
| --- | --- | --- |
| Intake audit | `deepsci-org-master` | Used when existing state must be trusted or reconciled before routing. |
| Scout | `deepsci-org-framer` | Bounded framing, not exhaustive survey. |
| Baseline | `deepsci-org-framer` | Establishes comparator and metric contract; can request execution help if reproduction is heavy. |
| Idea | `deepsci-org-designer` | Produces one selected falsifiable route. |
| Optimize | `deepsci-org-designer` | Manages frontier, candidate briefs, promotion, fusion, debug, or stop. |
| Experiment | `deepsci-org-experimenter` | Produces main measured evidence. Multiple instances may run task-level parallel attempts. |
| Analysis campaign | `deepsci-org-analyzer` | Produces follow-up slice evidence tied to a parent object. |
| Science computation | `deepsci-org-experimenter` or `deepsci-org-analyzer` | Routed by whether the work is main Run execution or follow-up validation. |
| Paper outline | `deepsci-org-publisher` | Separates paper view from evidence view. |
| Write | `deepsci-org-publisher` | Drafts from durable evidence and routes back on gaps. |
| Paper plot | `deepsci-org-publisher` or `deepsci-org-analyzer` | Publisher owns paper-facing plots; analyzer owns diagnostic result displays. |
| Figure polish | `deepsci-org-publisher` or `deepsci-org-analyzer` | Publisher owns final figures; analyzer owns milestone figures. |
| Review | `deepsci-org-reviewer` | Independent audit before finalization or revision. |
| Rebuttal | `deepsci-org-reviewer` with `deepsci-org-publisher` | Review normalizes pressure and routes work; publication writes response text. |
| Decision | `deepsci-org-master` | Specialists may recommend, but the master records route authority. |
| Finalize | `deepsci-org-master` with `deepsci-org-publisher` | Master owns closure; publication prepares final artifacts. |

## Coordination Policy

The Coordination Policy should enforce these rules:

- `deepsci-org-master` is the only default dispatcher inside the team. Specialists do not recursively launch other specialists unless the Topic Agent Team Profile explicitly grants that authority.
- Every Research Task names one accountable Task Handler, even when several Agent Instances participate.
- Agent Workspaces have advisory Workspace Boundaries. Peer Read Access is allowed for declared handoff material, but durable dependencies must be promoted into Artifacts, Evidence Items, Findings, Decision Records, or Provenance Records.
- Handoffs must include inspected inputs, produced outputs, affected Research Claims, Evidence Items, unresolved caveats, next recommended Workflow Stage Cursor, and any Gate recommendation.
- Publication work cannot upgrade unsupported evidence. It must route missing support back to frame, execution, analysis, review, or decision.
- Review work cannot silently mutate the manuscript. It records findings, revision logs, and route recommendations for master decision.
- Final completion requires explicit completion approval when the active Gate Policy requires it, even in fully automatic mode.

## Parallel Execution

The default `deepsci-org` parallelism is task-level, not inquiry-level.

- `deepsci-org-experimenter` can fan out across multiple Agent Instances for independent candidate attempts, seeds, environments, or implementation variants when the Research Task defines clear isolation and merge rules.
- `deepsci-org-analyzer` can fan out across independent slices when each slice has a parent claim, fixed conditions, comparability boundary, and evidence path expectation.
- `deepsci-org-framer`, `deepsci-org-designer`, `deepsci-org-publisher`, and `deepsci-org-reviewer` should normally run as single Agent Instances per Agent Team Instance because their context is coherence-heavy.
- Topic-level parallel execution should create multiple Agent Team Instances from different Topic Agent Team Profiles when the user wants to compare different research strategies.

## Template Defaults

Recommended defaults for the Domain Agent Team Template:

| Setting | Default |
| --- | --- |
| Core roles | 7 |
| Horizontally scalable roles | `deepsci-org-experimenter`, `deepsci-org-analyzer` |
| Required shared skill | `isomer-rsch-shared-v2` for all roles |
| Default dispatcher | `deepsci-org-master` |
| Default Control Mode | Manual Mode for first launch, automatic mode only after Gate policies and Capability Bindings are configured |
| Gate-sensitive actions | Credential use, paid or long compute, private data, data export, destructive mutation, baseline waiver, publication-facing finality, final completion |
| Evidence truth source | Decision Records, Artifacts, Evidence Items, Findings, Research Claims, Provenance Records, Workspace Runtime records |
| Runtime exclusions | Source DeepScientist scheduler fields, source artifact APIs, concrete runner homes, provider-specific command bodies, mailbox routes, gateway routes, credentials |

## Open Design Questions

- Whether `deepsci-org-framer` should own heavy baseline reproduction itself or dispatch execution support through a Service Request when reproduction requires substantial environment repair.
- Whether Nature-family companion skills should be migrated into the Isomer research-paradigm skillset or bound only from source DeepScientist projections for Topic Agent Team Profiles that target Nature-family outputs.
- Whether `deepsci-org-reviewer` should have direct peer-read access to all Agent Artifacts or only to promoted Artifacts and declared handoff bundles.
- How much automatic-mode fanout should be allowed before `deepsci-org-master` opens a cost or long-compute Gate.
