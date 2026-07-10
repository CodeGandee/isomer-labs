## 1. Update `SKILL.md` entrypoint

- [x] 1.1 Add the six new subcommands to the `## Subcommands` table in `imsight-llm-wiki/SKILL.md`.
- [x] 1.2 Update the `## Workflow` step that selects subcommands to mention the new options.
- [x] 1.3 Update `## When to Use` with new trigger scenarios for research, collect, inventory, and project.

## 2. Add `research` subcommand

- [x] 2.1 Create `imsight-llm-wiki/commands/research.md` with workflow, constraints, and quality gates.
- [x] 2.2 Document provider-agnostic search strategy: native web-search tool/skill first, CLI fallback (e.g., `tvly`), explicit failure if none available.
- [x] 2.3 Implement user confirmation before ingesting discovered sources.
- [x] 2.4 Wire discovered sources into the existing `ingest` pipeline.
- [x] 2.5 Append a `research` log entry after ingestion.

## 3. Add `collect` subcommand

- [x] 3.1 Create `imsight-llm-wiki/commands/collect.md` with workflow, constraints, and quality gates.
- [x] 3.2 Implement web-only artifact discovery and deduplication.
- [x] 3.3 Write collected artifacts to `wiki/collections/<slug>.md` with provenance.
- [x] 3.4 Update `wiki/index.md` to list the collection.
- [x] 3.5 Append a `collect` log entry.

## 4. Add `inventory` subcommand

- [x] 4.1 Create `imsight-llm-wiki/commands/inventory.md` with workflow, constraints, and quality gates.
- [x] 4.2 Implement `inventory add` to create `wiki/inventory/<slug>.md` candidate files.
- [x] 4.3 Implement `inventory list` to show open candidates.
- [x] 4.4 Implement `inventory ingest <slug>` to promote a candidate through the ingest pipeline.
- [x] 4.5 Implement `inventory reject <slug>` with reason capture.
- [x] 4.6 Append `inventory` log entries for promotions.

## 5. Add `project` subcommand

- [x] 5.1 Create `imsight-llm-wiki/commands/project.md` with workflow, constraints, and quality gates.
- [x] 5.2 Implement `project create <slug> "<goal>"` to create `outputs/projects/<slug>/WHY.md`.
- [x] 5.3 Implement `project add <slug> <file-or-query>` to copy or generate deliverables.
- [x] 5.4 Implement `project list` to enumerate projects.
- [x] 5.5 Implement `project archive <slug>` to move a project to `outputs/projects/.archive/`.
- [x] 5.6 Append `project` log entries.

## 6. Enhance `lint` with quality scans

- [x] 6.1 Update `imsight-llm-wiki/commands/lint.md` to describe quality scan behavior.
- [x] 6.2 Add opt-in stale-article detection with `--stale` / `--stale-days N`.
- [x] 6.3 Add overlong-page detection (>>1200 words).
- [x] 6.4 Add orphan-concept detection (no inbound wikilinks).
- [x] 6.5 Add frontmatter field validation.
- [x] 6.6 Write findings to `outputs/lint-report-<YYYY-MM-DD>.md`.
- [x] 6.7 Require user confirmation before applying quality fixes.

## 7. Enhance `query` with resume

- [x] 7.1 Update `imsight-llm-wiki/commands/query.md` to document `--resume` behavior.
- [x] 7.2 Implement `--resume` to load the most recent `outputs/queries/*.md` file.
- [x] 7.3 Include prior question summary in the follow-up answer.
- [x] 7.4 Save resumed query to a new `outputs/queries/<YYYY-MM-DD>-<follow-up-slug>.md`.
- [x] 7.5 Append a `query` log entry referencing the prior query slug.

## 8. Validation and polish

- [x] 8.1 Ensure `agents/openai.yaml` reflects the expanded subcommand surface.
- [x] 8.2 Run `pixi run lint` and fix any style issues in new or modified files.
- [x] 8.3 Verify every `commands/*.md` has a `## Workflow` section.
- [x] 8.4 Spot-check that new subcommands reference the correct scripts and output paths.
