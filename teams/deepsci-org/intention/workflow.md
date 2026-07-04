# Workflow Intention

This file describes how work should move through `deepsci-org` after a Topic Agent Team Profile specializes the template and before any generated `execplan/` contracts exist.

## Lifecycle Flow

```text
{domain_agent_team_template_ref}
  |
  v
{topic_agent_team_profile_id} for {research_topic_id}
  |
  v
{agent_team_instance_id}
  |
  v
{research_task_id} attempted by {run_id}
```

The Domain Agent Team Template owns reusable method shape. The Topic Agent Team Profile owns topic specialization. The Agent Team Instance owns runtime membership. Workspace Runtime records Runs, handoffs, Gates, Artifacts, Evidence Items, Findings, Research Claims, Decision Records, and Provenance Records.

## Operating Model

- The intended topology is a tree-loop rooted at `deepsci-org-master`.
- The master owns stage routing, handoff normalization, Gates, Decision Records, finalization, and parking.
- Specialists own bounded Research Tasks and return durable handoffs to the master.
- Workflow Stages remain visible in routing, but Agent Roles stay grouped by context locality.
- The Project-facing Operator Agent may create `{topic_agent_team_profile_id}` and launch `{agent_team_instance_id}`, but it is not a member role in this template.

## Manual Mode

1. The user gives `{research_topic_id}`, constraints, and desired `{control_mode}` through the Project-facing Operator Agent or another approved entrypoint.
2. The Operator Agent or Execution Adapter resolves Effective Topic Context and selects `{domain_agent_team_template_ref}`.
3. `{topic_agent_team_profile_id}` specializes the template with selected roles, constraints, expected Artifacts, Skill Binding projection refs, Capability Binding refs, Gate policy refs, Scheduler policy refs, and provider binding refs.
4. `{agent_team_instance_id}` launches from the profile; `deepsci-org-master` becomes the root role inside the team.
5. For each `{research_task_id}`, the master writes a handoff with scope, inspected inputs, expected outputs, Gate constraints, Skill Binding projection ref, Capability Binding ref, and `{completion_watcher_contract_ref}`.
6. The specialist Agent Instance works inside `{agent_workspace_ref}`, records Agent Artifacts, and returns promoted Artifacts, Evidence Items, Findings, Research Claim updates, Decision Record recommendations, caveats, and blockers.
7. The master normalizes the handoff into `{workspace_runtime_ref}`, advances or holds `{workflow_stage_cursor_ref}`, and asks the user only for true Gates.

Manual Mode is the default for first launch because it lets the user inspect the topic profile, workspace boundaries, governed resources, and early scientific route before automatic continuation.

## Fully Automatic Mode

1. `{scheduler_policy_ref}` authorizes the master to continue from durable state after non-blocking milestones.
2. The master performs intake, chooses the next Workflow Stage Cursor, and dispatches the smallest useful Research Task.
3. `{completion_watcher_contract_ref}` observes candidate completion through Agent Instance replies, inspected Agent Artifacts, adapter events, file observations, validation rules, correlation keys, or staleness rules.
4. When a specialist completes, the master records the handoff, runs the required validation or decision skill, and dispatches the next Research Task if no Gate is required.
5. Routine route choices can proceed through `isomer-deepsci-decision` without user interruption when `{gate_policy_ref}` allows it.
6. Governed actions still open Gates for cost, credentials, private data, data export, destructive mutation, long compute, baseline waiver, publication-facing finality, and final completion.
7. When state is blocked, stale, contradictory, or repeatedly unchanged, the master records the blocker and parks `{agent_team_instance_id}` with a resume packet.

Automatic mode is valid only after the Topic Agent Team Profile declares enough policies, bindings, and completion watchers for the topic.

## Stage Routing

| Workflow Stage or Companion Work | Intended Owner | Topic-Level Slots |
| --- | --- | --- |
| Intake audit | `deepsci-org-master` | `{workspace_runtime_ref}`, `{decision_record_refs}` |
| Scout | `deepsci-org-framer` | `{literature_provider_binding_ref}`, `{research_topic_config_ref}` |
| Baseline | `deepsci-org-framer` | `{baseline_artifact_ref}`, `{baseline_waiver_policy_ref}` |
| Idea | `deepsci-org-designer` | `{candidate_route_refs}`, `{objective_contract_ref}` |
| Optimize | `deepsci-org-designer` | `{optimization_frontier_ref}`, `{scheduler_policy_ref}` |
| Experiment | `deepsci-org-experimenter` | `{execution_adapter_ref}`, `{run_contract_ref}`, `{expected_metric_artifact_refs}` |
| Analysis campaign | `deepsci-org-analyzer` | `{parent_claim_ref}`, `{analysis_slice_refs}` |
| Science computation | `deepsci-org-experimenter` for main Runs, `deepsci-org-analyzer` for follow-up validation | `{research_operation_extension_point_refs}` |
| Paper outline | `deepsci-org-publisher` | `{paper_contract_ref}`, `{artifact_format_profile_ref}` |
| Write | `deepsci-org-publisher` | `{claim_evidence_map_ref}`, `{draft_artifact_ref}` |
| Paper plot | `deepsci-org-publisher` for paper-facing plots, `deepsci-org-analyzer` for diagnostic displays | `{figure_artifact_refs}` |
| Figure polish | `deepsci-org-publisher` for final figures, `deepsci-org-analyzer` for milestone figures | `{figure_render_binding_ref}` |
| Review | `deepsci-org-reviewer` | `{review_report_ref}`, `{peer_read_access_policy_ref}` |
| Rebuttal | `deepsci-org-reviewer` routes pressure, `deepsci-org-publisher` writes response text | `{reviewer_item_refs}`, `{revision_log_ref}` |
| Decision | `deepsci-org-master` | `{decision_record_ref}`, `{gate_policy_ref}` |
| Finalize | `deepsci-org-master` with `deepsci-org-publisher` | `{final_package_ref}`, `{closure_state_ref}` |

## Handoff Expectations

- Each handoff names `{research_topic_id}`, `{research_inquiry_id}`, `{research_task_id}`, and `{run_id}` when available.
- Each handoff names inspected inputs, produced outputs, affected Research Claims, Evidence Items, unresolved caveats, next recommended Workflow Stage Cursor, and Gate recommendations.
- Specialists may recommend routes, but `deepsci-org-master` records the route authority inside `{workspace_runtime_ref}`.
- Publication work routes missing support back to analysis, framing, review, or master decision.
- Review work records findings and route recommendations; it must not silently mutate publication Artifacts.

## Completion

- The master can close the loop only after supported claims, limitations, recommendations, and closure state are consolidated.
- Final completion still requires explicit approval when `{gate_policy_ref}` requires it.
- Parking is valid when a blocker, stale state, contradiction, missing credential, missing policy, or governed decision prevents safe continuation.
