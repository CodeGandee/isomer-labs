# Help

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Print a concise description of `isomer-admin-project-mgr`:
   - It initializes, checks, cleans up, and manages an Isomer Project.
   - It coordinates Project config, Research Topics, Topic Workspaces, Workspace Runtime preparation, and the Isomer-managed Houmao overlay under `.isomer-labs/`.
2. Explain that invoking this skill without a prompt defaults to this `help` output.
3. List the available subcommands: `help`, `init-project`, `cleanup-project`, `move-content`, `check-project`, `list-topics`, `show-context`, `init-runtime`, `prep-runtime`, `prepare-topic`, `manual-research`, and `specialize-team`.
4. Explain the main outputs:
   - Project root, Project Manifest path, generated content root, Houmao Project directory, and overlay status.
   - Topic and workspace refs, Effective Topic Context, effective Topic Actor context when selected, runtime status, and Topic Workspace visibility layout summary.
   - Cleanup plan, relocation plan, diagnostics, commands run, and next operator action.
5. State the key guardrails:
   - `isomer-cli project init` bootstraps `.isomer-labs/`, `.isomer-labs/.houmao/`, and the selected generated content root without creating a Research Topic.
   - Root `.houmao/` is external user-owned Houmao state if present.
   - Research Topic lifecycle uses `isomer-cli project topics create`, `show`, `update`, `delete --dry-run`, and `delete --yes`.
   - Cleanup starts with `isomer-cli project cleanup --part <part> --dry-run`; use `--yes` only after review.
   - Whole content-root removal requires `--purge-content-root`.
   - Generated content-root relocation starts with `isomer-cli project content-root move --to <content-dir> --dry-run`; use `--yes` only after review.
   - Relocation does not rewrite Workspace Runtime records or Pixi environments.
   - Checks stay read-only, Workspace Runtime creation is explicit, and readiness preparation is explicit.
   - Common topic preparation belongs to `isomer-admin-topic-prepare`.
   - Topic Actor CRUD, Topic Actor Workspace materialization, actor-scoped diagnostics, optional topology inspection, and branch helpers belong to `isomer-admin-topic-workspace-mgr`.
   - Human-orchestrated manual research sessions and per-actor start packs belong to `isomer-admin-manual-research-session`.
   - Topic Team Specialization belongs to `isomer-admin-topic-team-specialize` only when the user explicitly asks for a Domain Agent Team Template.

If the user's task does not map cleanly to these steps, use your native planning tool to decide which parts of the skill usage information to print, then execute the plan.
