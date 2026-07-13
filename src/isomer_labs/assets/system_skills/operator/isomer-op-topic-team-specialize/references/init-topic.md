# Init Topic

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. `init-topic` has no predecessor artifact requirement, so do not refuse to run because earlier flow artifacts are missing.
2. Read the user's Research Topic prompt, source material, or explicitly supplied topic ref, and decide whether it contains enough topic substance to status.
3. If the user did not supply a Research Topic, stop before creating files:
   - Ask for the concrete research topic before creating any directory or topic overview file.
   - Do not infer the topic from Project Manifest defaults, the registered id `default`, current directory, existing Topic Workspace names, or a generic placeholder statement.
4. If a topic ref is supplied but its registered Research Topic Config only contains a generic or placeholder statement:
   - Ask the user for the concrete research topic before creating or overwriting `topic.intent.overview`.
5. If no topic workspace directory is supplied and the user-supplied Research Topic is clear, choose a provisional seed directory:
   - Derive a short topic slug.
   - Use the Project Manifest `topic_workspace_base_dir` when present.
   - Otherwise use the built-in `isomer-content/topic-ws/` base, giving a normal default such as `isomer-content/topic-ws/<topic-slug>/`.
6. If no topic workspace directory is supplied and the Research Topic is unclear, ask for more topic detail before choosing a directory.
7. If the derived or supplied directory is unsafe or ambiguous, stop before creating files:
   - Treat paths outside the Project root, existing paths, collisions with registered Project material, and other ambiguous paths as blockers.
   - Ask the user to confirm that directory or provide another one.
8. Create the selected topic directory only after the Research Topic and directory are clear.
9. Route topic understanding to `resolve-topic-intent`, which resolves `topic.intent.overview` and writes the topic overview at the resolved path.
10. Report topic initialization output:
   - Include `topic_overview_label`, the resolved `topic_overview_path`, provisional status, assumptions, open questions, and the next safe subcommand.
   - When the created topic material is not already manifest-backed, name `ensure-topic-registration` as the next registration action before specialization or setup.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the topic prompt, selected directory, Project Config boundary, and guardrails in this skill, then execute the plan.

## Prerequisite Artifacts

No predecessor artifacts are required. This is the first procedural step.

If the user is actually asking for a later procedural subcommand and predecessor artifacts are missing, refuse to run that later subcommand directly and offer targeted fast-forward recovery from `init-topic` toward the selected target. Use `python scripts/query_step_dependencies.py path --target <selected-target> --include-target` for the inclusive default path or `--exclude-target` for the exclusive path.

## Topic Overview Template

`resolve-topic-intent` writes `topic.intent.overview` with these sections:

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

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

### Essential Output

State whether topic initialization completed, is provisional, blocked, or was not checked. Name the Research Topic and Topic Workspace, the overview path when created or resolved, registration posture, open questions for `clarify-topic`, and the next operator action.

### Complete Output

Group the complete explanation by topic identity, overview label and path, storage profile and source, registration posture, open questions, and next operator action.

## Guardrails

Do not create files until the user has supplied a concrete Research Topic and the topic workspace directory is clear. A clear user-supplied Research Topic without an explicit directory may use the derived `isomer-content/topic-ws/<topic-slug>/` default; missing topics, generic default topic registrations, unclear topics, collisions, and unsafe paths still require user confirmation.

Do not hand-edit `.isomer-labs/manifest.toml` or Research Topic Config files. If the topic must become authoritative Project Manifest state, route to `ensure-topic-registration`, which may use `isomer-cli project topics create <topic-id> --statement "<research topic>" --workspace-dir <topic-workspace-dir>` or another supported Isomer CLI/API path when available and otherwise report a blocker.

Do not claim the created directory is a registered Research Topic or Topic Workspace unless the Project Manifest already proves that registration.
