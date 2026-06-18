# Source Term Mapping

Use this reference when converting source research methods into Isomer Labs
language.

## Accepted Mappings

| Source term or operation | Isomer Labs framing |
| --- | --- |
| lifecycle-level research work | Research Topic, Research Inquiry, or Research Task depending on scope |
| Research Goal | Research Topic; put metrics or targets in optional Measurable Objectives |
| Research Thread | Research Inquiry |
| Research Branch | Research Inquiry Relationship; do not imply a tree or branch collection |
| Isomer Workspace | Topic Workspace through Workspace Path Resolution |
| initial goal or objective text | Research Topic with optional Measurable Objective |
| bounded unit of research work | Research Task |
| one execution attempt | Run |
| forked research route | Research Inquiry Relationship plus Decision Record when a choice is made |
| filesystem area for topic, task, run, output, or agent work | Topic Workspace, Workspace Runtime, semantic Artifact kind, or Agent Workspace through Workspace Path Resolution |
| persistent task state | Workspace Runtime |
| per-agent scratch or local trace area | Agent Workspace or Agent Runtime |
| artifact operation | Artifact, Evidence Item, Decision Record, Gate, Provenance Record, or host API |
| memory operation | Finding, Evidence Item, Artifact, or durable context query |
| command execution | Execution Adapter Command Request with Research Operation Extension Point, Capability Binding, Skill Binding projection, Gate Policy, Scheduler Policy, workspace, and recording refs |
| paper lookup | Literature Provider Binding; record context-only provider output first as a provider-output Artifact before deriving Findings or Evidence Items |
| route decision | Decision Record, possibly resolving a Gate |
| user choice on scope, cost, privacy, safety, publication-facing output, or finality | Gate Policy preflight and Gate through the Operator Agent when human judgment is required |

## Rejected Source Runtime Concepts

Do not port source runtime scheduling terms as Isomer concepts. The Operator
Agent is always the human-facing control boundary. Delegated Agent Team
Instances either advance under approved Coordination Policy or pause for
Operator Agent instruction.

| Source behavior | Isomer skill text should say |
| --- | --- |
| `workspace_mode` | source runtime collaboration detail; do not use as an Isomer mode |
| `continuation_policy` | use Scheduler Policy refs for dispatch behavior, and recommend the next Workflow Stage, Gate, Decision Record, observation, or pause for durable routing |
| `auto_continue` | source scheduler detail; do not schedule turns in skill text |
| `wait_for_user_or_resume` | pause for Operator Agent instruction, or record a Gate or handoff state |
| `continuation_anchor` | next recommended Workflow Stage or Decision Record target |
| `continuation_reason` | pause reason, Gate reason, failure reason, or Decision Record rationale |

## Unsettled Surface Rule

When a method needs a concrete API, schema, provider, command, runner home, prompt-injection mechanism, generated layout, or path outside Workspace Path Resolution, Research Recording Contracts, Research Lifecycle State, CLI Topic Context Resolution, or Research Execution and Extension Contract, use a registered TBD-surface placeholder and add or reuse the id in `tbd-surface-registry.md`.

Do not guess folders such as artifacts, experiments, paper, memory, runs, or agent homes as ad hoc Isomer defaults. Name the semantic Artifact kind or workspace scope and let the Workspace Path Resolver choose the effective path.
