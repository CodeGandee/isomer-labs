# Source Term Mapping

Use this reference when converting source research methods into Isomer Labs
language.

## Accepted Mappings

| Source term or operation | Isomer Labs framing |
| --- | --- |
| lifecycle-level research work | Research Thread |
| initial goal or objective text | Research Goal, Measurable Objective, or Exploratory Goal |
| bounded unit of research work | Research Task |
| one execution attempt | Run |
| forked research route | Research Branch |
| filesystem area for one task | Isomer Workspace, if storage scope is known |
| persistent task state | Workspace Runtime |
| per-agent scratch or local trace area | Agent Workspace or Agent Runtime |
| artifact operation | Artifact, Evidence Item, Decision Record, Gate, Provenance Record, or host API |
| memory operation | Finding, Evidence Item, Artifact, or durable context query |
| command execution | Capability Binding through an Execution Adapter |
| paper lookup | literature search capability; provider is unsettled |
| route decision | Decision Record, possibly resolving a Gate |
| user choice on scope, cost, privacy, safety, or finality | Gate through the Operator Agent |

## Rejected Source Runtime Concepts

Do not port source runtime scheduling terms as Isomer concepts. The Operator
Agent is always the human-facing control boundary. Delegated Agent Team
Instances either advance under approved Coordination Policy or pause for
Operator Agent instruction.

| Source behavior | Isomer skill text should say |
| --- | --- |
| `workspace_mode` | source runtime collaboration detail; do not use as an Isomer mode |
| `continuation_policy` | recommend the next Workflow Stage, Gate, Decision Record, observation, or pause |
| `auto_continue` | source scheduler detail; do not schedule turns in skill text |
| `wait_for_user_or_resume` | pause for Operator Agent instruction, or record a Gate or handoff state |
| `continuation_anchor` | next recommended Workflow Stage or Decision Record target |
| `continuation_reason` | pause reason, Gate reason, failure reason, or Decision Record rationale |

## Unsettled Surface Rule

When a method needs a concrete path, API, schema, provider, command, storage
root, runner home, prompt-injection mechanism, or generated layout, use
`[[tbd-surface:<id>]]` and add or reuse the id in `tbd-surface-registry.md`.

Do not guess folders such as artifacts, experiments, paper, memory, runs, or
agent homes as Isomer defaults.

