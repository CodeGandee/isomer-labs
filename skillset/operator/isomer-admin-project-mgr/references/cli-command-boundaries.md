# CLI Command Boundaries

Use root-level `--print-json` when deterministic output is needed.

Fresh Project bootstrap:

```bash
pixi run isomer-cli project init
pixi run isomer-cli project --root <project-root> init
pixi run isomer-cli project init --content-dir <content-dir>
pixi run isomer-cli project --root <project-root> init --content-dir <content-dir>
```

Omit `--content-dir <content-dir>` to use `isomer-content/`. Include it only when the Project should store generated content under a different project-local root; the derived Topic Workspace base for later topic creation is `<content-dir>/topic-ws/`.

Research Topic lifecycle:

```bash
pixi run isomer-cli --print-json project topics create <topic-id> --statement "<research topic>"
pixi run isomer-cli --print-json project topics create <topic-id> --statement "<research topic>" --workspace-dir <dir> --set-default
pixi run isomer-cli --print-json project topics show <topic-id>
pixi run isomer-cli --print-json project topics update <topic-id> --statement "<research topic>"
pixi run isomer-cli --print-json project topics update <topic-id> --status active
pixi run isomer-cli --print-json project topics update <topic-id> --set-default
pixi run isomer-cli --print-json project topics delete <topic-id> --dry-run
pixi run isomer-cli --print-json project topics delete <topic-id> --yes
```

Use `topics delete --dry-run` first and apply `--yes` only after the user reviews the plan. Topic deletion preserves the Topic Workspace directory; use cleanup surfaces later if the user explicitly wants filesystem removal.

Cleanup planning and confirmed cleanup:

```bash
pixi run isomer-cli --print-json project cleanup --part <part> --dry-run
pixi run isomer-cli --print-json project cleanup --part <part> --yes
pixi run isomer-cli --print-json project cleanup --part runtime --topic <topic-id> --dry-run
pixi run isomer-cli --print-json project cleanup --part content-root --purge-content-root --yes
```

Prefer dry-run first. Use `--yes` only after plan review. Use `--purge-content-root` only when the user explicitly asks to remove the entire selected generated content root.

Generated content-root relocation:

```bash
pixi run isomer-cli --print-json project content-root move --to <content-dir> --dry-run
pixi run isomer-cli --print-json project content-root move --to <content-dir> --yes
pixi run isomer-cli --print-json project --root <project-root> content-root move --to <content-dir> --dry-run
```

Prefer dry-run first. Relocation updates Project Manifest paths and moves Isomer-managed content containers only. It preserves unmanaged leftovers and does not rewrite Workspace Runtime records, Pixi environments, installed packages, adapter runtime material, logs, stored path plans, or generated runtime internals. Warn the user to reinstall or reinitialize moved runtimes if needed.

Read-only Project checks:

```bash
pixi run isomer-cli --print-json project validate
pixi run isomer-cli --print-json project doctor
pixi run isomer-cli --print-json project topics list
pixi run isomer-cli --print-json project workspaces list
pixi run isomer-cli --print-json project context show --topic <topic-id>
pixi run isomer-cli project paths preview --topic <topic-id>
```

Explicit Workspace Runtime mutations:

```bash
pixi run isomer-cli --print-json project runtime init --topic <topic-id>
pixi run isomer-cli --print-json project runtime prepare --topic <topic-id>
```

Read-only runtime validation:

```bash
pixi run isomer-cli --print-json project runtime validate --topic <topic-id>
pixi run isomer-cli --print-json project runtime validate --topic <topic-id> --require-ready-readiness
```

Do not use command-local `--json`, `--format json`, or `--format=json` in new operator instructions; root-level `--print-json` is the public deterministic output shape.
