# Workspace Intention

This file records workspace and artifact expectations for the `deepsci-mini` Domain Agent Team Template. It does not create Topic Workspaces, Agent Workspaces, runtime state, credentials, provider payloads, or launch artifacts.

## Authoring Package

- Template authoring package: `teams/deepsci-mini/`.
- Editable intention source: `teams/deepsci-mini/intention/`.
- Design source: `teams/deepsci-mini/source/team-design.md`.
- Generated operational material: `teams/deepsci-mini/execplan/`.
- Tool-local generated-loop run state: `teams/deepsci-mini/runs/`, if that execution surface is prepared. This is not Isomer Workspace Runtime.
- Isomer runtime state for a real research topic: `{topic_workspace_ref}`, not `teams/deepsci-mini/`.

## Project and Topic Mapping

- `{project_ref}` is the user-owned repository, checkout, or directory tree managed by Isomer.
- `{project_config_dir}` is the Project Config Directory, usually `.isomer-labs/`.
- `{project_manifest_ref}` is the discovery authority for `{research_topic_config_ref}`, `{topic_workspace_ref}`, `{domain_agent_team_template_ref}`, `{topic_agent_team_profile_bundle_ref}`, `{agent_team_instance_id}`, Agent Profiles, Capability Binding refs, provider binding refs, Artifact Format Profile refs, and GUI Component Registry refs.
- `{research_topic_config_ref}` stores topic defaults and refs for `{research_topic_id}`; it must not store Workspace Runtime state, Run status, command outputs, provider payloads, rich Artifact contents, credentials, or secrets.
- `{topic_workspace_ref}` is the Project Manifest-declared Topic Workspace for one Research Topic.

## Topic Workspace Runtime

`{topic_workspace_ref}` owns `{workspace_runtime_ref}`, Research Inquiries, Research Tasks, Runs, rich Artifacts, generated View Manifests, Agent Workspaces, and logs for `{research_topic_id}`.

Recommended semantic contents for a concrete topic are:

```text
{topic_workspace_ref}/
  state.sqlite
  artifacts/
  agents/
  views/
  runs/
  logs/
```

These names describe a typical Topic Workspace shape, not paths this template creates. The Project Manifest and workspace policy decide the concrete path and tracking policy.

## Agent Workspace Expectations

- Each concrete `{agent_instance_id}` inside `{agent_team_instance_id}` should receive `{agent_workspace_ref}` under `{topic_workspace_ref}`.
- Each Agent Workspace should declare an advisory Workspace Boundary through README, boundary manifest, Agent Team Instance record, or Coordination Policy.
- Durable dependencies should be promoted into Artifacts, Evidence Items, Findings, Decision Records, Gates, View Manifests, or Provenance Records before another role relies on them.
- `deepsci-mini-scout` owns source notes and initial claim/Evidence Item candidates.
- `deepsci-mini-synth-reviewer` owns factor synthesis, inquiry option comparison, weak-claim review notes, and accepted/rejected evidence posture.
- Peer writes should be treated as validation issues unless `{coordination_policy_ref}` explicitly assigns repair, migration, or cleanup work.

## Artifact Expectations

- Required UC-01 Artifacts: seed-source summaries, literature notes, claim candidate notes, synthesis notes, review notes, inquiry option notes, Decision Record content, and View Manifest files.
- Evidence Item candidates become accepted Evidence Items only after `deepsci-mini-lead` normalizes them into Workspace Runtime.
- Claim candidates must not become supported Research Claims unless valid Evidence Item links pass validation.
- GUI View Manifests and AG-UI payloads may show state, previews, or pending Gates, but they are not the source of research truth.

## Execution and Platform Boundary

- This template does not define concrete credentials, provider payloads, mailbox routes, gateway routes, scheduler internals, command bodies, launch commands, or live process ids.
- Execution should later use `{execution_adapter_ref}`, `{research_operation_extension_point_refs}`, `{capability_binding_ref}`, `{skill_binding_projection_ref}`, `{scheduler_policy_ref}`, `{gate_policy_ref}`, and `{completion_watcher_contract_ref}`.
- Houmao can be one Execution Adapter surface, but this intention uses Isomer domain language so the template can map to other execution backends.
- Service Team support should enter through `{service_request_ref}` and remain outside research decision ownership.
