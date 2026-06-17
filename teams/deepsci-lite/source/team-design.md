# DeepScientist Lite Research Team Design

This document designs a small, operator-controlled Houmao research team modeled on a human-led research lab. The team preserves the DeepScientist stage-skill pipeline while using purpose-driven role names. The operator still controls every major transition.

For the full 12-role design, see `teams/deepsci-org/source/team-design.md`.

## Naming Convention

Every specialist uses the prefix `deepsci-lite-` followed by a purpose-driven role name:

```text
deepsci-lite-<purpose>
```

The purpose suffix reflects what the agent produces or governs, not a generic human job title.

## Role Map

| Houmao Specialist | Purpose | Merged DeepScientist Sources | Responsibility |
| --- | --- | --- | --- |
| `deepsci-lite-scout` | Scout and baseline | `scout` + `baseline` | Survey literature, clarify datasets and metrics, then reproduce and verify the chosen baseline. |
| `deepsci-lite-design` | Design approach | `idea` + `optimize` | Generate hypotheses, analyze limitations, design the approach, and search the optimization frontier. |
| `deepsci-lite-experiment` | Run experiments | `experiment` + `analysis-campaign` | Implement the selected approach, run the main experiment, and run follow-up ablations and robustness checks. |
| `deepsci-lite-writer` | Produce manuscript | `write` + `finalize` + `paper-outline` + `paper-plot` + `review` | Draft the report or paper, create outlines and figures, run a skeptical self-review, and finalize claims and exports. |
| `deepsci-lite-lead` | Coordinate and decide | `decision` | Review evidence at each gate and make explicit go, stop, branch, reset, or finalize transitions. |

## Role Responsibilities

### `deepsci-lite-scout`

This agent scouts the research landscape and establishes the baseline. It surveys literature, clarifies datasets and metrics, and reproduces the chosen baseline so later experiments have a fair comparison point.

- Reads the research brief and operator requirements.
- Surveys related work, public datasets, and standard metrics.
- Identifies the strongest baseline candidates.
- Reproduces or imports the selected baseline and records metrics, environment, and acceptance criteria.
- Outputs `scout-report.md` and `artifacts/baselines/`.
- Requests operator approval to open the baseline gate.

#### System Prompt

TBD

### `deepsci-lite-design`

This agent designs the research approach. It generates hypotheses, analyzes limitations, selects the leading idea, and searches the optimization frontier.

- Reads the baseline output and accepted baseline.
- Generates candidate hypotheses and limitation analyses.
- Selects the leading idea and designs the candidate approach.
- Maintains an optimization frontier and branch-promotion log when algorithm-first search is needed.
- Outputs `artifacts/ideas/selected-idea.md` and `artifacts/optimization/`.
- Hands off to `deepsci-lite-experiment` with a clear implementation brief.

#### System Prompt

TBD

### `deepsci-lite-experiment`

This agent runs the experimental work. It implements the selected design, runs the main experiment, and validates the result through follow-up analyses.

- Implements the selected approach or promoted candidate.
- Runs the main experiment and records `experiments/main/RUN.md` and `RESULT.json`.
- Compares results against the accepted baseline.
- Plans and executes follow-up ablations, robustness checks, error analysis, and failure analysis.
- Records analysis slices in `experiments/analysis/`.
- Summarizes whether the main result holds under scrutiny.

#### System Prompt

TBD

### `deepsci-lite-writer`

This agent produces the final research manuscript. It drafts, reviews, and finalizes reports and papers from durable evidence.

- Drafts the report or paper from durable evidence only.
- Creates or repairs outlines and turns structured numeric data into figures.
- Runs a skeptical self-review of substantial drafts.
- Consolidates final claims, limitations, recommendations, and summary exports.
- Writes drafts to `paper/` and final reports to `artifacts/reports/`.

#### System Prompt

TBD

### `deepsci-lite-lead`

This agent coordinates the team and makes explicit transition decisions. It corresponds to a principal investigator who reviews evidence at major gates before the team moves forward.

- Reviews evidence at any gate.
- Makes explicit transition decisions: go, stop, branch, reuse baseline, write, finalize, reset, or request operator input.
- Records each decision with reasoning in `artifacts/decisions/`.
- Does not approve quest completion without explicit operator approval.

#### System Prompt

TBD

## When This Lite Design Fits

Use this design when:

- The operator wants fewer agents to launch and track.
- Stages are short enough that handoffs would add overhead.
- The team will run on a single tool lane and model family.
- The operator prefers to think in four research phases: baseline, design, experiment, write.

Use the full 12-role design (`teams/deepsci-org/source/team-design.md`) when:

- Different stages need different tools or models.
- A stage becomes large enough to warrant its own persistent specialist.
- Multiple experiments or analyses run in parallel and need separate mailboxes.

## Communication and Control Model

The operator still owns transitions.

- **Prompting**: The operator sends phase-specific prompts to the active role.
- **Handoffs**: When a phase finishes, the operator copies the relevant artifact summary into the next role's prompt.
- **Mailbox**: Each role uses its project mailbox for async context. The operator routes key handoffs.
- **Memory**: Durable context lives in `memory/` and in artifact files.
- **Gateway**: The operator uses the gateway for live inspection, reminders, and notifier rounds.
- **Decision gate**: `deepsci-lite-lead` runs only when the operator asks for an explicit transition call.

## Tool and Credential Strategy

- All five roles use the same tool lane (for example, Kimi) and one project credential to keep the team homogeneous.
- The default credential name is `research-kimi`.
- If a phase later needs a different model or reasoning level, create a profile variant rather than a new specialist.

## Operational Workflow

1. Operator creates the project overlay (done).
2. Operator adds one project credential (pending).
3. Create one specialist per purpose role.
4. Create one project profile per specialist for repeatable launch.
5. Launch `deepsci-lite-scout` first with the research brief.
6. After each phase, the operator inspects output and decides the next role.
7. `deepsci-lite-lead` runs at major gates; final completion still requires operator approval.

## Next Steps

1. Review and approve this lite design, or switch to the full design at `teams/deepsci-org/source/team-design.md`.
2. Add a project credential through `houmao-credential-mgr`.
3. Create the five specialists through `houmao-agent-definition`.
4. Create project profiles for repeatable launch.
5. Draft role-specific system prompts in the `#### System Prompt` sections above.
6. Run the first scout phase.
