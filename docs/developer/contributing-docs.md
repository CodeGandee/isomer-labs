# Contributing to Docs

This developer guide describes how to maintain the Isomer Labs documentation set without drifting from the CLI, GUI data contracts, or canonical domain language.

## Audience Sections

Use the section that matches the reader:

- `docs/tutorial/` teaches an operator a concrete path with minimal theory.
- `docs/manual/` explains stable user-facing commands, concepts, files, and troubleshooting behavior.
- `docs/developer/` explains implementation details, validation, packaging, contracts, and release work.
- `docs/ui/contracts/` records GUI data contracts for backend and frontend maintainers.

Do not move a page without checking whether its tone still fits. A tutorial should read like a guided task, a manual page should read like a reference, and a developer page should name implementation responsibilities.

## Required Pages

The docs validation script requires the main entry pages:

- `docs/index.md`
- `docs/tutorial/index.md`
- `docs/tutorial/quickstart.md`
- `docs/tutorial/system-skills.md`
- `docs/manual/index.md`
- `docs/manual/concepts.md`
- `docs/manual/cli-reference.md`
- `docs/manual/project-lifecycle.md`
- `docs/manual/topic-workspaces.md`
- `docs/manual/workspace-runtime.md`
- `docs/manual/research-records.md`
- `docs/manual/project-web.md`
- `docs/manual/houmao-adapter.md`
- `docs/manual/troubleshooting.md`
- `docs/developer/index.md`
- `docs/developer/architecture.md`
- `docs/developer/packaged-system-skills.md`
- `docs/developer/contributing-docs.md`

If you add a page, update `docs/index.md`, `mkdocs.yml`, and any nearby overview page.

## CLI Coverage Checks

`docs/manual/cli-reference.md` should document every public `isomer-cli` command. The repository-local docs validation script compares the installed command surface against the CLI reference and reports missing commands.

When you add or rename a command:

1. Update `docs/manual/cli-reference.md` with purpose, prerequisites, side effects, examples, and JSON/text output posture.
2. Update the side-effect summary table if the new command mutates state.
3. Update `docs/manual/project-lifecycle.md` if the command belongs to a documented operator path.
4. Run the docs validation command to confirm coverage.

## Canonical Language Checks

Use the canonical Isomer domain language from `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md`. Keep Houmao-specific terms on [Houmao Adapter](../manual/houmao-adapter.md) unless accepted domain language promotes a term.

The docs validation script flags known stale terms, stale JSON flags, legacy workspace paths, and fixed-path-only wording. Review the context before changing prose; the check catches common mistakes but does not replace human review.

## Running Docs Validation

```bash
pixi run docs-validate
```

The validation script checks required pages, README links, CLI command coverage, CLI error examples, stale JSON flags, canonical language, legacy workspace paths, and semantic path documentation.

## README and Cross-refs

`README.md` should give a concise public orientation and link to:

- `docs/index.md` for the documentation home.
- `docs/tutorial/quickstart.md` for the smallest useful path.
- `docs/manual/cli-reference.md` for command details.
- `docs/developer/index.md` for maintainer guidance.

When a docs page is renamed or folded into another page, update internal links, MkDocs navigation, and validation constants in one change.
