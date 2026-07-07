# GPU Analytical Modeling User-Plugin Feature Requirement

## Goal

Create a project-local user-plugin named `gpu-analytical-modeling` at `skillset/user-plugins/gpu-analytical-modeling` that supplies User Skill Callback instruction material for GPU performance research. The plugin should steer participating DeepSci system skills toward hardware-grounded analytical models: explicit equations, stated assumptions, measurable validation, and source trails for GPU internal architecture and execution behavior.

The first useful version should make agents treat an analytical model as a falsifiable white-box explanation of runtime, throughput, saturation, and bottlenecks, not as a black-box fit or prose-only intuition. It should help a Project Operator Session register the callback skills against chosen system skills and stages through the existing `isomer-cli project skill-callbacks` mechanism.

## Non-Goals

- Do not implement a new callback registry, plugin installer, or first-class user-plugin runtime unless a later design stage decides that current `--skill-dir` registration is insufficient.
- Do not execute benchmarks, collect Nsight Compute traces, run AccelSim, or mutate Topic Workspace records as part of the callback material itself.
- Do not make the plugin override system instructions, developer instructions, owning system skill rules, current user requests, evidence Gates, validation obligations, or Isomer domain constraints.
- Do not encode one fixed GPU, kernel, paper, or Topic Workspace as the only supported target.
- Do not accept curve fitting, learned regression, or generic roofline commentary as sufficient proof of an analytical model.

## Users And Workflows

- Project Operator Session: creates or updates `skillset/user-plugins/gpu-analytical-modeling`, reviews the callback skills, and registers selected callback directories with `pixi run isomer-cli --print-json project skill-callbacks register`.
- Research agent: resolves begin and end callbacks for the owning DeepSci system skill, then uses the returned instructions to shape source discovery, model construction, experiment design, analysis, review, and final reporting.
- Research reviewer: uses the plugin's evidence and model-quality checklist to decide whether a proposed GPU analytical model is explanatory, falsifiable, and sufficiently validated for the Research Topic.
- Project user: injects local preferences for GPU analytical modeling into a topic without editing packaged system skills or making the preference global to unrelated research.

Primary workflow:

1. The Project Operator Session creates the user-plugin directory under `skillset/user-plugins/gpu-analytical-modeling`.
2. The plugin exposes one or more callback skill directories, each with a `SKILL.md` body that can be used as `--skill-dir` source material for a User Skill Callback.
3. The Project Operator Session registers topic-scoped or project-scoped callbacks for target DeepSci system skills and stages, using callback ids that name the modeling concern and target stage.
4. During a participating workflow, the system skill resolves begin callbacks after mandatory entry checks and resolves end callbacks after tentative outputs exist.
5. The research agent follows the plugin instructions within the owning skill's authority, reports conflicts, and records analytical-model assumptions, equations, validation evidence, and unresolved gaps in its normal artifacts.

## Functional Requirements

- The user-plugin shall live at `skillset/user-plugins/gpu-analytical-modeling`.
- The plugin shall include a README that explains the plugin purpose, supported callback skill directories, expected target system skills, suggested registration commands, and topic versus project scope guidance.
- Each callback skill directory shall contain a `SKILL.md` that is valid as a `project skill-callbacks register --skill-dir <dir>` source.
- The plugin shall define at least three callback concerns: model expectation, evidence gate, and source priority.
- The model expectation callback shall define what counts as a GPU analytical model: named inputs, explicit outputs, dimensional units, equations, architectural terms, data movement, execution stages, occupancy or scheduling assumptions, calibration parameters, and a validity envelope.
- The model expectation callback shall prefer decomposed models that separate memory movement, compute pipelines, synchronization, occupancy, scheduling, cache behavior, tensor-core or CUDA-core issue limits, and launch or pipeline overhead when those components are relevant.
- The model expectation callback shall require each model term to map to either a measured quantity, a hardware specification, a cited source, a small calibrated parameter, or an explicit assumption.
- The model expectation callback shall ask agents to state math shape: component equations, max or saturation operators, piecewise regimes, bottleneck selection logic, uncertainty bounds, and units.
- The plugin shall reject pure black-box regression, ungrounded coefficient fitting, vague "memory bound" labels, and roofline-only explanations unless they are explicitly marked as baselines rather than the analytical model.
- The evidence gate callback shall define tests that can support or falsify the model, including held-out configurations, saturation probes, component ablations, microbenchmarks, runtime error bounds, counter trend checks, and bottleneck agreement checks.
- The evidence gate callback shall ask agents to separate calibration data from validation data and to report when evidence is missing, noisy, contradicted, or only suggestive.
- The evidence gate callback shall include pass/fail guidance for analytical claims: predicted runtime or throughput tolerance, correct bottleneck regime, correct monotonic trends under controlled perturbations, and consistency with relevant profiler counters.
- The source priority callback shall direct agents toward local topic context first, then authoritative GPU architecture and tooling sources, then implementation sources, then simulator or research infrastructure sources.
- The source priority callback shall name AccelSim or GPGPU-Sim as sources for internal architecture concepts and execution-path reasoning when appropriate, while treating simulator behavior as supporting evidence rather than vendor truth.
- The source priority callback shall include NVIDIA architecture whitepapers, CUDA programming documentation, PTX and SASS references, Nsight Compute documentation, kernel source code, benchmark scripts, FlashAttention and related kernel papers, and local Topic Workspace artifacts as preferred sources when relevant.
- The plugin shall include a suggested callback-target map for DeepSci skills such as `isomer-deepsci-scout`, `isomer-deepsci-analysis`, `isomer-deepsci-experiment`, `isomer-deepsci-review`, `isomer-deepsci-write`, `isomer-deepsci-baseline`, and `isomer-deepsci-science`.
- The plugin shall distinguish begin-stage instructions from end-stage instructions: begin callbacks should shape source search, model framing, and experiment plans; end callbacks should check whether tentative outputs include equations, assumptions, evidence, limitations, and unresolved gaps.
- The plugin shall document how to register callbacks as topic-scoped for a single Research Topic and project-scoped for general GPU modeling preference.
- The plugin shall keep callback bodies free of credentials, API keys, benchmark-private results, and large copied source documents.
- The plugin shall provide enough structure for later usecase and interface design to decide whether a manifest file, registration helper, or validation command is needed.

## System Boundaries

- In scope: project-local callback skill material under `skillset/user-plugins/gpu-analytical-modeling`, documentation for registering it with existing User Skill Callback commands, and quality criteria for GPU analytical modeling.
- In scope: guidance that participating agents consume through existing `begin` and `end` callback resolution.
- In scope: reusable preferences for white-box GPU performance models across topics such as FlashAttention runtime modeling, kernel comparison, and architecture-sensitive bottleneck analysis.
- Out of scope: changing packaged DeepSci system skill bodies, changing User Skill Callback storage semantics, adding a plugin marketplace, launching agents, running experiments, or writing topic-specific research conclusions.
- Out of scope: treating AccelSim, GPGPU-Sim, or any simulator as the canonical source of real hardware behavior without calibration against measurements and vendor documentation.

## Operational Constraints

- The feature must stay compatible with current User Skill Callback rules: target one active packaged system skill, choose `begin` or `end`, resolve scope through project or Research Topic registries, and use `prompt`, `prompt_file`, or `skill_dir` sources.
- Callback instructions must be supplemental and subordinate to the owning system skill, shared DeepSci constraints, current user prompt, evidence rules, Gates, validation, and recording obligations.
- Topic-scoped callbacks must resolve before project-scoped callbacks according to current callback resolution behavior.
- The plugin should not rely on network access at callback resolution time; it should name source classes and preferred repositories rather than requiring live fetches inside the callback.
- The plugin should be useful even when a Research Topic lacks all desired evidence by making gaps explicit instead of blocking ordinary progress.
- Callback ids and directory names should be stable, lowercase, and descriptive enough for registry inspection.
- Markdown should remain readable as source material and should avoid large embedded tables or copied documentation.

## Assumptions

- The existing `project skill-callbacks register --skill-dir` flow is sufficient for the first version, so a user-plugin can be represented as a curated set of callback skill directories plus documentation.
- The initial users care most about GPU white-box runtime and bottleneck modeling for modern accelerator kernels, especially FlashAttention-style workloads, but the plugin should generalize to other CUDA and GPU performance studies.
- DeepSci skills already resolve User Skill Callbacks at begin and end stages, so this feature can inject preferences without modifying the packaged skills.
- A useful analytical model can mix first-principles equations, small calibrated constants, and bounded empirical checks when each part is named and justified.
- AccelSim is useful as a source of architectural and execution-path concepts, but real-hardware documentation and measurements remain necessary for claims about specific GPUs.

## Open Questions

- Which exact callback skill directories should the first implementation create: one combined callback, one per concern, or begin/end variants for each concern?
- Should the plugin include a small manifest that maps callback directories to target system skills and stages, even if the current CLI does not consume it?
- Which DeepSci skills should receive default registration examples for GPU analytical modeling, and should any be intentionally excluded?
- What default numerical tolerances should the evidence gate suggest for runtime prediction, throughput prediction, counter trend agreement, and bottleneck classification?
- Should architecture-specific profiles, such as Blackwell or B200 guidance, live inside this plugin now or in topic-specific callback material later?
- Should the plugin include reusable checklists for Nsight Compute counter selection, microbenchmark design, and calibration or validation splits?
