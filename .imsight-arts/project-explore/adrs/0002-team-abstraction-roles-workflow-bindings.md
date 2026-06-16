# Team Abstraction Includes Roles, Workflow, and Bindings

Isomer Labs will model an agent team as roles plus workflow plus bindings. A team definition should name the participating roles, describe which roles own which workflow stages or handoffs, and bind those roles to runners, tools, or agent profiles needed for execution.

## Status

accepted

## Considered Options

- Define teams as roles only.
- Define teams as roles, workflow, and bindings.
- Define teams as full execution graphs with every state transition, budget, and GUI surface included.

## Consequences

- Team definitions are concrete enough to run, inspect, and reproduce.
- Users can customize team shape without writing a full execution graph.
- Team definitions should provide enough identity and ownership information for a Research Engine Adapter to construct Agent Instances and per-agent Agent Workspaces during execution.
- Lower-level execution policy, budgets, and generated GUI details can stay in separate manifest or workspace documents.
