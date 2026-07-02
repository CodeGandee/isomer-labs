## 1. Create the Tool-Pack Skill

- [x] 1.1 Initialize `skillset/misc/isomer-misc-tool-packs/` with `SKILL.md`, `agents/openai.yaml`, and `references/`.
- [x] 1.2 Write `SKILL.md` as a lean resolver for `install toolset <name>` and related named-toolset requests.
- [x] 1.3 Add `references/tool-packs.md` with canonical pack definitions, aliases, included packs, required tools, optional tools, verification checks, blockers, and helper-skill routes.
- [x] 1.4 Define initial packs for `paper-writing`, `paper-figures-python`, `paper-figures-r`, `paper2ppt`, `paper-citation`, `cuda-build`, `torch-gpu`, and `topic-python-starter`.
- [x] 1.5 Ensure `paper-writing` includes `paper-figures-python` by default and keeps `paper-figures-r` opt-in.
- [x] 1.6 Classify pack entries by dependency kind so CLI tools prefer `uv tool install`, then `pixi global install`, while importable Python packages target the Topic Workspace Pixi environment.

## 2. Preserve Manual Invocation Boundary

- [x] 2.1 Configure `skillset/misc/isomer-misc-tool-packs/agents/openai.yaml` so implicit invocation is disabled.
- [x] 2.2 State in `SKILL.md` that service, operator, and research workflow skills should not route to the tool-pack skill automatically yet.
- [x] 2.3 Preserve setup ownership of Pixi mutation, enclosure policy, topic-local fallback, no-sudo blockers, and readiness verification by returning contracts instead of installing.
- [x] 2.4 Keep service environment setup guidance free of `isomer-misc-tool-packs` routing until automatic routing is explicitly designed.

## 3. Register and Validate

- [x] 3.1 Add `misc/isomer-misc-tool-packs` to the core skillset manifest.
- [x] 3.2 Validate the new skill frontmatter and `agents/openai.yaml` metadata.
- [x] 3.3 Run repository skill validators relevant to misc, service, operator, and research skill boundaries.
- [x] 3.4 Run OpenSpec validation for `add-misc-tool-packs` in strict mode.
- [x] 3.5 Inspect active operator and research-paradigm v2 skill text to confirm the new implementation does not add cross-boundary references from operator skills to research-paradigm v2 paper-writing skills.
