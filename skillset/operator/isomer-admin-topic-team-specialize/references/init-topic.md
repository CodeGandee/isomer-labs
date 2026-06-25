# Init Topic

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. `init-topic` has no predecessor artifact requirement, so do not refuse to run because earlier flow artifacts are missing.
2. Read the user's Research Topic prompt, source material, or explicitly supplied topic ref, and decide whether it contains enough topic substance to summarize.
3. If the user did not supply a Research Topic, stop and ask for the concrete research topic before creating any directory or topic overview file. Do not infer the topic from Project Manifest defaults, the registered id `default`, current directory, existing Topic Workspace names, or a generic placeholder statement.
4. If a topic ref is supplied but its registered Research Topic Config only contains a generic or placeholder statement, ask the user for the concrete research topic before creating or overwriting `topic-overview.md`.
5. If no topic workspace directory is supplied and the user-supplied Research Topic is clear, derive a short topic slug and choose a provisional seed directory under the effective Topic Workspace base. Use the Project Manifest `topic_workspace_base_dir` when present; otherwise use the built-in `isomer-content/topic-ws/` base, giving a normal default such as `isomer-content/topic-ws/<topic-slug>/`.
6. If no topic workspace directory is supplied and the Research Topic is unclear, ask for more topic detail before choosing a directory.
7. If the derived or supplied directory is outside the Project root, already exists, collides with registered Project material, or is otherwise ambiguous, stop and ask the user to confirm that directory or provide another one before creating files.
8. Create the selected topic directory and `<topic-dir>/topic-def/` only after the Research Topic and directory are clear.
9. Write `<topic-dir>/topic-def/topic-overview.md` from the agent's understanding of the Research Topic with the sections in **Topic Overview Template**.
10. Report the created `topic_overview_path`, provisional status, assumptions, open questions, and the next safe subcommand.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the topic prompt, selected directory, Project Config boundary, and guardrails in this skill, then execute the plan.

## Prerequisite Artifacts

No predecessor artifacts are required. This is the first procedural step.

If the user is actually asking for a later procedural subcommand and predecessor artifacts are missing, refuse to run that later subcommand and tell the user to run `init-topic` first.

## Topic Overview Template

Write `topic-overview.md` with these sections:

```markdown
# Topic Overview

## Research Topic

## Agent Understanding

## Scope

## Initial Objectives

## Assumptions

## Open Questions

## Source Prompt or Source Material
```

## Output Contract

Report:

- `research_topic_ref`: the topic label or provisional topic id.
- `topic_workspace_ref`: the selected directory as a provisional topic workspace seed unless it is already registered.
- `topic_overview_path`: `<topic-dir>/topic-def/topic-overview.md`.
- `topic_registration_status`: registered, provisional, blocked, or not checked.
- `open_questions`: questions that should go to `clarify-topic`.
- `next_operator_action`: usually `clarify-topic` or `specialize-team`.

## Guardrails

Do not create files until the user has supplied a concrete Research Topic and the topic workspace directory is clear. A clear user-supplied Research Topic without an explicit directory may use the derived `isomer-content/topic-ws/<topic-slug>/` default; missing topics, generic default topic registrations, unclear topics, collisions, and unsafe paths still require user confirmation.

Do not hand-edit `.isomer-labs/manifest.toml` or Research Topic Config files. If the topic must become authoritative Project Manifest state, route through `isomer-cli project topics create <topic-id> --statement "<research topic>"` or another supported Isomer CLI/API path when available and otherwise report a blocker.

Do not claim the created directory is a registered Research Topic or Topic Workspace unless the Project Manifest already proves that registration.
