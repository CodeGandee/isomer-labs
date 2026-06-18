# Constraints and Open Questions

This file records guardrails and unresolved decisions for future Topic Agent Team Profile specialization and generated execplan work.

## Hard Constraints

- Treat `deepsci-org` as a Domain Agent Team Template, not a concrete Topic Agent Team Profile, Agent Team Instance, Run, or Topic Workspace.
- Do not turn Workflow Stages into one Agent Role per stage; role boundaries follow context reuse.
- Keep `deepsci-org-master` as the root of the team after `{agent_team_instance_id}` is launched.
- Keep specialist role names in agent-noun form: `deepsci-org-framer`, `deepsci-org-designer`, `deepsci-org-experimenter`, `deepsci-org-analyzer`, `deepsci-org-publisher`, and `deepsci-org-reviewer`.
- Preserve Isomer domain language from `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md`.
- Do not infer Topic Workspaces by scanning directories; use `{project_manifest_ref}` and `{topic_workspace_ref}`.
- Do not put runtime research state, rich Artifacts, command outputs, provider payloads, credentials, or secrets in Project Config Directory material.
- Do not import source DeepScientist runtime APIs, scheduler fields, concrete runner homes, provider-specific command bodies, mailbox routes, gateway routes, or credential details into generic intention source.
- Do not generate `execplan/` during intention revision.

## Topic Specialization Constraints

- A concrete topic must create `{topic_agent_team_profile_id}` before launch.
- `{topic_agent_team_profile_id}` must select or tune roles, Workflow Stages, expected Artifacts, Coordination Policy, Capability Binding refs, Skill Binding projection refs, Gate policy refs, Scheduler policy refs, literature provider refs, baseline-waiver policy refs, and allowed Research Operation Extension Point refs.
- `{agent_team_instance_id}` must be created only from an approved Topic Agent Team Profile.
- Agent Profiles and Capability Bindings should carry provider-neutral refs; provider-specific payloads belong behind `{execution_adapter_ref}` or adapter-owned payload refs.
- `{research_topic_config_ref}` can select defaults and refs, but it must not become the complete team workflow or runtime state store.

## Gate-Sensitive Actions

- Credential use.
- Paid or long compute.
- Private data access.
- Data export or external upload.
- Destructive mutation.
- Baseline waiver.
- Publication-facing finality.
- Final completion.

## Evidence Constraints

- Prefer durable records over recollection.
- Treat negative, failed, blocked, infeasible, null, and contradictory results as evidence.
- Do not let polished prose hide missing evidence.
- Baseline-dependent claims require a durable accepted comparator or `{baseline_waiver_policy_ref}` plus required Gate or Decision Record.
- Publication and review work must route evidence gaps back to framing, experimentation, analysis, or master decision.

## Open Questions

- Should `deepsci-org-framer` own heavy baseline reproduction, or should `{topic_agent_team_profile_id}` route substantial environment repair through `{service_request_ref}` or execution support?
- Should Nature-family companion skills be migrated into the Isomer research-paradigm skillset, or should Topic Agent Team Profiles bind source DeepScientist projections only when needed?
- Should `deepsci-org-reviewer` have direct Peer Read Access to all Agent Artifacts, or only to promoted Artifacts and declared handoff bundles?
- How much automatic-mode fanout should `{scheduler_policy_ref}` allow before `deepsci-org-master` opens a cost or long-compute Gate?
- Should automatic mode be enabled by default for this template, or only after `{gate_policy_ref}` and role-scoped Capability Bindings are configured for the topic?
