# Storage Validate

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve Project, Research Topic, Topic Workspace, Topic Workspace Manifest, and semantic paths through `storage-resolve`.
2. Validate `topic.repos.main`, `topic.repos.main.tmp`, `topic.repos.main.isomer_managed`, projection roots, `topic.records.*`, `topic.runtime`, and any requested `custom.*` labels against Workspace Path Resolution evidence.
3. Validate additional non-main `topic.repos.*` labels and confirm they are supporting repositories, not Topic Actor Workspace or Agent Workspace worktree sources.
4. Check path safety, storage profile consistency, path source, default-layout fallback evidence, ignored tmp posture, tracked tmp contents, and hard-coded default-only evidence.
5. Report blockers instead of silently repairing unsafe paths, missing bindings, non-Git repositories, cross-topic refs, or ambiguous custom labels.

If the user's task does not map cleanly to these steps, validate the labels named in the prompt first, then report which storage checks were skipped.

## Output

Report the validation outcome and selected Research Topic, then summarize semantic paths, Topic Main Development Repository, local temporary-path posture, projection roots, custom labels, storage-profile evidence, blockers, and the next action.

## Guardrails

- MUST use Workspace Path Resolution for storage answers. Do not infer the selected Topic Workspace by scanning sibling directories, and do not edit `topic-workspace.toml` by hand.
