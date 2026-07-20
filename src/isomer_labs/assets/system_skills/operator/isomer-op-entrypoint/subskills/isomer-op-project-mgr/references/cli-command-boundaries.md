---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# CLI Command Boundaries

Use root-level `--print-json` when deterministic output is needed.

Fresh Project bootstrap:

```bash
isomer-cli project init
isomer-cli project --root <project-root> init
isomer-cli project init --content-dir <content-dir>
isomer-cli project --root <project-root> init --content-dir <content-dir>
```

Omit `--content-dir <content-dir>` to use `isomer-content/`. Include it only when the Project should store generated content under a different project-local root; the derived Topic Workspace base for later topic creation is `<content-dir>/topic-ws/`.

Direct Project initialization does not scan agent skill roots or register optional extensions. An operator-controlled `init-project` delegates the separate additive reconciliation step through `isomer-op-entrypoint->system-skills` unless the user opts out.

Research Topic lifecycle:

```bash
isomer-cli --print-json project topics create <topic-id> --statement "<research topic>"
isomer-cli --print-json project topics create <topic-id> --statement "<research topic>" --workspace-dir <dir> --set-default
isomer-cli --print-json project topics show <topic-id>
isomer-cli --print-json project topics update <topic-id> --statement "<research topic>"
isomer-cli --print-json project topics update <topic-id> --status active
isomer-cli --print-json project topics update <topic-id> --set-default
isomer-cli --print-json project topics delete <topic-id> --dry-run
isomer-cli --print-json project topics delete <topic-id> --yes
```

Use `topics delete --dry-run` first and apply `--yes` only after the user reviews the plan. Topic deletion preserves the Topic Workspace directory; use cleanup surfaces later if the user explicitly wants filesystem removal.

Cleanup planning and confirmed cleanup:

```bash
isomer-cli --print-json project cleanup --part <part> --dry-run
isomer-cli --print-json project cleanup --part <part> --yes
isomer-cli --print-json project cleanup --part runtime --topic <topic-id> --dry-run
isomer-cli --print-json project cleanup --part content-root --purge-content-root --yes
```

Prefer dry-run first. Use `--yes` only after plan review. Use `--purge-content-root` only when the user explicitly asks to remove the entire selected generated content root.

Generated content-root relocation:

```bash
isomer-cli --print-json project content-root move --to <content-dir> --dry-run
isomer-cli --print-json project content-root move --to <content-dir> --yes
isomer-cli --print-json project --root <project-root> content-root move --to <content-dir> --dry-run
```

Prefer dry-run first. Relocation updates Project Manifest paths and moves Isomer-managed content containers only. It preserves unmanaged leftovers and does not rewrite Workspace Runtime records, Pixi environments, installed packages, adapter runtime material, logs, stored path plans, or generated runtime internals. Warn the user to reinstall or reinitialize moved runtimes if needed.

Read-only Project checks:

```bash
isomer-cli --print-json project validate
isomer-cli --print-json doctor
isomer-cli --print-json project topics list
isomer-cli --print-json project workspaces list
isomer-cli --print-json project context show --topic <topic-id>
isomer-cli project paths preview --topic <topic-id>
```

Topic Actor and Topic Actor Workspace operations:

```bash
isomer-cli --print-json project topic-actors list --topic <topic-id>
isomer-cli --print-json project topic-actors show <topic-actor-name> --topic <topic-id>
isomer-cli --print-json project topic-actors register <topic-actor-name> --topic <topic-id> --actor-kind manual_worker --runtime-kind codex --role-kind scout --controller-kind human_user --materialize
isomer-cli --print-json project topic-actors update <topic-actor-name> --topic <topic-id> --status active
isomer-cli --print-json project topic-actors materialize <topic-actor-name> --topic <topic-id>
isomer-cli --print-json project topic-actors repair <topic-actor-name> --topic <topic-id>
isomer-cli --print-json project topic-actors diagnose --topic <topic-id> --topic-actor <topic-actor-name>
isomer-cli --print-json project topic-actors archive <topic-actor-name> --topic <topic-id> --reason <reason>
```

Use these operations through `isomer-op-topic-mgr`. They mutate or inspect Topic Workspace Manifest actor bindings and Topic Actor Workspace materialization. They do not create Agent Team Instance records, Agent Instance records, formal Agent Workspaces, Houmao launch material, or research records.

Explicit Workspace Runtime mutations:

```bash
isomer-cli --print-json project runtime init --topic <topic-id>
isomer-cli --print-json project runtime prepare --topic <topic-id>
```

Read-only runtime validation:

```bash
isomer-cli --print-json project runtime validate --topic <topic-id>
isomer-cli --print-json project runtime validate --topic <topic-id> --require-ready-readiness
```

Do not use command-local `--json`, `--format json`, or `--format=json` in new operator instructions; root-level `--print-json` is the public deterministic output shape.
