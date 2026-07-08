## Context

User Skill Callbacks already let a Project or Research Topic attach supplemental instruction material to one packaged system skill and one `begin` or `end` stage. The callback source may be a `--skill-dir` containing `SKILL.md`, which makes it a good fit for project-local user-plugin material under `skillset/user-plugins/`.

The Flash Attention 4 white-box runtime modeling topic provides the motivating evidence. The topic started with a clear request for hardware-grounded modeling, then repeatedly needed corrections around NCU validation, emulator versus real-silicon evidence, component-level bottlenecks, execution-path saturation, and publication-claim honesty. Those lessons are useful beyond FA4: GPU kernel analytical modeling often needs the same source discipline, equation shape, calibration split, counter mapping, and claim gate.

Existing Isomer system skills prefer an entrance skill with local command/reference pages over many tiny skills. The user-plugin should follow that pattern so operators register a few stable callback skill directories instead of managing a large list of narrow callbacks.

## Goals / Non-Goals

**Goals:**

- Add a reusable `gpu-analytical-modeling` user-plugin under `skillset/user-plugins/gpu-analytical-modeling/`.
- Include a `manifest.toml` that records the plugin identity and desired callback registrations in a future-installer-friendly shape, including skill-directory, prompt-file, and inline-prompt callback sources.
- Organize the plugin as three callback skill entrypoints with internal command pages: modeling method, evidence and experiment, reporting and closure.
- Author each callback skill using the `$imsight-agent-skill-handling create` style guidance.
- Make each callback skill usable as a `project skill-callbacks register --skill-dir <dir>` source.
- Keep the guidance generic to GPU kernel analytical modeling while allowing topics to supply GPU-, kernel-, and hardware-specific facts.
- Provide operator-facing registration guidance for DeepSci skills and stages.
- Preserve existing callback authority rules: the plugin supplies supplemental instructions only.

**Non-Goals:**

- Do not add a new plugin installer, manifest runtime, callback stage, callback registry schema, or CLI subcommand.
- Do not edit packaged DeepSci system skills as part of this change.
- Do not make the plugin execute NCU, benchmarks, simulators, scripts, or network searches on its own.
- Do not bake Flash Attention 4, B200, or one Topic Workspace path into the generic plugin instructions.
- Do not make project-local user-plugin material part of the packaged system skill inventory or distribution.

## Decisions

### 1. Use three entrance callback skills

The plugin will expose these callback skill directories:

```text
skillset/user-plugins/gpu-analytical-modeling/
  manifest.toml
  README.md
  prompts/
    ncu-command-posture.md
    no-emulator-overclaim.md
  gpu-modeling-method/
    SKILL.md
    commands/source-map.md
    commands/model-shape.md
    commands/baseline-contract.md
  gpu-evidence-and-experiment/
    SKILL.md
    commands/evaluation-contract.md
    commands/ncu-protocol.md
    commands/component-bottleneck-proof.md
    commands/failure-refinement.md
  gpu-reporting-and-closure/
    SKILL.md
    commands/claim-gate.md
    commands/math-writing.md
    commands/closure-limits.md
```

`gpu-modeling-method` shapes the research frame before implementation. `gpu-evidence-and-experiment` makes model claims falsifiable against real measurements and counters. `gpu-reporting-and-closure` prevents publication or summary claims from outrunning evidence.

Alternative considered: create one callback skill per concern. That would make registration precise but too noisy for operators and inconsistent with the local system skill style.

### 2. Use Imsight skill creation style

Each callback skill should be authored as a real skill, not as a loose prompt file. Use the style guidance from `$imsight-agent-skill-handling create`: valid YAML frontmatter, `name` matching the directory, description beginning with "Use when...", a concise `## Overview`, a `## When to Use` section, a near-top numbered `## Workflow`, local command pages when detail would otherwise bloat the workflow, and `## Common Mistakes`.

The three callback skills are a collection of related routines rather than one mandatory complex procedure, so their subcommand detail should use a simple collection-of-routines flavor. Command pages under `commands/` should have their own `## Workflow` entrypoint when they are subcommand-like active guidance.

Do not create empty `agents/`, `scripts/`, `references/`, or `assets/` directories for symmetry. The first version needs `SKILL.md`, `commands/` where command pages exist, `prompts/` for reusable prompt-file callbacks, README, and manifest only.

Alternative considered: write these callback sources as simple Markdown prompts without skill structure. That would be quicker, but it would lose discoverability, validation shape, and consistency with the rest of the Imsight-authored skillset.

### 3. Keep the plugin local and undistributed

The implementation will only create or update files under `skillset/user-plugins/gpu-analytical-modeling/`. These skills are not copied into `src/isomer_labs/assets/system_skills/`, not registered as packaged system skills, not added to distribution manifests, and not included in packaged validation inventory.

Alternative considered: promote the plugin into a packaged domain extension. That would be the wrong boundary for user preference material and would make local research style choices part of the Isomer distribution.

### 4. Add a manifest as an install recipe, not an installer

Each user-plugin should include a project-local `manifest.toml` that tells Isomer how callbacks should be installed when installer support exists. In this change, the manifest is required documentation and validation material only; operators still activate callbacks with explicit `isomer-cli project skill-callbacks register ...` commands.

The manifest should describe plugin identity, locality, and callback entries. Each callback entry should mirror the existing User Skill Callback source union: exactly one of `skill_dir`, `prompt_file`, or inline `prompt`. `skill_dir` and `prompt_file` paths are relative to the plugin root.

```toml
schema_version = "isomer-user-plugin.v1"
id = "gpu-analytical-modeling"
kind = "user-skill-callback-bundle"
name = "GPU Analytical Modeling"
description = "Project-local callback skills and prompts for GPU kernel analytical modeling."
distribution = "project-local"

[install]
default_scope = "research_topic"
requires_explicit_install = true

[[callbacks]]
id = "gpu-modeling-method.scout.begin"
skill_dir = "gpu-modeling-method"
target_skill = "isomer-deepsci-scout"
stage = "begin"
priority = 100
source_type = "skill_dir"
description = "Apply GPU source and model-shape discipline before scout framing."

[[callbacks]]
id = "gpu-evidence.ncu-command.experiment.begin"
target_skill = "isomer-deepsci-experiment"
stage = "begin"
priority = 90
source_type = "prompt_file"
prompt_file = "prompts/ncu-command-posture.md"
description = "Remind experiment agents to use the local Pixi/NCU command shape."

[[callbacks]]
id = "gpu-reporting.no-emulator-overclaim.write.end"
target_skill = "isomer-deepsci-write"
stage = "end"
priority = 80
source_type = "prompt"
prompt = """
Before finalizing GPU analytical-modeling claims, classify emulator, simulator, synthetic, and real-hardware evidence separately. Do not describe emulator-only validation as measured hardware accuracy.
"""
description = "Prevent publication-facing overclaiming from proxy evidence."
```

The manifest is not the installed callback registry. The registry remains under `.isomer-labs/user-skill-callbacks/.../registry.toml` after manual registration or a future installer writes it.

Prefer `prompt_file` over inline `prompt` for reusable short reminders because files are easier to review, diff, lint, and scan for secret-like material. Inline `prompt` remains supported for tiny static instructions because the callback CLI already supports it.

Alternative considered: add `isomer-cli project skill-callbacks install --plugin-dir ...` now. That would satisfy automatic installation, but it expands this change from creating local user-plugin skills into callback CLI behavior. That belongs in a later change once the manifest shape settles.

### 5. Keep command pages as active references, not executable commands

The `commands/*.md` files are directly linked active instruction pages read by the agent after the callback `SKILL.md` routes to them. They are not CLI commands and do not change the callback source contract. This mirrors system skill organization while staying inside the existing `--skill-dir` behavior.

Alternative considered: support only `skill_dir` entries in the manifest. That would under-model the existing callback mechanism and force small one-line reminders into full skill directories. Supporting the full source union keeps the manifest aligned with `project skill-callbacks register`.

Alternative considered: encode all detailed guidance in the manifest. That would make the manifest too large and blur the boundary between install recipe and instruction material.

### 6. Register by purpose and stage, not by internal command

The README will document recommended registrations such as:

- `gpu-modeling-method` for `isomer-deepsci-scout:begin/end`, `isomer-deepsci-baseline:begin/end`, `isomer-deepsci-idea:begin/end`, and `isomer-deepsci-analysis:begin`.
- `gpu-evidence-and-experiment` for `isomer-deepsci-experiment:begin/end`, `isomer-deepsci-analysis:begin/end`, `isomer-deepsci-review:begin`, `isomer-deepsci-decision:begin/end`, and `isomer-deepsci-pipeline:begin/end`.
- `gpu-reporting-and-closure` for `isomer-deepsci-write:end`, `isomer-deepsci-review:end`, `isomer-deepsci-finalize:begin/end`, and `isomer-deepsci-analysis:end`.

Operators can register a smaller subset when a topic needs only framing, only evidence discipline, or only publication-claim gates.

Alternative considered: provide automatic registration. That would require new CLI behavior and would hide explicit user intent, so it stays out of scope for this change.

### 7. Encode evidence classes explicitly

The plugin will distinguish source and evidence classes: vendor documentation, kernel source, PTX/SASS/disassembly, NCU measurements, microbenchmarks, simulator evidence, emulator evidence, analytical derivation, calibrated parameters, and unsupported assumptions. This decision directly addresses the FA4 topic failure where emulator-only validation initially looked like model accuracy.

Alternative considered: only require citations. Citations are necessary but not enough; the key risk is confusing the trust level of different evidence sources.

### 8. Make component bottlenecks first-class

The evidence skill will require component-level and path-level claims to name the predicted saturated component, blocking execution path, counter mapping, and mismatch diagnosis. Coarse compute-bound or memory-bound labels are allowed only as baselines or summaries.

Alternative considered: accept NCU's coarse Speed of Light label as bottleneck truth. The topic showed that label can be too coarse when all configurations report compute-bound while the research question needs Tensor Core, FMA, SFU, TMA, TMEM, L2, HBM, scheduler, or dependency-path detail.

## Risks / Trade-offs

- Too much callback guidance could burden simple GPU topics → Mitigation: split into three entrance skills and recommend topic-scoped registration only for the concerns the topic needs.
- Callback `SKILL.md` may link command pages that resolution does not automatically inline → Mitigation: make each `SKILL.md` explicitly instruct the agent which local command pages to read for the current stage and keep those pages under the callback skill directory.
- Generic guidance could become accidentally FA4-specific → Mitigation: use FA4/B200 only as examples in rationale or README notes, not as normative requirements.
- NCU metric names and counter availability vary across GPU generations → Mitigation: require counter-to-component mapping and evidence-class labeling rather than hard-coding one metric set as universal truth.
- A project-local user-plugin bundle may look installable as a packaged system skill → Mitigation: README and specs state that the bundle is a collection of callback `--skill-dir` sources, not a packaged system skill family.

## Migration Plan

1. Create the `skillset/user-plugins/gpu-analytical-modeling/` directory, README, and manifest.
2. Add the three callback skill directories with valid `SKILL.md` frontmatter and Imsight-style concise workflow routing.
3. Add each skill's command pages under its local `commands/` directory.
4. Add registration examples for topic-scoped and project-scoped callback use.
5. Validate that each callback skill directory contains Imsight-style `SKILL.md`, each prompt file exists, each inline prompt is short static instruction material, and no plugin material contains secret-like or topic-private material.
6. Optionally smoke-test registration and resolution against a temporary topic or project-scope callback registry, then remove or keep only intended registrations.

Rollback is file-level: remove the user-plugin directory or disable callback records that reference it. Existing projects without registrations are unaffected.

## Open Questions

- What exact CLI surface should a future manifest installer use if this recipe proves useful?
- Should architecture-specific supplements, such as Blackwell/B200 metric hints, live as optional command pages inside this plugin or as topic-local callback material?
- Should validation of `skillset/user-plugins/` remain a lightweight filesystem smoke check, since this plugin is not part of the packaged distribution?
