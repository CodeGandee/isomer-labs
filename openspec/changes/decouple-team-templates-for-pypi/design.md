## Context

`src/isomer_labs/teams/templates.py` used to derive the repository root from `Path(__file__).resolve().parents[2]` and register `teams/deepsci-org/execplan` and `teams/deepsci-mini/execplan` as built-in Domain Agent Team Templates. That works in an editable checkout, but it is the wrong boundary for a PyPI package: installed source code should not require repository-local `teams/`, `skillset/`, `tests/`, `openspec/`, or other development-tree material.

The desired product shape is that Isomer core is the reusable platform package and Agent Team definitions are plugins. A future Team Repository can contain many team templates with a manifest, and `isomer-cli` can list, select, register, and specialize those teams without bundling the team source into `src/`.

## Goals / Non-Goals

**Goals:**

- Remove implicit core built-ins for `deepsci-org` and `deepsci-mini`.
- Add a Team Repository manifest contract that lists Domain Agent Team Template ids and paths.
- Let `isomer-cli` discover configured Team Repositories and list their available templates.
- Let users register or select a Team Repository template for a Project before specialization.
- Keep Domain Agent Team Template validation, Project-local template registration, and Topic Team Specialization logic in Isomer core.
- Add architecture and package checks that prove `src/` can run without repository-local template directories.
- Separate PyPI runtime dependencies from development, documentation, and test dependencies.

**Non-Goals:**

- Do not implement remote registry hosting or package-manager installation for Team Repositories in this first change.
- Do not copy all existing `teams/` material into `src/`.
- Do not remove the repository-local `teams/` tree; it can become fixture or seed Team Repository material.
- Do not change the Topic Agent Team Profile schema beyond what is needed to resolve a template source from Project or Team Repository context.
- Do not make Isomer core depend on a specific DeepSci Team Repository being present.

## Decisions

1. Team definitions are external content, not package assets.

   Isomer core should ship validation and specialization code, while `deepsci-org`, `deepsci-mini`, and future team definitions live in Team Repositories. The alternative was to move `teams/` under `src/isomer_labs/assets`, but that would make the PyPI package carry one opinionated team catalog and keep template content coupled to core releases.

2. Team Repository manifests are local filesystem manifests first.

   The first implementation should support one or more local Team Repository roots with an `isomer-team-repo.toml` manifest. Remote URLs, version resolution, signed catalogs, and marketplace behavior can layer on later. This keeps the refactor small enough to unblock PyPI packaging while preserving the future plugin direction.

3. Project-local template registration remains valid.

   Projects can still declare `[[domain_agent_team_templates]]` with project-scoped source paths. Team Repository templates add another source kind rather than replacing project-local templates. Non-built-in paths outside the Project root remain invalid unless they resolve through an explicitly configured Team Repository.

4. The CLI should make the missing-catalog state explicit.

   After removing built-ins, `isomer-cli project team-templates list` may return only Project-local templates. It should explain configured Team Repository sources, missing catalog configuration, or no available templates rather than silently pretending DeepSci templates are built in.

5. Source architecture tests become a packaging gate.

   Tests should reject repo-root derivation and repo-only path tokens in `src/` except for user-facing path examples that describe Project content, such as `repos/extern`. They should also prove a wheel-style import and basic CLI path works without relying on checkout-only team directories.

6. Dependency cleanup is part of the same PyPI readiness pass.

   Runtime metadata should include only packages imported by `src/` at runtime. Development tools such as Ruff, MyPy, and MkDocs Material belong in Pixi or optional dependency groups, not in the default PyPI install requirement set.

## Risks / Trade-offs

- Existing workflows may assume `deepsci-mini` is always available. Mitigation: update tests and docs to configure a fixture or seed Team Repository explicitly.
- Template source paths can point outside the Project root through Team Repositories. Mitigation: allow this only for configured Team Repository roots and report source metadata in CLI output.
- Removing built-ins is a breaking behavior change for default template listing. Mitigation: document migration and add CLI diagnostics that guide users to add or select a Team Repository.
- Package-resource and filesystem-template paths have different behavior. Mitigation: keep Team Repositories filesystem-backed in this change and leave zip/resource abstractions out of scope.
- Dependency cleanup can reveal hidden test-only imports. Mitigation: run import, unit, lint, typecheck, and build/smoke checks before archiving.
