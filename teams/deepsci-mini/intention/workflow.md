# Workflow Intention

This file describes how work should move through `deepsci-mini` after a Topic Agent Team Profile specializes the template and before any generated execplan contracts are consumed at runtime.

## Lifecycle Flow

```text
{domain_agent_team_template_ref}
  |
  v
{topic_agent_team_profile_bundle_ref} for {research_topic_id}
  |
  v
{agent_team_instance_id}
  |
  v
{research_task_id} attempted by {run_id}
```

The Domain Agent Team Template owns reusable method shape. The Topic Agent Team Profile owns topic specialization. The Agent Team Instance owns runtime membership. Workspace Runtime records Runs, handoffs, Gates, Artifacts, Evidence Items, Findings, Decision Records, View Manifests, and Provenance Records.

## Manual UC-01 Flow

1. The Operator Agent resolves Effective Topic Context for `{research_topic_id}` and selects `deepsci-mini` as `{domain_agent_team_template_ref}`.
2. The Topic Agent Team Profile Bundle specializes the template with UC-01 constraints, expected Artifact kinds, Skill Binding projection refs, Capability Binding refs, Gate policy refs, and literature provider refs when available.
3. `{agent_team_instance_id}` launches or simulates from the approved profile bundle; `deepsci-mini-lead` becomes the root role inside the team.
4. The lead creates or receives the initial `{research_inquiry_id}` and a bounded `{research_task_id}` for UC-01.
5. The lead dispatches a scout handoff to `deepsci-mini-scout`.
6. The scout returns seed-source summaries, literature notes, claim candidates, Evidence Item candidates, caveats, blockers, and suggested synthesis focus.
7. The lead normalizes accepted scout output into `{workspace_runtime_ref}` before relying on it.
8. The lead dispatches a synthesis-review handoff to `deepsci-mini-synth-reviewer`.
9. The synth reviewer returns factor clusters, inquiry options, weak-claim notes, rejected or downgraded claim candidates, and review notes.
10. The lead normalizes accepted synthesis-review output, writes minimal View Manifest refs, and opens a follow-up Research Inquiry Gate.
11. The Operator Agent presents the Gate to the user.
12. The selected inquiry and rationale are recorded as a Decision Record with Evidence Item links.

## Stage Routing

| Workflow Stage or Companion Work | Intended Owner | Topic-Level Slots |
| --- | --- | --- |
| Intake audit | `deepsci-mini-lead` | `{workspace_runtime_ref}`, `{decision_record_refs}` |
| Scout | `deepsci-mini-scout` | `{literature_provider_binding_ref}`, `{research_topic_config_ref}` |
| Literature note extraction | `deepsci-mini-scout` | `{artifact_format_profile_ref}`, `{source_artifact_refs}` |
| Evidence synthesis | `deepsci-mini-synth-reviewer` | `{evidence_item_refs}`, `{claim_candidate_refs}` |
| Inquiry option comparison | `deepsci-mini-synth-reviewer` | `{research_inquiry_option_refs}`, `{view_manifest_refs}` |
| Skeptical review | `deepsci-mini-synth-reviewer` | `{review_note_refs}`, `{weak_claim_refs}` |
| Decision | `deepsci-mini-lead` | `{decision_record_ref}`, `{gate_policy_ref}` |
| Finalize or park | `deepsci-mini-lead` | `{closure_state_ref}`, `{resume_packet_ref}` |

## Handoff Expectations

- Each handoff names `{research_topic_id}`, `{research_inquiry_id}`, `{research_task_id}`, and `{run_id}` when available.
- Each handoff names inspected inputs, produced outputs, affected claim candidates, Evidence Items, unresolved caveats, next recommended Workflow Stage Cursor, and Gate recommendations.
- Specialists may recommend routes, but `deepsci-mini-lead` records route authority inside `{workspace_runtime_ref}`.
- Scout output is not authoritative until accepted by the lead.
- Synthesis-review output is not authoritative until accepted by the lead.
- UC-01 closeout must stop at the follow-up Research Inquiry Gate unless the Topic Agent Team Profile explicitly marks the run as read-only inspection.
