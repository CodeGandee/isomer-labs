# Service Skills

This subtree contains Service Team skills for bounded operational support. Service skills use the `isomer-srv-<purpose>` naming convention and are intended for Service Agent Instances, Topic Service Agents, and Topic Service Masters.

| Skill | Purpose |
| --- | --- |
| `isomer-srv-agent-env-setup` | Prepare Git-backed Agent Workspace cwd readiness from Topic Workspace predecessor evidence and `topic.intent.agent_env_requirements` or an explicit agent env target spec. |
| `isomer-srv-topic-env-setup` | Prepare or check Topic Workspace Pixi setup and produce predecessor evidence; it does not prove per-Agent Workspace cwd readiness. |
| `isomer-srv-topic-service-agent-support` | Guide Topic Service Agents through bounded support for Topic Team Specialization, environment readiness, work-agent setup, monitoring, diagnostics, and support Artifacts. |

Service skills act at the command of a Project Operator Session or Operator Agent through a Service Request. They must not own Research Topics, Research Claims, Gates, Decision Records, research task routing, or Agent Team Instance membership.
