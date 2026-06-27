# Isomer Labs Documentation

Isomer Labs is a private research platform that uses multi-agent teams as a research engine while a human operator sets goals and steers work at critical steps. This documentation explains the platform model, how to operate it safely, and where the current implementation ends and future work begins.

The canonical Isomer domain language lives in `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md`. These docs use that language consistently and keep Houmao-specific terms on the [Houmao adapter](houmao-adapter.md) page.

## Where to Start

- [Getting Started](getting-started.md) — initialize a Project, validate it, prepare a Topic Workspace, and create an Agent Team Instance record.
- [Concepts](concepts.md) — a concise guide to Project, Topic Workspace, Workspace Runtime, Agent Team Instance, and other canonical terms.
- [Topic Workspace Definition](topic-workspace-definition.md) — the standard Topic Workspace and Agent Workspace directory structure.
- [System Design](system-design.md) — how Project discovery, Effective Topic Context, Workspace Path Resolution, Workspace Runtime, and team execution fit together.

## Operating Isomer

- [isomer-cli Reference](isomer-cli.md) — every public command, its prerequisites, side effects, JSON/text output posture, and common examples.
- [Workflows](workflows.md) — operator-oriented paths from inspection through quick launch, stop, reconciliation, and adoption.
- [Houmao Adapter](houmao-adapter.md) — quick launch, prepare-only materialization, manifest reconciliation, inspect-live, stop, and direct Houmao operation.
- [Troubleshooting](troubleshooting.md) — diagnostics and recovery for missing Projects, readiness failures, manifest drift, partial launch or stop, and direct Houmao reconciliation.

## Files, Assumptions, and Maintenance

- [Runtime and Files](runtime-and-files.md) — Project files, Workspace Runtime records, adapter manifests, payload refs, and durable-versus-cache classification.
- [Assumptions and Roadmap](assumptions-and-roadmap.md) — current assumptions, non-goals, advisory workspace boundaries, milestone status, and planned features.
- [Contributing to Docs](contributing-docs.md) — style expectations, canonical language checks, CLI coverage checks, and how to keep docs current.

## Documentation Navigation

These pages are plain Markdown files in `docs/`. Relative links connect them; no external documentation hosting service is required. If the repository later adopts a static-site generator, the same files can serve as source material.

| Page | Purpose | Primary concepts |
|---|---|---|
| `index.md` | Home and navigation map | documentation set |
| `getting-started.md` | Smallest useful operator path | Project, Research Topic, Topic Workspace, Agent Team Instance |
| `concepts.md` | Canonical concept summary | domain language, execution layers, state ownership |
| `topic-workspace-definition.md` | Topic and agent workspace structure standard | Topic Workspace, Agent Workspace, Agent Name, Topic Main Repository |
| `system-design.md` | Architecture and boundaries | discovery, context, path resolution, runtime, adapter boundary |
| `isomer-cli.md` | Command reference | commands, side effects, JSON output, examples |
| `workflows.md` | Task-oriented operating guides | inspection, init, prepare, launch, stop, reconcile, adopt |
| `houmao-adapter.md` | Adapter-specific behavior | manifests, quick launch, prepare-only, inspect-live, stop |
| `runtime-and-files.md` | Runtime files and durability | Project files, runtime records, manifests, payload refs |
| `assumptions-and-roadmap.md` | Assumptions and non-goals | boundaries, security, roadmap status |
| `troubleshooting.md` | Diagnostics and recovery | common failures, repair paths |
| `contributing-docs.md` | Documentation maintenance | style, validation, CLI coverage |
