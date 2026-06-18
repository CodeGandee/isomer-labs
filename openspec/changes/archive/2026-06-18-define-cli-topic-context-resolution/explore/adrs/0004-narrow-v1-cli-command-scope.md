# Narrow V1 CLI Command Scope

The first implementation of `isomer-cli` topic context resolution uses project-scoped, topic-scoped, and run-scoped command families. Project validation and discovery commands do not require Effective Topic Context; topic-owned research commands do; run commands also validate Run consistency with the selected Research Task, Research Inquiry, Research Topic, and Topic Workspace.

## Status

accepted

## Considered Options

- Narrow v1 scope table.
- Broad rule where any command touching a Topic Workspace resolves Effective Topic Context.
- Minimal v1 where only context show/validate and path resolution use Effective Topic Context.

## Consequences

The scope table gives implementation and tests a concrete boundary without settling the future Execution Adapter command request. Workspace path commands are project-scoped when they list registered Topic Workspaces and topic-scoped when they resolve paths for one selected Topic Workspace.
