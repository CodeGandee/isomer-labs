# DeepSci Org

`teams/deepsci-org/` contains a domain-level agent team definition for the full DeepScientist-inspired Isomer research organization. It defines `deepsci-org` as a reusable Domain Agent Team Template, not as a concrete Topic Agent Team Profile, Agent Team Instance, Run, Topic Workspace, or provider-specific launch package.

The template captures the reusable research method: `deepsci-org-master` owns the team as the internal root role, while `deepsci-org-framer`, `deepsci-org-designer`, `deepsci-org-experimenter`, `deepsci-org-analyzer`, `deepsci-org-publisher`, and `deepsci-org-reviewer` preserve context across related Workflow Stages. Role boundaries follow context reuse instead of one role per step.

## Contents

- `source/team-design.md` explains the role design, skill bindings, manual mode, automatic mode, Coordination Policy, and default constraints.
- `intention/` contains editable intention material for future generated execution contracts, with placeholders for topic-level instantiation.
- `intention/instantiation-placeholders.md` lists the refs a Topic Agent Team Profile, Research Topic Config, Agent Team Instance, Capability Binding, Skill Binding projection, policy, provider binding, or Workspace Runtime record can fill in later.

## Isomer Boundary

This directory is authoring material for `{domain_agent_team_template_ref}`. A Project Manifest may register or reference it, and a concrete Research Topic may specialize it into `{topic_agent_team_profile_id}` before launch. A running team exists only after `{agent_team_instance_id}` is created from that profile.

Runtime research state belongs in the manifest-declared `{topic_workspace_ref}` and its Workspace Runtime, not in `teams/deepsci-org/`. Concrete Agent Instances receive Agent Workspaces inside the Topic Workspace; this template only defines default roles, skill projections, coordination intent, workspace expectations, and topic-level binding slots.
