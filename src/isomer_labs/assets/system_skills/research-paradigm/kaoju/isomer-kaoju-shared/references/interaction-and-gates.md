# Interaction and Gates

## Clarification-First Mode

When the user asks to clarify before work, perform only read-only inspection needed to identify material ambiguity. Before acquisition, mutation, or a research Run, ask one structured A/B/C/D question:

| Id | Content |
| --- | --- |
| A | Concrete option with explanation, pros, and cons. |
| B | Concrete option with explanation, pros, and cons. |
| C | Concrete option with explanation, pros, and cons. |
| D | “Say what you like,” for a free-form answer. |

Mark exactly one of A, B, or C as suggested. After the answer, ask: “Do you want to clarify more or proceed to execution?” If inspection finds no material ambiguity, state that the request is ready and still ask that question.

## Comparison Intent Checkpoint

Empirical comparison requires an accepted Comparison Intent Document and a Proceed Decision before candidate preparation, downloads, environment mutation, or Runs. Present the document, list unresolved decisions, and ask whether the user wants to clarify for more detail or proceed.

## Gate Triggers

Use existing Gate owners for credentials, private or restricted data, material license uncertainty, large downloads, costly builds, external side effects, accelerators, or resource use beyond the accepted boundary. A rejected or unavailable Gate yields `paused` or `blocked`; it never becomes implicit permission.

## Resume

Resume is context, not a procedure. Accept durable input refs, verify their current identity and audit state, state the starting stage, and preserve previous failures and decisions.
