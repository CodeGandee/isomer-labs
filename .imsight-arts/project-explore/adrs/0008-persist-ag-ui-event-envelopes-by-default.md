# Persist AG-UI Event Envelopes by Default

Isomer Labs will persist AG-UI Event Envelopes by default when Agent Team Instance members publish directly to the GUI Backend. The envelope records durable metadata, render payload refs, component refs, layout refs, and Artifact refs for auditability, while full AG-UI payload content is saved only when the human user explicitly instructs the system to retain it.

## Status

accepted

## Considered Options

- Treat direct AG-UI Event Batches as live-only traffic.
- Persist AG-UI Event Envelopes and referenced artifacts by default.
- Persist full AG-UI event streams for replay by default.

## Consequences

- The GUI Backend should store publisher identity, Project, Isomer Workspace, Run, Agent Team Instance, Agent Instance, render payload id, component id, component instance id, layout spec id, Artifact refs, timestamps, status, and retention policy for each direct AG-UI Event Batch.
- Canonical recovery should use Workspace Runtime state, Artifacts, View Manifests, component refs, and Provenance Records instead of assuming full AG-UI replay is available.
- Full AG-UI payload retention is explicit, user-directed behavior. It should be visible in the Operator Agent interaction because full payloads may contain sensitive research context, large data, or generated UI details.
