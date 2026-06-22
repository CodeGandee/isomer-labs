# Project Context: deepsci-mini

## Detected Project

- Project root: `/data/huangzhe/code/isomer-labs`.
- Repository identity: `isomer-labs`.
- Project summary: Isomer Labs is an interactive, semi-automatic research-conduction platform powered by multi-agent research teams.
- This loop directory: `teams/deepsci-mini`, interpreted as a reusable Domain Agent Team Template authoring package.
- This intention source belongs to a domain-level `deepsci-mini` Domain Agent Team Template, not a concrete Research Topic, Topic Agent Team Profile, Agent Team Instance, Run, or Topic Workspace.

## Tools And Commands

- Python project: Pixi-managed Python 3.11 project with a `src/` layout and importable package under `src/isomer_labs/`.
- Install command: `pixi install`.
- Lint command: `pixi run lint`.
- Typecheck command: `pixi run typecheck`.
- Unit test command: `pixi run test`.
- Import smoke command: `pixi run python -c "import isomer_labs"`.
- Research skill validation command: `pixi run validate-research-skills`.

## Contracts And Surfaces

- Canonical domain language: `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md`.
- UC-01 source: `.imsight-arts/project-explore/use-cases/uc-01-explore-new-research-direction.md`.
- Active Milestone 6 change: `openspec/changes/implement-milestone-6-uc01-headless-vertical-slice/`.
- Full team template reference: `teams/deepsci-org/`.
- Existing condensed intention-only reference: `teams/deepsci-lite/`.
- Houmao adapter docs: `docs/houmao-adapter.md`.
- Runtime docs: `docs/runtime-and-files.md`.

## Domain Notes

- Isomer domain terms distinguish Domain Agent Team Template, Topic Agent Team Profile, and Agent Team Instance.
- `deepsci-mini` is a reusable Domain Agent Team Template; it should not store runtime research records, concrete topic paths, credentials, mailbox routes, gateway routes, live process ids, or provider payloads.
- The Project-facing Operator Agent chooses, specializes, launches, and records team work; inside this template, `deepsci-mini-lead` is the internal root role.
- UC-01 needs source gathering, literature notes, Evidence Item candidates, claim/factor synthesis, skeptical review notes, follow-up Research Inquiry options, View Manifests, a Gate, and a Decision Record.
- Houmao can be the Execution Adapter, but generic research records must use Isomer domain terms.

## Open Questions

- UNRESOLVED - The exact Project Manifest registration format for `deepsci-mini` is still governed by the Milestone 6 implementation.
- UNRESOLVED - Live Houmao launch remains gated by local Houmao readiness; deterministic adapter simulation should be the default validation path.
