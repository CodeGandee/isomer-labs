# Publish All Available Topic Components by Default

Each publication plan selects every currently available Topic Main, registered Topic Actor Workspace, and selected-team Agent Workspace that read-only Isomer queries resolve for the Research Topic. This favors a complete survey-topic snapshot over worker-level opt-in, while preserving privacy review and state-bound approval before any newly available component is committed or pushed.

## Status

accepted

## Considered Options

- Select all available Topic Main, Topic Actor, and Agent components by default.
- Select Topic Main by default and require worker-component opt-in.
- Require explicit selection of every component.

## Consequences

- A publication may be root-only at an early lifecycle stage and gain components as they become available.
- A newly available component changes the expected projection, invalidates an older plan, and requires a new privacy review and approval before push.
- Users may explicitly exclude an available component in the current publication plan, but absence is never inferred from directory scanning.
