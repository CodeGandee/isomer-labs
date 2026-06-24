# Houmao Bootstrap

Isomer uses Houmao as the implementation and adapter layer for agent-team construction and management. Fresh Project initialization must create or validate the Project-level Houmao overlay at `.houmao/`.

The supported Houmao Project bootstrap command shape is:

```bash
houmao-mgr --print-json project --project-dir <project-root> init
```

The supported read-only Project status command shape is:

```bash
houmao-mgr --print-json project --project-dir <project-root> status
```

Isomer's CLI resolves the Houmao command through its adapter boundary. Operators should report failures as blockers when the command is unavailable, emits invalid JSON, exits nonzero, times out, or completes without creating `.houmao/`.

Project-level `.houmao/` is not per-team launch material. Later Houmao-backed Agent Team Instance preparation or launch stores adapter manifests, command payloads, and generated launch material under the selected Topic Workspace runtime adapter paths.
