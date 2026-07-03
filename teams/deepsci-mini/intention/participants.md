# Participants

This file describes the default Agent Roles in the `deepsci-mini` Domain Agent Team Template. These are role definitions and topic-level binding slots, not concrete Agent Instances.

## Topology

- Topology intention: tree-loop.
- Root role: `deepsci-mini-lead`.
- Specialist roles: `deepsci-mini-scout` and `deepsci-mini-synth-reviewer`.
- Routing rule: specialists return durable handoffs to `deepsci-mini-lead`; they do not dispatch peers unless the approved Topic Agent Team Profile Bundle explicitly grants that authority through `{coordination_policy_ref}`.
- Runtime rule: a concrete `{agent_instance_id}` exists only after `{agent_team_instance_id}` is launched from the approved Topic Agent Team Profile Bundle.

## Topic-Level Binding Slots

| Agent Role | Agent Profile Placeholder | Capability Binding Placeholder | Skill Binding Projection Placeholder |
| --- | --- | --- | --- |
| `deepsci-mini-lead` | `{deepsci_mini_lead_agent_profile_ref}` | `{deepsci_mini_lead_capability_binding_ref}` | `{deepsci_mini_lead_skill_projection_ref}` |
| `deepsci-mini-scout` | `{deepsci_mini_scout_agent_profile_ref}` | `{deepsci_mini_scout_capability_binding_ref}` | `{deepsci_mini_scout_skill_projection_ref}` |
| `deepsci-mini-synth-reviewer` | `{deepsci_mini_synth_reviewer_agent_profile_ref}` | `{deepsci_mini_synth_reviewer_capability_binding_ref}` | `{deepsci_mini_synth_reviewer_skill_projection_ref}` |

## `deepsci-mini-lead`

- Purpose: own the mini team after launch, interpret the Research Topic, route UC-01 handoffs, normalize results, open the follow-up Research Inquiry Gate, and record the Decision Record through the Operator Agent path.
- Required skills: `isomer-rsch-shared`, `isomer-rsch-decision`, `isomer-rsch-finalize`.
- Optional skills: `isomer-rsch-review` for a final skeptical pass when `deepsci-mini-synth-reviewer` flags a serious evidence boundary.
- Hot context: `{research_topic_id}`, `{research_inquiry_id}`, `{workflow_stage_cursor_ref}`, `{gate_state_ref}`, `{decision_record_refs}`, `{handoff_refs}`, `{completion_watcher_contract_ref}`, and closeout state.

## `deepsci-mini-scout`

- Purpose: collect and bound the external context for UC-01 without turning scouting into an open-ended literature survey.
- Required skills: `isomer-rsch-shared`, `isomer-rsch-scout`.
- Optional skills: `isomer-rsch-baseline`, `isomer-rsch-science`, and `isomer-rsch-paper-outline` when the topic needs comparator context, scientific package checks, or early paper-facing evidence boundaries.
- Hot context: seed sources, literature neighborhood, dataset or benchmark notes, source identity, limitation notes, claim candidates, and Evidence Item candidates.
- Expected outputs: seed-source summaries, literature notes, candidate claims, Evidence Item candidates, unresolved source caveats, and recommended next synthesis focus.

## `deepsci-mini-synth-reviewer`

- Purpose: combine lightweight analysis and skeptical review so UC-01 can produce defensible follow-up Research Inquiry options with only three agents.
- Required skills: `isomer-rsch-shared`, `isomer-rsch-idea`, `isomer-rsch-analysis`, `isomer-rsch-review`.
- Optional skills: `isomer-rsch-science` for domain validation and `isomer-rsch-paper-plot` when a lightweight diagnostic view is needed.
- Hot context: source summaries, Evidence Item candidates, claim candidates, factor clusters, disagreement points, weak-claim notes, and follow-up inquiry options.
- Expected outputs: factor map, inquiry comparison, weak-claim review notes, accepted Evidence Item refs, rejected or downgraded claim candidates, and Gate-ready follow-up inquiry options.
