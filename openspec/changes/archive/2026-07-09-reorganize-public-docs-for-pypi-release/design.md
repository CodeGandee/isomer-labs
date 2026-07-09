## Context

The repository currently has a flat `docs/` tree and a README that teaches `pixi install` plus `pixi run isomer-cli ...`. That is a developer checkout workflow, not the normal path for a PyPI user. The package now publishes `isomer-cli` to PyPI, Project Web docs to GitHub Pages, and official system skills as package assets mirrored through the repository `skillset/` authoring view.

The CLI has broad user-facing surfaces: Project lifecycle, Research Topics, Topic Workspace paths, Workspace Runtime, Team Profiles, Agent Team Instances, Houmao adapter commands, research record commands, and Project Web. The docs need to separate quick learning, reference usage, and contributor maintenance so new users are not asked to understand every internal concept before starting.

## Goals / Non-Goals

**Goals:**
- Make README a concise public entrypoint for installing and trying Isomer Labs from PyPI.
- Split docs into `tutorial/`, `manual/`, and `developer/` sections with stable MkDocs navigation.
- Examine every current docs page and rewrite it for its chosen section rather than mechanically moving text.
- Preserve CLI command reference completeness and side-effect clarity after moving pages.
- Add clear system-skill installation guidance using `npx skills add`.
- Keep Pixi setup visible for contributors and local development, but no longer as the primary user install path.
- Update documentation validation so moved pages remain enforced.

**Non-Goals:**
- Add a new public `isomer-cli system-skills export/install` command.
- Redesign Isomer domain language, CLI command shapes, Workspace Runtime, or Project Web behavior.
- Preserve every detail from the old docs verbatim. Rewrites should keep important contracts and command facts, but can remove repetition and adjust tone for the new audience.
- Guarantee that every agent host has identical skill-loading semantics beyond documenting `npx skills add` examples and verification guidance.

## Decisions

1. **Use audience-oriented docs sections.**

   `docs/tutorial/` should hold task-first walkthroughs, `docs/manual/` should hold operator/reference material, and `docs/developer/` should hold architecture, data contracts, release, and contribution material. This reduces the current flat list and makes the GitHub Pages landing page easier to scan.

   Alternative considered: keep the flat tree and only rewrite README. That would be faster, but it leaves users choosing from many similarly weighted pages.

2. **Rewrite pages for section tone, not just location.**

   Each old docs page should be read and classified before implementation. Tutorial pages should be friendly, sequential, and copy-paste oriented; manual pages should be precise, complete, and side-effect explicit; developer pages should explain design intent, invariants, validation, and maintenance boundaries.

   Alternative considered: move files first and fix tone later. That would satisfy the directory shape but leave a confusing public docs site.

3. **Make `uv` the primary public install path.**

   README and tutorial docs should recommend `uv tool install isomer-labs` because the published package exposes a CLI script and `uv tool` keeps command-line tools isolated from project dependencies.

   Alternative considered: recommend `pipx` or `pip install`. `pipx` is acceptable but less aligned with the user's request; `pip install` risks polluting project environments.

4. **Keep Pixi as the developer workflow.**

   Developer docs should keep `pixi install`, `pixi run lint`, `pixi run test`, `pixi run typecheck`, and docs validation commands. Public tutorials should show bare `isomer-cli` commands after installation.

   Alternative considered: keep `pixi run isomer-cli` everywhere. That accurately reflects this checkout but is wrong for published users.

5. **Document `npx skills add` as the system-skill installation path.**

   Add a tutorial/manual page that shows listing and installing skills through `npx skills add CodeGandee/isomer-labs`, including `--agent`, `--skill`, `--global`, and `--yes` examples. The page should identify core operator/service/misc skills and optional DeepSci extension skills.

   Alternative considered: document Python package-resource helpers. Those helpers are useful internally but are not a friendly public install story.

6. **Update validation paths instead of weakening validation.**

   `scripts/validate_docs.py` currently hardcodes pages like `docs/getting-started.md` and `docs/isomer-cli.md`. The implementation should update required pages and checks to the new canonical paths, while preserving CLI coverage, stale JSON example checks, semantic path checks, and forbidden-term checks.

   Alternative considered: temporarily remove strict docs validation. That would make the reorganization easier but would invite stale CLI examples and broken links.

## Risks / Trade-offs

- **Skill CLI detection mismatch**: `npx skills add` may not automatically detect Isomer's symlinked `skillset/` layout or nested package asset layout. Mitigation: implementation should test `npx skills add CodeGandee/isomer-labs --list` or a local equivalent and document only the command shapes that work, adding a compatible skills-facing layout only through a separate change if needed.
- **Broken relative links after moving docs**: Moving many Markdown files can break local and MkDocs links. Mitigation: run `mkdocs build --strict`, docs validation, and targeted `rg` checks for old paths.
- **Flat CLI reference is large**: Moving `isomer-cli.md` under `docs/manual/` may leave one long page. Mitigation: keep the move first, then split command groups in later changes if the page becomes hard to maintain.
- **Published 0.1.0 metadata remains sparse**: README and docs fixes improve future releases but do not change the existing PyPI description. Mitigation: pair implementation with a later patch release that adds `project.description`, `readme`, and URLs if desired.
