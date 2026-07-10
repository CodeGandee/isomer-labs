# Register GUI Components Before Loading

Isomer Labs will require all GUI Components to be registered before the GUI Backend can use them. Built-in GUI Components are registered by the built-in GUI Backend at startup. Agents may write component source, a Declarative GUI Component Spec, or a component manifest into a project-scope GUI component directory, but the GUI Backend should discover, validate, build when needed, sandbox when needed, and track approval state before use.

## Status

accepted

## Considered Options

- Load arbitrary project component files directly from the GUI Backend.
- Require registry metadata, validation, sandboxing, and approval before loading Executable GUI Components.
- Require a separate signed or versioned prebuilt plugin bundle before loading Executable GUI Components.

## Consequences

- Direct AG-UI Event Batches and AG-UI Render Payloads may reference only registered component ids.
- The registry must track component id, component kind, registration source, source path, manifest path, build output, dependency declarations, sandbox policy, producer Agent Instance when applicable, approval state, and compatibility version.
- The human user can explicitly choose an approve-all mode through the Operator Agent. ADR 0010 scopes approve-all to the whole Project until revoked.
- Approve-all mode must be visible in GUI and Operator Agent state because it changes the trust posture for agent-produced UI code.
