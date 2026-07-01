# Service Skills

This subtree contains Service Team skills for bounded operational support. Service skills use the `isomer-srv-<purpose>` naming convention and are intended for Service Agent Instances, Topic Service Agents, and optional Topic Service Masters. If no Topic Service Master is started for a Topic Workspace, the Project Operator Session or Operator Agent performs the same bounded Topic Workspace manager duties directly.

| Skill | Purpose |
| --- | --- |
| `isomer-srv-agent-env-setup` | Prepare Git-backed Agent Workspace worktrees and cwd readiness from Topic Workspace, Topic Main Development Repository, and projection predecessor evidence plus `topic.intent.agent_env_requirements` or an explicit agent env target spec. |
| `isomer-srv-topic-env-setup` | Prepare or check Topic Workspace Pixi setup, Topic Main Development Repository readiness, canonical external repositories, external repo projections, and topic-level predecessor evidence; it does not prove per-Agent Workspace cwd readiness. |
| `isomer-srv-topic-service-agent-support` | Guide Topic Service Agents and optional Topic Service Masters through bounded Topic Workspace management, Topic Team Specialization support, environment readiness, work-agent setup, monitoring, diagnostics, and support Artifacts. |

Service skills act at the command of a Project Operator Session or Operator Agent through a Service Request. They must not own Research Topics, Research Claims, Gates, Decision Records, research task routing, or Agent Team Instance membership.
