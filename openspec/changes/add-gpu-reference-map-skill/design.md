## Context

The `gpu-analytical-modeling` user plugin currently mixes source lookup rules with operational modeling guidance. `gpu-modeling-method/commands/source-map.md` already ranks useful sources, and experiment guidance names profiler and counter sources, but these details are scattered across skills whose main job is methodology, evidence gating, or reporting.

The user wants source lookup guidance grouped into a dedicated skill so it can be updated easily as tools, docs, profiler counters, simulator projects, and modeling literature change. The new skill should keep updatable source taxonomy in one place while letting operational skills remain stable and principle-focused.

## Goals / Non-Goals

**Goals:**

- Add a project-local `gpu-reference-map` skill as the central place for GPU analytical-modeling source discovery and source limitations.
- Cover source families for local topic context, kernel implementation, hardware architecture docs, profiler and counter evidence, simulator architecture references, measurements and microbenchmarks, and literature.
- Make each source family state what it can justify, what it cannot justify, and what metadata should be preserved.
- Update operational skills and README/manifest text to point to `gpu-reference-map` when source lookup is needed.
- Keep implementation under `skillset/user-plugins/gpu-analytical-modeling/` and this change directory.

**Non-Goals:**

- Do not add packaged system skills, callback registry behavior, CLI commands, or runtime loading changes.
- Do not remove modeling, evidence, or reporting gates from their current skills.
- Do not turn the reference-map skill into a crawler, search runner, profiler runner, simulator runner, benchmark runner, or paper downloader.
- Do not hard-code a specific topic workspace, kernel, GPU SKU, host, paper venue, or artifact path.

## Decisions

1. **Add a fourth top-level project-local skill for source lookup.**

`gpu-reference-map` should be a sibling of `gpu-modeling-method`, `gpu-evidence-and-experiment`, and `gpu-reporting-and-closure`. That keeps source maintenance independent from operational modeling rules.

Alternative considered: keep expanding `gpu-modeling-method/commands/source-map.md`. That keeps fewer top-level skills but leaves source taxonomy inside a modeling-method workflow where it is harder to update without changing operational guidance.

2. **Use command pages by source family.**

The skill should expose command pages for `local-topic-sources`, `kernel-sources`, `hardware-doc-sources`, `profiler-counter-sources`, `simulator-sources`, `measurement-sources`, and `literature-sources`. This gives maintainers small update surfaces when a tool, documentation source, or source limitation changes.

Alternative considered: one long source-map page. That would be simpler initially but harder to maintain as reference classes evolve.

3. **Operational skills should point to the reference map instead of duplicating taxonomy.**

`gpu-modeling-method/commands/source-map.md` can become a thin bridge or summary that sends agents to `gpu-reference-map`. It should retain only operational source-priority posture and avoid owning detailed lists that will drift from the dedicated skill.

Alternative considered: remove `source-map.md`. That would be a bigger callback compatibility change because `gpu-modeling-method` currently links it.

4. **Keep Isomer/Pixi NCU posture local but scoped to profiler-counter sources.**

Pixi is required system context for Isomer Labs, so Pixi-managed NCU command posture is allowed. The reference-map skill should still frame it as profiler/counter source guidance rather than a general modeling principle.

## Risks / Trade-offs

- **Risk: Agents consult both the old source-map and new reference-map and receive duplicate instructions.** -> Mitigation: make the old source-map explicitly delegate detailed source taxonomy to `gpu-reference-map`.
- **Risk: A fourth skill increases manifest surface.** -> Mitigation: register it only at stages where source lookup naturally happens: scout, baseline, idea, analysis, experiment, and review.
- **Risk: Source guidance becomes stale.** -> Mitigation: organize source families into separate command pages so maintainers can update one family without editing modeling or evidence gates.
- **Risk: Source examples become topic-specific.** -> Mitigation: allow source classes and common simulator/profiler examples, but prohibit topic workspace paths, specific kernels, specific GPU SKUs, fixed artifact paths, and venue-specific paper instructions.

## Migration Plan

Implementation should add the new skill directory, update README and manifest entries, and lightly revise existing source pointers. No runtime migration is required because the plugin manifest is declarative project-local guidance.

Rollback is a normal file revert of the new skill directory, manifest/README updates, and the source-map bridge edit.

## Open Questions

No user decision is currently required. During implementation, keep source-family pages concise enough to be maintainable but concrete enough to prevent agents from treating simulators, profiler summaries, or informal notes as stronger evidence than they are.
