## Why

The current `imsight-llm-wiki` skill is a faithful but minimal port of the Karpathy-style LLM wiki pattern. It supports scaffold, ingest, compile, query, lint, audit, and viewer deploy, but it is entirely passive: it waits for the user to supply sources and questions. After comparing it with `nvk/llm-wiki`, we see opportunities to add proactive research, lightweight backlog management, and quality-aware maintenance without turning the skill into a full hub-and-spoke platform.

## What Changes

Add six capabilities to `imsight-llm-wiki`:

1. **`research` subcommand** — search the web for a topic, evaluate results, and ingest high-signal sources through the normal `ingest` pipeline.
2. **`collect` subcommand** — find, dedupe, and catalog many small artifacts (tools, examples, memes, papers) into a single `wiki/collections/<slug>.md` page.
3. **`inventory` subcommand** — maintain a lightweight backlog of ingest candidates under `wiki/inventory/` with add/list/ingest workflows.
4. **`project` subcommand** — group related outputs into `outputs/projects/<slug>/` with a `WHY.md` and deliverables.
5. **Enhanced `lint` with quality scans** — add staleness, overlength, orphan, and frontmatter checks on top of the existing link/index health checks.
6. **Enhanced `query` with resume** — allow `query --resume` to continue from the most recent query output.

No existing behavior is removed. The single-wiki-root model is preserved. The bundled web viewer is unchanged.

## Capabilities

### New Capabilities

- `imsight-llm-wiki-research`: Web research and bulk ingestion of discovered sources.
- `imsight-llm-wiki-collect`: Catalog generation for bounded artifact collections.
- `imsight-llm-wiki-inventory`: Candidate backlog for future ingestion.
- `imsight-llm-wiki-project-outputs`: Grouped deliverable folders for research outputs.
- `imsight-llm-wiki-quality-lint`: Quality and staleness checks beyond link/index health.
- `imsight-llm-wiki-resume-query`: Follow-up query mode that loads prior query context.

### Modified Capabilities

- None. Existing `lint` and `query` subcommands gain new options, but no existing spec-level requirements change because the skill has no prior OpenSpec coverage.

## Impact

- Affected skill: `extern/orphan/houmao-agents/skillset/imsight-skills/imsight-llm-wiki`.
- New files: `commands/research.md`, `commands/collect.md`, `commands/inventory.md`, `commands/project.md`, updated `commands/lint.md`, updated `commands/query.md`, updated `SKILL.md` subcommand table, possibly new helper scripts.
- Dependencies: web search provider (prefer Tavily, already available in user skills) or shell fallback to `curl`/`tvly`.
- No breaking changes to existing wiki directory layout or file formats.
