# Lifecycle-Specific Houmao Skill Routes

Status: accepted

Each Topic Service Master lifecycle subcommand will resolve a distinct stable Isomer route to projected Houmao skill material: `prepare-topic-service-master`, `launch-topic-service-master`, `inspect-topic-service-master`, `stop-topic-service-master`, and `repair-topic-service-master`. This avoids reintroducing generic Houmao administration as the Isomer-facing interface and makes each lifecycle operation independently testable.

## Considered Options

- One projected Houmao skill route per lifecycle command.
- One projected `topic-service-master` Houmao skill with internal modes.
- One generic Houmao agent-admin skill reused across many Isomer operations.

## Consequences

The projection manifest must store one route entry per lifecycle command. `isomer-cli project integrations houmao skill-context <skill-name>` should reject unknown route names and should not derive paths by string interpolation.
