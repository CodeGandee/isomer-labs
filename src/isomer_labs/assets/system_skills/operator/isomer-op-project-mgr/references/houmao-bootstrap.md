# Houmao Bootstrap

Isomer uses Houmao as the implementation and adapter layer for agent-team construction and management. Fresh Project initialization must create or validate the Isomer-managed Houmao overlay at `.isomer-labs/.houmao/`. Root `.houmao/` is external user-owned Houmao state if present and is not used for Isomer Project bootstrap.

The supported Houmao Project bootstrap command shape is:

```bash
houmao-mgr --print-json project --project-dir <project-root>/.isomer-labs init
```

The supported read-only Project status command shape is:

```bash
houmao-mgr --print-json project --project-dir <project-root>/.isomer-labs status
```

Isomer's CLI resolves the Houmao command through its adapter boundary. Operators should report failures as blockers when the command is unavailable, emits invalid JSON, exits nonzero, times out, or completes without creating `.isomer-labs/.houmao/`.

Project-level `.isomer-labs/.houmao/` is not per-team launch material. Later Houmao-backed Agent Team Instance preparation or launch stores adapter manifests, command payloads, and generated launch material under the selected Topic Workspace runtime adapter paths.

For Houmao loop explanation, adapter customization guidance, Domain Agent Team Template mapping, mailbox or gateway support, or runtime inspection, route bounded service support to `isomer-srv-houmao-interop`. Keep this Project Manager surface focused on Project bootstrap and read-only Project status checks.
