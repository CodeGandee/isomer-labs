## Context

`imsight-llm-wiki` is a project-local, Imsight-style skill migrated from `llm-wiki-all-in-one`. It operates on a single wiki root with five core operations: scaffold, compile, ingest, query, lint, and audit, plus viewer deployment. The skill is intentionally minimal and self-contained.

`nvk/llm-wiki` is a mature upstream knowledge-base platform with a hub-and-spoke topic model, ~20+ commands, session capture, feedback curation, and plugin packaging. The goal of this change is to cherry-pick the highest-value capabilities from `nvk/llm-wiki` while preserving the simplicity of `imsight-llm-wiki`.

## Goals / Non-Goals

**Goals:**

- Add proactive web research (`research`) to discover and ingest sources.
- Add bounded artifact cataloging (`collect`) for lists and collections.
- Add a lightweight ingest backlog (`inventory`) for "read later" candidates.
- Add grouped output folders (`project`) for multi-deliverable research.
- Extend `lint` with quality/staleness scans.
- Extend `query` with a resume mode for follow-up questions.
- Keep the single-wiki-root model and existing directory layout.
- Maintain Imsight skill style: concise `SKILL.md`, explicit subcommands, `commands/` detail pages.

**Non-Goals:**

- No hub-and-spoke multi-wiki architecture.
- No session capture or feedback curation pipeline.
- No plugin packaging for Claude/Codex marketplaces.
- No derived-index caching or dual-linking format changes.
- No dataset manifest layer or large-data registry.

## Decisions

### Use a provider-agnostic web search strategy

- **Rationale**: Hardcoding Tavily limits portability. The agent may already have a native web search tool, a relevant skill, or a known CLI provider available.
- **Resolution order**: (1) native agent web-search tool or skill (e.g., Tavily skills) when available; (2) known CLI providers such as `tvly`; (3) direct HTTP fetch for explicit URLs when no search provider is available.
- **Fallback**: If no provider is available, `research` and `collect` refuse with a clear message telling the user how to install or configure one.

### Implement new capabilities as subcommands, not modes

- **Rationale**: Imsight style favors explicit subcommands with detail pages. Each new capability gets its own `commands/<name>.md`.
- **Alternative**: Natural-language router inside `wiki` command (like `nvk/llm-wiki`). Rejected because it complicates trigger boundaries.

### Reuse existing `ingest` pipeline for `research` and `inventory`

- **Rationale**: Both produce the same artifacts (`raw/`, `wiki/summaries/`, `wiki/concepts/`, `wiki/index.md`). Reusing the ingest pipeline keeps behavior consistent.
- **Implication**: `research` and `inventory ingest` are thin wrappers around source discovery + existing ingest.

### Store inventory candidates under `wiki/inventory/`

- **Rationale**: Candidates are wiki-adjacent metadata; placing them under `wiki/` keeps them discoverable and lintable, while distinguishing them from immutable `raw/` sources.
- **Alternative**: `raw/inventory/`. Rejected because candidates are mutable backlog items, not immutable sources.

### Store project outputs under `outputs/projects/`

- **Rationale**: Consistent with existing `outputs/queries/` and mirrors `nvk/llm-wiki` project layout without adding new top-level directories.

### Collect is web-only external discovery

- **Rationale**: Matches the upstream `nvk/llm-wiki` `/wiki:collect` command, which uses web search to discover external artifacts and writes a catalog to `output/`.
- **Scope**: `collect` discovers memes, tools, projects, examples, people, media, and similar artifacts outside the wiki. It does not search the existing local wiki; for that, users use `query` or `--resume`.
- **Output**: `wiki/collections/<slug>.md` with a provenance-rich catalog.

### Quality lint has no default stale check

- **Rationale**: "Stale" is context-dependent. A fast-moving topic wiki and a slow reference wiki need different thresholds. Running stale detection by default would be noisy or silent for many wikis.
- **Behavior**: Overlength, orphan, and frontmatter checks run by default. Staleness checks run only when the user explicitly passes `--stale` or `--check-stale`, optionally with a threshold like `--stale-days 30`.
- **Default thresholds**: 1200 words for overlong pages remains the existing convention and stays as the default.

### Resume query loads only the most recent query output

- **Rationale**: Simple and stateless. No session database needed.
- **Limitation**: If the user wants to resume an older query, they must reference it explicitly (future enhancement).

## Risks / Trade-offs

- **[Risk]** Web search results vary in quality → **Mitigation**: require user confirmation before ingesting; allow `--auto` opt-in for trusted sources.
- **[Risk]** `collect` can generate large catalogs that bloat the wiki → **Mitigation**: require a bounded query and a maximum result count (default 20).
- **[Risk]** `inventory` can become a graveyard of unprocessed candidates → **Mitigation**: lint flags stale open candidates older than 30 days.
- **[Risk]** Quality lint slows down the lint pass → **Mitigation**: keep checks lightweight; word counts and frontmatter parsing are fast.
- **[Risk]** `project` deliverables duplicate content from `wiki/` or `outputs/queries/` → **Mitigation**: project folders contain copies or generated artifacts; originals stay in place.

## Migration Plan

- No migration needed. The change is purely additive.
- Existing wikis continue to work without `wiki/inventory/` or `outputs/projects/` directories; these are created lazily.

## Open Questions

- None resolved. All design decisions are captured above.
