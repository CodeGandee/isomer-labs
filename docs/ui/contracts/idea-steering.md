# Research Idea Steering Contract

Steering is the explicit mutating boundary behind `Explore this idea` and `Explore instead`. Node selection, filtering, focus, layout, detail inspection, and traversal remain read-only.

`POST /api/topics/{topic_id}/ideas/steer` accepts `action`, `target_idea_id`, `actor_ref`, `idempotency_key`, optional `expected_index_revision`, exact `expected_states`, rationale, user prompt, reopening confirmation, Gate policy and resolution, and dispatch routing hints. `explore_instead` also requires exact `replaced_idea_ids`; each replacement defaults to `deferred` or may be set to `closed` with one canonical closure reason. The server never infers replacements from browser selection or global state.

Before submission, Project Web shows the target, every replacement, and each expected transition. A closed or deferred target requires `reopen_confirmed` and rationale. Configured Gate policy can return `gate_required` before mutation.

An accepted response distinguishes canonical acceptance from actor delivery. It includes `operation_id`, `canonical_accepted`, Decision Record ref when applicable, Research Inquiry ref, Research Task ref, Provenance Record ref, handoff ref, transition refs, decision-option refs, resulting idea facets, new or pending index revision, `dispatch_status`, dispatch details, retry ref, and diagnostics. Canonical writes commit before adapter delivery. A pending or blocked delivery leaves the decision and task durable and returns an idempotent retry ref.

A conflict response has `mutated: false`, current revision, current idea facets, and diagnostics. Retrying equivalent input with the same idempotency key returns the original durable refs without duplicate decisions, transitions, tasks, or handoffs.
