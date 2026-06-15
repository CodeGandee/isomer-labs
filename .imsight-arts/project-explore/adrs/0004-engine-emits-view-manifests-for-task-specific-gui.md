# Engine Emits View Manifests for Task-Specific GUI

Isomer Labs will describe task-specific GUI needs through engine-produced view manifests rather than a fixed dashboard or agent-generated frontend code. The research engine owns semantic state, artifact references, view intent, available actions, and decision gates; the GUI owns rendering, layout, widgets, and interaction polish.

## Status

accepted

## Considered Options

- Use a fixed GUI with configurable panels.
- Have the engine emit view manifests that the GUI renders.
- Let agents generate frontend code for each research task.

## Consequences

- The engine stays useful from command-line and agent workflows because the GUI contract is data, not runtime UI code.
- The project needs a stable view-manifest schema covering artifact sources, view types, data bindings, actions, and decision-gate affordances.
- The GUI can evolve independently as long as it honors the view-manifest contract.
