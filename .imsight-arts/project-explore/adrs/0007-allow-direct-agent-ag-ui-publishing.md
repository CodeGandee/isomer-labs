# Allow Direct Agent AG-UI Publishing

Isomer Labs will allow Agent Team Instance members to publish AG-UI Event Batches directly to the GUI Backend for live GUI updates. These batches carry AG-UI Render Payloads such as data, DSL, JSON, Artifact refs, visualization intent, component hints, and optional layout refs. This deliberately extends the earlier View Manifest model: View Manifests remain the durable engine-owned description of semantic views, while direct AG-UI publishing gives agents a low-latency path for interactive UI updates, previews, and registered component output.

## Status

accepted

## Considered Options

- Route all AG-UI publishing through the Operator Agent and engine.
- Let Agent Team Instance members publish AG-UI Event Batches directly to the GUI Backend.
- Split channels, with direct agent publishing only for previews and engine-mediated publishing for durable views.

## Consequences

- The GUI Backend must authenticate direct agent publishers and associate every AG-UI Event Batch with a Project, Isomer Workspace, Run, Agent Team Instance, Agent Instance, and Artifact or component reference when available.
- The GUI Backend resolves AG-UI Render Payloads to registered GUI Components, creates or updates GUI Component Instances, and updates GUI Runtime State.
- Direct AG-UI Event Batches are live interaction traffic, not canonical research state. Durable claims, Gates, decisions, Artifacts, and reusable views still need Workspace Runtime, Artifact, View Manifest, or Provenance Records.
- ADR 0008 defines the default retention boundary: persist AG-UI Event Envelopes by default, and save full event payload content only when the human user explicitly instructs the system to retain it.
- The Operator Agent remains the human-facing control point. Direct agent publishing must not create direct human operation of team Agent Instances or bypass Gate resolution rules.
