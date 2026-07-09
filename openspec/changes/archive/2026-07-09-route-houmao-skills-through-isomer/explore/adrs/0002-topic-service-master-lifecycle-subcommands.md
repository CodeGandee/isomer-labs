# Topic Service Master Lifecycle Subcommands

Status: accepted

`isomer-srv-topic-service-agent-support` will expose explicit Topic Service Master lifecycle subcommands: `prepare-topic-service-master`, `launch-topic-service-master`, `inspect-topic-service-master`, `stop-topic-service-master`, and `repair-topic-service-master`. This makes the Isomer-facing route discoverable and testable while keeping Houmao-specific procedures behind Isomer-provided skill context.

## Considered Options

- Add explicit lifecycle subcommands.
- Add one generic `topic-service-master` subcommand with internal modes.
- Implement only preparation in the first slice.

## Consequences

The service skill needs one reference page per lifecycle operation. Topic Creator should normally route only preparation during topic setup; launch, inspect, stop, and repair remain explicit service operations after the Project has enabled Houmao integration.
