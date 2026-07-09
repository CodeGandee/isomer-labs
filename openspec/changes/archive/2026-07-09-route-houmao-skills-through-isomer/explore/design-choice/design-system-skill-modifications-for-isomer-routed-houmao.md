# System Skill Modifications for Isomer-Routed Houmao

## Decision

Isomer-facing system skills remain the user and operator surface for Houmao-backed Topic Service Master work. `isomer-srv-topic-service-agent-support` owns explicit Topic Service Master lifecycle subcommands, while `isomer-srv-houmao-interop` bridges from Isomer context to projected Houmao-owned skill material.

## Chosen Shape

- Keep `isomer-srv-houmao-interop` and `isomer-srv-topic-service-agent-support` in the core Isomer system-skill group.
- Add `prepare-topic-service-master`, `launch-topic-service-master`, `inspect-topic-service-master`, `stop-topic-service-master`, and `repair-topic-service-master` to `isomer-srv-topic-service-agent-support`.
- Map each lifecycle subcommand to one stable Isomer route in `.isomer-labs/houmao-skills/`.
- Require each lifecycle subcommand to call `isomer-cli project integrations houmao skill-context <route-name>` before routing to projected Houmao skill material.
- Tell agents to follow the returned `houmao_skill_path` and run Houmao commands with the returned `houmao_project_path`.
- Keep Topic Creator responsible only for preparation during topic setup; launch, inspect, stop, and repair are explicit later lifecycle operations.

## Rejected Alternatives

- Do not make `isomer-srv-houmao-interop` the user-facing owner of Topic Service Master commands. That would mix Isomer service-agent semantics with Houmao mechanics.
- Do not create a new `isomer-srv-topic-service-master` skill yet. The existing Topic Service Agent support skill already has the correct service boundary.
- Do not move the Isomer-facing bridge/support skills into an optional Isomer extension. The optional state is the Project-local Houmao skill projection and Project Manifest integration policy.
- Do not use one generic projected Houmao admin skill. Lifecycle-specific routes are easier to validate and keep Houmao administration internal.

## System Skill Changes

| Skill | Change |
| --- | --- |
| `isomer-op-topic-creator` | During `setup-actors`, route enabled Houmao-backed Topic Service Master setup to `isomer-srv-topic-service-agent-support prepare-topic-service-master`; when disabled, record a skipped integration state. |
| `isomer-op-topic-creator` finalization/status pages | Report Topic Service Master readiness as ready, skipped, blocked, or not configured without prescribing a direct Houmao operation to the user. |
| `isomer-op-topic-mgr` | Stay out of launch/profile ownership; at most route initialized-topic Topic Service Master lifecycle requests to `isomer-srv-topic-service-agent-support`. |
| `isomer-srv-topic-service-agent-support` | Become the Isomer-facing owner of Topic Service Master lifecycle subcommands and reference pages. |
| `isomer-srv-houmao-interop` | Stop assuming operator-installed Houmao skills or implicit Houmao project discovery; bridge only through Isomer CLI skill context. |
| `isomer-op-entrypoint` and help indexes | Keep user-facing language Isomer-first and describe Houmao as an internal integration provider. |

## Acceptance Signals

- Core Isomer system-skill installation includes the bridge/support skills but does not create `.isomer-labs/houmao-skills/`.
- A disabled Project reports skipped Houmao integration from Topic Creator and service support.
- An enabled Project can prepare projected lifecycle-specific Houmao skill routes.
- Every lifecycle subcommand requests a matching route name and uses the returned absolute paths.
- Tests reject generic or fabricated Houmao skill paths.
