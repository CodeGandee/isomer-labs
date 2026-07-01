# Refactor Migrate

## Overview

Use `refactor-migrate` to migrate one DeepScientist source skill into an Isomer Labs skill that looks native to the current project. Preserve the source skill's essential logic, constraints, assumptions, inputs, outputs, and workflow evidence, but rewrite the entrypoint and subpages according to the current Isomer skill contract and style.

This mode is analysis-first. It must create durable source provenance under `<target-skill-dir>/org/` before rewriting the target skill.

## Workflow

When `refactor-migrate` is invoked, execute the following steps in order.

1. **Resolve the source and target**. See **Source and Target**.
2. **Copy the source skill files** into `<target-skill-dir>/org/src/` and copy runtime support files into `<target-skill-dir>/`. See **Source Copy Rules**.
3. **Deep-inspect the source skill** by invoking `$imsight-agent-skill-handling deep-inspect`. See **Source Analysis**.
4. **Write the migration plan** at `<target-skill-dir>/migrate/migration-plan.md`. See **Migration Plan**.
5. **Create the placeholder registry** at `<target-skill-dir>/migrate/placeholders.md`. See **Placeholder Rules**.
6. **Rewrite the target skill and subpages** according to `$imsight-agent-skill-handling create`, the source analysis, the migration plan, and the placeholder registry. See **Native Rewrite** and **Main Workflow Support Extraction**.
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
- Runtime support copy: `<target-skill-dir>/...`, excluding the source entrypoint and `agents/openai.yaml`.
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

Also copy every source file from `<source-skill-dir>/` into `<target-skill-dir>/` with paths preserved, except:

- `SKILL.md` or `skill.md`, because the target entrypoint must keep the migrated skill name and metadata.
- `agents/openai.yaml`, because the target skill owns OpenAI-facing metadata and routing text.

The runtime copy is mutable migration material. Refactor those copied files in place into native Isomer workflow pages, templates, scripts, assets, package cards, or references as appropriate. Do not omit source subpages, templates, references, scripts, assets, package cards, or other support files from the runtime copy merely because the target entrypoint can summarize them.

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
- **Rewrite Targets**: target `SKILL.md` plus every copied runtime source file outside `<target-skill-dir>/org/` that must be refactored, with explicit notes for any copied file that is intentionally left as an asset, data file, package card, or passive template.
- **Main Workflow Support Mapping**: for each target main workflow step, list the source entrypoint sections and source reference pages that provide preferences, constraints, guidance, quality gates, common mistakes, stop conditions, or output requirements for that step.
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

Rewrite `<target-skill-dir>/SKILL.md` and every copied runtime subpage that represents executable skill behavior. Use `$imsight-agent-skill-handling create` as the style and contract reference for the target skill, not as permission to ignore the source analysis.

Refactor mode may change wording, headings, and Isomer-facing organization, but it must not drop source support pages from the runtime tree. Keep copied passive templates, package cards, assets, data files, and examples available at their preserved paths unless a later user request explicitly asks to prune them. If a copied runtime file is not rewritten, record why in the migration plan or report.

The rewritten skill must:

- Match the source process described in `<target-skill-dir>/org/analysis/analysis-of-<source-skill-name>.md`.
- Apply substitutions from `<target-skill-dir>/migrate/migration-plan.md`.
- Replace source artifact mentions with placeholders defined in `<target-skill-dir>/migrate/placeholders.md`.
- Replace source-skill routes without matching Isomer skills with missing skill-route placeholders defined in `<target-skill-dir>/migrate/placeholders.md`.
- Preserve essential source logic, constraints, assumptions, inputs, outputs, gates, evidence handoffs, and stop conditions.
- Fit the current project's skill style, including concise frontmatter, `## Overview`, `## Workflow`, subcommand structure when needed, and `## Common Mistakes`.
- Rewrite subpages so they are native Isomer workflow pages rather than lightly edited DeepScientist pages.
- Reference the relevant support section or support page from every main workflow step so the running agent knows what to read before executing that step.
- Keep `<target-skill-dir>/org/src/` as the untouched audit copy of the original source skill.

## Main Workflow Support Extraction

After the first native rewrite from analyzed source logic, reread `<target-skill-dir>/org/src/SKILL.md` or `<target-skill-dir>/org/src/skill.md` directly. Do not rely only on the deep-inspection summary. Extract the source skill's preferences, constraints, guidance, quality gates, common mistakes, stop conditions, artifact rules, memory rules, and output requirements, even when those rules are not explicitly linked from the source control workflow.

For each step in the target skill's main `## Workflow`:

1. Identify the source sections and source reference pages that constrain or guide that step. Include top-level source sections such as protocols, mandates, non-negotiable rules, failure handling, quality rules, memory rules, artifact rules, and interaction rules when they affect the step.
2. Create or update a corresponding refactored support section or runtime support page under `<target-skill-dir>/`. Use native Isomer wording, but preserve the operative rule, gate, preference, or stop condition.
3. Put step-specific material near the step's support page or under the standard support blocks in **Step Support Templates**. Put rules that apply across all steps in a clearly named global support section such as `## Global Constraints` or `## Cross-Step Quality Gates`, using the same block shapes.
4. Reference the support section or support page from the matching main workflow step. A step should not depend on hidden source knowledge that is absent from the target runtime tree.
5. Record in `<target-skill-dir>/migrate/migration-plan.md` how source support sections map to target workflow steps, including any source rule intentionally left as a global rule instead of a step-specific rule.

Do not drop a source rule merely because it appears outside the source's numbered workflow, because it is duplicated in a later section, or because the target main workflow has fewer steps than the source. Compress wording when useful, but keep the operational content discoverable from the target main workflow.

## Step Support Templates

Use these block shapes when extracting source support material into target runtime pages. These sections are optional for any given workflow step. If the source skill has no information that fits a support type, omit that section instead of inventing filler.

Before omitting a support section, look hard for clues in the source entrypoint, linked and unlinked source references, templates, examples, non-negotiable rules, common mistakes, validation rules, artifact rules, memory rules, and failure-handling sections. Do not give up after a rough scan just because the source does not use the exact words `guidance`, `preferences`, `constraints`, or `quality gates`.

Every emitted `Guidance`, `Preferences`, `Constraints`, and `Quality Gates` section must begin with a short interpretive paragraph of one to three sentences under the section heading. Use that paragraph to tell the future agent how to read the bullets or substeps, what kind of authority they have, and when to revise, route, or block instead of treating the list as decorative text.

### Guidance

`Guidance` expands one main workflow step into a smaller step-by-step workflow. It should read like a local `## Workflow`, with ordered substeps that an agent can execute.

Use this shape:

```markdown
## Guidance

Read this section as the local execution procedure for this workflow step. Follow the substeps in order unless a substep explicitly routes to a blocker or another skill; each substep should leave the named intermediate output.

1. **<Substep name>**. <Concrete action and expected intermediate output.>
2. **<Substep name>**. <Concrete action and expected intermediate output.>
3. **<Substep name>**. <Concrete action and expected intermediate output.>
```

### Preferences

`Preferences` list preferred ways of thinking and doing the step. Each item should be a sentence in the form `Prefer ...` with any condition or fallback in parentheses.

Use this shape:

```markdown
## Preferences

Read these preferences as route-shaping defaults, not hard requirements. Apply the preferred path when its condition holds, and use the fallback or record a reason when the condition does not hold.

- Prefer <preferred approach> (if <condition>, otherwise <fallback>).
- Prefer <preferred evidence source or reasoning style> (if <condition>, otherwise <fallback>).
```

### Constraints

`Constraints` list hard or strong requirements for the step. Each item should name the subject and use `should`, `should not`, `must`, or `must not`.

Use this shape:

```markdown
## Constraints

Read these constraints as the boundaries that make the step valid. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- <Subject> must <required behavior>.
- <Subject> must not <forbidden behavior>.
- <Subject> should <recommended behavior when not absolute>.
- <Subject> should not <discouraged behavior when not absolute>.
```

### Quality Gates

`Quality Gates` assess the outcome quality of the step. Split them into `Metrics` and `Checks` so measurable quality signals do not get mixed with boolean pass/fail conditions. If `Quality Gates` exists in the refactored output, both subsections must exist. If the source has no meaningful material for one subsection after a careful search, write `None` under that subsection instead of omitting it.

`Metrics` list measurable or ordinal signals. Each item should use the shape `<Metric name>: <definition>; <direction> is better.` The direction should be explicit, such as `higher`, `lower`, `larger`, `smaller`, `earlier`, `later`, `more complete`, or `less frequent`.

`Checks` list conditions that should be satisfied. Each item should use the shape `<Check name>: <condition that should be satisfied>.` Each check should be inspectable from the step output, local evidence, placeholders, or runtime records.

Use this shape:

```markdown
## Quality Gates

Read these gates after producing the step output and before handing off or claiming completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or route change rather than polished prose.

### Metrics

- <Metric name>: <definition>; <direction> is better.
- <Metric name>: <definition>; <direction> is better.

Or, when no meaningful metric exists:

None

### Checks

- <Check name>: <condition that should be satisfied>.
- <Check name>: <condition that should be satisfied>.

Or, when no meaningful check exists:

None
```

Use this example as the interpretive-paragraph pattern, not as fixed migration content:

```markdown
## Guidance

Read this section as the route-selection procedure for the baseline step. Follow the substeps in order so the final route is based on trust evidence rather than whichever comparator is easiest to run.

1. **Name the acceptance target**. Choose comparison-ready, paper-repro-ready, registry-publishable, waived, or blocked.
2. **List comparator evidence**. Record the available package, local path, service, source repository, metric contract, outputs, and blockers.
3. **Choose the lightest trustworthy route**. Select attach, import, verify-local-existing, reproduce, repair, publish, waive, or block with the reason.

## Preferences

Read these preferences as defaults for choosing among valid baseline routes. Prefer the lighter path only when it preserves downstream trust; otherwise escalate and record why the lighter route failed.

- Prefer attach when a trustworthy reusable comparator already exists (if outputs and metric contract can be inspected, otherwise import or verify).
- Prefer reproduce only when lighter routes leave the comparator incomparable (if a source audit is needed, otherwise start with the audit checklist).

## Constraints

Read these constraints as the acceptance boundary for the baseline step. A result that violates a `must` item cannot open the downstream gate until the violation is fixed, waived, or recorded as a blocker.

- The comparator route record must choose one dominant route and acceptance target.
- A heavier route must name the unresolved comparison risk it removes.
- Waiver must not be used merely because reproduction is inconvenient.

## Quality Gates

Read these gates before accepting the baseline route or handing off to the next skill. Metrics indicate whether the route is becoming more trustworthy and cheaper to resume; checks decide whether the gate can actually close.

### Metrics

- Contract field coverage: fraction of comparator identity, task, dataset, split, evaluation path, required metric keys, metric directions, source identity, known deviations, and caveats recorded; higher is better.
- Downstream guesswork count: number of comparator, metric, provenance, or caveat questions later stages would still need to infer; lower is better.

### Checks

- Target gate: acceptance target and current trust state are explicit.
- Evidence gate: trusted outputs or metrics trace to concrete evidence.
- Closeout gate: acceptance, waiver, blocker, or route change is durable.
```

## Validation

Before finishing, validate both structure and semantic preservation.

1. Confirm `<target-skill-dir>/org/src/`, `<target-skill-dir>/org/analysis/analysis-of-<source-skill-name>.md`, `<target-skill-dir>/org/README.md`, `<target-skill-dir>/migrate/migration-plan.md`, and `<target-skill-dir>/migrate/placeholders.md` exist.
2. Confirm every source file was copied under `<target-skill-dir>/org/src/` with paths preserved.
3. Confirm every source file except `SKILL.md` or `skill.md` and `agents/openai.yaml` was copied under `<target-skill-dir>/` with paths preserved.
4. Confirm the rewritten `SKILL.md` and rewritten workflow subpages match the source process analysis, not merely the source wording.
5. Confirm every main workflow step references the support section or support page that carries its extracted preferences, constraints, guidance, quality gates, stop conditions, and output requirements.
6. Confirm extracted step support uses the standard `Guidance`, `Preferences`, `Constraints`, and `Quality Gates` shapes when those support types are present. Confirm each present support section starts with a one-to-three-sentence interpretive paragraph before bullets or substeps. If `Quality Gates` exists, confirm it contains both `Metrics` and `Checks`, and that any subsection without meaningful source material says `None`. Confirm omitted support types were omitted because the source lacked fitting material after a careful search.
7. Confirm the migration plan records the mapping from source support sections and source reference pages to target workflow steps or global target support sections.
8. Confirm substitutions in the migration plan are reflected in rewritten pages.
9. Confirm every source artifact mention outside `<target-skill-dir>/org/` has been replaced by a placeholder listed in `<target-skill-dir>/migrate/placeholders.md`.
10. Confirm every rewritten skill page that uses placeholders references `<target-skill-dir>/migrate/placeholders.md`.
11. Confirm every source-skill route without a matching Isomer skill has been replaced by a missing skill-route placeholder listed in `<target-skill-dir>/migrate/placeholders.md`.
12. Run the skill validator when available:

```bash
python /home/huangzhe/.codex/skills/.system/skill-creator/scripts/quick_validate.py <target-skill-dir>
```

13. Inspect leftovers outside audit material:

```bash
rg -n "DeepScientist MCP|mcp__|quest|quest_root|venv|artifact\.|memory\.|bash_exec" <target-skill-dir>
```

Leftovers inside `<target-skill-dir>/org/` are expected when they document the source. Leftovers in rewritten runtime instructions need review.

## Common Mistakes

- Rewriting from intuition instead of from the deep-inspection output.
- Treating `refactor-migrate` as a cosmetic cleanup of `copy-migrate`.
- Copying source files only into `org/src/` and forgetting the required runtime support copy under `<target-skill-dir>/`.
- Collapsing source subpages into a smaller set of native pages instead of copying and refactoring each source support file in the runtime tree.
- Skipping `<target-skill-dir>/org/README.md`, which records analysis coverage.
- Creating `<target-skill-dir>/migrate/migration-plan.md` after the rewrite instead of before it.
- Creating placeholders in rewritten pages without listing them in `<target-skill-dir>/migrate/placeholders.md`.
- Forgetting to reference `<target-skill-dir>/migrate/placeholders.md` from a rewritten page that uses placeholders.
- Leaving a route to a missing source skill as if the matching Isomer skill already exists.
- Rewriting only from analyzed high-level logic and failing to reread the source entrypoint for preferences, constraints, guidance, quality gates, and stop conditions.
- Leaving main workflow steps without references to the support sections or pages they require.
- Dropping source rules because they live outside the source's numbered control workflow.
- Mixing guidance, preferences, constraints, and quality gates into one prose blob instead of using the standard support block shapes.
- Mixing directional quality metrics and boolean checks into one flat `Quality Gates` list.
- Adding `Quality Gates` with only `Metrics` or only `Checks`; when the section exists, both subsections must be present.
- Inventing empty support sections when the source has no fitting material, or omitting support sections after only a rough scan.
- Preserving native-looking prose while losing source gates, evidence handoffs, assumptions, inputs, or outputs.
- Overwriting `<target-skill-dir>/agents/openai.yaml` with source agent metadata.
- Editing files under `<target-skill-dir>/org/src/` so they no longer serve as an untouched source copy.
