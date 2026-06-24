# CLI Command Boundaries

Use root-level `--print-json` when deterministic output is needed.

Fresh Project bootstrap:

```bash
pixi run isomer-cli project init <topic-id> --topic-statement "<topic statement>"
pixi run isomer-cli project --root <project-root> init <topic-id> --topic-statement "<topic statement>"
pixi run isomer-cli project init <topic-id> --content-dir <content-dir> --topic-statement "<topic statement>"
pixi run isomer-cli project --root <project-root> init <topic-id> --content-dir <content-dir> --topic-statement "<topic statement>"
```

Omit `--content-dir <content-dir>` to use `isomer-content/`. Include it only when the Project should store generated content under a different project-local root; the derived Topic Workspace base is `<content-dir>/topic-ws/`.

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
