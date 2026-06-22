## 1. Inventory and Structure

- [x] 1.1 Inventory current `README.md`, `docs/`, `ROADMAP.md`, accepted OpenSpec specs, CLI help, and tests for documentation source material.
- [x] 1.2 Define the final `docs/` information architecture with page ownership for index, getting started, concepts, system design, CLI reference, workflows, runtime files, Houmao adapter, assumptions, troubleshooting, and docs maintenance.
- [x] 1.3 Decide whether to add a MkDocs navigation file during implementation, defaulting to plain Markdown navigation if no repo-local convention already exists.
- [x] 1.4 Map canonical domain language terms from `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md` to the docs pages that must use them.

## 2. Core Documentation Rewrite

- [x] 2.1 Write `docs/index.md` as the documentation home and navigation map.
- [x] 2.2 Write `docs/getting-started.md` with the smallest useful Project setup, validation, runtime preparation, and Agent Team Instance record path.
- [x] 2.3 Write `docs/concepts.md` with a concise canonical concept guide and links to the full domain language source.
- [x] 2.4 Write `docs/system-design.md` covering Project discovery, Effective Topic Context, Workspace Path Resolution, Workspace Runtime, team template/profile/instance flow, Operator Agent role, Execution Adapter boundary, and roadmap boundaries.
- [x] 2.5 Write `docs/runtime-and-files.md` covering Project files, Topic Workspace files, Workspace Runtime records, path plans, Agent Workspaces, adapter material, manifests, payload refs, and durable-versus-cache classification.
- [x] 2.6 Write `docs/assumptions-and-roadmap.md` covering implementation assumptions, non-goals, advisory workspace boundaries, current milestone status, partial features, and future work.

## 3. CLI, Workflows, and Troubleshooting

- [x] 3.1 Capture the current `isomer-cli` command surface from Click help or the command registry for documentation coverage.
- [x] 3.2 Write `docs/isomer-cli.md` with every public command, purpose, prerequisites, side-effect boundary, common examples, and JSON/text output posture.
- [x] 3.3 Write `docs/workflows.md` for operator-oriented flows: read-only inspection, Project initialization, runtime preparation, Topic Agent Team Profile validation, Agent Team Instance creation, prepare-only Houmao materialization, quick launch, inspect-live, stop, reconcile, and adopt.
- [x] 3.4 Replace or fold `docs/houmao-cli-adapter.md` into `docs/houmao-adapter.md`, preserving quick launch, prepare-only/manual operation, manifest reconciliation, inspect-live, stop, and troubleshooting details.
- [x] 3.5 Write `docs/troubleshooting.md` with diagnostics and recovery paths for missing Project, Pixi/readiness failures, invalid topic bindings, Workspace Runtime schema issues, missing Agent Workspaces, invalid CLI JSON, manifest drift, partial launch, partial stop, and direct Houmao reconciliation.
- [x] 3.6 Write `docs/contributing-docs.md` describing documentation style, canonical language checks, CLI coverage checks, and how contributors should update docs with future CLI changes.

## 4. README and Validation Tooling

- [x] 4.1 Rewrite `README.md` as a concise project orientation with links to the comprehensive docs and a short command sampler.
- [x] 4.2 Add a repository-local docs validation script that checks required docs pages, README links, CLI command coverage in `docs/isomer-cli.md`, and selected forbidden stale terms.
- [x] 4.3 Add or update a Pixi task for docs validation without introducing a new external service.
- [x] 4.4 Add focused tests or script fixtures for the docs validation behavior.
- [x] 4.5 Update any docs references that still point to renamed or folded pages.

## 5. Verification

- [x] 5.1 Run the docs validation command and fix reported coverage, link, or language issues.
- [x] 5.2 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
- [x] 5.3 Run `openspec validate rewrite-docs-comprehensive-system-guide --strict`.
- [x] 5.4 Review the final docs against the proposal and spec scenarios to ensure implemented behavior is not overstated as future roadmap behavior.
