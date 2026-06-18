# V1 CLI Command Scope

The accepted first-version design uses a narrow command-scope table for `isomer-cli`.

## Accepted Choice

Option A: Project validation and discovery commands stay project-scoped. Effective Topic Context, Research Inquiry, Research Task, Artifact, Gate, Topic Agent Team Profile, Agent Team Instance topic-participation, topic-scoped view, and topic-specific path preview commands are topic-scoped. Run inspect, resume, cancel, record, and export commands are run-scoped.

## Rationale

This makes Effective Topic Context resolution testable without designing the full Execution Adapter command request. It also avoids a vague workspace-scoped bucket: listing registered Topic Workspaces is project-scoped, while resolving paths for one selected Topic Workspace is topic-scoped.

## Consequences

- Project-level discovery can work without an active Research Topic.
- Topic-scoped commands must resolve and validate Effective Topic Context before they inspect or mutate topic-owned records.
- Run-scoped commands must validate that the selected Run belongs to the selected Research Task, Research Inquiry, Research Topic, and Topic Workspace.
- Concrete shell, package manager, HPC, notebook, agent launch, and service request execution remains out of scope for this change.

## Rejected Alternatives

- Treat anything touching a Topic Workspace as topic-scoped. This is simple but over-scopes listing and inspection commands.
- Limit v1 to only `context show/validate` and path resolution. This is small but leaves Research Task, Artifact, and Run behavior ambiguous.
