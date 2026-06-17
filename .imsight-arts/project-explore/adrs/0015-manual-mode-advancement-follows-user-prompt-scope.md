# Manual Mode Advancement Follows User Prompt Scope

Manual mode will use the user's prompt scope to decide whether the Operator Agent waits after a completed handoff or advances to the next step. If the user asks for a single-stage operation, the Operator Agent records completion, summarizes the result, and waits for the next instruction. If the user prompt defines a multi-step operation, the Operator Agent may continue through those declared steps automatically after each completed handoff.

## Status

accepted

## Considered Options

- Always wait after each completed manual handoff.
- Auto-advance within one approved Workflow Stage.
- Auto-advance until a Gate, failure, or terminal condition appears.
- Let Coordination Policy alone define the cadence.
- Let the user's prompt scope define whether the Operator Agent waits or continues.

## Consequences

- Manual mode remains user-driven without forcing the user to confirm every step of an explicitly requested multi-step operation.
- The Operator Agent must preserve the original prompt scope as part of the Run or handoff context so it can distinguish single-stage instructions from multi-step instructions during recovery.
- Existing Gate rules still apply. A multi-step prompt must stop for irreversible or claim-shaping decisions, failed or stale handoffs, missing completion evidence, invalid Artifacts, or any step outside the user-defined scope.
