# Generic Research Team Design

This document maps a generic Isomer research team to the portable
research-paradigm skills in `skillset/research-paradigm/`. The design keeps
research judgment separate from runtime concerns such as launch topology,
credentials, mailbox routing, gateway inspection, scheduler state, and concrete
artifact paths.

For a condensed 5-role version of this team, see
`teams/deepsci-lite/source/team-design.md`.

## Team Purpose

The team conducts a complete research cycle from intake through final reporting.
The Operator Agent is the human-facing control boundary and stays in manual
mode. Delegated Agent Team Instances either advance within an approved work loop
or pause and wait for Operator Agent instruction.

Each role owns a narrow research responsibility. Stage transitions happen
through durable Artifacts, Evidence Items, Findings, Decision Records, and
Gates, not through source-specific runtime commands.

## Role Map

| Generic Agent | Installed Research-Paradigm Skills | Stage Purpose |
| --- | --- | --- |
| `research-lead` | `isomer-labs-research-shared`, `isomer-labs-research-intake`, `isomer-labs-research-decision`, `isomer-labs-research-finalize` | Own the Research Thread, resolve scope, record Gates and Decision Records, and close the final package. |
| `research-scout` | `isomer-labs-research-shared`, `isomer-labs-research-scout`, `isomer-labs-research-baseline`, `isomer-labs-research-paper-outline` | Frame the problem, scout literature and datasets, identify or validate baselines, and outline evidence needs. |
| `research-designer` | `isomer-labs-research-shared`, `isomer-labs-research-idea`, `isomer-labs-research-optimize`, `isomer-labs-research-science` | Generate candidate ideas, reason about limitations, promote a branch, and define measurable experiments. |
| `research-executor` | `isomer-labs-research-shared`, `isomer-labs-research-experiment`, `isomer-labs-research-analysis`, `isomer-labs-research-science`, `isomer-labs-research-paper-plot`, `isomer-labs-research-figure-polish` | Run the selected implementation or experiment, preserve evidence, analyze robustness, and prepare figures from verified data. |
| `research-writer` | `isomer-labs-research-shared`, `isomer-labs-research-write`, `isomer-labs-research-paper-outline`, `isomer-labs-research-paper-plot`, `isomer-labs-research-figure-polish`, `isomer-labs-research-rebuttal` | Draft reports or papers from durable evidence, keep claims calibrated, and prepare revision responses when needed. |
| `research-reviewer` | `isomer-labs-research-shared`, `isomer-labs-research-review`, `isomer-labs-research-rebuttal`, `isomer-labs-research-analysis`, `isomer-labs-research-decision` | Audit claims, find missing evidence, route rebuttal work, and recommend go, stop, branch, or revise decisions. |

## Role Responsibilities

### `research-lead`

- Starts the Research Thread with a brief, constraints, known artifacts, and
  success criteria.
- Maintains the current Workflow Stage, Gate state, Decision Records, and final
  completion criteria.
- Sends bounded work to delegated Agent Team Instances and receives their
  durable handoffs.
- Finalizes claims, limitations, recommendations, and provenance once the
  reviewer confirms evidence coverage.

### `research-scout`

- Clarifies the problem, assumptions, datasets, metrics, and external evidence
  needs.
- Searches or reads literature through the host paper-reading capability when a
  provider is available.
- Records candidate baselines, known failure modes, and open questions.
- Hands off a baseline recommendation or baseline gate request to
  `research-lead`.

### `research-designer`

- Converts the scout and baseline evidence into candidate hypotheses.
- Compares ideas against limitations, feasibility, risk, and expected evidence.
- Uses optimization discipline when the task needs a candidate frontier or
  branch-promotion logic.
- Produces an experiment-ready selected direction with metrics and stop
  criteria.

### `research-executor`

- Runs the selected experiment through the host Execution Adapter.
- Records inputs, commands or notebooks, outputs, metrics, failures, and
  provenance as durable Artifacts.
- Performs follow-up analysis such as ablations, robustness checks, error
  analysis, and failure analysis.
- Produces verified tables, plots, and figure-ready evidence only from recorded
  data.

### `research-writer`

- Drafts reports, papers, summaries, outlines, and responses from durable
  evidence only.
- Keeps unsupported claims out of the draft and marks evidence gaps for the
  lead or reviewer.
- Coordinates figure polish and plot generation when the report needs visual
  evidence.
- Prepares rebuttal or revision material from reviewer findings and new
  evidence.

### `research-reviewer`

- Audits drafts, reports, experiment packages, and claims with a skeptical
  stance.
- Checks whether the evidence supports each claim, whether limitations are
  explicit, and whether missing controls are visible.
- Recommends a Gate outcome or Decision Record update for `research-lead`.
- Routes needed fixes to the writer, executor, scout, or designer.

## Control Model

The Operator Agent remains manual and decides when to start, pause, resume, or
stop delegated Agent Team Instances. Research skills can recommend the next
Workflow Stage, Gate, or Decision Record; they do not define scheduler fields or
continuation-policy state.

Delegated instances may run a bounded approved loop, such as an experiment run
or analysis pass. When the approved loop ends, fails, or needs a judgment call,
the instance pauses and returns a durable handoff to the Operator Agent.

## Handoff Contract

Every role handoff should name:

- The Research Thread or Research Task being updated.
- The current Workflow Stage and requested next Gate or decision.
- Durable Artifacts, Evidence Items, Findings, Decision Records, and Provenance
  Records produced or consumed.
- Claims that are supported, claims that are unsupported, and concrete
  unresolved questions.
- Any unsettled path, provider, command, schema, or storage surface as a
  `[[tbd-surface:<id>]]` placeholder listed by the shared research-paradigm
  registry.

## Topology-Neutral Boundaries

Team topology, credential selection, mailbox routing, gateway inspection,
scheduler behavior, concrete workspace paths, and platform API calls belong in
runtime profiles or platform documentation. They are intentionally outside the
research-paradigm skill bodies.

The generic mapping above can be implemented as one role per Agent Team Instance
or folded into fewer instances when an operator wants a smaller team. That
runtime choice must not change the extracted skill contracts.

## Operational Workflow

1. `research-lead` creates or receives the Research Thread brief.
2. `research-scout` frames the problem and baseline evidence.
3. `research-designer` selects the research direction and experiment plan.
4. `research-executor` runs experiments and follow-up analyses.
5. `research-writer` drafts from recorded evidence.
6. `research-reviewer` audits claims and recommends the next Gate.
7. `research-lead` records the final decision and closes the package.
