# Loop Overview: deepsci-org

`deepsci-org` is a Domain Agent Team Template for DeepScientist-style research in Isomer Labs. The template defines a reusable research-method team; it does not define a user's concrete topic, Topic Workspace, launch profile, credentials, or live Agent Instances.

## Objective

- Define the reusable team intent for `{domain_agent_team_template_ref}`.
- Preserve the central design principle: Agent Roles are grouped by reusable context, not by one Workflow Stage per role.
- Expose topic-level slots for `{research_topic_id}`, `{topic_agent_team_profile_id}`, `{agent_team_instance_id}`, `{topic_workspace_ref}`, Capability Binding refs, Skill Binding projection refs, Gate policy refs, Scheduler policy refs, and provider binding refs.
- Keep generated execution contracts out of the intention source until a later `execplan/` generation step.

## Template Lifecycle

| Isomer Layer | Meaning for `deepsci-org` |
| --- | --- |
| Domain Agent Team Template | This reusable package, `{domain_agent_team_template_ref}`, with default roles, stages, Coordination Policy intent, and binding slots. |
| Topic Agent Team Profile | `{topic_agent_team_profile_id}`, a topic-specific specialization for `{research_topic_id}` with selected roles, stage tuning, expected Artifacts, policies, and bindings. |
| Agent Team Instance | `{agent_team_instance_id}`, the runtime team created from the profile with concrete Agent Instances and Agent Workspaces. |
| Run | `{run_id}`, a bounded execution attempt for `{research_task_id}` recorded through Workspace Runtime. |

## Default Participants

- `deepsci-org-master`: root of the team, owns routing, Decisions, Gates, and closure.
- `deepsci-org-framer`: owns scouting, task framing, and baseline context.
- `deepsci-org-designer`: owns idea selection, route design, and optimization frontier context.
- `deepsci-org-experimenter`: owns main implementation and measured Runs.
- `deepsci-org-analyzer`: owns follow-up slices, ablations, robustness checks, error analysis, and claim updates.
- `deepsci-org-publisher`: owns outline, writing, plots, figure polish, data availability, and presentation surfaces.
- `deepsci-org-reviewer`: owns independent skeptical audit and rebuttal routing.

## Operating Model

- The intended topology is a tree-loop with `deepsci-org-master` as the internal team root.
- Work enters the team through `{research_topic_id}`, `{research_inquiry_id}`, `{research_task_id}`, and `{control_mode}` resolved from Effective Topic Context.
- The Project-facing Operator Agent may select this template, specialize it into `{topic_agent_team_profile_id}`, launch `{agent_team_instance_id}`, and record task-routing changes, but `deepsci-org-master` remains the root role inside the team.
- Specialists own bounded context-heavy Research Tasks and return durable handoffs to `deepsci-org-master`.
- Manual Mode is the first-launch default for a new topic profile; automatic mode requires explicit Scheduler Policy, Gate Policy, Capability Binding, and Skill Binding projection refs.
- The loop finishes when `deepsci-org-master` records closure, parks the package with a resume packet, or opens a Gate that prevents safe continuation.

## Workspace Expectations

- `teams/deepsci-org/` is an authoring package for the reusable template.
- `{project_manifest_ref}` is the discovery authority for Research Topics, Topic Workspaces, Domain Agent Team Templates, Topic Agent Team Profiles, and Agent Team Instances.
- `{topic_workspace_ref}` is the topic-level storage and runtime area for one Research Topic.
- `{workspace_runtime_ref}` records Research Inquiries, Research Tasks, Runs, handoffs, Artifacts, Evidence Items, Findings, Research Claims, Gates, Decision Records, View Manifests, and Provenance Records.
- Agent Workspaces live inside `{topic_workspace_ref}` for concrete `{agent_instance_id}` values; the template only states the boundary rules.
- The engine must not infer this template from a Topic Workspace path, and a Topic Workspace must not contain a workspace-local `teams/` directory.

## Open Questions

- Should heavy baseline reproduction remain with `deepsci-org-framer`, or should the Topic Agent Team Profile route substantial repair through `{service_request_ref}` or `deepsci-org-experimenter`?
- Which Nature-family companion skills should become Isomer-native projections, and which should remain optional source projections for topic profiles that need them?
- What default Peer Read Access should `deepsci-org-reviewer` receive in `{coordination_policy_ref}`?
- What fanout threshold should `{scheduler_policy_ref}` treat as a cost or long-compute Gate?
