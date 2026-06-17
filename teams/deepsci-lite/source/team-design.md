# DeepScientist Lite Research Team Design

This document designs a small, operator-controlled Houmao research team modeled on a human-led research lab. The team preserves the DeepScientist stage-skill pipeline while using purpose-driven role names. The `deepsci-lite-lead` agent owns the loop: it starts the loop, dispatches the other participants, and ends the loop with a final decision.

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
| `deepsci-lite-lead` | Own the loop | `decision` | Open the loop with a Research Thread plan, dispatch stages, review evidence at gates, and close with a final decision. |
| `deepsci-lite-scout` | Scout and baseline | `scout` + `baseline` | Survey literature, clarify datasets and metrics, then reproduce and verify the chosen baseline. |
| `deepsci-lite-design` | Design approach | `idea` + `optimize` | Generate hypotheses, analyze limitations, design the approach, and search the optimization frontier. |
| `deepsci-lite-experiment` | Run experiments | `experiment` + `analysis-campaign` | Implement the selected approach, run the main experiment, and run follow-up ablations and robustness checks. |
| `deepsci-lite-writer` | Produce manuscript | `write` + `finalize` + `paper-outline` + `paper-plot` + `review` | Draft the report or paper, create outlines and figures, run a skeptical self-review, and finalize claims and exports. |

## Role Responsibilities

### `deepsci-lite-lead`

This agent owns the research loop. It corresponds to a principal investigator who interprets the user's Research Thread direction, plans the loop, dispatches the other participants, reviews evidence at gates, and closes the loop with a final decision.

- Opens the loop by reading the user's Research Thread direction and producing a loop plan.
- Decides which stages to run and what each stage must produce.
- Dispatches `deepsci-lite-scout`, `deepsci-lite-design`, `deepsci-lite-experiment`, and `deepsci-lite-writer` in the standard order.
- Reviews evidence at any gate and makes explicit transition decisions: go, stop, branch, reuse baseline, write, finalize, reset, or request operator input.
- Records each decision with reasoning in `artifacts/decisions/`.
- Closes the loop with a final decision: finalize the manuscript, stop and report partial findings, or request a new Research Thread direction.
- Does not approve quest completion without explicit operator approval.

#### System Prompt

TBD

### `deepsci-lite-scout`

This agent scouts the research landscape and establishes the baseline. It surveys literature, clarifies datasets and metrics, and reproduces the chosen baseline so later experiments have a fair comparison point.

- Reads the loop plan and stage brief from `deepsci-lite-lead`.
- Surveys related work, public datasets, and standard metrics.
- Identifies the strongest baseline candidates.
- Reproduces or imports the selected baseline and records metrics, environment, and acceptance criteria.
- Outputs `scout-report.md` and `artifacts/baselines/`.
- Returns results to `deepsci-lite-lead` for gate review.

#### System Prompt

TBD

### `deepsci-lite-design`

This agent designs the research approach. It generates hypotheses, analyzes limitations, selects the leading idea, and searches the optimization frontier.

- Reads the baseline output and accepted baseline from `deepsci-lite-lead`.
- Generates candidate hypotheses and limitation analyses.
- Selects the leading idea and designs the candidate approach.
- Maintains an optimization frontier and branch-promotion log when algorithm-first search is needed.
- Outputs `artifacts/ideas/selected-idea.md` and `artifacts/optimization/`.
- Returns results to `deepsci-lite-lead` for gate review.

#### System Prompt

TBD

### `deepsci-lite-experiment`

This agent runs the experimental work. It implements the selected design, runs the main experiment, and validates the result through follow-up analyses.

- Reads the selected idea and design brief from `deepsci-lite-lead`.
- Implements the selected approach or promoted candidate.
- Runs the main experiment and records `experiments/main/RUN.md` and `RESULT.json`.
- Compares results against the accepted baseline.
- Plans and executes follow-up ablations, robustness checks, error analysis, and failure analysis.
- Records analysis slices in `experiments/analysis/`.
- Summarizes whether the main result holds under scrutiny.
- Returns results to `deepsci-lite-lead` for gate review.

#### System Prompt

TBD

### `deepsci-lite-writer`

This agent produces the final research manuscript. It drafts, reviews, and finalizes reports and papers from durable evidence.

- Reads the validated experiment evidence from `deepsci-lite-lead`.
- Drafts the report or paper from durable evidence only.
- Creates or repairs outlines and turns structured numeric data into figures.
- Runs a skeptical self-review of substantial drafts.
- Consolidates final claims, limitations, recommendations, and summary exports.
- Writes drafts to `paper/` and final reports to `artifacts/reports/`.
- Returns the manuscript to `deepsci-lite-lead` for final gate review.

#### System Prompt

TBD

## When This Lite Design Fits

Use this design when:

- The operator wants fewer agents to launch and track.
- Stages are short enough that handoffs would add overhead.
- The team will run on a single tool lane and model family.
- The operator prefers a single lead agent to own loop planning and dispatch.

Use the full 12-role design (`teams/deepsci-org/source/team-design.md`) when:

- Different stages need different tools or models.
- A stage becomes large enough to warrant its own persistent specialist.
- Multiple experiments or analyses run in parallel and need separate mailboxes.

## Communication and Control Model

The operator sets the Research Thread direction; the lead owns loop execution.

- **Prompting**: The operator prompts `deepsci-lite-lead` with a Research Thread direction. The lead then dispatches the other participants.
- **Handoffs**: `deepsci-lite-lead` passes a stage brief and relevant artifact refs to each participant. Participants return results to the lead.
- **Mailbox**: Each role uses its project mailbox for async context. `deepsci-lite-lead` routes key handoffs.
- **Memory**: Durable context lives in `memory/` and in artifact files.
- **Gateway**: The operator uses the gateway for live inspection, reminders, and notifier rounds.
- **Decision gate**: `deepsci-lite-lead` reviews evidence and decides transitions. The operator resolves Gates that require human approval.

## Tool and Credential Strategy

- All five roles use the same tool lane (for example, Kimi) and one project credential to keep the team homogeneous.
- The default credential name is `research-kimi`.
- If a phase later needs a different model or reasoning level, create a profile variant rather than a new specialist.

## Operational Workflow

1. Operator creates the project overlay (done).
2. Operator adds one project credential (pending).
3. Create one specialist per purpose role.
4. Create one project profile per specialist for repeatable launch.
5. Launch `deepsci-lite-lead` first with the Research Thread direction.
6. `deepsci-lite-lead` produces a loop plan and dispatches `deepsci-lite-scout`.
7. After each participant finishes, `deepsci-lite-lead` reviews evidence and dispatches the next participant or stops for a Gate.
8. The loop ends when `deepsci-lite-lead` records a final decision and awaits operator approval to finalize.

## Next Steps

1. Review and approve this lite design, or switch to the full design at `teams/deepsci-org/source/team-design.md`.
2. Add a project credential through `houmao-credential-mgr`.
3. Create the five specialists through `houmao-agent-definition`.
4. Create project profiles for repeatable launch.
5. Draft role-specific system prompts in the `#### System Prompt` sections above.
6. Launch `deepsci-lite-lead` with a Research Thread direction.
