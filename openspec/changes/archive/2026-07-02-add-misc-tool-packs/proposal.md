## Why

Users can ask for task-level toolsets such as `paper-writing`, but there is no stable catalog for what those names mean. A manually invoked tool-pack catalog gives agents a stable way to translate user phrases like "install toolset paper-writing" into installable dependency contracts without coupling operator, service, or research skills to specific paper-writing tool details.

## What Changes

- Add a new manually invoked misc skill, `isomer-misc-tool-packs`, that resolves named toolsets into dependency/tool contracts.
- Define initial packs for paper authoring, Python figures, R figures, paper-to-PPT, CUDA build support, PyTorch GPU support, and the existing topic Python starter set.
- Make `paper-writing` a composite pack that includes manuscript build tools, citation/bibliography support, and `paper-figures-python` by default.
- Keep tool-pack resolution separate from installation: the misc skill returns contracts, while the setup owner owns Pixi mutation, enclosure, package-source checks, and verification after the user asks to proceed.
- Define CLI tool installation preference as `uv tool install` first when `uv` is available and PyPI has the CLI package, `pixi global install` second when the uv tool path does not work, and Topic Workspace Pixi dependencies for Python libraries/packages.
- Keep service, operator, and research workflow skills from routing to the new skill automatically for now.

## Capabilities

### New Capabilities
- `isomer-misc-tool-packs-skill`: Resolve named installable toolsets into dependency contracts, aliases, required and optional tools, verification expectations, and routes to existing package/setup helper skills.

### Modified Capabilities
- None. This change intentionally avoids automatic service, operator, or research workflow routing.

## Impact

- Affects `skillset/misc/` by adding a new skill folder with `SKILL.md`, `agents/openai.yaml`, and a focused tool-pack reference.
- Affects `skillset/manifest.toml` so the new misc skill is packaged with the core skillset.
- Does not add a new installer, mutate service setup guidance, mutate research-paradigm v2 skills, or make operator skills reference research-paradigm v2 specifics.
