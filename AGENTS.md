# Repository Guidelines

## Project Structure & Module Organization

This is a Pixi-managed Python project using a `src/` layout. Importable code lives in `src/isomer_labs/`. Unit tests belong in `tests/unit/`, integration tests in `tests/integration/`, and manual checks in `tests/manual/`. Keep documentation in `docs/`, project context and design notes in `context/`, helper scripts in `scripts/`, and project-specific agent skills in `skillset/`.

External code has two homes: use `extern/tracked/` for vendored or submodule-style dependencies that should be committed, and `extern/orphan/` for local-only checkouts. Do not commit generated Pixi environments, caches, or disposable work from `.pixi/`, `.mypy_cache/`, `.ruff_cache/`, or `tmp/`.

## Build, Test, and Development Commands

Use Pixi from the repository root:

- `pixi install`: resolve and install the default environment from `pyproject.toml` and `pixi.lock`.
- `pixi run lint`: run Ruff across the repository.
- `pixi run typecheck`: run MyPy against `src/`.
- `pixi run test`: discover and run unit tests under `tests/unit/`.
- `pixi run python -c "import isomer_labs"`: quick package import smoke test.

## Coding Style & Naming Conventions

Target Python 3.11. Use four-space indentation, type annotations for public functions, and clear module names in `snake_case`. Keep package code under the `isomer_labs` namespace. Prefer small modules with explicit imports over broad utility files.

Ruff is the linting authority for style issues. MyPy is the type-checking authority. Keep code compatible with editable installation through the existing Pixi PyPI dependency.

## Testing Guidelines

Use Python `unittest` unless the project explicitly adopts another framework. Name test files `test_<module>.py` and test classes or methods after the behavior being verified. Keep fast, deterministic tests in `tests/unit/`; place filesystem, service, or multi-component checks in `tests/integration/`. Manual tests should not be collected by the default `pixi run test` command.

## Commit & Pull Request Guidelines

Current history uses concise Conventional Commit-style subjects, for example `docs: sketch lab readme`. Continue that pattern with prefixes such as `feat:`, `fix:`, `docs:`, `test:`, and `chore:`.

Pull requests should describe the change, explain validation performed, and link related issues or notes when available. Include screenshots only for UI-visible changes. Before requesting review, run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.

## Agent-Specific Instructions

Make scoped edits that preserve the existing Pixi and `src/` layout. Prefer repository commands over ad hoc environment setup, and do not revert unrelated uncommitted changes.
