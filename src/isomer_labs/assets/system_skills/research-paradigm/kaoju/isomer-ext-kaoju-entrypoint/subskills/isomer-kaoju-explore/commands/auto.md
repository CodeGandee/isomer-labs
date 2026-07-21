# Explore: Auto

## Workflow

1. **Read the user's task prompt and resolved context**. Identify the Research Topic, implied Kaoju stage, prior survey state, active Runs, and the user's goal.
2. **Select a context mode**. Map the prompt to the most specific subcommand: `directions`, `reading-list`, `intake`, `comparison`, `trial`, `paper`, or `wiki`. Use `directions` when the stage is unclear.
3. **Run that mode's planning discussion in memory**. Ask up to five clarification questions, one material choice at a time. Do not write files or artifacts.
4. **Build the plan summary**. Include selected command, scope, evidence strategy, output form, risks, and exact public invocation.
5. **Ask for consent**. If the user confirms, hand off to the selected command. If not, stop and return the plan as a paused recommendation.

If the task does not map cleanly to these steps, use the native planning tool to compare the user's prompt against the available context modes and recommend one.

## Gates, Blockers, and Resume

Pause on unresolved context, missing workspace readiness, or an open planning question. Resume by re-invoking `explore` with the same prompt and any previously resolved context.
