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

When generating Markdown, do not hard-wrap prose lines; keep each paragraph or list item on one logical line unless Markdown syntax or readability requires a deliberate line break.

<!-- BEGIN agent-style v0.3.5 -->
<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Adapter: AGENTS.md cross-agent standard -->
<!-- Target path: <repo root>/AGENTS.md -->
<!-- Load class: single-file; install_mode: append-block -->

# agent-style v0.3.5 — AGENTS.md adapter

agent-style is a literature-backed English technical-prose writing ruleset for AI agents. This adapter is the compact rule payload that AGENTS.md-aware tools (Codex, Jules, Zed, Warp, Gemini CLI, VS Code, Aider via `.aider.conf.yml`, and others) load at session start.

## Self-Verification Handshake

When asked "is agent-style active?" or "what writing rules apply here?", answer: `agent-style v0.3.5 active: 21 rules (RULE-01..12 canonical + RULE-A..I field-observed); full bodies at .agent-style/RULES.md.`

## Load Statement

This adapter is loaded as the root `AGENTS.md` file at the repository root. AGENTS.md-aware tools do not auto-import a second file; the compact directives below are what reach context. Full rule bodies at `.agent-style/RULES.md` are a human-readable reference but are not auto-loaded by AGENTS.md consumers.

## The 21 Rules (Compact Directives)

Canonical rules (from Strunk & White 1959, Orwell 1946, Pinker 2014, Gopen & Swan 1990):

- **RULE-01 Curse of knowledge**: Name your intended reader; do not assume they share your tacit knowledge.
- **RULE-02 Passive voice**: Prefer active voice when the agent is known and worth naming.
- **RULE-03 Concrete language**: Prefer concrete, specific terms over abstract category words like "factors" or "aspects".
- **RULE-04 Needless words**: Cut filler phrases like "in order to", "due to the fact that", "may potentially".
- **RULE-05 Dying metaphors**: Delete clichés like "pushes the boundaries", "paradigm shift", or "state of the art".
- **RULE-06 Plain English**: Prefer "use" over "leverage", "method" over "methodology", "feature" over "functionality".
- **RULE-07 Affirmative form**: Prefer "trivial" to "not important", "forgot" to "did not remember".
- **RULE-08 Claim calibration**: Calibrate verbs to evidence; do not write "proves" when the evidence is "suggests".
- **RULE-09 Parallel structure**: Express coordinate ideas in the same grammatical form.
- **RULE-10 Related words together**: Keep subject close to verb and modifier close to modified; split long parentheticals.
- **RULE-11 Stress position**: Place new or important information at the end of the sentence.
- **RULE-12 Long sentences**: Split sentences over 30 words; vary length across a paragraph.

Field-observed rules (maintainer observation of LLM output, 2022-2026):

- **RULE-A Bullet overuse**: Keep prose in paragraphs when ideas connect; bullets only for genuine lists; avoid forced 3-item triads.
- **RULE-B Dash overuse**: Do not use em or en dashes as casual sentence punctuation; prefer commas, semicolons, colons, parentheses.
- **RULE-C Same-starts**: Do not open two or more consecutive sentences with the same word.
- **RULE-D Transitions**: Do not open sentences with "Additionally", "Furthermore", "Moreover", "In addition".
- **RULE-E Summary closers**: Do not end every paragraph with a sentence that restates its point.
- **RULE-F Term consistency**: Once you define a term or abbreviation, keep using it; do not alternate synonyms.
- **RULE-G Title case**: Use title case for section and subsection headings; articles and short prepositions stay lowercase.
- **RULE-H Citation discipline (critical)**: Support factual claims with verifiable citation or concrete evidence; never fabricate citations.
- **RULE-I Contractions**: Prefer "it is" / "does not" / "cannot" over "it's" / "doesn't" / "can't" in formal technical prose.

## Escape Hatch

*"Break any of these rules sooner than say anything outright barbarous."* — George Orwell, "Politics and the English Language" (1946), Rule 6. Rules are guides to clarity, not ends in themselves.

## Full Rule Bodies (Canonical)

Full directive text, BAD/GOOD example pairs, and rationale per rule: see `.agent-style/RULES.md` in this project, or https://raw.githubusercontent.com/yzhao062/agent-style/v0.3.5/RULES.md for the pinned canonical source.
<!-- END agent-style -->
