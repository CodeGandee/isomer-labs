# DeepSci Org Domain Template Intention Source

This directory is editable intention source for `deepsci-org` as a Domain Agent Team Template. It is derived from `../source/team-design.md`, but it deliberately stops before any concrete Research Topic, Topic Agent Team Profile, Agent Team Instance, Project path, credential, provider payload, launch choice, or runtime state.

## Purpose

- Preserve the DeepScientist-inspired research method as reusable Isomer template material.
- Keep role boundaries based on context reuse, not one Agent Role per Workflow Stage.
- Leave topic-specific choices as placeholders so a later Topic Agent Team Profile can specialize this template for `{research_topic_id}`.
- Keep `deepsci-org-master` as the team root while allowing the Project-facing Operator Agent to select, specialize, launch, or stop the team outside this template.
- Keep this source editable before future generated `execplan/` material exists.

## Files

- `loop-overview.md` is the entrypoint and states the template lifecycle.
- `participants.md` defines default Agent Roles, context boundaries, skill projections, and topic-level binding slots.
- `workflow.md` describes manual and automatic coordination without binding to a concrete topic.
- `workspace.md` maps this authoring package to Isomer Project, Topic Workspace, Workspace Runtime, and Agent Workspace rules.
- `constraints.md` records guardrails and open decisions that generated contracts must respect.
- `instantiation-placeholders.md` catalogs placeholder names for topic-level specialization.

## Source Boundary

- Source design: `../source/team-design.md`.
- Editable Domain Agent Team Template intention source: this directory.
- Future generated operational material: `../execplan/`, if a Houmao or other Execution Adapter workflow generates it from this source.
- Tool-local generated-loop execution state for that generated package: `../runs/`, if that execution surface is prepared. This is not Isomer Workspace Runtime.
- Isomer runtime truth: `{topic_workspace_ref}` and its Workspace Runtime, not `teams/deepsci-org/`.
- Project discovery truth: `{project_manifest_ref}` in the Project Config Directory, not inferred filesystem scanning.

## Template Boundary

This package may be registered or referenced as `{domain_agent_team_template_ref}` from a Project Manifest, commonly under a Project Config Directory such as `.isomer-labs/`. That path is a semantic Isomer example, not a requirement that this authoring package create project config files. A concrete topic must create `{topic_agent_team_profile_id}` from this template before launch. A running team exists only after `{agent_team_instance_id}` is created from that profile.

## Placeholder Convention

Curly-brace names such as `{research_topic_id}`, `{topic_workspace_ref}`, and `{deepsci_org_master_capability_binding_ref}` are intentional placeholders. A topic-level instantiation should replace them with refs from the Project Manifest, Research Topic Config, Topic Agent Team Profile, Capability Bindings, Skill Binding projections, Gate policies, Scheduler policies, provider bindings, or Workspace Runtime records.
