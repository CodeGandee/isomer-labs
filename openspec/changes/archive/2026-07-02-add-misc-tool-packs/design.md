## Context

Isomer currently has good environment setup primitives: topic env setup owns Pixi mutation and verification, package repository resolution owns mirrors and channels, package specifics owns named-package caveats, NVIDIA tools owns CUDA/C++ environment preferences, and bounded-run tips owns resource-risk handling. What is missing is a manually invoked layer between user-facing task names and raw dependencies. A user can reasonably ask to "install toolset paper-writing", but the current flow has no stable catalog for what that means.

Recent paper-writing skill review surfaced recurring external tool groups: LaTeX/Tectonic manuscript builds, Python figure generation, optional R figure generation, paper-to-PPT generation, citation retrieval, CUDA builds, and PyTorch GPU execution. These are cross-cutting misc/setup concerns, not operator concerns and not research-paradigm v2-specific knowledge.

## Goals / Non-Goals

**Goals:**

- Add a misc skill that resolves named toolsets into dependency contracts.
- Make `paper-writing` a composite pack that includes `paper-figures-python` by default.
- Keep pack definitions v2-independent and task-oriented.
- Keep actual installation with the setup owner after the user chooses to act on the returned contract.
- Preserve existing package-source, NVIDIA, PyTorch, bounded-run, and repository-resolution ownership.

**Non-Goals:**

- Do not create a second installer.
- Do not mutate Topic Workspace Pixi environments from the misc tool-pack skill.
- Do not route to the misc tool-pack skill automatically from service, operator, or research workflow skills yet.
- Do not make operator skills reference research-paradigm v2 skills.
- Do not make research-paradigm v2 skills reference the misc pack catalog directly as an implementation dependency.
- Do not install both Python and R figure stacks for paper writing by default.

## Decisions

### Tool Packs Are Dependency Contracts, Not Installers

`isomer-misc-tool-packs` should resolve pack names and aliases into a structured contract containing required tools, optional tools, preferred package sources, verification checks, blockers, and routes to existing helper skills. It should stop at the contract boundary.

Alternative considered: put install commands directly in the new skill. That would duplicate `isomer-srv-topic-env-setup`, bypass environment enclosure policy, and make it harder to keep install evidence in `topic.env.topic_setup_target_spec`.

### Manual Invocation First

`isomer-misc-tool-packs` should be available when the user explicitly invokes it or directly asks to resolve a named toolset. Service, operator, and research workflow skills should not route to it automatically yet. When a user wants to proceed after seeing a contract, the contract can be handed to the setup owner as explicit planning context.

Alternative considered: have topic env setup consume pack contracts automatically during target-spec derivation and install planning. That is useful later, but for this slice it would broaden the routing surface before the catalog has settled.

### CLI Tools Prefer User Tool Installs

Pack contracts should distinguish CLI tools from importable Python packages. For CLI tools, the preferred install route is `uv tool install <package>` when `uv` is available and PyPI has the package. If the uv tool route is unavailable, unsuitable, or cannot expose the desired command, the fallback is `pixi global install <package>`. Importable Python packages and libraries needed by the runnable target still belong in the selected Topic Workspace Pixi environment.

Alternative considered: install every CLI into the Topic Workspace Pixi environment. That keeps everything project-local, but it mixes user-facing command tools with project import dependencies and makes common CLI tools harder to reuse across topics.

### Paper Writing Is Composite and Python-First for Figures

`paper-writing` should include manuscript-build, citation-bibliography, and `paper-figures-python`. `paper-figures-python` remains independently installable for figure-only tasks. `paper-figures-r` remains opt-in because the Nature figure workflow gates backend selection on Python versus R.

Alternative considered: define `paper-writing` as LaTeX-only. That would underfit the real paper-writing tool surface, where first-pass figures are part of the normal manuscript path.

### Pack Catalog Uses Progressive Disclosure

Keep `SKILL.md` as a small router with aliases and output shape. Put initial pack definitions in `references/tool-packs.md`. This matches existing misc skill patterns and keeps token cost low until a named pack is requested.

Alternative considered: one large `SKILL.md`. That would make the trigger expensive and bury the resolver workflow inside package tables.

## Risks / Trade-offs

- Pack drift → Keep pack definitions explicit and route package-specific caveats to existing helper skills instead of copying details.
- Over-installation → Keep narrower packs available and make composite inclusion visible in the returned contract.
- Ambiguous user pack names → Define aliases, report the canonical pack name, and block when two packs plausibly match.
- CLI reuse versus enclosure → Prefer user-level CLI installs for CLI commands, while preserving Topic Workspace Pixi installs for importable Python packages and target runtime libraries.
- Platform-specific package availability → Treat package lists as install intent, not proof; let topic env setup, package repo resolution, and package specifics choose reachable sources.
- Research-skill coupling returns → State in both design and spec that pack names are task-level setup vocabulary, not research-paradigm v2 skill references.

## Migration Plan

1. Add `skillset/misc/isomer-misc-tool-packs/` with a concise `SKILL.md`, `agents/openai.yaml`, and `references/tool-packs.md`.
2. Add the new skill to `skillset/manifest.toml` core group.
3. Set `agents/openai.yaml` so implicit invocation is disabled.
4. Validate the new skill with the skill validator and run boundary searches to confirm service, operator, and research workflow skills do not route to it.
5. Roll back by removing the new skill and manifest entry; no runtime data migration is required.

## Open Questions

- Should `paper-citation` include any concrete command-line tools in the first version, or should it stay as service/API capability notes until a specific package is chosen?
- Should `paper-writing` include `pdfcrop` as required because the NeurIPS template Makefile uses it, or optional because Tectonic-first builds may not need it?
