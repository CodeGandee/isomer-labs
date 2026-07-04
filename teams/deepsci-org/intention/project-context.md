# Project Context: deepsci-org

## Detected Project

- Project root: `/data/huangzhe/code/isomer-labs`.
- Repository identity: `isomer-labs`, with `origin` at `https://github.com/CodeGandee/isomer-labs`.
- Project summary: Isomer Labs is a private lab for an interactive, semi-automatic research-conduction platform powered by multi-agent research teams.
- This loop directory: `teams/deepsci-org`, interpreted as the loop root because the user selected `teams/deepsci-org/intention`.
- This intention source belongs to a domain-level `deepsci-org` Domain Agent Team Template, not a concrete Research Topic, Topic Agent Team Profile, Agent Team Instance, Run, or Topic Workspace.

## Tools And Commands

- Python project: Pixi-managed Python 3.11 project with a `src/` layout and importable package under `src/isomer_labs/`.
- Package tooling: `pyproject.toml`, Hatchling build backend, editable Pixi PyPI dependency `isomer_labs = { path = ".", editable = true }`.
- Install command: `pixi install`.
- Lint command: `pixi run lint`, which runs Ruff across the repository.
- Typecheck command: `pixi run typecheck`, which runs MyPy against `src`.
- Unit test command: `pixi run test`, which discovers tests under `tests/unit`.
- Import smoke command: `pixi run python -c "import isomer_labs"`.
- Research skill validation command: `pixi run validate-research-skills`.

## Project Layout

- `src/isomer_labs/`: importable Python package surface.
- `tests/unit/`, `tests/integration/`, `tests/manual/`: unit, integration, and manual checks.
- `context/`: design notes, plans, and exploratory analysis.
- `.imsight-arts/project-explore/`: project-explore ADRs, domain concepts, use cases, and accepted design material.
- `skillset/research-paradigm/`: Isomer-native research skills named `isomer-deepsci-*`.
- `teams/`: domain-level team definition packages, including `teams/deepsci-org` and `teams/deepsci-lite`.
- `extern/orphan/DeepScientist`: local-only DeepScientist reference checkout; do not assume it is committed.

## Contracts And Surfaces

- Canonical domain language: `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md`.
- Workspace design: `context/design/rough-architecture.md`, especially Project Config Directory, Project Manifest, Research Topic Config, Topic Workspace, Workspace Runtime, Agent Workspace, Domain Agent Team Template, Topic Agent Team Profile, and Agent Team Instance boundaries.
- Research execution examples: `context/design/research-execution-extension-examples.md`, which shows topic-level refs for Research Topic Configs, Topic Agent Team Profiles, Capability Bindings, Skill Binding projections, Gate policies, Scheduler policies, provider bindings, and Execution Adapter Command Requests.
- Research method skills: `skillset/research-paradigm/README.md` and the `isomer-deepsci-*` skill folders.
- DeepScientist migration context: `context/explore/deepscientist-skill-analysis/` plus local source under `extern/orphan/DeepScientist`.
- Writing constraints: keep Markdown prose on logical lines, preserve Isomer domain terms, and avoid hard-wrapping prose unless syntax or readability requires it.

## deepsci-org Template Context

- `teams/deepsci-org/source/team-design.md` is the design source for the full DeepScientist-inspired research organization.
- `teams/deepsci-org/intention/` is editable Houmao pro intention source.
- Future `teams/deepsci-org/execplan/` material would be generated operational material, not the editable source of truth.
- Runtime topic state belongs under a Project Manifest-declared `{topic_workspace_ref}` and its Workspace Runtime, not under `teams/deepsci-org/`.
- Topic-level instantiation should replace placeholders such as `{research_topic_id}`, `{topic_agent_team_profile_id}`, `{agent_team_instance_id}`, `{topic_workspace_ref}`, `{capability_binding_ref}`, `{skill_binding_projection_ref}`, `{scheduler_policy_ref}`, and `{gate_policy_ref}`.

## Domain Notes

- Isomer research flow is user-steered: the user defines the Research Topic, supplies context, chooses constraints, approves Gates, and can redirect or pause work.
- The Operator Agent is the project-facing controller and user interaction point. It can specialize a Domain Agent Team Template into a Topic Agent Team Profile and launch an Agent Team Instance, but it is not a member role inside the `deepsci-org` team template.
- Inside the launched team, `deepsci-org-master` is the internal root role that owns routing, Decisions, Gates, handoffs, and closure.
- Topic Workspaces are declared by the Project Manifest. They own Workspace Runtime, Research Inquiries, Research Tasks, Runs, rich Artifacts, View Manifests, Agent Workspaces, and logs.
- Agent Workspace boundaries are advisory ownership and peer-read contracts. Durable dependencies should be promoted into Artifacts, Evidence Items, Findings, Research Claims, Decision Records, Gates, or Provenance Records.
- Provider-specific commands, credentials, live process ids, mailbox routes, gateway routes, scheduler internals, and raw provider payloads must stay outside generic template and intention source.

## Open Questions

- UNRESOLVED - The exact schema and registration format for Domain Agent Team Template, Topic Agent Team Profile, and Agent Team Instance files remains design-stage material.
- UNRESOLVED - This package is authoring material under `teams/deepsci-org`; a future Project Manifest registration path for this template has not been chosen.
- UNRESOLVED - The future Houmao `execplan/` generation target and whether it should stay purely adapter-local or map into Isomer manifest refs has not been decided.
