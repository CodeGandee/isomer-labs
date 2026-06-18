# Workspace Path Resolver Defines Ordinary Research Paths

Isomer Labs will resolve ordinary Project, Topic Workspace, Workspace Runtime, Run, Artifact, View Manifest, log, and Agent Workspace paths through a single Workspace Path Resolver. Topic selection happens before path resolution: `isomer-cli`, the Operator Agent, or an Execution Adapter supplies validated Effective Topic Context when a command is topic-scoped. The resolver uses recorded workspace plans first, then supported Execution Adapter `ISOMER_*` path environment variables, then Project Manifest defaults, then built-in defaults. It canonicalizes paths, rejects paths outside the Project root unless explicitly allowed, and records the effective path set and source in Workspace Runtime or Provenance Records before downstream research work depends on those paths.

## Status

accepted

## Considered Options

- Keep ordinary workspace and output locations as per-skill TBD placeholders.
- Let each Execution Adapter define its own path environment variables.
- Use one Workspace Path Resolver with a bounded, scope-explicit environment override set.

## Consequences

- Research skills request semantic Artifact kinds or workspace scopes instead of inventing paths.
- Execution Adapters can still override launch-time paths, but the process environment is not durable truth.
- Effective Topic Context supplies selected Project, Research Topic, Topic Workspace, Research Task, Run, Agent Team Instance, and Agent Instance refs without making the resolver perform independent Research Topic selection.
- Validation can audit path source, Project-boundary rules, missing files, and stale references consistently.
- API, schema, provider, command, scheduler, branching, baseline-waiver, cost, and privacy surfaces remain separate contracts. Branching is settled by Research Lifecycle State, while execution, provider, scheduler, Skill Binding projection, baseline-waiver, cost, and privacy extension refs are settled by Research Execution and Extension Contract; Workspace Path Resolver still owns only ordinary path resolution.
