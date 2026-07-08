## 1. Plugin Structure and Manifest

- [x] 1.1 Create `skillset/user-plugins/gpu-analytical-modeling/manifest.toml` with plugin identity, callback-bundle kind, project-local distribution marker, install defaults, and desired callback entries.
- [x] 1.2 Make manifest callback entries support `source_type = "skill_dir"`, `source_type = "prompt_file"`, and `source_type = "prompt"` with exactly one matching source field per entry.
- [x] 1.3 Create `skillset/user-plugins/gpu-analytical-modeling/README.md` with purpose, scope, callback registration model, manifest role, recommended target map, and topic-scoped/project-scoped examples.
- [x] 1.4 Create reusable prompt files under `skillset/user-plugins/gpu-analytical-modeling/prompts/` for short prompt-file callbacks.
- [x] 1.5 Create `gpu-modeling-method/`, `gpu-evidence-and-experiment/`, and `gpu-reporting-and-closure/` child directories under the plugin root.
- [x] 1.6 Add Imsight-style `SKILL.md` files to each child callback skill with stable frontmatter, `## Overview`, `## When to Use`, numbered `## Workflow`, and `## Common Mistakes`.
- [x] 1.7 Add local `commands/` directories and command pages listed in the design for each callback skill, using command pages only for real active detail.

## 2. Modeling Method Callback

- [x] 2.1 Write `gpu-modeling-method/SKILL.md` as the entrance callback skill for GPU source priority, analytical model shape, and baseline evidence-class discipline.
- [x] 2.2 Write `commands/source-map.md` with source ordering for topic records, kernel source, vendor docs, PTX/SASS evidence, NCU docs, microbenchmark literature, and simulator architecture references.
- [x] 2.3 Write `commands/model-shape.md` defining required inputs, outputs, units, equations, hardware parameters, component terms, saturation operators, bounded calibration, assumptions, and validity envelopes.
- [x] 2.4 Write `commands/baseline-contract.md` separating analytical derivation, real hardware measurement, NCU counter evidence, microbenchmark evidence, simulator evidence, emulator evidence, roofline baselines, and unsupported assumptions.

## 3. Evidence and Experiment Callback

- [x] 3.1 Write `gpu-evidence-and-experiment/SKILL.md` as the entrance callback skill for falsifiable evaluation, NCU evidence, component bottleneck proof, and refinement routing.
- [x] 3.2 Write `commands/evaluation-contract.md` covering predicted outputs, metrics, calibration/validation/query split, fair-comparison rules, and accepted evidence classes.
- [x] 3.3 Write `commands/ncu-protocol.md` covering command shape, target device, kernel selection, metric names, counter-to-component mapping, measured values or artifact paths, command failures, harness fixes, and `pixi run ncu ...` posture.
- [x] 3.4 Write `commands/component-bottleneck-proof.md` requiring saturated-component and blocking-path validation beyond coarse compute/memory labels.
- [x] 3.5 Write `commands/failure-refinement.md` with mismatch classes and route guidance for missing hardware nodes, hidden overlap, cache reuse, scheduler effects, counter mapping errors, harness issues, unsupported regimes, and invalid calibration parameters.

## 4. Reporting and Closure Callback

- [x] 4.1 Write `gpu-reporting-and-closure/SKILL.md` as the entrance callback skill for user-facing claims, math presentation, and closure decisions.
- [x] 4.2 Write `commands/claim-gate.md` requiring support classification for runtime, counter-trend, saturated-component, and blocking-path claims.
- [x] 4.3 Write `commands/math-writing.md` requiring concise mathematical symbols, nearby notation definitions, explicit units, and avoidance of code-like long variable names in formulas.
- [x] 4.4 Write `commands/closure-limits.md` requiring park, limit, defer, or route-back decisions when real-hardware evidence or component/path proof is missing for central claims.

## 5. Registration Guidance and Validation

- [x] 5.1 Add README examples that register each callback skill with representative DeepSci target skills and `begin` or `end` stages using `isomer-cli project skill-callbacks register --skill-dir`.
- [x] 5.2 Verify every plugin callback skill is generic to GPU kernel analytical modeling and does not hard-code Flash Attention 4, B200, private topic outputs, credentials, or absolute Topic Workspace paths as required context.
- [x] 5.3 Verify the implementation does not edit packaged system skill assets, distribution manifests, system skill inventory, or callback registry behavior.
- [x] 5.4 Smoke-check that every manifest callback entry uses exactly one source type, uses `begin` or `end`, and names a packaged DeepSci target skill.
- [x] 5.5 Smoke-check that every `skill_dir` callback source points to an existing child directory containing `SKILL.md`.
- [x] 5.6 Smoke-check that every `prompt_file` callback source points to an existing plugin-local prompt file and every inline `prompt` entry is short static instruction material without secret-like content.
- [x] 5.7 Smoke-check that each linked local command page exists.
- [x] 5.8 Validate each callback skill against the relevant `$imsight-agent-skill-handling create` style expectations: frontmatter, matching name, description trigger form, required sections, concise workflow, freeform fallback, and no empty symmetry directories.
- [x] 5.9 Skip temporary live callback registration to avoid mutating project/topic callback registries; manifest, filesystem, source-type, stage, target-skill, prompt-file, inline-prompt, and command-link smoke checks cover the non-mutating validation path.
