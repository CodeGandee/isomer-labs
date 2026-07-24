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

## Review Mode Resolution

Automatable Kaoju review checkpoints are explore plan handoff, Direction Set selection and acceptance, Reading List refinement and acceptance, Comparison Intent review and Proceed Decision, bounded trial-plan review and execution authorization within pinned inputs and resources, paper structure and draft review, and bounded local paper-build authorization.

Human review is the default when the current prompt is silent, merely asks to continue, or authorizes only `run to <target>`. Use agent review only when the current prompt explicitly and unambiguously delegates the applicable checkpoint or a semantically clear set of checkpoints for a named target. Target-scoped “automate everything” may include review only when its wording and context clearly cover those checkpoints. Ambiguous delegation retains human review or triggers one clarification.

Agent review may revise, narrow, reject, or accept a candidate inside the accepted target, evidence, meaning, validation, input, resource, attempt, and interpretation boundaries. It never means automatic acceptance. A candidate that lacks required evidence, violates its focused contract, or fails validation must be rejected, revised, narrowed, or paused. Record the review mode, prompt-scoped basis, reviewing actor, rationale, affected refs, and terminal or resume posture through existing owner-supported decision, Run, Artifact, and provenance fields. The delegation expires when the target completes, the user changes the target, or the workflow reaches a checkpoint outside the delegated set.

## Comparison Intent Checkpoint

Empirical comparison requires an accepted Comparison Intent Document and a Proceed Decision before candidate preparation, downloads, environment mutation, or Runs. Under human review, present the document, list unresolved decisions, and ask whether the user wants to clarify for more detail or proceed. Under explicit prompt-delegated agent review, the comparison owner may revise, narrow, reject, or accept the intent and record the Proceed Decision without another user turn. Material ambiguity outside delegated scope still pauses.

## Gate Triggers

Generic review delegation does not authorize credentials, private or restricted data, material license uncertainty, destructive or irreversible action, unexpected cost or resource expansion, public network exposure, publication acceptance, external publication, or submission. Use the existing Gate owner for each protected action. A rejected or unavailable Gate yields `paused` or `blocked`; it never becomes implicit permission.

Run-to authorization alone does not delegate review or satisfy a protected Gate. The prompt-level controller may traverse routine in-scope prerequisites and explicitly delegated eligible review checkpoints, but it pauses before every nondelegable boundary and returns the decision, target, accepted refs, and resume point. A material alternative or changed research meaning outside the delegated scope also requires a fresh user choice.

## Prerequisite Recovery

Before target mutation, classify a missing input with a known in-scope producer as `paused` and use `prerequisite-recovery.md`. An ordinary target request receives the four recovery choices before any producer procedure starts. Explicit target-scoped run-to authorization lets the controller consume routine procedure terminal reports, but every procedure remains bounded and records a separate Run.

## Resume

Resume is context, not a procedure. Accept durable input refs, verify their current identity and audit state, state the starting stage, and preserve previous failures and decisions.
