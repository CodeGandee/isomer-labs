# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Isomer Labs is a private, multi-agent research-conduction platform. The executable `src/isomer_labs/` package implements Project discovery, manifest validation, Effective Topic Context resolution, side-effect-free Workspace Path previews, and the first design-time Domain Agent Team Template / Topic Agent Team Profile commands for `deepsci-org`. Workspace Runtime, live Houmao launch, Operator control loop, and GUI surfaces are described in `ROADMAP.md` and OpenSpec contracts but are not fully built yet. `AGENTS.md` is the canonical contributor guide and overlaps this file; consult it for contribution conventions.

The canonical domain language (concept names, capitalization, what counts as a neutral Isomer term vs. a provider term like "Houmao") lives in `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md`. Match those terms exactly in schemas, CLI labels, error messages, and identifiers; do not introduce conflicting synonyms.

## Commands

All development runs through Pixi from the repo root:

```
pixi install
pixi run lint           # ruff check .
pixi run typecheck      # mypy src
pixi run test           # python -m unittest discover -s tests/unit
pixi run validate-research-skills   # scripts/validate_research_paradigm_skillset.py
```

These four tasks plus `validate-research-skills` are the standing quality gate (`ROADMAP.md` tracks keeping them green). Run lint + typecheck + test before requesting review.

Run a single test, module, or method:

```
pixi run python -m unittest tests.unit.test_isomer_cli
pixi run python -m unittest tests.unit.test_isomer_cli.IsomerCliTests.test_validate_json
```

Smoke-test the package: `pixi run python -c "import isomer_labs"`.

The CLI entrypoint is `isomer-cli` (registered via `[project.scripts]`). Examples:

```
pixi run isomer-cli init
pixi run isomer-cli validate --json
pixi run isomer-cli topics list
pixi run isomer-cli workspaces list
pixi run isomer-cli context show --topic default --json
pixi run isomer-cli paths preview --topic default
pixi run isomer-cli schemas list
pixi run isomer-cli team-templates list
pixi run isomer-cli team-templates validate deepsci-org
pixi run isomer-cli team-profiles specialize --topic default --profile-id default-deepsci --use-case UC-01 --json
pixi run isomer-cli team-profiles validate .isomer-labs/team-profiles/default-deepsci.toml
```

Target Python 3.11. Tests use `unittest` (not pytest). Ruff is the style authority; mypy is the type authority.

## Architecture

### The core CLI data flow

Every CLI command that is not `init` follows the same pipeline, and reading it top-to-bottom explains most of the package:

1. **Discovery** (`project.py:discover_project`) — locate the Project Manifest. Resolution order: `--manifest` selector → ancestor `.isomer-labs/manifest.toml` from cwd → `ISOMER_PROJECT_MANIFEST` env → `--project` selector. `discover_project` returns `(Project | None, list[Diagnostic])`.
2. **Parse + build state** (`manifest.py`, `topic_config.py`, `validation.py:build_project_state`) — parse the manifest, load each Research Topic Config, load `.isomer-labs/local.toml` if present, and produce a `ProjectState` carrying the `Project`, resolved `topic_configs`, optional `local_context`, and accumulated diagnostics.
3. **Resolve context** (`context.py:resolve_effective_topic_context`) — pick the Research Topic from an ordered set of candidates, then resolve the Topic Workspace, producing an `EffectiveTopicContext`.
4. **Optional path preview** (`paths.py:preview_paths`) — side-effect-free resolution of all workspace paths from context + env, returning `ResolvedPathEntry` records.
5. **Render** (`rendering.py`) — every command emits through `_emit`, which picks JSON (`render_json`, wrapped in `isomer-cli-output.v1`) or text. JSON always includes `output_schema_version`, `command`, payload, and `diagnostics`.

The CLI layer (`cli.py`) is thin Click glue: it builds a `CliOptions` dataclass from shared option decorators (`_common_options`, `_topic_selection_options`) and delegates to `_cmd_*` functions. Adding a command means a small Click function plus a `_cmd_*` that calls `_discover`/`_context_for_options` and `_emit`.

### Research Topic selection candidates

`context.py:_selection_candidates` evaluates candidates in a fixed precedence order and uses the first one with a non-null `research_topic_id`: explicit selectors (`--topic`, `--topic-workspace`, etc.) → current directory (matches cwd against a registered workspace path, deepest match wins) → `ISOMER_*` identity env vars → `.isomer-labs/local.toml` → Project Manifest default topic → single manifest registration. Lifecycle refs that Milestone 1 cannot validate (research inquiry/task/run/agent ids, which need the unbuilt Workspace Runtime) emit `ISO015` warnings rather than errors.

### The Diagnostic model is the contract

`diagnostics.py:Diagnostic` (code like `ISO001`, severity, neutral `concept`, message, optional path/field/line) is the unit every parse/resolve/validate step returns. Commands never raise on bad input — they accumulate diagnostics and return a non-zero exit code only when `has_errors(diagnostics)` is true. `concept` names must use the neutral Isomer domain term first and the concrete file/field/path second (a Milestone 1 exit criterion). JSON output serializes these verbatim, so diagnostic codes and concept strings are a stable external contract.

### Path resolution rules

`path_utils.py` provides canonicalization and the `is_within` containment check that all workspace paths must satisfy (a path escaping the Project root is `ISO005`). `paths.py` resolves each workspace surface from a precedence of env var (`ISOMER_TOPIC_WORKSPACE_*` / `ISOMER_AGENT_WORKSPACE_*`) → manifest `paths`/`path_defaults` keys → built-in defaults, always reporting the `source` per entry. The preview is read-only by design; nothing is created on disk.

### Configuration files

`isomer-cli init` (in `init_project.py`) writes the minimal valid Project: `.isomer-labs/manifest.toml`, `.isomer-labs/research-topics/default.toml`, and `topic-workspaces/default/`. It deliberately does not create `state.sqlite` or Workspace Runtime subdirectories — those are Milestone 2+. The local active context `.isomer-labs/local.toml` is a separate, untracked identity-ref file whose allowed fields are pinned in `topic_config.py:LOCAL_CONTEXT_ALLOWED_FIELDS`.

### Team template and profile surfaces

`team_templates.py` discovers the built-in `deepsci-org` Domain Agent Team Template from `teams/deepsci-org/execplan/`, parses its generated TOML/JSON contracts, validates role mappings, artifact paths, placeholders, and optional harness output, and exposes deterministic report records. `team_profiles.py` derives design-time Topic Agent Team Profile previews from Effective Topic Context, validates role bindings, fanout policy, reviewer access policy, topic isolation, and rejects runtime truth or secret-like fields. These commands are pure configuration and validation surfaces: they do not launch Houmao agents, create Agent Team Instances, write mailboxes, or create Workspace Runtime records.

### Schemas and validation philosophy

`builtins.py` enumerates the built-in schema/contract registry surfaced by `schemas list` (e.g. `isomer-project-manifest.v1`, `isomer-research-topic-config.v1`). `validation.py` enforces Milestone 1 invariants: secret-term and runtime-truth-key rejection in config (configs must be declarative, never carry live state or secrets), duplicate-id and cross-reference checks, and schema-version validation.

## Non-code assets that matter

- `openspec/` — OpenSpec specs and changes are the design authority. Active changes live in `openspec/changes/`; merged ones in `openspec/changes/archive/`. Specs cover things Milestone 1 deps on (cli-topic-context-resolution, workspace-path-resolution) and things not yet built (research-lifecycle-state, research-recording-contracts, research-execution-extension-contract). Use the openspec skills (`openspec-new-change`, `openspec-apply-change`, etc.) for spec-driven work; the roadmap says to promote OpenSpec contracts into tests before implementing each major API.
- `skillset/research-paradigm/` — the research-paradigm skill bundle; `validate-research-skills` is a release gate and the only test outside `tests/unit`.
- `teams/deepsci-org/execplan/` — the first seed Domain Agent Team Template, validated through `team-templates` and specialized into design-time Topic Agent Team Profiles through `team-profiles`.
- `extern/orphan/` — local-only checkouts (notably `DeepScientist`); never committed. Add vendored/committed deps under `extern/tracked/`.

## Conventions

- Conventional Commit subjects (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).
- When writing Markdown, do not hard-wrap prose; keep each paragraph or list item on one logical line.
- `ruff` excludes `teams/lfeng-team`.
- Keep Project-owned files first-class: Isomer manages Topic Workspaces and records rather than hiding all research work in a platform-owned directory.
