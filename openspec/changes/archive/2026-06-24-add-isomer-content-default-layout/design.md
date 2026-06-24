## Context

Isomer currently initializes new Projects with `.isomer-labs/manifest.toml`, a Research Topic Config, `.houmao/`, and a default Topic Workspace under `topic-workspaces/<topic-id>/`. Workspace Path Resolution already supports Project Manifest path defaults through `[paths]` and `[path_defaults]`, and the domain language keeps `.isomer-labs/` as configuration and discovery state rather than a generated-content home.

The topic-team specialization skill now has an `init-topic` subcommand that can create provisional topic material. Without a default output root, it must ask for a directory whenever the user omits one. The new layout gives CLI commands and skills a predictable Project-local default while keeping generated bodies out of `.isomer-labs/`.

## Goals / Non-Goals

**Goals:**

- Create `isomer-content/` during Project initialization as the default root for Isomer-generated content.
- Keep `isomer-content/README.md` and `isomer-content/.gitignore` trackable while ignoring generated content underneath by default.
- Move default Topic Workspace paths to `isomer-content/topic-ws/<topic-id>/`.
- Store default path policy in the Project Manifest so skills and CLI path resolution share the same source.
- Let `init-topic` derive a provisional topic directory for clear topics when no output directory is supplied.
- Preserve existing Projects that explicitly register `topic-workspaces/<topic-id>/` or another project-local Topic Workspace path.

**Non-Goals:**

- Do not migrate existing Project Manifests automatically.
- Do not make generated Topic Workspace contents tracked by Git by default.
- Do not store Topic Workspace bodies, runtime state, or generated content inside `.isomer-labs/`.
- Do not add a new CLI command for topic registration in this change.
- Do not create Workspace Runtime state during `isomer-cli project init` or `init-topic`.

## Decisions

### Use `isomer-content/` as the Project generated-content root

The Project Manifest will record the root through `[paths]` as `isomer_content_root = "isomer-content"` and `topic_workspace_base_dir = "isomer-content/topic-ws"`.

Alternative considered: use `generated_content_root`. That name describes implementation but is less aligned with the user-facing root name. `isomer_content_root` is more direct and still lives inside the existing path-default mechanism.

### Keep `.isomer-labs/` configuration-only

The content root sits beside `.isomer-labs/`, not inside it. The Project Manifest remains the discovery authority, while generated files live under a separate user-visible directory.

Alternative considered: place generated defaults under `.isomer-labs/generated/`. That would hide content in the config directory and conflict with the domain rule that Project Config Directory should not contain default cache, temporary files, or generated bodies.

### Track only the content-root policy files by default

`isomer-cli project init` will create:

```text
isomer-content/
  README.md
  .gitignore
  topic-ws/
    <topic-id>/
```

The generated `.gitignore` will be:

```gitignore
*
!.gitignore
!/README.md
```

This keeps the default generated-content policy visible and commit-friendly while keeping generated topic and support files local by default. If a future workflow needs selected generated files to be tracked, it can add explicit unignore rules or ask the user to force-add a file.

Alternative considered: unignore `topic-ws/` or common durable files. That would make `isomer-cli project init` noisier for Git users and blur the current decision that `isomer-content/` is ignored by default except for its policy files.

### Preserve explicit registered paths

New defaults move to `isomer-content/topic-ws/<topic-id>/`, but explicit Topic Workspace registrations continue to win. Workspace Path Resolution keeps its current precedence: recorded plan, environment override, Project Manifest default or registration, then built-in default.

Alternative considered: rewrite old manifest paths on validation. That would be surprising and could invalidate existing runtime path plans, so validation should report issues without moving user data.

### Derive `init-topic` output only when the topic is clear

When the user supplies a clear Research Topic but no output directory, `init-topic` derives a slug and creates `<topic-workspace-base>/<topic-slug>/topic-def/topic-overview.md`. It still asks for clarification when the topic is absent, unclear, or the derived path already exists in a way that could collide with existing material.

Alternative considered: always ask for a directory. That preserves control but wastes the new default and keeps the common path unnecessarily interactive.

## Risks / Trade-offs

- Existing docs and tests mention `topic-workspaces/<topic-id>/` in many places → Update docs, tests, skill text, and expected CLI output together so the layout does not split.
- Ignoring generated content may hide files users expected to commit → The generated README must explain the policy and how users can intentionally track selected generated files.
- A derived topic slug may collide with an existing provisional seed → `init-topic` must stop and ask before overwriting or merging ambiguous directories.
- New path-default keys could drift from existing aliases → Path resolution should keep existing `topic_workspace_base_dir` aliases and add only the content-root key needed by the new layout.

## Migration Plan

Fresh Projects use `isomer-content/topic-ws/<topic-id>/` immediately after this change. Existing Projects keep their explicit Project Manifest registrations and continue to validate when those paths resolve inside the Project root.

Rollback is straightforward for new Projects before runtime work starts: edit the Project Manifest Topic Workspace path and `[paths].topic_workspace_base_dir` back to the old layout, then move or recreate the directory. Runtime path plans remain authoritative once Workspace Runtime has been initialized, so this change must not rewrite historical path plans.

## Open Questions

- None for this change. Future work can decide whether selected generated Artifact classes should be unignored or tracked by default.
