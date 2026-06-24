## Context

`isomer-cli` currently exposes most Project-targeted commands at the root: `init`, `validate`, `doctor`, `topics`, `workspaces`, `context`, `paths`, `runtime`, `team-instances`, `handoffs`, `team-templates`, and `team-profiles`. These commands all depend on a selected Isomer Project, except for a few global surfaces such as built-in schema listing. Project discovery already behaves like Git by walking from cwd through parent directories until `.isomer-labs/manifest.toml` is found, but the root command shape hides that model.

The CLI should make the target explicit: `isomer-cli` is global, while `isomer-cli project` is the namespace for commands that operate on one Project. This also gives the active cleanup proposal a clearer home: cleanup is a Project lifecycle command, so its canonical shape is `isomer-cli project cleanup`.

## Goals / Non-Goals

**Goals:**

- Add a root-level `project` Click group as the canonical home for Project-scoped commands.
- Move Project-targeted command groups and commands under `project`, including lifecycle, diagnostics, runtime, topic/team, adapter, and handoff commands.
- Keep Project-independent commands, such as `schemas list`, at the root.
- Preserve Git-style ancestor discovery for Project commands.
- Make `project init` refuse nested initialization inside an already discovered ancestor Project.
- Introduce `--root <project-root>` as the canonical Project selector on `project`, with `--project` as a compatibility alias during refactor.
- Update operator skills and docs to use only canonical `isomer-cli project ...` command examples.
- Coordinate with `add-project-cleanup-command` so cleanup lands at `isomer-cli project cleanup`.

**Non-Goals:**

- Do not rewrite Project Manifest parsing or the existing ancestor-discovery algorithm beyond exposing it at the `project` boundary.
- Do not change command behavior, output payload meaning, or runtime side-effect boundaries except for the command names and selector placement.
- Do not move commands that are genuinely Project-independent under `project`.
- Do not introduce nested Project creation support.

## Decisions

### Add `project` as the Project context boundary

The canonical command tree should be:

```text
isomer-cli
├── schemas list
└── project
    ├── init
    ├── cleanup
    ├── validate
    ├── doctor
    ├── topics list
    ├── workspaces list
    ├── context show
    ├── paths preview
    ├── runtime init|prepare|inspect|validate
    ├── team-templates list|inspect|validate
    ├── team-profiles specialize|materialize|validate
    ├── team-instances ...
    └── handoffs dispatch|observe|normalize
```

Alternative considered: keep root-level commands and only document them as Project-scoped. That leaves the global CLI ambiguous and makes future global commands harder to scan.

### Put Project selectors on the `project` group

The canonical selector shape should be:

```bash
isomer-cli project --root <project-root> validate
isomer-cli project --manifest <manifest-path> validate
```

`--root` is clearer than `--project` because the group name already says Project. `--project` can remain as a hidden or documented compatibility alias during this refactor if the implementation wants to avoid breaking all existing tests at once.

Alternative considered: keep selectors on every subcommand. Group-level selectors reduce repetition and match the idea that every nested command shares the same Project context.

### Keep root-level global options global

`--print-json` should remain on the root command so it still applies uniformly:

```bash
isomer-cli --print-json project validate
```

Alternative considered: move JSON selection under `project`. That would make Project commands more self-contained but needlessly changes the global output contract.

### Preserve Git-style Project discovery

For `isomer-cli project <subcmd>`, discovery defaults to cwd and walks parent directories until it finds `.isomer-labs/manifest.toml`. Explicit `--root` or `--manifest` selectors still win. Environment fallbacks remain lower priority.

Alternative considered: require `--root` for all Project commands. That is too verbose and less ergonomic than the Git-like model the user wants.

### Refuse nested Project initialization

`isomer-cli project init` is special because it can create Project state. Before initializing cwd or `--root`, it should check whether that target is inside an existing ancestor Project. If so, it refuses and reports the ancestor Project root instead of creating a nested `.isomer-labs/`.

Alternative considered: allow nested Projects by default. That is surprising when the command is run from a subdirectory of an existing Project and conflicts with the parent-directory discovery model.

### Treat legacy root project commands as temporary compatibility only

The canonical documentation, skill guidance, and tests should use `isomer-cli project ...`. Root-level Project command forms can be removed immediately if the project is comfortable breaking internal scripts, or kept as hidden compatibility aliases that emit deprecation guidance. They should not appear in root help or new docs.

Alternative considered: keep root-level commands visible indefinitely. That defeats the refactor because users would still see two competing command surfaces.

### Coordinate active cleanup work

The active cleanup proposal currently names `isomer-cli cleanup`. This refactor should update that planning material if it is still active, or ensure implementation registers cleanup as `isomer-cli project cleanup` if cleanup is applied after this refactor.

Alternative considered: let cleanup remain a root command because it can act when no manifest exists. Cleanup is still a Project-root operation; bounded no-manifest cleanup can live under `project cleanup --root <dir>`.

## Risks / Trade-offs

- Existing tests and docs call root-level Project commands → Update test helpers and docs together, and keep compatibility aliases only if needed for transition.
- Active cleanup planning uses root-level cleanup → Update or coordinate that change so two active changes do not introduce conflicting command shapes.
- Moving many Click groups at once can create import cycles → Register Project-scoped groups under a shared `project_group` and keep command handlers unchanged where possible.
- `project init` needs different discovery behavior than read-only commands → Add a small preflight that searches ancestor Projects for the target root before calling initialization.
- Hidden aliases can mask missed doc updates → If aliases are kept, add tests that root help does not advertise them and docs/skills use canonical commands.

## Migration Plan

Update the command registration first while reusing existing command handlers. Then update tests and documentation to canonical `isomer-cli project ...` examples. If root aliases are retained, mark them deprecated and hide them from help. After the refactor is stable, later cleanup can remove aliases in a separate change.

Rollback is straightforward: move command registration back to root-level groups while leaving the underlying command handlers unchanged. No Project data migration is required.

## Open Questions

- Should root-level compatibility aliases be removed immediately or hidden with deprecation guidance for one internal transition period? The design prefers canonical-only docs either way.
- Should `--project` remain forever as an alias for `project --root`, or should it be deprecated in favor of `--root` after this refactor?
