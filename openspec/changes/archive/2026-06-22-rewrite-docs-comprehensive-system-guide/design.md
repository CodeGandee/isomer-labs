## Context

The repository currently has a detailed `README.md`, a new Houmao adapter page in `docs/`, and many accepted OpenSpec contracts, but it does not have a coherent documentation set that helps a user or contributor understand the whole system. The current reader has to infer the platform model from `README.md`, `ROADMAP.md`, `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md`, CLI help, tests, and scattered OpenSpec specs.

The docs rewrite should make `docs/` the long-form home for Isomer Labs. It should explain the Project and Topic Workspace model, the Workspace Runtime substrate, the `isomer-cli` command surface, current Houmao-backed Agent Team Instance launch paths, assumptions, side-effect boundaries, intended usage, troubleshooting, and roadmap status. The canonical domain language remains `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md`; documentation should use those terms and avoid promoting Houmao-specific terms into core Isomer language.

The current `docs/` tree is small enough to rewrite directly. `README.md` should become a concise orientation page that links to the detailed documentation rather than duplicating the entire command reference. Documentation checks can be lightweight and repository-local: command help snapshots, required-page checks, link checks, and content checks against known command names are enough for this change.

## Goals / Non-Goals

**Goals:**
- Make `docs/` a complete user and contributor documentation set for the current Isomer Labs system.
- Document the intended operator path from Project initialization through runtime preparation, Agent Team Instance creation, Houmao prepare-only materialization, quick launch, inspect-live, stop, reconciliation, and adoption.
- Document `isomer-cli` commands with side-effect boundaries, required context, typical examples, JSON output posture, and troubleshooting notes.
- Document the system design: Project discovery, Effective Topic Context, Workspace Path Resolution, Workspace Runtime, team template/profile/instance flow, Houmao Execution Adapter, manifest reconciliation, runtime validation, and roadmap boundaries.
- Keep documentation aligned with the canonical domain language and current CLI help.
- Keep `README.md` concise and make it point to the comprehensive docs.

**Non-Goals:**
- Do not change runtime CLI behavior, Workspace Runtime schema behavior, or Houmao adapter behavior as part of the documentation rewrite.
- Do not document future roadmap features as implemented behavior.
- Do not turn Houmao specialists, project profiles, launch dossiers, mailboxes, gateways, or managed-agent ids into core Isomer concepts.
- Do not require a new documentation hosting service or external publication pipeline.
- Do not make generated API reference the only source of documentation; explanatory guides remain hand-authored.

## Decisions

### Use a layered documentation information architecture

`docs/` should be organized around reader intent rather than source-code layout:

- `docs/index.md`: start page and navigation map.
- `docs/getting-started.md`: smallest useful Project and CLI path.
- `docs/concepts.md`: canonical concept summary, with pointers to the full domain language source.
- `docs/system-design.md`: architecture, boundaries, state ownership, and data flow.
- `docs/isomer-cli.md`: complete CLI reference and side-effect matrix.
- `docs/workflows.md`: task-oriented operating guides.
- `docs/houmao-adapter.md`: Houmao adapter launch paths, manifests, reconciliation, inspect-live, and stop.
- `docs/runtime-and-files.md`: Project files, Topic Workspace files, Workspace Runtime records, generated material, and durable versus cache state.
- `docs/assumptions-and-roadmap.md`: assumptions, limitations, current milestone status, and future features.
- `docs/troubleshooting.md`: common diagnostics and recovery paths.
- `docs/contributing-docs.md`: documentation maintenance and verification.

Alternative considered: keep all documentation in `README.md`. That would keep discovery simple, but it makes the README too large and hides important design details from readers looking for a specific workflow.

### Treat the CLI reference as checked documentation

The `isomer-cli` command reference should be hand-authored for clarity but checked against Click help or an equivalent command registry snapshot. At minimum, the verification should fail when a documented command disappears or when a public command is missing from the reference.

Alternative considered: fully generate the command reference from Click help. That would stay mechanically current, but raw help output does not explain side effects, prerequisites, runtime records, or safe usage.

### Keep examples realistic but non-mutating by default

Documentation examples should prefer read-only commands or dry-run style steps until the guide explicitly enters mutation sections. Commands that mutate Project files, Workspace Runtime records, Houmao managed agents, or adapter manifests should say so before the example.

Alternative considered: present a single long happy-path script. That is useful for smoke testing, but it does not teach users where boundaries and recovery points are.

### Use canonical Isomer language first

Docs should use Project, Project Manifest, Research Topic, Topic Workspace, Workspace Runtime, Domain Agent Team Template, Topic Agent Team Profile, Agent Team Instance, Agent Instance, Agent Workspace, Execution Adapter, Operator Agent, Research Task, Run, Artifact, Gate, Decision Record, and Provenance Record consistently. Houmao terms belong in the Houmao adapter page and should be described as adapter implementation details.

Alternative considered: describe the system through Houmao operations because Houmao is the current backend. That would be familiar for Houmao operators, but it would obscure Isomer's provider-neutral model and make later adapters harder to explain.

### Add lightweight documentation verification

Implementation should add a small repository-local check, for example `scripts/validate_docs.py` and a Pixi task, that verifies required docs pages exist, `README.md` links to the docs, public CLI commands are represented in `docs/isomer-cli.md`, and forbidden stale terms are not introduced in key docs.

Alternative considered: rely on manual review. Manual review remains valuable, but a lightweight check prevents docs from drifting as the CLI grows.

## Risks / Trade-offs

- [Risk] The docs may overstate current implementation maturity. -> Mitigation: require an assumptions and roadmap page that separates implemented behavior from planned behavior.
- [Risk] Command documentation can drift from Click help. -> Mitigation: add a check that compares documented commands against the current command surface.
- [Risk] The comprehensive docs can become too long for new users. -> Mitigation: make `docs/index.md` and `docs/getting-started.md` short, then link to deeper pages.
- [Risk] Houmao details can leak into core Isomer language. -> Mitigation: keep a dedicated Houmao adapter page and check important docs against canonical terminology.
- [Risk] Documentation verification can become brittle. -> Mitigation: check only stable page existence, command coverage, links, and forbidden stale terms, not prose formatting.

## Migration Plan

1. Inventory current `README.md`, `docs/houmao-cli-adapter.md`, `ROADMAP.md`, accepted OpenSpec specs, and CLI help to produce the new documentation outline.
2. Rewrite `docs/` around the layered information architecture.
3. Update `README.md` so it introduces the project briefly and links to `docs/index.md`, `docs/getting-started.md`, and `docs/isomer-cli.md`.
4. Add a lightweight documentation validation script and Pixi task.
5. Run docs validation, `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
6. Rollback, if needed, by restoring the previous docs pages and README pointers; no runtime migration is required.

## Open Questions

- None for the first implementation. Use plain Markdown navigation with stable relative links; add MkDocs navigation only if the existing dependency and repo conventions make it low-cost during implementation. Keep `README.md` concise with a short command sampler and links to the full docs.
