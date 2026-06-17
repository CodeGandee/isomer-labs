# Do Not Port DeepScientist Continuation Policy

## Status

accepted

## Context

DeepScientist uses `continuation_policy` as a daemon-level scheduling and collaboration control. Its runtime can auto-schedule another turn, wait for a user message or resume command, monitor external progress at a lower cadence, or stop auto-continuation. It also uses related source terms such as `workspace_mode`, `auto_continue`, `continuation_anchor`, `continuation_reason`, and `wait_for_user_or_resume`.

Isomer Labs has a different control boundary. The Operator Agent is always the human-facing actor that receives user instructions, resolves Gates, records routing decisions, and instructs delegated Agent Team Instances. Delegated Agent Team Instances either continue doing approved work under Coordination Policy or pause and wait for Operator Agent instruction.

## Decision

Do not port DeepScientist `continuation_policy` into the research-paradigm skills as an Isomer concept, field, or required runtime operation.

When source behavior depends on continuation policy, map it as follows:

| DeepScientist source behavior | Isomer framing for skill text |
| --- | --- |
| `auto` | Delegated Agent Team Instance may advance under approved Coordination Policy. |
| `when_external_progress` | Long-running work remains active; observe it through Completion Watcher Contracts, Signal Observations, Execution Adapter metadata, Artifacts, and Provenance Records. |
| `wait_for_user_or_resume` | Delegated Agent Team Instance is paused and waiting for Operator Agent instruction, or a Gate/handoff is waiting, depending on the reason. |
| `none` | No automatic advancement is requested; wait for Operator Agent instruction or a recorded Decision Record. |
| `continuation_anchor` | Next recommended Workflow Stage or Decision Record target. |
| `continuation_reason` | Pause reason, Gate reason, failure reason, or Decision Record rationale. |
| `auto_continue` turn | Source daemon scheduling detail. Skills should recommend next action, not schedule turns. |

Extracted skills should say what research action is justified next: continue an approved Workflow Stage, open a Gate, record a Decision Record, create or inspect Artifacts, observe long-running work, or pause for Operator Agent instruction. They must not tell the host to set `continuation_policy` or create an `auto_continue` turn.

Concrete Agent Team Instance lifecycle states, scheduler behavior, and pause-state schema remain `yet-to-be-determined:schema` or `yet-to-be-determined:policy` until accepted by Isomer platform design.

## Considered Options

- Port `continuation_policy` as an Isomer runtime field.
- Map `continuation_policy` to Run Control Mode.
- Map continuation behavior to Agent Team Instance advancement or pause state and keep scheduling out of skill text.

## Consequences

- Research-paradigm skills stay portable and do not assume a DeepScientist daemon.
- The Operator Agent remains the only human-facing control boundary.
- Skills preserve the useful research behavior: recommend the next stage, gate, decision, observation, or pause.
- Platform scheduling can be designed later without being locked by copied DeepScientist terminology.
