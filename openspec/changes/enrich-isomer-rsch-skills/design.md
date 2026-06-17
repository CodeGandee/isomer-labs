## Context

The research-paradigm skillset already has the `isomer-rsch-*` naming scheme, shared research vocabulary, and initial DeepScientist-to-Isomer concept mapping. The gap is depth: most stage skills still compress rich DeepScientist source behavior into short `Procedure` sections and point at source-analysis notes outside their own skill directories. `isomer-rsch-analysis` has been enriched into the desired pattern with a concise `SKILL.md`, local references, provenance, a local TBD registry copy, and an Imsight-style workflow entrypoint.

This change should make the rest of the skillset match that pattern while preserving Isomer boundaries: skills describe research judgment and durable outputs, not concrete runtime APIs, scheduler fields, command wrappers, storage layouts, or provider integrations.

## Goals / Non-Goals

**Goals:**

- Preserve as much reusable DeepScientist methodology as possible for each `isomer-rsch-*` skill: route taxonomies, gates, templates, examples, checklists, failure handling, and boundary cases.
- Keep every enriched skill self-contained by moving long detail into local one-level `references/` files and adding local provenance.
- Use accepted Isomer terms for outputs and decisions: Artifacts, Evidence Items, Findings, Research Claims, Decision Records, Gates, Workflow Stages, Capability Bindings, Execution Adapters, Provenance Records, and Operator Agent handoffs.
- Format every `SKILL.md` entrypoint with `$imsight-agent-skill-handling format-skill`: near-top `## Workflow`, numbered steps, concise reference routing, and a freeform fallback.
- Add or refresh `agents/openai.yaml` manifests for standalone bundles, with `interface.display_name` equal to the skill name.
- Use subagents during implementation with disjoint write scopes, then integrate and validate centrally.

**Non-Goals:**

- Do not introduce Isomer runtime APIs, scheduler policies, storage schemas, command wrappers, literature providers, or execution adapters.
- Do not port DeepScientist `artifact.*`, `memory.*`, `bash_exec(...)`, DeepXiv, `continuation_policy`, `auto_continue`, `workspace_mode`, or `wait_for_user_or_resume` as Isomer requirements.
- Do not import source-local demo paths, user paths, generated output paths, registry layouts, or paper layouts as concrete Isomer defaults.
- Do not migrate optional Nature-specific publication skills in this change.

## Decisions

### Treat `isomer-rsch-analysis` as the canonical target shape

Each enriched skill should use the analysis pattern: concise entrypoint, `## Reference Routing`, self-contained `references/`, local provenance, and validation against source-runtime leakage. This avoids another round of thin summaries and makes every skill usable without loading source analysis files.

Alternative considered: bulk-copy source `SKILL.md` files into target folders and edit terms afterward. This would preserve more raw text quickly, but it would also import DeepScientist runtime surfaces and make the Isomer contract harder to audit.

### Preserve rich detail through local references, not oversized entrypoints

Long playbooks, templates, examples, route taxonomies, and checklists should live under each skill's `references/` directory and be linked directly from `SKILL.md`. Entry points should teach routing and core judgment, not carry every template inline.

Alternative considered: put all migrated details into `SKILL.md` for each skill. This would make triggering expensive and would violate the progressive-disclosure direction already used by `isomer-rsch-analysis`.

### Use explicit concept translation and TBD placeholders

Workers should translate source concepts into Isomer terms or use `[[tbd-surface:<id>]]` for unsettled concrete surfaces. Missing placeholder ids, such as the current `schema-figure-output` usage, should be registered or replaced with existing ids.

Alternative considered: keep source terms in provenance notes and rely on readers to infer mappings. That leaves too much room for runtime coupling to leak into active skill behavior.

### Parallelize by disjoint skill clusters

Implementation should use workers with non-overlapping write scopes:

| Worker | Skill folders |
| --- | --- |
| Foundation | `isomer-rsch-intake`, `isomer-rsch-scout`, `isomer-rsch-decision`, `isomer-rsch-finalize` |
| Baseline | `isomer-rsch-baseline` |
| Idea and execution | `isomer-rsch-idea`, `isomer-rsch-optimize`, `isomer-rsch-experiment` |
| Writing and review | `isomer-rsch-write`, `isomer-rsch-review`, `isomer-rsch-rebuttal`, `isomer-rsch-paper-outline` |
| Figures and science | `isomer-rsch-paper-plot`, `isomer-rsch-figure-polish`, `isomer-rsch-science`, plus shared TBD registry updates if needed |

The main agent should own integration, validation, and any changes to shared docs or specs. This reduces conflicts while allowing the large source-import work to proceed in parallel.

### Split large generated resources when needed

`isomer-rsch-science` and `isomer-rsch-paper-plot` contain source resources that may be large or script-like. The core workflow and essential references should be migrated in this change. Large generated package-card catalogs, copied plotting scripts, or assets should be included only when sanitized and directly useful; otherwise they should be deferred into a follow-up task or clearly bounded subtask.

## Risks / Trade-offs

- Source-runtime leakage → Mitigate with search validation for DeepScientist-specific APIs, scheduler terms, concrete paths, and source tool names, allowing matches only in provenance or explicit mapping text.
- Overlarge skill bundles → Mitigate with one-level references and staged imports for large catalogs, scripts, and assets.
- Worker merge conflicts → Mitigate with disjoint folder ownership and central integration of shared files.
- Loss of source nuance during translation → Mitigate by comparing each target skill against both the source skill directory and the existing source-analysis note before marking it complete.
- Placeholder drift → Mitigate by validating every `[[tbd-surface:<id>]]` against the shared registry or a skill-local registry modeled after analysis.

## Migration Plan

1. Preserve the existing uncommitted `isomer-rsch-analysis/SKILL.md` formatting edit and do not overwrite it during worker tasks.
2. Launch subagents with explicit ownership of disjoint skill folders and instructions to avoid reverting other workers' edits.
3. For each skill, read the DeepScientist source `SKILL.md`, source references, source assets/scripts when present, the existing target skill, `isomer-rsch-analysis`, the shared registry, and the migration contract.
4. Rewrite each target entrypoint in the Imsight style, add local reference routing, migrate rich details into local references, and add or refresh `agents/openai.yaml`.
5. Integrate worker outputs, resolve shared TBD registry updates, and remove active external source-analysis dependencies from target skill docs.
6. Validate every skill with the skill validator, run coupling searches, run placeholder registry checks, and inspect diffs for copied runtime assumptions.

## Open Questions

- Should the large `science` package catalog be imported in this change or split into a follow-up resource-only change?
- Should `paper-plot` include sanitized scripts now, or should this change migrate only style references and leave executable templates for a later script-focused task?
- Should `schema-figure-output` become a registered shared TBD surface, or should `figure-polish` use existing `path-figure-output`, `api-artifact-record`, and evidence schema placeholders?
