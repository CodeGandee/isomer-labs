# Manual Mode Is Run-Level Control Mode

Manual mode will be represented at the Run level instead of the Project, Research Topic, Research Inquiry, Research Task, or handoff-only level. A Run records its control mode, such as manual or automatic, and manual Runs preserve prompt-scope metadata so the Operator Agent can recover whether the user asked for a single-stage operation or a multi-step operation. Individual handoffs still record their dispatch source, resolved watcher contract, and completion state, but they do not replace the Run-level mode.

## Status

accepted

## Considered Options

- Store control mode on each Run, with prompt-scope metadata for manual Runs.
- Store mode on each Research Task and let Runs inherit it.
- Store mode on the whole Research Topic or Research Inquiry.
- Store no Run mode and infer manual behavior only from handoff records.

## Consequences

- One Research Topic, Research Inquiry, or Research Task can contain both manual and automatic Runs, which supports retries and mixed operating styles.
- GUI, CLI, and recovery views can show the active control mode without scanning every handoff.
- Workspace Runtime must store Run-level control mode plus enough prompt-scope metadata to reconstruct advancement behavior after interruption.
