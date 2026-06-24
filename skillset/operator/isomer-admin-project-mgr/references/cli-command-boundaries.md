# CLI Command Boundaries

Use root-level `--print-json` when deterministic output is needed.

Fresh Project bootstrap:

```bash
pixi run isomer-cli init <topic-id> --topic-statement "<topic statement>"
pixi run isomer-cli --project <project-root> init <topic-id> --topic-statement "<topic statement>"
```

Read-only Project checks:

```bash
pixi run isomer-cli --print-json validate
pixi run isomer-cli --print-json doctor
pixi run isomer-cli --print-json topics list
pixi run isomer-cli --print-json workspaces list
pixi run isomer-cli --print-json context show --topic <topic-id>
pixi run isomer-cli paths preview --topic <topic-id>
```

Explicit Workspace Runtime mutations:

```bash
pixi run isomer-cli --print-json runtime init --topic <topic-id>
pixi run isomer-cli --print-json runtime prepare --topic <topic-id>
```

Read-only runtime validation:

```bash
pixi run isomer-cli --print-json runtime validate --topic <topic-id>
pixi run isomer-cli --print-json runtime validate --topic <topic-id> --require-ready-readiness
```

Do not use command-local `--json`, `--format json`, or `--format=json` in new operator instructions; root-level `--print-json` is the public deterministic output shape.
