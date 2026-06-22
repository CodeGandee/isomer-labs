# DeepSci Mini Domain Template Intention Source

This directory is editable intention source for `deepsci-mini` as a small Domain Agent Team Template. It deliberately stops before any concrete Research Topic, Topic Agent Team Profile, Agent Team Instance, Project path, credential, provider payload, launch choice, or runtime state.

## Purpose

- Preserve the smallest useful DeepScientist-style team for UC-01, Explore a New Research Direction.
- Keep the team at three Agent Roles: one internal lead, one scout, and one synthesis reviewer.
- Leave topic-specific choices as placeholders so a later Topic Agent Team Profile can specialize this template for `{research_topic_id}`.
- Keep generated execution contracts out of the intention source except as derived `../execplan/` material.

## Files

- `loop-overview.md` is the entrypoint and states the template lifecycle.
- `participants.md` defines Agent Roles, context boundaries, skill projections, and topic-level binding slots.
- `workflow.md` describes the manual UC-01 flow and handoff expectations.
- `workspace.md` maps the package to Isomer Project, Topic Workspace, Workspace Runtime, and Agent Workspace boundaries.
- `constraints.md` records guardrails and open decisions that generated contracts must respect.
- `instantiation-placeholders.md` catalogs placeholder names for topic-level specialization.
- `project-context.md` records concise surrounding project context.

## Source Boundary

- Design source: `../source/team-design.md`.
- Editable Domain Agent Team Template intention source: this directory.
- Generated operational material: `../execplan/`.
- Tool-local generated-loop execution state: `../runs/`, if that execution surface is prepared. This is not Isomer Workspace Runtime.
- Isomer runtime truth: `{topic_workspace_ref}` and its Workspace Runtime, not `teams/deepsci-mini/`.
- Project discovery truth: `{project_manifest_ref}` in the Project Config Directory, not inferred filesystem scanning.

## Template Boundary

This package may be registered or referenced as `{domain_agent_team_template_ref}` from a Project Manifest. A concrete topic must create `{topic_agent_team_profile_id}` from this template before launch. A running team exists only after `{agent_team_instance_id}` is created from that profile.
