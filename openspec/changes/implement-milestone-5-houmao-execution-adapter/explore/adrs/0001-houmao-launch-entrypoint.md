# Use Houmao Project-Profile Launch as the Adapter Entrypoint

Milestone 5 needs a stable launch boundary between Isomer's Houmao Execution Adapter and the local Houmao checkout. Isomer will launch through Houmao's documented public project-backed CLI path, `houmao-mgr --print-json project --project-dir <dir> agents launch --profile <generated-profile>`, because that path is maintained as Houmao's source-scoped managed-agent birth surface and returns machine-readable output for adapter recording.

## Status

accepted

## Considered Options

- Public Houmao project-profile CLI launch.
- Direct launch-dossier or native-agent internals.
- Managed-agent gateway or passive-server API as launch authority.

## Consequences

Isomer must materialize or select Houmao project-profile launch material before launch and record the resulting Houmao runtime refs as opaque adapter payload refs. Gateway, mailbox, passive-server, and selected-agent commands remain post-launch control and observation surfaces for this milestone.
