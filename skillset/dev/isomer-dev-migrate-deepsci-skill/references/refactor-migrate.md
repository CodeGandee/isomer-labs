# Refactor Migrate

## Overview

Use `refactor-migrate` to migrate one DeepScientist source skill into an Isomer Labs skill that looks native to the current project. Preserve the source skill's essential logic, constraints, assumptions, inputs, outputs, and workflow evidence, but rewrite the entrypoint and subpages according to the current Isomer skill contract and style.

This mode is analysis-first. It must create durable source provenance under `<target-skill-dir>/org/` before rewriting the target skill.

## Workflow

When `refactor-migrate` is invoked, execute the following steps in order.

1. **Resolve the source and target**. See **Source and Target**.
2. **Copy the source skill files** into `<target-skill-dir>/org/src/`. See **Source Copy Rules**.
3. **Deep-inspect the source skill** by invoking `$imsight-agent-skill-handling deep-inspect`. See **Source Analysis**.
4. **Write the migration plan** at `<target-skill-dir>/migrate/migration-plan.md`. See **Migration Plan**.
5. **Create the placeholder registry** at `<target-skill-dir>/migrate/placeholders.md`. See **Placeholder Rules**.
6. **Rewrite the target skill and subpages** according to `$imsight-agent-skill-handling create`, the source analysis, the migration plan, and the placeholder registry. See **Native Rewrite**.
7. **Validate semantic match and skill format**. See **Validation**.
8. **Report** changed files, analysis artifacts, migration-plan choices, copied files, rewritten pages, validation results, and unresolved issues.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan using the constraints in this page, then execute the plan.

## Source and Target

Use `<repo>/...` for paths relative to the Isomer Labs repository root. Use `<source-skill-dir>/...` for paths relative to the selected upstream DeepScientist source skill directory. Use `<target-skill-dir>/...` for paths relative to the migrated target skill directory.

- Default upstream source root: `<repo>/extern/orphan/DeepScientist/src/skills/`.
- Target root for research-paradigm migrations: `<repo>/skillset/research-paradigm/`.
- Canonical Isomer Labs domain language: `<repo>/.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md`.
- Analysis directory: `<target-skill-dir>/org/`.
- Source copy: `<target-skill-dir>/org/src/`.
- Deep inspection output: `<target-skill-dir>/org/analysis/analysis-of-<source-skill-name>.md`.
- Analysis README: `<target-skill-dir>/org/README.md`.
- Migration support directory: `<target-skill-dir>/migrate/`.
- Migration plan: `<target-skill-dir>/migrate/migration-plan.md`.
- Placeholder registry: `<target-skill-dir>/migrate/placeholders.md`.

Do not use an existing Isomer `v1` or `v2` migrated skill as the source of truth unless the user explicitly asks for that. The upstream DeepScientist source skill owns the original logic.

## Org Layout

Create `<target-skill-dir>/org/` as the migration provenance area. It must contain:

- `<target-skill-dir>/org/src/...`: the untouched upstream source skill copied as-is.
- `<target-skill-dir>/org/analysis/analysis-of-<source-skill-name>.md`: deep inspection of the source entrypoint and workflow subpages.
- `<target-skill-dir>/org/README.md`: a short inventory explaining what is inside `org/`, what was analyzed, what was not analyzed, and why.

The source entrypoint remains available in `<target-skill-dir>/org/src/`.

## Source Copy Rules

Inspect the source and target before editing, and preserve unrelated user changes in the target. Inventory every file in `<source-skill-dir>/`, including the entrypoint, internal pages, references, scripts, templates, and assets.

Copy every source file into `<target-skill-dir>/org/src/` while preserving paths relative to `<source-skill-dir>/`. The original source entrypoint remains at `<target-skill-dir>/org/src/SKILL.md` or `<target-skill-dir>/org/src/skill.md`.

Keep the copied source files available as source material until the rewrite has been validated against `<target-skill-dir>/org/analysis/analysis-of-<source-skill-name>.md`.

## Source Analysis

Invoke `$imsight-agent-skill-handling deep-inspect` on the upstream source skill before planning or rewriting. Pass an explicit output path so the analysis lands at `<target-skill-dir>/org/analysis/analysis-of-<source-skill-name>.md`.

The deep inspection must cover:

- `<source-skill-dir>/SKILL.md` or `<source-skill-dir>/skill.md`.
- Every directly linked page that defines a public subcommand, mode, workflow, primitive, routing behavior, or executable procedure.
- Any additional source page that represents a workflow even if it is not linked cleanly from the entrypoint.

Create `<target-skill-dir>/org/README.md` after the inspection. State what is inside `org/`, what was analyzed, what was not analyzed, and why. Use this README to record exclusions such as passive examples, static assets, generated files, copied templates, or files that do not affect runtime behavior.

## Migration Plan

Create `<target-skill-dir>/migrate/migration-plan.md` before copying and rewriting. The plan should explain how the migration will substitute DeepScientist terms, harness calls, storage assumptions, environment assumptions, artifact mentions, artifact handoffs, and source-skill routes that have no matching Isomer skill.

Include these sections:

- **Scope**: source skill, target skill, and whether any source files were excluded from deep inspection.
- **Term Substitutions**: DeepScientist terms mapped to Isomer Labs terms.
- **Harness Substitutions**: DeepScientist MCP or harness calls mapped to `isomer-cli ext deepsci` commands.
- **Storage and Artifact Substitutions**: concrete source paths or artifacts mapped to semantic placeholders.
- **Unmatched Skill-Route Substitutions**: source skill calls, routes, or delegations with no matching Isomer skill mapped to semantic placeholders.
- **Environment Substitutions**: source environment assumptions, including `venv`, mapped to Isomer Labs conventions such as Pixi.
- **Placeholder Registry**: required entries for `<target-skill-dir>/migrate/placeholders.md` and the migrated pages that must reference it.
- **Rewrite Targets**: target `SKILL.md` and subpages that must be rewritten.
- **Semantic Match Checks**: the logic, constraints, assumptions, inputs, and outputs that the rewritten skill must preserve.

## Placeholder Rules

Use placeholders for every artifact mentioned in the source skill until Isomer storage bindings are finalized. This includes handoff artifacts, output artifacts, input artifacts, evidence files, state files, reports, generated figures, datasets, scripts treated as research artifacts, and any source path whose meaning is artifact-like. A placeholder should name the semantic object, not a filesystem path.

Use placeholders for source-skill routes that have no matching skill in this project. If the source skill invokes, delegates to, routes to, or otherwise depends on another DeepScientist skill and there is no matching Isomer skill, replace that route with a semantic placeholder such as `<MISSING_REVIEW_SKILL_ROUTE>` or `<MISSING_BASELINE_SKILL_ROUTE>`.

- Use angle-bracket names such as `<SCOUT_CONTEXT_BRIEF>`, `<BASELINE_EVIDENCE_SUMMARY>`, `<SELECTED_RESEARCH_INQUIRY>`, `<EXPERIMENT_RUN_RECORD>`, or `<PAPER_OUTLINE_INPUT>`.
- Define each placeholder once in `<target-skill-dir>/migrate/placeholders.md`.
- For each artifact placeholder, record the source artifact text or path, placeholder name, meaning, producer skill or stage, consumer skill or stage, and whether it represents evidence, a decision, a handoff, a run record, a draft, runtime state, a dataset, code, a figure, or a report.
- For each missing skill-route placeholder, record the source route text, source skill name, expected behavior, nearest Isomer candidate if any, caller page, and status `missing-isomer-skill`.
- Add a reference to `<target-skill-dir>/migrate/placeholders.md` in every rewritten skill page that mentions one or more placeholders. The reference can be a short sentence near the first placeholder use, such as `Placeholder definitions live in migrate/placeholders.md.`
- Keep concrete paths only inside `<target-skill-dir>/org/` provenance material, or when the user explicitly asks for a storage binding pass.

Use this shape for `<target-skill-dir>/migrate/placeholders.md`:

```markdown
# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| `<PLACEHOLDER_NAME>` | `<source artifact text or path>` | <Semantic meaning.> | <Skill or stage.> | <Skill or stage.> | <evidence, decision, handoff, run record, draft, runtime state, dataset, code, figure, or report> |
| `<MISSING_SKILL_ROUTE>` | `<source route text>` | <Expected routed behavior.> | <Caller page or skill.> | <Missing source skill and nearest Isomer candidate, if any.> | missing-isomer-skill |
```

## Native Rewrite

Rewrite `<target-skill-dir>/SKILL.md` and every target subpage that represents executable skill behavior. Use `$imsight-agent-skill-handling create` as the style and contract reference for the target skill, not as permission to ignore the source analysis.

The rewritten skill must:

- Match the source process described in `<target-skill-dir>/org/analysis/analysis-of-<source-skill-name>.md`.
- Apply substitutions from `<target-skill-dir>/migrate/migration-plan.md`.
- Replace source artifact mentions with placeholders defined in `<target-skill-dir>/migrate/placeholders.md`.
- Replace source-skill routes without matching Isomer skills with missing skill-route placeholders defined in `<target-skill-dir>/migrate/placeholders.md`.
- Preserve essential source logic, constraints, assumptions, inputs, outputs, gates, evidence handoffs, and stop conditions.
- Fit the current project's skill style, including concise frontmatter, `## Overview`, `## Workflow`, subcommand structure when needed, and `## Common Mistakes`.
- Rewrite subpages so they are native Isomer workflow pages rather than lightly edited DeepScientist pages.
- Keep `<target-skill-dir>/org/src/` as the untouched audit copy of the original source skill.

## Validation

Before finishing, validate both structure and semantic preservation.

1. Confirm `<target-skill-dir>/org/src/`, `<target-skill-dir>/org/analysis/analysis-of-<source-skill-name>.md`, `<target-skill-dir>/org/README.md`, `<target-skill-dir>/migrate/migration-plan.md`, and `<target-skill-dir>/migrate/placeholders.md` exist.
2. Confirm every source file was copied under `<target-skill-dir>/org/src/` with paths preserved.
3. Confirm the rewritten `SKILL.md` and rewritten workflow subpages match the source process analysis, not merely the source wording.
4. Confirm substitutions in the migration plan are reflected in rewritten pages.
5. Confirm every source artifact mention outside `<target-skill-dir>/org/` has been replaced by a placeholder listed in `<target-skill-dir>/migrate/placeholders.md`.
6. Confirm every rewritten skill page that uses placeholders references `<target-skill-dir>/migrate/placeholders.md`.
7. Confirm every source-skill route without a matching Isomer skill has been replaced by a missing skill-route placeholder listed in `<target-skill-dir>/migrate/placeholders.md`.
8. Run the skill validator when available:

```bash
python /home/huangzhe/.codex/skills/.system/skill-creator/scripts/quick_validate.py <target-skill-dir>
```

9. Inspect leftovers outside audit material:

```bash
rg -n "DeepScientist MCP|mcp__|quest|quest_root|venv|artifact\.|memory\.|bash_exec" <target-skill-dir>
```

Leftovers inside `<target-skill-dir>/org/` are expected when they document the source. Leftovers in rewritten runtime instructions need review.

## Common Mistakes

- Rewriting from intuition instead of from the deep-inspection output.
- Treating `refactor-migrate` as a cosmetic cleanup of `copy-migrate`.
- Skipping `<target-skill-dir>/org/README.md`, which records analysis coverage.
- Creating `<target-skill-dir>/migrate/migration-plan.md` after the rewrite instead of before it.
- Creating placeholders in rewritten pages without listing them in `<target-skill-dir>/migrate/placeholders.md`.
- Forgetting to reference `<target-skill-dir>/migrate/placeholders.md` from a rewritten page that uses placeholders.
- Leaving a route to a missing source skill as if the matching Isomer skill already exists.
- Preserving native-looking prose while losing source gates, evidence handoffs, assumptions, inputs, or outputs.
- Editing files under `<target-skill-dir>/org/src/` so they no longer serve as an untouched source copy.
