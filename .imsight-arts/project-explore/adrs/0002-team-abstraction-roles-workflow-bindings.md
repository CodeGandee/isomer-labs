# Agent Team Abstraction Includes Agent Roles, Workflow, Policy, and Capability Bindings

Isomer Labs will model an Agent Team as Agent Roles, Workflow Stages, Coordination Policy, and Capability Bindings. An Agent Team should name participating Agent Roles, describe which Agent Roles own which Workflow Stages or handoffs, define how Agent Instances coordinate, and bind Agent Roles or Agent Profiles to capabilities needed for execution.

## Status

accepted

## Considered Options

- Define teams as Agent Roles only.
- Define teams as Agent Roles, workflow, Coordination Policy, and Capability Bindings.
- Define teams as full execution graphs with every state transition, budget, and GUI surface included.

## Consequences

- Agent Teams are concrete enough to run, inspect, and reproduce.
- Users can customize team shape without writing a full execution graph.
- Agent Teams should provide enough identity and ownership information for an Execution Adapter to construct Agent Instances and per-agent Agent Workspaces during execution.
- Lower-level execution policy, budgets, and generated GUI details can stay in separate manifest or workspace documents.
