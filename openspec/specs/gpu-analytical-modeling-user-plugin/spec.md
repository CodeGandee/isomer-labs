# gpu-analytical-modeling-user-plugin Specification

## Purpose
TBD - created by archiving change add-gpu-analytical-modeling-user-plugin. Update Purpose after archive.
## Requirements
### Requirement: GPU Analytical Modeling User-Plugin Layout
The project SHALL provide a project-local user-plugin named `gpu-analytical-modeling` under `skillset/user-plugins/gpu-analytical-modeling/` as a bundle of User Skill Callback skill directories for GPU kernel analytical modeling.

#### Scenario: Plugin root exists
- **WHEN** the project-local user-plugin tree is inspected
- **THEN** `skillset/user-plugins/gpu-analytical-modeling/` exists
- **AND** it contains `manifest.toml`
- **AND** it contains a README that explains the plugin purpose, registration model, and recommended callback targets

#### Scenario: Manifest declares local callback bundle
- **WHEN** `skillset/user-plugins/gpu-analytical-modeling/manifest.toml` is inspected
- **THEN** it declares schema version, plugin id, plugin kind, display name, description, distribution locality, and install defaults
- **AND** the plugin kind identifies the plugin as a User Skill Callback bundle rather than a packaged system skill

#### Scenario: Callback skill entrypoints exist
- **WHEN** the plugin root is inspected
- **THEN** it contains `gpu-modeling-method/`, `gpu-evidence-and-experiment/`, and `gpu-reporting-and-closure/`
- **AND** each directory contains a `SKILL.md` suitable for `isomer-cli project skill-callbacks register --skill-dir <dir>`

#### Scenario: Internal command pages are local
- **WHEN** a plugin callback skill links detailed command or reference pages
- **THEN** those pages live inside that callback skill directory
- **AND** the callback skill does not require active runtime files outside its own directory except for the current Project, Topic Workspace, and normal DeepSci context supplied by the owning workflow

#### Scenario: Plugin remains undistributed
- **WHEN** the implementation is inspected
- **THEN** the GPU analytical modeling user-plugin files remain under `skillset/user-plugins/gpu-analytical-modeling/`
- **AND** they are not copied into packaged system skill assets, distribution manifests, or packaged system skill inventory

#### Scenario: Manifest is not an installed registry
- **WHEN** the plugin manifest declares desired callbacks
- **THEN** it is treated as an install recipe
- **AND** it does not replace `.isomer-labs/user-skill-callbacks/.../registry.toml` as the installed callback registry
- **AND** this change does not require an automatic installer command

### Requirement: Imsight-Style Callback Skill Authoring
The plugin callback skills SHALL follow the skill creation style guided by `$imsight-agent-skill-handling create`.

#### Scenario: Callback skill frontmatter is valid
- **WHEN** a plugin callback skill `SKILL.md` is inspected
- **THEN** it contains YAML frontmatter with `name` and `description`
- **AND** the `name` matches the callback skill directory name
- **AND** the `description` begins with "Use when"

#### Scenario: Callback skill has required sections
- **WHEN** a plugin callback skill `SKILL.md` is inspected
- **THEN** it contains `## Overview`, `## When to Use`, `## Workflow`, and `## Common Mistakes`
- **AND** the workflow appears near the top of the skill
- **AND** the workflow is a concise numbered list with a freeform fallback

#### Scenario: Command pages hold long active detail
- **WHEN** a workflow step needs detailed rules, examples, or subcommand-like guidance
- **THEN** the skill links to a local `commands/*.md` page rather than inlining long procedure text in the workflow
- **AND** each active command page has its own `## Workflow` entrypoint

#### Scenario: Empty symmetry directories are absent
- **WHEN** the plugin callback skill directories are inspected
- **THEN** they do not contain empty `agents/`, `scripts/`, `references/`, or `assets/` directories created only for symmetry

### Requirement: GPU Modeling Method Callback Skill
The `gpu-modeling-method` callback skill SHALL guide source selection, analytical model shape, and baseline evidence-class discipline before GPU kernel model implementation or analysis proceeds.

#### Scenario: Source-map guidance is available
- **WHEN** an agent reads `gpu-modeling-method/SKILL.md`
- **THEN** the skill routes source-priority work to local guidance that prefers topic records, kernel source, vendor architecture documentation, PTX or SASS evidence, Nsight Compute documentation, microbenchmark literature, and simulator architecture references in a documented order

#### Scenario: Analytical model shape is defined
- **WHEN** the modeling-method callback is applied to a DeepSci framing, ideation, or analysis workflow
- **THEN** it instructs the agent to require named inputs, outputs, units, equations, hardware parameters, component terms, saturation or max operators, bounded calibration parameters, assumptions, and validity envelopes

#### Scenario: Black-box fitting is rejected
- **WHEN** a proposed GPU model relies on a generic fitted function, unbounded empirical coefficients, or roofline-only commentary as the main model
- **THEN** the callback instructs the agent to treat that proposal as a baseline, comparator, or blocker rather than an accepted analytical model

#### Scenario: Evidence classes are separated
- **WHEN** the agent describes baselines or sources
- **THEN** the callback instructs it to distinguish analytical derivation, real hardware measurement, NCU counter evidence, microbenchmark evidence, simulator evidence, emulator evidence, and unsupported assumptions

### Requirement: GPU Evidence and Experiment Callback Skill
The `gpu-evidence-and-experiment` callback skill SHALL guide falsifiable evaluation, NCU evidence collection, component bottleneck proof, and model-refinement decisions for GPU kernel analytical models.

#### Scenario: Evaluation contract is required
- **WHEN** the callback is applied before an experiment or analysis pass
- **THEN** it instructs the agent to define predicted outputs, primary and secondary metrics, calibration and validation split, query set separation, fair-comparison rules, and accepted evidence classes before accuracy claims are made

#### Scenario: Real-hardware evidence is distinguished
- **WHEN** an experiment result uses emulator, simulator, synthetic, or analytical-proxy ground truth
- **THEN** the callback instructs the agent to label that evidence as non-silicon support and not report it as real-hardware prediction accuracy

#### Scenario: NCU protocol is documented
- **WHEN** the agent designs or reports NCU validation
- **THEN** it records the command shape, target device, kernel selection, raw metric names, counter-to-component mapping, measured values or artifact paths, and any command failures or harness fixes that affect interpretation

#### Scenario: Pixi NCU command posture is explicit
- **WHEN** the callback gives command-shape guidance for local Pixi environments
- **THEN** it instructs agents to prefer `pixi run ncu ...` over `ncu pixi run ...` unless local project evidence proves a different wrapper is required

#### Scenario: Component bottleneck proof is first-class
- **WHEN** the model claims to predict a saturated component or blocking execution path
- **THEN** the callback instructs the agent to compare the prediction against component-level evidence such as per-unit active cycles, instruction mix, pipeline activity, SASS or PTX dependency path, or an explicit evidence gap

#### Scenario: Mismatches trigger refinement analysis
- **WHEN** model predictions disagree with NCU counters, runtime measurements, or disassembly-derived execution paths
- **THEN** the callback instructs the agent to name a likely mismatch class such as missing hardware node, hidden overlap, cache reuse, scheduler effect, counter-mapping error, harness issue, unsupported shape regime, or invalid calibrated parameter

### Requirement: GPU Reporting and Closure Callback Skill
The `gpu-reporting-and-closure` callback skill SHALL keep GPU analytical modeling claims, mathematical presentation, and closure decisions aligned with the available evidence.

#### Scenario: Claim gate classifies support
- **WHEN** a writing, review, analysis, or finalization workflow prepares user-facing claims
- **THEN** the callback instructs the agent to classify runtime, counter-trend, saturated-component, and blocking-path claims as supported, partially supported, unsupported, or deferred with evidence classes and caveats

#### Scenario: Math notation is publication-friendly
- **WHEN** the agent writes formulas for a report or paper
- **THEN** the callback instructs it to use concise mathematical symbols, define notation near first use, avoid code-like long variable names in formulas, and keep units explicit

#### Scenario: Central proof is not buried
- **WHEN** component-level or path-level validation is central to the contribution
- **THEN** the callback instructs the agent to keep the proof in the main result narrative or provide a clear main-text summary with detailed appendix support

#### Scenario: Closure refuses overclaiming
- **WHEN** real-hardware evidence, component-level proof, or path-level validation is missing for a central claim
- **THEN** the callback instructs finalization or decision workflows to park, limit, defer, or route back rather than publish or close with unsupported claims

### Requirement: Recommended Callback Target Map
The plugin manifest and README SHALL document recommended DeepSci target skills and callback stages for each plugin callback skill while leaving final registration explicit and user-controlled.

#### Scenario: Manifest callback entries are declared
- **WHEN** the plugin manifest is inspected
- **THEN** it contains callback entries with stable callback id, relative `skill_dir`, target packaged system skill, stage, priority, and a short description
- **AND** every `skill_dir` points to a child directory containing `SKILL.md`

#### Scenario: Manifest callback sources match callback source types
- **WHEN** a callback entry is inspected in the plugin manifest
- **THEN** it declares one `source_type` value of `skill_dir`, `prompt_file`, or `prompt`
- **AND** it provides exactly one matching source field for that source type
- **AND** it does not provide source fields for the other source types

#### Scenario: Skill directory source is relative
- **WHEN** a manifest callback entry uses `source_type = "skill_dir"`
- **THEN** its `skill_dir` value resolves relative to the plugin root
- **AND** the resolved directory contains `SKILL.md`

#### Scenario: Prompt file source is relative
- **WHEN** a manifest callback entry uses `source_type = "prompt_file"`
- **THEN** its `prompt_file` value resolves relative to the plugin root
- **AND** the resolved file exists as reusable instruction material

#### Scenario: Inline prompt source is bounded
- **WHEN** a manifest callback entry uses `source_type = "prompt"`
- **THEN** its `prompt` value is short static instruction material
- **AND** it is subject to the same secret-like material restrictions as normal User Skill Callback registration

#### Scenario: Modeling-method targets are documented
- **WHEN** the manifest or README is inspected
- **THEN** it recommends `gpu-modeling-method` for framing and model-shaping stages such as `isomer-deepsci-scout`, `isomer-deepsci-baseline`, `isomer-deepsci-idea`, and early `isomer-deepsci-analysis`

#### Scenario: Evidence targets are documented
- **WHEN** the manifest or README is inspected
- **THEN** it recommends `gpu-evidence-and-experiment` for experiment, analysis, review, decision, and pipeline stages that design, collect, interpret, or route evidence

#### Scenario: Reporting targets are documented
- **WHEN** the manifest or README is inspected
- **THEN** it recommends `gpu-reporting-and-closure` for writing, review, finalization, and end-stage analysis workflows that may make user-facing claims

#### Scenario: Registration remains explicit
- **WHEN** an operator wants to activate the plugin
- **THEN** the README shows `isomer-cli project skill-callbacks register` examples for topic-scoped and project-scoped use
- **AND** the manifest provides the equivalent desired callback entries for future installer support
- **AND** the plugin does not require automatic registration behavior

### Requirement: Generic GPU Kernel Scope
The plugin SHALL remain generic to GPU kernel analytical modeling and SHALL NOT encode one topic, kernel, GPU SKU, or local workspace as the only supported target.

#### Scenario: Topic-specific facts are examples
- **WHEN** the plugin mentions Flash Attention 4, B200, Blackwell, AccelSim, GPGPU-Sim, or Nsight Compute
- **THEN** those mentions are framed as examples, source classes, or motivating evidence rather than mandatory topic identity

#### Scenario: Topic supplies concrete hardware details
- **WHEN** a Research Topic has a target GPU, kernel, metric set, or toolchain
- **THEN** the plugin instructs agents to derive concrete parameters from topic records, local hardware evidence, source material, and user constraints rather than inventing them in the callback material

#### Scenario: Secrets and private outputs are absent
- **WHEN** the plugin files are inspected
- **THEN** they do not contain credentials, API keys, private benchmark outputs, topic-private raw logs, or hard-coded absolute Topic Workspace paths

