## 1. Documentation Structure

- [x] 1.1 Create `docs/tutorial/`, `docs/manual/`, and `docs/developer/` directories with index pages for each section.
- [x] 1.2 Examine every current top-level docs page and assign it to tutorial, manual, developer, or UI contract material before moving or rewriting.
- [x] 1.3 Rewrite current getting-started content into tutorial pages for quickstart, first Project, first Research Topic, Project Web GUI, and system-skill installation using task-first tutorial tone.
- [x] 1.4 Rewrite operator/reference content into manual pages for CLI reference, Project lifecycle, Research Topics, Topic Workspace, Workspace Runtime, research records, Project Web, Houmao adapter, and troubleshooting using precise lookup tone.
- [x] 1.5 Rewrite maintainer content into developer pages for architecture, storage, packaged system skills, UI contracts, release process, testing, and contributing docs using implementation and maintenance tone.
- [x] 1.6 Keep GUI contract documentation reachable from a stable UI Contracts navigation entry and update links to any moved developer context.

## 2. README and Package-facing Docs

- [x] 2.1 Rewrite `README.md` as a published-tool entrypoint with a short product explanation.
- [x] 2.2 Add public installation instructions using `uv tool install isomer-labs` and bare `isomer-cli` examples.
- [x] 2.3 Add quick commands for `project init`, `project topics create`, and `project web serve`.
- [x] 2.4 Add system-skill installation examples using verified direct skill-directory `npx skills add` URLs with `--agent` and `--yes`.
- [x] 2.5 Keep developer checkout setup in a separate README section that points to developer docs and uses Pixi.

## 3. MkDocs Navigation and Links

- [x] 3.1 Update `mkdocs.yml` navigation for Tutorials, Manual, Developer, and UI Contracts.
- [x] 3.2 Update all internal Markdown links after moving pages.
- [x] 3.3 Remove or replace stale flat-page links from README and docs index pages.
- [x] 3.4 Run link/path searches for old locations such as `docs/getting-started.md` and `docs/isomer-cli.md`.

## 4. Validation Updates

- [x] 4.1 Update `scripts/validate_docs.py` required page list to the new docs layout.
- [x] 4.2 Update README link validation targets to accept the new tutorial/manual/developer entry points.
- [x] 4.3 Update CLI coverage and CLI error example validation to read the moved manual CLI reference.
- [x] 4.4 Update semantic path and stale wording checks so they scan nested docs pages, not only flat `docs/*.md`.
- [x] 4.5 Update `tests/unit/test_validate_docs.py` for the new required paths and moved CLI reference.

## 5. Skill Installation Verification

- [x] 5.1 Test or dry-run `npx skills add` against local and GitHub skill-directory sources, and check whether repository-root `--skill` discovery can find packaged system skills.
- [x] 5.2 If current repository layout is not discoverable by `npx skills`, document the verified working command shape and record follow-up work for a compatible skills-facing layout.
- [x] 5.3 Ensure docs explain core skills, optional DeepSci skills, `isomer-op-entrypoint`, and `isomer-op-welcome`.

## 6. Verification

- [x] 6.1 Run `pixi run docs-validate`.
- [x] 6.2 Run `pixi run mkdocs build --strict`.
- [x] 6.3 Run `pixi run test`.
- [x] 6.4 Run `openspec validate reorganize-public-docs-for-pypi-release`.
