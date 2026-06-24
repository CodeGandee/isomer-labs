## Context

The completed generated-content layout change gives Isomer a default Project-local generated content root at `isomer-content/` and a default Topic Workspace base at `isomer-content/topic-ws/`. `initialize_project` currently chooses those defaults internally and writes matching Project Manifest `[paths]` entries. Users who want another generated-content directory must initialize with the default and then manually edit the Project Manifest and move files, which is awkward during fresh Project bootstrap.

This change builds on that layout. It adds an init-time CLI selector for the generated content root while preserving the same generated policy files, manifest path-default mechanism, and Project-local safety rules.

## Goals / Non-Goals

**Goals:**

- Add `isomer-cli project init --content-dir <content-dir>` for fresh Project initialization.
- Resolve the selected content root relative to the Project root unless an absolute path is supplied, then reject values outside the Project root.
- Reject content roots inside `.isomer-labs/` and unsafe collisions with `.isomer-labs/` or `.houmao/`.
- Derive `topic_workspace_base_dir` as `<content-dir>/topic-ws`.
- Create the first Topic Workspace under `<content-dir>/topic-ws/<topic-id>/`.
- Write manifest `[paths]` values that preserve the user's chosen content directory in project-relative form when possible.
- Keep the omitted-option default exactly as `isomer-content/`.

**Non-Goals:**

- Do not add a separate `--topic-workspace-base-dir` option in this change.
- Do not allow generated content outside the Project root.
- Do not migrate existing Projects or add force-overwrite behavior.
- Do not create Workspace Runtime state during initialization.
- Do not change runtime path precedence beyond consuming the manifest values written by init.

## Decisions

### Add `--content-dir` to `isomer-cli project init`

The public shape will be:

```bash
isomer-cli project init [topic-id] --content-dir <content-dir>
```

The option belongs on `project init` rather than `project paths preview` because the user is choosing what files fresh initialization creates and what path defaults it records.

Alternative considered: require users to edit `[paths].isomer_content_root` after init. That keeps the CLI smaller but makes the first Topic Workspace and content-root policy files land in the wrong place, which is the problem this change solves.

### Derive the Topic Workspace base from the content root

When the user supplies `--content-dir custom-content`, init writes:

```toml
[paths]
isomer_content_root = "custom-content"
topic_workspace_base_dir = "custom-content/topic-ws"
```

and creates `custom-content/topic-ws/<topic-id>/`.

Alternative considered: add a second option for `topic_workspace_base_dir`. That would give more control but adds a second path that can conflict with the selected content root. Existing Project Manifest editing remains available for advanced custom layouts.

### Validate before writing Isomer config or content material

The selected content root must resolve inside the Project root and outside `.isomer-labs/`. It must not equal `.isomer-labs/` or `.houmao/`, and it must not place the derived Topic Workspace base inside those directories. Existing-manifest refusal still happens before mutation. Houmao bootstrap still must succeed before Isomer config and content files are written, so a bootstrap failure does not leave content material behind.

Alternative considered: create the content root before Houmao bootstrap so path errors surface early. That risks leaving generated files behind when Houmao bootstrap fails, so validation should be early but filesystem mutation should remain after successful bootstrap.

### Preserve project-relative manifest text

When the selected content root is inside the Project root, generated manifest values should be project-relative strings such as `custom-content` and `custom-content/topic-ws`. This keeps manifests portable. Absolute values are accepted only if they resolve inside the Project root, and then can still be rendered as project-relative values in the generated manifest.

Alternative considered: preserve the exact CLI input string. That would keep user input verbatim but could write absolute machine-local paths into a fresh Project Manifest even when a portable relative value is available.

## Risks / Trade-offs

- Users may expect `--content-dir` to move existing content in an existing Project -> Milestone 1 init still refuses existing manifests, so docs and diagnostics must state this is fresh-init only.
- A custom content directory could already contain files -> Init should allow an existing empty or policy-compatible directory only when safe, and tests should cover no unintended overwrites. If ambiguity exists, fail with diagnostics rather than merging.
- Additional path validation can duplicate Project Manifest validation -> Keep validation helper reuse small and focused so `project init` and Project validation enforce the same project-local rules.
- Two active changes touch generated-content defaults -> Apply this after the generated-content layout change, or keep the tasks explicit that this builds on `isomer_content_root` and `topic_workspace_base_dir`.

## Migration Plan

Fresh Projects can start using `--content-dir` immediately after implementation. Existing Projects should edit their Project Manifest and move content manually or wait for a future migration command; this change does not alter existing Project behavior.

Rollback is straightforward before runtime work starts: rerun initialization in a clean directory without `--content-dir`, or edit `[paths]` and move generated content back to `isomer-content/`.

## Open Questions

- None for this change. A future change can decide whether `--topic-workspace-base-dir` is useful for advanced layouts.
