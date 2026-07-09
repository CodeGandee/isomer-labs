# Topic Service Master Skill Ownership

Status: accepted

Topic Service Master commands will be owned by `isomer-srv-topic-service-agent-support`, while `isomer-srv-houmao-interop` will act as the internal bridge from Isomer context to projected Houmao skill procedures. This keeps the user-facing workflow in Isomer language and prevents the Houmao interop service from becoming the owner of Topic Service Agent semantics.

## Considered Options

- `isomer-srv-topic-service-agent-support` owns Topic Service Master commands, with `isomer-srv-houmao-interop` as the Houmao bridge.
- `isomer-srv-houmao-interop` owns Topic Service Master commands directly.
- A new dedicated `isomer-srv-topic-service-master` skill owns the commands.

## Consequences

`isomer-srv-topic-service-agent-support` needs command-style subcommands for prepare, launch, inspect, stop, and repair. `isomer-srv-houmao-interop` should not be presented as the user-facing route for Topic Service Master operations; it should be invoked only after Isomer CLI returns explicit `houmao_skill_path` and `houmao_project_path` context.
