# Contributing to Docs

This page describes how to maintain the Isomer Labs documentation set, the style expectations, the canonical language checks, and how to keep the CLI reference aligned with the installed command surface.

## Documentation Style

- Use the canonical Isomer domain language from `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md`.
- Use concrete terms rather than abstract category words.
- Prefer active voice when the actor is known.
- Keep paragraphs on one logical line; do not hard-wrap prose.
- Keep `README.md` concise and link to detailed docs rather than duplicating them.
- Keep Houmao-specific terms on the [Houmao Adapter](houmao-adapter.md) page unless accepted domain language promotes a term.

## Required Pages

The documentation set expects these entry pages:

- `docs/index.md`
- `docs/getting-started.md`
- `docs/concepts.md`
- `docs/system-design.md`
- `docs/isomer-cli.md`
- `docs/workflows.md`
- `docs/houmao-adapter.md`
- `docs/runtime-and-files.md`
- `docs/assumptions-and-roadmap.md`
- `docs/troubleshooting.md`
- `docs/contributing-docs.md`

If you add a page, update `docs/index.md` and any relevant navigation tables.

## CLI Coverage Checks

`docs/isomer-cli.md` should document every public `isomer-cli` command. The repository-local docs validation script compares the installed command surface against the CLI reference and reports missing commands.

When you add or rename a command:

1. Update `docs/isomer-cli.md` with purpose, prerequisites, side effects, examples, and JSON/text output posture.
2. Update the side-effect summary table if the new command mutates state.
3. Update `docs/workflows.md` if the command belongs to a documented operator path.
4. Run the docs validation command to confirm coverage.

## Canonical Language Checks

The docs validation script checks selected docs for known stale or forbidden project terms. Current checks include:

- `quest` and `quest workspace` — Isomer uses **Research Topic** and **Topic Workspace**.
- `research goal` as a separate level — Isomer uses **Research Topic** and **Measurable Objective**.
- `state of the art` and similar clichés.
- legacy workspace layout guidance such as `.isomer-agent/`, top-level `repos/topic-main/{shared,artifacts,tasks,runs,views,logs,tools}`, or `repos/topic-main/extern/` outside explicit breaking-layout diagnostics — Isomer uses `isomer-managed/`.

If the script reports a likely violation, review the context. The check does not replace human review; it only flags common mistakes.

## Running Docs Validation

```bash
pixi run docs-validate
```

The validation script checks:

- required docs pages exist;
- `README.md` links to the docs;
- `docs/isomer-cli.md` includes current public command names;
- selected docs do not introduce known stale terms.
- selected docs do not present legacy worker-facing workspace paths as current layout.

Fix reported issues before committing doc changes.

## README and Docs Cross-references

`README.md` should give a concise project orientation and link to:

- `docs/index.md` for the documentation home.
- `docs/getting-started.md` for the smallest useful path.
- `docs/isomer-cli.md` for the command reference.

When a docs page is renamed or folded into another page, update all internal links and the README pointers.

## Adding Tests for Docs Validation

If you extend the docs validation script, add focused unit tests in `tests/unit/test_validate_docs.py`. Test the behavior, not the full CLI surface, so tests remain fast and deterministic.
