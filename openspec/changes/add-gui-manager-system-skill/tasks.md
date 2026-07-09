## 1. Skill Asset Structure

- [x] 1.1 Create `src/isomer_labs/assets/system_skills/operator/isomer-op-gui-mgr/` with `SKILL.md`, `agents/openai.yaml`, and bounded reference pages.
- [x] 1.2 Define GUI Manager workflows for help, launch/status, backend API reference, record refresh/index maintenance, and troubleshooting.
- [x] 1.3 Add an Essential Output and Complete Output contract covering status, Project root, service URL or route family, cache mode, diagnostics, blockers, and next action.
- [x] 1.4 Add guardrails that keep GUI Backend lifecycle local, route non-GUI repairs to existing owner skills, and avoid claiming canonical research-state ownership.

## 2. Manifest and Routing

- [x] 2.1 Add `operator/isomer-op-gui-mgr` to `src/isomer_labs/assets/system_skills/manifest.toml` under `groups.core.skills`.
- [x] 2.2 Update `isomer-op-entrypoint` route references so GUI lifecycle, debug, refresh, and API-reference requests route to `isomer-op-gui-mgr`.
- [x] 2.3 Update `isomer-op-welcome` references `help`, `show-options`, `choose-path`, and `show-skill-map` so GUI Manager is visible from welcome menus and path selection.
- [x] 2.4 Ensure all new skill names match across folder name, `SKILL.md` frontmatter, `agents/openai.yaml` display name, and default prompt.

## 3. Backend API Reference Content

- [x] 3.1 Document `isomer-cli project web serve --root <project-root>` and the `--host`, `--port`, `--reload`, `--no-browser`, and `--cache-mode normal|debug` options in the skill references.
- [x] 3.2 Document Project Web route families for health, Project, topics, explorer/openable items, runtime, overview, actors, records, graphs, recent errors, events, record details, idea details, record viewer, rendered Markdown, lineage, siblings, files, facets, and index maintenance.
- [x] 3.3 Link detailed GUI payload expectations to `docs/ui/contracts/` instead of duplicating full response schemas.
- [x] 3.4 Distinguish read-only API routes from explicit mutation routes for index rebuild and cleanup.

## 4. Tests and Validation

- [x] 4.1 Add or update tests that packaged system-skill discovery lists `isomer-op-gui-mgr` in the core group.
- [x] 4.2 Add or update tests that core materialization or system-skills installation includes `operator/isomer-op-gui-mgr/SKILL.md` and its linked reference pages.
- [x] 4.3 Add or update validation coverage for GUI Manager skill structure, local references, naming consistency, and global `isomer-cli` command guidance.
- [x] 4.4 Add or update validation coverage that entrypoint and welcome routing references include `isomer-op-gui-mgr`.
- [x] 4.5 Run `openspec validate add-gui-manager-system-skill --strict`.
- [x] 4.6 Run targeted unit tests plus `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
