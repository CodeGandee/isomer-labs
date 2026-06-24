# Help

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Print a concise description of `isomer-admin-project-mgr`: it initializes, checks, cleans up, and manages an Isomer Project by coordinating Project config, Research Topics, Topic Workspaces, Workspace Runtime preparation, and the Project-level Houmao overlay.
2. Explain that invoking this skill without a prompt defaults to this `help` output.
3. List the available subcommands: `help`, `init-project`, `cleanup-project`, `check-project`, `list-topics`, `show-context`, `init-runtime`, `prep-runtime`, and `specialize-team`.
4. Explain the main outputs: Project root, Project Manifest path, generated content root, Houmao Project overlay status, topic and workspace refs, Effective Topic Context, runtime status, cleanup plan, diagnostics, commands run, and next operator action.
5. State the key guardrails: `isomer-cli project init` bootstraps `.isomer-labs/`, `.houmao/`, and the selected generated content root (`isomer-content/` by default or `--content-dir <content-dir>` when supplied), cleanup starts with `isomer-cli project cleanup --part <part> --dry-run` and uses `isomer-cli project cleanup --part <part> --yes` only after review, whole content-root removal requires `--purge-content-root`, checks stay read-only, Workspace Runtime creation is explicit, readiness preparation is explicit, and Topic Team Specialization belongs to `isomer-admin-topic-team-specialize`.

If the user's task does not map cleanly to these steps, use your native planning tool to decide which parts of the skill usage information to print, then execute the plan.
