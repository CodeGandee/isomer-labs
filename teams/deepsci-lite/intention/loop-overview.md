# Loop Overview: deepsci-lite

## Objective

Run a complete research cycle from problem framing through final reporting using a small, operator-controlled Houmao agent team. The loop follows the DeepScientist stage-skill pipeline in a condensed form: scout the landscape and establish a baseline, design the approach, run experiments, write the manuscript, and make explicit transition decisions at each gate.

The `deepsci-lite-lead` agent owns the loop. It starts the loop by interpreting the user's chosen Research Thread, dispatches the other participants in order, and ends the loop with a final completion or stop decision. The loop supports two Run-level control modes. In automatic mode, the lead advances the team through the standard workflow and stops at Gates for human resolution. In manual mode, the user drives selected participants through the Operator Agent, and the lead remains the authority for opening and closing the loop.

## Participants

| Participant | Purpose | DeepScientist Source |
| --- | --- | --- |
| `deepsci-lite-lead` | Own the loop: open with a Research Thread plan, dispatch stages, review evidence at gates, and close with a final decision. | `decision` |
| `deepsci-lite-scout` | Scout literature, datasets, and metrics; reproduce and verify the chosen baseline. | `scout` + `baseline` |
| `deepsci-lite-design` | Generate hypotheses, analyze limitations, design the approach, and search the optimization frontier. | `idea` + `optimize` |
| `deepsci-lite-experiment` | Implement the selected approach, run the main experiment, and validate results through follow-up analyses. | `experiment` + `analysis-campaign` |
| `deepsci-lite-writer` | Draft, review, and finalize the report or paper from durable evidence. | `write` + `finalize` + companions |

## Operating Model

### Lead-Owned Loop

- The loop begins when the user gives `deepsci-lite-lead` a Research Thread direction or Research Goal.
- `deepsci-lite-lead` produces an initial loop plan: which stages to run, what each stage must produce, and where Gates require human approval.
- `deepsci-lite-lead` dispatches `deepsci-lite-scout`, `deepsci-lite-design`, `deepsci-lite-experiment`, and `deepsci-lite-writer` in the standard order.
- After each stage completes, `deepsci-lite-lead` reviews the produced evidence and decides whether to continue, revise, branch, or stop.
- The loop ends when `deepsci-lite-lead` records a final decision: finalize the manuscript, stop and report partial findings, or request a new Research Thread direction from the user.

### Automatic Mode

- Each Run has `control_mode = automatic`.
- `deepsci-lite-lead` dispatches participants according to the approved workflow and Gate policy.
- The standard sequence is `lead` → `scout` → `design` → `experiment` → `writer` → `lead`.
- `deepsci-lite-lead` stops at Gates and waits for human resolution before continuing.
- Gates occur at irreversible or claim-shaping decisions: baseline acceptance or waiver, idea selection, experiment validation, finalization, and destructive actions.

### Manual Mode

- Each Run has `control_mode = manual`.
- The user gives the Operator Agent a single-stage or multi-step prompt targeting selected participants.
- `deepsci-lite-lead` still opens and closes the loop; manual prompts execute inside the lead's loop plan.
- The Operator Agent opens a durable handoff in Workspace Runtime before sending any direct message to a participant.
- Each handoff carries a resolved Completion Watcher Contract derived from Coordination Policy defaults.
- The Operator Agent observes file, channel, inspection, or adapter signals, normalizes them, and records handoff completion in Workspace Runtime before advancing.
- For a single-stage prompt, the Operator Agent summarizes completion and waits for the next user instruction.
- For a multi-step prompt, the Operator Agent may continue to the next in-scope step without asking, but it must stop at any Gate, failure, stale handoff, invalid artifact, missing evidence, or out-of-scope step.

### Research Thread Steering

- The human user decides which Research Thread or Research Branch the team pursues.
- `deepsci-lite-lead` translates that direction into a Research Goal, Measurable Objective, or Exploratory Goal and into a concrete loop plan.
- The team executes inside one or more Isomer Workspaces, each realizing one Research Task.
- A Research Thread can contain both automatic Runs and manual Runs.

### Collaboration Rules

- `deepsci-lite-lead` is the only participant that can open a new loop, dispatch stages, and close a loop.
- Other participants do not self-advance; they return results to `deepsci-lite-lead`.
- Each participant reads durable context from Workspace Runtime, `memory/`, and artifacts produced by earlier stages.
- Each participant writes outputs to predictable artifact paths under `artifacts/`, `experiments/`, or `paper/`.
- Handoffs between participants are recorded in Workspace Runtime with produced artifact refs and provenance.
- `deepsci-lite-lead` cannot approve quest completion without explicit human approval.

## Workspace Expectations

- The loop uses the Houmao project overlay at the repository root (`<repo-root>/.houmao`).
- Each participant maps to one project specialist and one project profile for repeatable launch.
- All participants initially share one tool lane and one project credential to keep the loop homogeneous.
- Design documents and runbooks live under `teams/deepsci-lite/`; generated loop material lives under `teams/deepsci-lite/execplan/`.

## Constraints

- `deepsci-lite-lead` cannot approve completion or finalize a Research Thread without explicit human approval.
- Participants other than `deepsci-lite-lead` cannot open new loops or dispatch other participants.
- Participants must not invent unsupported claims; the writer works from durable evidence only.
- Manual Mode does not bypass Gates.
- Manual Mode cannot advance beyond the user's declared prompt scope.
- Auto-continue is disabled by default; advancement follows workflow policy and Gate resolution.
- All baseline, experiment, and analysis artifacts must include reproducibility notes (environment, commands, data references).

## Open Questions

- Which tool lane and credential will the participants use? (Default candidate: Kimi with one project credential.)
- Which loop topology fits best: `tree-loop` for a strict stage sequence, or `generic-loop` for more flexible handoffs?
- Which Workflow Stages require Gates, and which can advance automatically?
- What are the default Completion Watcher Contracts for manual handoffs? (File observation, channel reply, adapter event, or agent inspection.)
- How many revision rounds should a single stage allow before human intervention is required?
- How are Research Threads, Research Branches, and Research Tasks created and named in this loop?
