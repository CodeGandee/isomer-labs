# Instantiation Placeholders

This file names placeholder refs that topic-level material can replace when it specializes the `deepsci-mini` Domain Agent Team Template.

## Project and Topic

- `{project_ref}`: user-owned Project root or Project id.
- `{project_config_dir}`: Project Config Directory, usually `.isomer-labs/`.
- `{project_manifest_ref}`: Project Manifest discovery ref.
- `{research_topic_id}`: concrete Research Topic id.
- `{research_topic_config_ref}`: Project Manifest-registered Research Topic Config ref.
- `{topic_workspace_ref}`: Project Manifest-declared Topic Workspace ref.
- `{workspace_runtime_ref}`: persistent Workspace Runtime ref inside the Topic Workspace.
- `{effective_topic_context_ref}`: process-local resolved context for commands, path resolution, Run initialization, and provider-backed operations.

## Team Lifecycle

- `{domain_agent_team_template_ref}`: ref for this reusable template.
- `{topic_agent_team_profile_id}`: topic-level specialization derived from this template.
- `{agent_team_instance_id}`: concrete runtime team created from the Topic Agent Team Profile.
- `{coordination_policy_ref}`: collaboration, handoff, peer-read, retry, escalation, and Gate routing policy.
- `{control_mode}`: Run-level `manual` or `automatic` setting.

## Research Work

- `{research_inquiry_id}`: question or line of inquiry under the Research Topic.
- `{research_task_id}`: bounded action assigned to a Task Handler.
- `{run_id}`: bounded execution attempt for a Research Task.
- `{workflow_stage_cursor_ref}`: current stage-routing state recorded through Workspace Runtime.
- `{completion_watcher_contract_ref}`: per-handoff observation rule for completion candidates.
- `{decision_record_ref}`: Decision Record produced by Gate resolution.

## Roles and Runtime Actors

- `{agent_profile_ref}`: reusable construction or configuration ref for an Agent Instance.
- `{agent_instance_id}`: concrete runtime actor created from an Agent Profile and assigned to an Agent Role.
- `{agent_workspace_ref}`: per-agent work area inside the Topic Workspace.
- `{task_handler_ref}`: Operator Agent or one delegated Agent Instance responsible for a Research Task.
- `{service_request_ref}`: bounded Service Team support command for operational work outside research decision ownership.

## Bindings and Policies

- `{capability_binding_ref}`: generic capability binding slot.
- `{skill_binding_projection_ref}`: provider-neutral skill availability projection.
- `{execution_adapter_ref}`: backend bridge for concrete execution.
- `{research_operation_extension_point_refs}`: allowed operation slots such as command execution, repository inspection, package management, document build, literature search, cost/privacy Gate, credential use, data export, skill binding, service request, or agent launch.
- `{scheduler_policy_ref}`: automatic dispatch, retry, queueing, monitoring, checkpoint, resume, or stop policy ref.
- `{gate_policy_ref}`: reusable preflight policy for governed actions.
- `{literature_provider_binding_ref}`: provider binding for search, metadata, reading, benchmark, repository, or adjacent-work scouting.

## Role Binding Slots

- `{deepsci_mini_lead_agent_profile_ref}`.
- `{deepsci_mini_lead_capability_binding_ref}`.
- `{deepsci_mini_lead_skill_projection_ref}`.
- `{deepsci_mini_scout_agent_profile_ref}`.
- `{deepsci_mini_scout_capability_binding_ref}`.
- `{deepsci_mini_scout_skill_projection_ref}`.
- `{deepsci_mini_synth_reviewer_agent_profile_ref}`.
- `{deepsci_mini_synth_reviewer_capability_binding_ref}`.
- `{deepsci_mini_synth_reviewer_skill_projection_ref}`.

## Artifacts and Evidence

- `{source_artifact_refs}`: seed-source, related-paper, dataset, benchmark, repository, or context Artifacts.
- `{literature_note_refs}`: literature note Artifact refs.
- `{claim_candidate_refs}`: provisional claim candidate refs.
- `{evidence_item_refs}`: accepted Evidence Item refs.
- `{finding_refs}`: Finding or file-backed synthesis metadata refs.
- `{review_note_refs}`: skeptical review note refs.
- `{research_inquiry_option_refs}`: follow-up inquiry option refs.
- `{view_manifest_refs}`: literature matrix, claim graph, and inquiry comparison View Manifest refs.
- `{gate_state_ref}`: follow-up Research Inquiry Gate state ref.
- `{closure_state_ref}`: finalization or parking state recorded by the lead.
- `{resume_packet_ref}`: state needed to resume after a blocked or parked UC-01 run.

## Replacement Rule

Replace placeholders only in Topic Agent Team Profiles, Research Topic Configs, Agent Team Instance records, Capability Bindings, Skill Binding projections, Workspace Runtime records, or generated execution contracts. Leave the Domain Agent Team Template source generic unless a new placeholder or default truly belongs to all research topics that use `deepsci-mini`.
