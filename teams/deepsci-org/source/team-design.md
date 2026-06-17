# DeepScientist Generic Research Team Design

This document designs an operator-controlled Houmao research team modeled on the DeepScientist stage-skill pipeline. The team breaks end-to-end research into discrete roles that an operator can stage, prompt, inspect, and transition manually.

For a condensed 5-role version of this team, see `teams/deepsci-lite/source/team-design.md`.

## Team Purpose

The team conducts a complete research cycle from problem framing through final reporting. Each role owns one stage. The operator decides when a stage finishes and which role runs next. This keeps human oversight at every major transition while letting each agent focus on a narrow, well-defined responsibility.

## Role Map

DeepScientist stage skills become Houmao project specialists. Companion skills become on-demand support roles.

| Houmao Specialist | DeepScientist Source | Stage Purpose |
| --- | --- | --- |
| `deepsci-scout` | `scout` | Frame the problem, scout literature, clarify datasets, metrics, and candidate baselines. |
| `deepsci-baseline` | `baseline` | Attach, reproduce, verify, compare, or publish a baseline and its metrics. |
| `deepsci-idea` | `idea` | Generate hypotheses, analyze limitations, and select a concrete candidate direction. |
| `deepsci-optimize` | `optimize` | Manage algorithm-first candidate briefs, optimization frontiers, and fusion-aware search. |
| `deepsci-experiment` | `experiment` | Run the main implementation pass or experiment tied to the selected idea and accepted baseline. |
| `deepsci-analysis` | `analysis-campaign` | Run follow-up ablations, robustness checks, error analysis, and failure analysis. |
| `deepsci-write` | `write` | Draft or refine a paper, report, or research summary from existing evidence. |
| `deepsci-finalize` | `finalize` | Consolidate final claims, limitations, recommendations, summary state, and graph exports. |
| `deepsci-decision` | `decision` | Make explicit go, stop, branch, reuse-baseline, write, finalize, reset, or user-decision transitions with evidence. |

### Companion Support Roles

| Houmao Specialist | DeepScientist Source | Support Purpose |
| --- | --- | --- |
| `deepsci-review` | `review` | Audit a substantial draft, paper, or report skeptically. |
| `deepsci-paper-outline` | `paper-outline` | Create, revise, validate, or repair a research-paper outline from experiment evidence. |
| `deepsci-paper-plot` | `paper-plot` | Turn structured numeric data into publication-quality figures using bundled templates. |

## Role Responsibilities

### `deepsci-scout`

- Reads the research brief and operator requirements.
- Searches for related work, public datasets, and standard metrics.
- Produces a `scout-report.md` with problem framing, known baselines, and open questions.
- Hands off to `deepsci-baseline` when framing is stable.

### `deepsci-baseline`

- Reproduces or imports the strongest baseline identified by the scout.
- Records baseline metrics, environment, and acceptance criteria in `artifacts/baselines/`.
- Confirms or waives the baseline gate before the team proceeds to ideation.

### `deepsci-idea`

- Reviews the scout report and baseline result.
- Generates candidate hypotheses and limitation analyses.
- Selects one idea and writes `artifacts/ideas/selected-idea.md`.
- Hands off to `deepsci-optimize` for algorithm-first work or directly to `deepsci-experiment` for implementation-first work.

### `deepsci-optimize`

- Explores the candidate space for the selected idea.
- Maintains an optimization frontier and branch-promotion log in `artifacts/optimization/`.
- Promotes the best candidate to `deepsci-experiment`.

### `deepsci-experiment`

- Implements the selected idea or promoted candidate.
- Runs the main experiment, records `RUN.md` and `RESULT.json` in `experiments/main/`.
- Compares results against the accepted baseline.
- Hands off to `deepsci-analysis` for follow-up campaigns or to `deepsci-decision` for a go/stop call.

### `deepsci-analysis`

- Plans and executes ablations, robustness checks, error analysis, and failure analysis.
- Records slices in `experiments/analysis/`.
- Summarizes whether the main result holds under scrutiny.

### `deepsci-write`

- Drafts the report or paper from durable evidence only.
- Uses `deepsci-paper-outline` and `deepsci-paper-plot` as companions when a full paper is required.
- Writes drafts to `paper/`.

### `deepsci-finalize`

- Consolidates final claims, limitations, and recommendations.
- Exports summary state and any final graphs.
- Produces a completion package in `artifacts/reports/`.

### `deepsci-decision`

- Reviews evidence at any gate and makes explicit transitions.
- Records each decision with reasoning in `artifacts/decisions/`.
- Never blocks completion without operator approval.

## Communication and Control Model

This is an operator-controlled team, not an autonomous loop. The operator owns transitions.

- **Prompting**: The operator sends stage-specific prompts to the active specialist through `houmao-agent-messaging` or the gateway.
- **Handoffs**: When a stage finishes, the operator copies the relevant artifact path or summary into the next specialist's prompt.
- **Mailbox**: Each specialist can use its project mailbox for async context, but the operator reads and routes key handoffs.
- **Memory**: Durable context lives in `memory/` and in the artifact files themselves. Each specialist reads the prior stage's memory and writes its own.
- **Gateway**: The operator uses the gateway for live inspection, reminders, and notifier rounds.
- **Decision gate**: `deepsci-decision` runs only when the operator asks for an explicit transition call.

## Workspace Layout

```text
teams/deepsci-org/
├── source/
│   └── team-design.md          # this document
├── agents/                     # per-role system prompts or skill overrides
│   ├── scout.md
│   ├── baseline.md
│   ├── idea.md
│   ├── optimize.md
│   ├── experiment.md
│   ├── analysis.md
│   ├── write.md
│   ├── finalize.md
│   ├── decision.md
│   ├── review.md
│   ├── paper-outline.md
│   └── paper-plot.md
├── runtime/                    # launch scripts or operator runbooks
│   └── README.md
└── README.md                   # team entry point and quick-start
```

The project overlay at `<repo-root>/.houmao` stores the actual specialist and profile definitions. The `teams/deepsci-org/` directory keeps design documents, role prompts, and operator runbooks under version control.

## Tool and Credential Strategy

- All specialists in the first version use the same tool lane (for example, Kimi) and one project credential to keep the team homogeneous.
- The credential name is `research-kimi` by default.
- If later stages need different models or reasoning levels, create tool-specific variants under separate profile names; do not overload one specialist with conflicting model settings.

## Operational Workflow

1. Operator creates the project overlay (done).
2. Operator adds one project credential (pending).
3. Create one specialist per role using the names and responsibilities above.
4. Create one project profile per specialist for repeatable launch.
5. Launch `deepsci-scout` first with the research brief.
6. After each stage, the operator inspects output and decides the next role.
7. Repeat until the decision role recommends completion, then the operator approves finalization.

## Next Steps

1. Review and approve this design.
2. Add a project credential through `houmao-credential-mgr`.
3. Create the specialists through `houmao-agent-definition`.
4. Create project profiles for repeatable launch.
5. Draft stage-specific system prompts under `teams/deepsci-org/agents/`.
6. Run the first scout stage.
