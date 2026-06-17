# Built-in Service Team for Operational Support

Isomer will provide a built-in Service Team for common operational support work, such as configuring development environments for a target Agent Workspace and tech stack, repairing dependency or runtime issues, collecting diagnostics, and resolving system compatibility problems. Service Team members act at the command of the Operator Agent through specific Service Requests. The Service Team is Isomer infrastructure, not a Domain Agent Team Template, Topic Agent Team Profile, or Agent Team Instance.

## Status

accepted

## Considered Options

- Model operational support as ordinary Agent Roles inside every research Agent Team Instance.
- Hide operational support inside Execution Adapter internals.
- Add a built-in Service Team with explicit Service Requests and Service Agent Instances.
- Restrict Service Team execution to only tool-native subagents or only launched service agents.

## Decision

Add **Service Team**, **Service Request**, **Service Dispatch Form**, and **Service Agent Instance** as Isomer concepts. The Operator Agent may open Service Requests for Projects, Isomer Workspaces, Runs, Agent Workspaces, Agent Instances, or tech-stack support scopes. For each Service Request, the Operator Agent chooses a Service Dispatch Form. In `tool_native_subagent` form, the Operator Agent uses native multi-agent or subagent tooling available in its execution surface. In `launched_service_agent` form, the Operator Agent or Execution Adapter launches or resolves Service Agent Instances and dispatches Service Requests to them. Workspace-scoped Service Requests use Workspace Runtime for handoff and completion records, and support work that changes state must produce Artifacts and Provenance Records.

## Consequences

- Research teams stay focused on research methodology, task execution, evidence, and review.
- Common environment and compatibility work has a durable Isomer record instead of living only in ad hoc chat or adapter behavior.
- Tool-native subagents and launched service agents are both valid Service Team realization paths.
- Service Agent Instances are outside Agent Team Instance membership and cannot be selected as Task Handlers for Research Tasks.
- Launched Service Agent Instances do not become a research Agent Team Instance.
- The Service Team does not own Research Goals, Research Claims, Gates, or research decisions.
- Execution Adapters can still implement backend-specific setup mechanics, but user-visible support work remains visible as Service Requests when it creates Artifacts or changes project, workspace, runtime, dependency, or environment state.
