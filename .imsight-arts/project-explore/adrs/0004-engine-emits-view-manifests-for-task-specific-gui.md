# Engine Emits View Manifests for Task-Specific GUI

Isomer Labs will describe durable task-specific GUI needs through engine-produced View Manifests rather than a fixed dashboard. The research engine owns semantic state, artifact references, view intent, available actions, decision gates, registered component refs, and optional GUI Layout Spec refs; the GUI owns rendering, live GUI Runtime State, layout application, widgets, and interaction polish. ADR 0007 extends this model by allowing Agent Team Instance members to publish AG-UI Event Batches directly to the GUI Backend for live updates.

## Status

accepted

## Considered Options

- Use a fixed GUI with configurable panels.
- Have the engine emit View Manifests that the GUI Backend and Renderer render.
- Let agents generate frontend code for each Research Task.

## Consequences

- The engine stays useful from command-line and agent workflows because the GUI contract is data, not runtime UI code.
- The project needs a stable view-manifest schema covering Artifact sources, view types, data bindings, registered component refs, GUI Layout Spec refs, actions, and decision-gate affordances.
- The GUI can evolve independently as long as it honors the view-manifest contract.
- Direct AG-UI publishing is live interaction traffic; durable GUI state and research semantics should still be recoverable from Workspace Runtime, Artifacts, View Manifests, and Provenance Records.
