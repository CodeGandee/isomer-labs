# Constraints and Open Questions

This file records guardrails and unresolved decisions for future Topic Agent Team Profile specialization and generated execplan work.

## Hard Constraints

- Treat `deepsci-mini` as a Domain Agent Team Template, not a concrete Topic Agent Team Profile, Agent Team Instance, Run, or Topic Workspace.
- Keep exactly three default Agent Roles unless a future accepted design decision revises the mini template.
- Preserve Isomer domain language from `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md`.
- Do not infer Topic Workspaces by scanning directories; use `{project_manifest_ref}` and `{topic_workspace_ref}`.
- Do not put runtime research state, rich Artifacts, command outputs, provider payloads, credentials, or secrets in Project Config Directory material.
- Do not import source DeepScientist runtime APIs, scheduler fields, concrete runner homes, provider-specific command bodies, mailbox routes, gateway routes, or credential details into generic intention source.

## Topic Specialization Constraints

- A concrete topic must materialize its fixed Topic Agent Team Profile Bundle at `{topic_agent_team_profile_bundle_ref}` before launch.
- The Topic Agent Team Profile Bundle must select or tune expected Artifacts, Coordination Policy, Capability Binding refs, Skill Binding projection refs, Gate policy refs, Scheduler policy refs, literature provider refs, and allowed Research Operation Extension Point refs.
- `{agent_team_instance_id}` must be created only from an approved Topic Agent Team Profile.
- Agent Profiles and Capability Bindings should carry provider-neutral refs; provider-specific payloads belong behind `{execution_adapter_ref}` or adapter-owned payload refs.
- `{research_topic_config_ref}` can select defaults and refs, but it must not become the complete team workflow or runtime state store.

## Gate-Sensitive Actions

- Follow-up Research Inquiry selection.
- Credential use.
- Paid or long compute.
- Private data access.
- Data export or external upload.
- Destructive mutation.
- Baseline waiver.
- Claim strengthening.
- Final completion.

## Evidence Constraints

- Prefer durable records over recollection.
- Treat negative, failed, blocked, infeasible, null, and contradictory results as evidence.
- Do not let source summaries become accepted Evidence Items until the lead normalizes them.
- Do not let claim candidates become supported Research Claims without accepted Evidence Item links.
- Do not let the lead close UC-01 without a Gate and Decision Record.

## Open Questions

- Should the Milestone 6 UC-01 command allow selecting `deepsci-org` as an explicit alternate template, or should it only support `deepsci-mini` until the larger template is needed?
- Should `deepsci-mini-synth-reviewer` produce first-class Finding records in Milestone 6, or lifecycle records with file-backed metadata until Milestone 8 expands recording APIs?
- Should deterministic adapter simulation produce all literature and claim data, or should some fixture Artifacts exist before handoff dispatch?
