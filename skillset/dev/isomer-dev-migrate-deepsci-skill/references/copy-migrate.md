# Copy Migrate

## Overview

Use `copy-migrate` to migrate one DeepScientist source skill into an Isomer Labs skill while keeping the migrated skill as close to the original as practical. Preserve the original document structure, section order, internal pages, assumptions, constraints, and workflow logic. Make targeted changes for Isomer Labs terms, storage placeholders, CLI names, harness calls, Pixi usage, and skill metadata.

Treat the upstream DeepScientist skill as the source of truth, keep the untouched source copy under `<target-skill-dir>/org/src/`, copy the source support files into the target runtime tree, translate user-facing terms into Isomer Labs language, replace DeepScientist MCP harness calls with `isomer-cli ext deepsci`, and defer concrete storage bindings through named placeholders.

## Workflow

When `copy-migrate` is invoked, execute the following steps in order.

1. **Resolve the source and target**. See **Source and Target**.
2. **Create the provenance workspace** under `<target-skill-dir>/org/`. See **Org Layout**.
3. **Copy the source skill files** into `<target-skill-dir>/org/src/` and copy runtime support files into `<target-skill-dir>/`. See **Source Copy Rules**.
4. **Analyze the source structure** at `<target-skill-dir>/org/analysis/analysis-of-<source-skill-name>.md`. See **Source Analysis**.
5. **Write the migration plan** at `<target-skill-dir>/migrate/migration-plan.md`. See **Migration Plan**.
6. **Create the placeholder registry** at `<target-skill-dir>/migrate/placeholders.md`. See **Placeholder Rules**.
7. **Adapt terms and implementation details** while preserving the original document structure. See **Term Mapping**, **Harness Replacement**, and **Placeholder Rules**.
8. **Format the migrated skill** and repair metadata without making it look more native than the source structure allows. See **Skill Format**.
9. **Validate and report** changed files, copied source files, term translations, harness replacements, placeholders, and unresolved issues. See **Validation**.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan using the constraints in this page, then execute the plan.

## Source and Target

Use `<repo>/...` for paths relative to the Isomer Labs repository root. Use `<source-skill-dir>/...` for paths relative to the selected upstream DeepScientist source skill directory. Use `<target-skill-dir>/...` for paths relative to the target skill directory being migrated.

- Default upstream source root: `<repo>/extern/orphan/DeepScientist/src/skills/`.
- Target root for research-paradigm migrations: `<repo>/skillset/research-paradigm/`.
- Canonical Isomer Labs domain language: `<repo>/.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md`.
- Existing migration guide, if present: `<repo>/skillset/research-paradigm/deepscientist-migration-guide.md`.
- Placeholder registry, if present: `<repo>/skillset/research-paradigm/deepsci/isomer-deepsci-shared/references/semantic-placeholders.md`.
- Source copy: `<target-skill-dir>/org/src/`.
- Runtime support copy: `<target-skill-dir>/...`, excluding the source entrypoint and `agents/openai.yaml`.
- Source analysis: `<target-skill-dir>/org/analysis/analysis-of-<source-skill-name>.md`.
- Org inventory: `<target-skill-dir>/org/README.md`.
- Migration support directory: `<target-skill-dir>/migrate/`.
- Migration plan: `<target-skill-dir>/migrate/migration-plan.md`.
- Placeholder registry: `<target-skill-dir>/migrate/placeholders.md`.

Do not use an existing Isomer `v1` or `v2` migrated skill as the source of truth unless the user explicitly asks for that. The upstream DeepScientist source skill owns the original logic.

## Org Layout

Create `<target-skill-dir>/org/` as the migration provenance area. It must contain:

- `<target-skill-dir>/org/src/...`: the untouched upstream source skill copied as-is.
- `<target-skill-dir>/org/analysis/analysis-of-<source-skill-name>.md`: analysis of the source entrypoint and workflow subpages.
- `<target-skill-dir>/org/README.md`: a short inventory explaining what is inside `org/`, what was analyzed, what was not analyzed, and why.

The source entrypoint remains available in `<target-skill-dir>/org/src/`.

## Source Copy Rules

Inspect the source and target before editing, and preserve unrelated user changes in the target. Inventory every file in `<source-skill-dir>/`, including the entrypoint, internal pages, references, scripts, templates, and assets.

Copy every source file into `<target-skill-dir>/org/src/` while preserving paths relative to `<source-skill-dir>/`. The original source entrypoint remains at `<target-skill-dir>/org/src/SKILL.md` or `<target-skill-dir>/org/src/skill.md`.

Also copy every source file from `<source-skill-dir>/` into `<target-skill-dir>/` with paths preserved, except:

- `SKILL.md` or `skill.md`, because the target entrypoint must keep the migrated skill name and metadata.
- `agents/openai.yaml`, because the target skill owns OpenAI-facing metadata and routing text.

The runtime copy is mutable migration material. Adapt those copied files in place for Isomer terms, placeholders, harness replacements, and target style. Do not omit source subpages, templates, references, scripts, assets, package cards, or other support files from the runtime copy merely because the target entrypoint can summarize them.

Use the files in `<target-skill-dir>/org/src/` as the source material for the migrated runtime files at `<target-skill-dir>/`. Keep all source files in `org/src/` even if some look verbose.

## Source Analysis

Create `<target-skill-dir>/org/analysis/analysis-of-<source-skill-name>.md` before adapting the migrated skill. For `copy-migrate`, this analysis can be concise, but it must cover the source entrypoint and every subpage that represents a workflow, mode, subcommand, primitive, routing rule, or executable procedure.

The analysis should record source document structure, section order, referenced internal pages, workflow gates, stop conditions, evidence handoffs, inputs, outputs, and implementation details that need substitution.

Create or update `<target-skill-dir>/org/README.md` after analysis. State what is inside `org/`, what source pages were analyzed, what source pages were not analyzed, and why.

## Migration Plan

Create `<target-skill-dir>/migrate/migration-plan.md` before adapting the migrated runtime files. The plan should explain how the migration will substitute DeepScientist terms, harness calls, storage assumptions, environment assumptions, artifact mentions, artifact handoffs, and source-skill routes that have no matching Isomer skill.

Include term substitutions, harness substitutions, storage and artifact substitutions, unmatched skill-route substitutions, environment substitutions, rewrite targets, placeholder registry requirements, and checks that the migrated skill still matches the source structure.

## Logic Preservation

Read `<target-skill-dir>/org/src/` and every source file referenced by the source entrypoint. Identify the source skill's purpose, activation conditions, internal workflow, decision gates, stop conditions, evidence checks, handoffs, output meanings, and harness calls before rewriting `<target-skill-dir>/SKILL.md`.

Preserve the original document structure as much as practical. Keep section order, internal headings, and reference placement close to the source. Add new sections only when Isomer-specific adaptation cannot fit cleanly into the original structure.

## Term Mapping

Use Isomer Labs domain terms in the migrated `<target-skill-dir>/SKILL.md`.

- Use `Project` for the user-owned repository or directory tree that contains Isomer-managed work.
- Use `Project Config Directory` for `<repo>/.isomer-labs/`; it stores configuration and discovery state, not runtime outputs.
- Use `Project Manifest` for `<repo>/.isomer-labs/manifest.toml`.
- Use `Research Topic Config` for the manifest-registered TOML file that configures one Research Topic.
- Use `Research Topic` for the research subject being pursued.
- Use `Research Inquiry` for a focused scientific question or direction inside a Research Topic.
- Use `Research Task` for a bounded unit of research work.
- Use `Topic Workspace` for the project-local directory owned by one Research Topic.
- Use `Topic Main Development Repository` for the main development repo where agents normally work.
- Use `Agent Workspace` for an agent-specific working area when the meaning is agent-local work.
- Use `Workspace Runtime` for durable runtime state under a Topic Workspace, such as `state.sqlite`, path plans, references, validation state, logs, and records.
- Use `Run` for one execution of a task or workflow.
- Use `Semantic Workspace Surface Label` for stable dotted labels such as `topic.repos.main`, `topic.runtime.db`, `topic.records.artifacts`, or `agent.workspace`.

Translate DeepScientist `quest`, `quest root`, and `quest workspace` according to context. They usually become `Research Topic`, `Topic Workspace`, `Run`, or `Workspace Runtime`, not one universal replacement.

## Harness Replacement

DeepScientist skills often call MCP-style tools such as `memory.*`, `artifact.*`, and `bash_exec.bash_exec`. Migrated Isomer skills should call the Isomer compatibility harness instead:

```bash
isomer-cli ext deepsci call <namespace.tool> --input-json '<json-object>'
```

Examples:

```bash
isomer-cli ext deepsci call memory.list_recent --input-json '{"scope":"topic","limit":10}'
isomer-cli ext deepsci call artifact.science --input-json '{"kind":"evidence","payload":{}}'
isomer-cli ext deepsci call bash_exec.bash_exec --input-json '{"cmd":"pixi run test","cwd":"<TOPIC_MAIN_DEVELOPMENT_REPOSITORY>"}'
```

Do not leave migrated instructions that tell the agent to call the DeepScientist MCP server directly. If the repository later adds a generic `isomer-cli ext harness` facade, prefer the concrete command that exists in the current codebase and mention the generic facade only when the target repo supports it.

## Placeholder Rules

Use placeholders for every artifact mentioned in the source skill until Isomer storage bindings are finalized. This includes handoff artifacts, output artifacts, input artifacts, evidence files, state files, reports, generated figures, datasets, scripts treated as research artifacts, and any source path whose meaning is artifact-like. A placeholder should name the semantic object, not a filesystem path.

Use placeholders for source-skill routes that have no matching skill in this project. If the source skill invokes, delegates to, routes to, or otherwise depends on another DeepScientist skill and there is no matching Isomer skill, replace that route with a semantic placeholder such as `<MISSING_REVIEW_SKILL_ROUTE>` or `<MISSING_BASELINE_SKILL_ROUTE>`.

- Use angle-bracket names such as `<SCOUT_CONTEXT_BRIEF>`, `<BASELINE_EVIDENCE_SUMMARY>`, `<SELECTED_RESEARCH_INQUIRY>`, `<EXPERIMENT_RUN_RECORD>`, or `<PAPER_OUTLINE_INPUT>`.
- Define each placeholder once in `<target-skill-dir>/migrate/placeholders.md`.
- For each artifact placeholder, record the source artifact text or path, placeholder name, meaning, producer skill or stage, consumer skill or stage, and whether it represents evidence, a decision, a handoff, a run record, a draft, runtime state, a dataset, code, a figure, or a report.
- For each missing skill-route placeholder, record the source route text, source skill name, expected behavior, nearest Isomer candidate if any, caller page, and status `missing-isomer-skill`.
- Add a reference to `<target-skill-dir>/migrate/placeholders.md` in every migrated skill page that mentions one or more placeholders. The reference can be a short sentence near the first placeholder use, such as `Placeholder definitions live in migrate/placeholders.md.`
- Keep concrete paths only inside `<target-skill-dir>/org/` provenance material, or when the user explicitly asks for a storage binding pass.

Use this shape for `<target-skill-dir>/migrate/placeholders.md`:

```markdown
# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| `<PLACEHOLDER_NAME>` | `<source artifact text or path>` | <Semantic meaning.> | <Skill or stage.> | <Skill or stage.> | <evidence, decision, handoff, run record, draft, runtime state, dataset, code, figure, or report> |
| `<MISSING_SKILL_ROUTE>` | `<source route text>` | <Expected routed behavior.> | <Caller page or skill.> | <Missing source skill and nearest Isomer candidate, if any.> | missing-isomer-skill |
```

## Skill Format

The target skill must include:

- `<target-skill-dir>/SKILL.md` with YAML frontmatter containing only `name` and `description`.
- A `description` that starts with practical trigger language such as `Use when...`.
- A concise overview that states the true purpose of the skill.
- The migrated workflow and checks from the source skill.
- References to copied internal files in the same proper places as the original source entrypoint.
- `<target-skill-dir>/agents/openai.yaml` with quoted `display_name`, `short_description`, and `default_prompt`.

The `default_prompt` in `<target-skill-dir>/agents/openai.yaml` must explicitly mention the migrated skill token, for example:

```yaml
default_prompt: "Use $isomer-deepsci-scout to scout the Research Topic."
```

## Validation

Before finishing, validate both provenance layout and migrated skill structure.

1. Confirm `<target-skill-dir>/org/src/`, `<target-skill-dir>/org/analysis/analysis-of-<source-skill-name>.md`, `<target-skill-dir>/org/README.md`, `<target-skill-dir>/migrate/migration-plan.md`, and `<target-skill-dir>/migrate/placeholders.md` exist.
2. Confirm every source file was copied under `<target-skill-dir>/org/src/` with paths preserved.
3. Confirm every source file except `SKILL.md` or `skill.md` and `agents/openai.yaml` was copied under `<target-skill-dir>/` with paths preserved.
4. Confirm the migrated runtime files at `<target-skill-dir>/` preserve the source document structure as closely as practical.
5. Confirm substitutions in the migration plan are reflected in migrated runtime files.
6. Confirm every source artifact mention outside `<target-skill-dir>/org/` has been replaced by a placeholder listed in `<target-skill-dir>/migrate/placeholders.md`.
7. Confirm every migrated skill page that uses placeholders references `<target-skill-dir>/migrate/placeholders.md`.
8. Confirm every source-skill route without a matching Isomer skill has been replaced by a missing skill-route placeholder listed in `<target-skill-dir>/migrate/placeholders.md`.
9. Run repository skillset validation, and optionally run an external skill-creator quick validator when available:

```bash
pixi run validate-skills
```

10. Inspect leftovers outside audit material:

```bash
rg -n "DeepScientist MCP|mcp__|quest|quest_root|venv|artifact\.|memory\.|bash_exec" <target-skill-dir>
```

Leftovers inside `<target-skill-dir>/org/` are expected because it contains source provenance and analysis. Leftovers in `<target-skill-dir>/SKILL.md` or migrated runtime support files need review. Keep source-specific names only when they describe historical source provenance or when no Isomer term exists yet.

## Common Mistakes

- Using an earlier migrated Isomer skill instead of the upstream DeepScientist source skill.
- Copying only files referenced by the entrypoint instead of every file in the source skill directory.
- Copying source files only into `org/src/` and forgetting the required runtime support copy under `<target-skill-dir>/`.
- Collapsing source subpages into a summary instead of copying and adapting them as runtime support files.
- Overwriting `<target-skill-dir>/SKILL.md` with the source entrypoint.
- Overwriting `<target-skill-dir>/agents/openai.yaml` with the source agent metadata.
- Editing files under `<target-skill-dir>/org/src/` so they no longer serve as an untouched source copy.
- Flattening the source workflow into vague advice and losing decision gates or stop conditions.
- Binding storage paths too early instead of using semantic placeholders.
- Creating placeholders in migrated pages without listing them in `<target-skill-dir>/migrate/placeholders.md`.
- Forgetting to reference `<target-skill-dir>/migrate/placeholders.md` from a migrated page that uses placeholders.
- Leaving a route to a missing source skill as if the matching Isomer skill already exists.
- Leaving direct DeepScientist MCP calls in migrated instructions.
- Replacing `venv` instructions with another virtualenv pattern instead of using Pixi.
