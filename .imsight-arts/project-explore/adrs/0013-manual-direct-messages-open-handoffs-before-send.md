# Manual Direct Messages Open Handoffs Before Send

Manual mode will send Operator Agent messages to delegated Agent Instances through durable handoffs. Before the Operator Agent sends a manual direct message, it records a handoff in Workspace Runtime with a stable handoff id, target Agent Instance, Run and Workflow Stage context, expected outputs, and completion-watch metadata. The message body can remain freeform, but the handoff identity is created first so retries, duplicate signals, produced Artifact refs, and completion records can attach to one durable task.

## Status

accepted

## Considered Options

- Open a structured handoff before sending each manual direct message.
- Send raw messages first and create handoff records only when results arrive.
- Let manual mode bypass handoff records unless the user asks to record a result.
- Let each Execution Adapter decide whether manual direct messages create handoffs.

## Consequences

- Manual mode keeps the same recovery and provenance shape as automatic delegation while still allowing the operator to write direct, contextual instructions.
- A failed send, duplicate send, late completion signal, or missing reply can be diagnosed against a known handoff id.
- Execution Adapters must accept or return enough routing metadata for the Operator Agent to associate outbound messages and observed completion signals with the pre-created handoff.
