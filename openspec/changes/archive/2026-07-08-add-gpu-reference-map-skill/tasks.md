## 1. Reference Map Skill

- [x] 1.1 Add `skillset/user-plugins/gpu-analytical-modeling/gpu-reference-map/SKILL.md` with overview, usage boundary, workflow, subcommand table, native-planning fallback, and common mistakes.
- [x] 1.2 Add command page `commands/local-topic-sources.md` for topic intent, durable records, local scripts, prior decisions, and local outputs.
- [x] 1.3 Add command page `commands/kernel-sources.md` for kernel repository, generated code, compiler output, launch configuration, harness, and disassembly sources.
- [x] 1.4 Add command page `commands/hardware-doc-sources.md` for vendor architecture docs, tuning guides, programming guides, PTX/SASS references, hardware queries, and concrete-limit provenance.
- [x] 1.5 Add command page `commands/profiler-counter-sources.md` for profiler docs, NCU/Pixi posture where relevant, raw metric names, collection context, normalization, counter-to-component mapping, and claim linkage.
- [x] 1.6 Add command page `commands/simulator-sources.md` for AccelSim, GPGPU-Sim, and similar projects as architecture and execution-path references rather than target-hardware truth.
- [x] 1.7 Add command page `commands/measurement-sources.md` for full-kernel timing, microbenchmark, hardware query, run metadata, and measurement caveat sources.
- [x] 1.8 Add command page `commands/literature-sources.md` for peer-reviewed and vendor-supported modeling papers, surveys, equations, validation methods, and citation limits.
- [x] 1.9 Add `agents/openai.yaml` metadata for `gpu-reference-map`.

## 2. Plugin Integration

- [x] 2.1 Update `README.md` contents and recommended target table to include `gpu-reference-map`.
- [x] 2.2 Update `manifest.toml` with project-local callback entries for `gpu-reference-map` at source-discovery and source-checking stages.
- [x] 2.3 Update `gpu-modeling-method/SKILL.md` so source lookup points to `gpu-reference-map` while modeling-method keeps model-shape and baseline responsibilities.
- [x] 2.4 Revise `gpu-modeling-method/commands/source-map.md` into a bridge that delegates detailed source taxonomy to `gpu-reference-map` and avoids duplicating maintainable source lists.
- [x] 2.5 Update any existing text that implies source taxonomy belongs in an operational skill when it should point to the dedicated reference-map skill.

## 3. Generic Scope and Boundaries

- [x] 3.1 Ensure the new reference-map guidance states what each source family can justify, what it cannot justify, and what metadata or caveats must be preserved.
- [x] 3.2 Ensure simulator guidance treats AccelSim, GPGPU-Sim, and similar projects as architecture references rather than direct target-hardware truth unless separately validated.
- [x] 3.3 Ensure profiler/counter guidance preserves raw observations, mapping rationale, derived-label separation, and support/refute/unresolved linkage to model claims.
- [x] 3.4 Inspect changed plugin guidance to ensure examples remain source-class examples and do not require a specific topic workspace, kernel, GPU SKU, host, paper venue, or artifact path.
- [x] 3.5 Verify implementation changes remain under `skillset/user-plugins/gpu-analytical-modeling/` and this change directory, with no packaged system skill, callback registry, CLI/runtime, or distribution manifest changes.

## 4. Validation

- [x] 4.1 Run the available skill validator against `gpu-reference-map`.
- [x] 4.2 Run the available skill validator against touched existing skill directories.
- [x] 4.3 Run a structural check that linked command pages in `gpu-reference-map/SKILL.md` and touched skill `SKILL.md` files exist and command-like pages still have numbered `## Workflow` sections with native-planning fallbacks.
- [x] 4.4 Run `openspec validate "add-gpu-reference-map-skill" --type change --strict`.
