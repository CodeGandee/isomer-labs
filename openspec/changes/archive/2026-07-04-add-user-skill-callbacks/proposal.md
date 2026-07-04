## Why

Users need a stable way to add topic- or project-specific instructions to packaged system skills without editing `SKILL.md` files, forking Isomer skill assets, or confusing instruction customization with provider-backed research operation extensions. A generic User Skill Callback contract gives agents a deterministic place to resolve user guidance at the beginning and end of top-level skill workflows while keeping owning skill guardrails intact.

## What Changes

- Introduce User Skill Callback as an instruction-layer customization attached to a system skill name and callback stage.
- Support the initial callback stages `begin` and `end` for top-level skill workflows.
- Add a generic `isomer-cli project skill-callbacks` command group for registering, resolving, listing, showing, disabling, and validating callbacks.
- Support callback sources from an inline prompt, a prompt file, or an external skill directory that contains `SKILL.md`.
- Store callback registry refs as declarative topic/project configuration refs rather than runtime truth, credentials, or executable provider payloads.
- Define deterministic callback resolution, merge, validation, and precedence rules so callbacks are followed as workflow instructions but cannot override higher-priority system, developer, owning-skill, user-request, or Isomer domain constraints.
- Add the first participating skill-family behavior to production `isomer-deepsci-*` skills: each top-level workflow checks `begin` callbacks before workflow-specific work and `end` callbacks before final completion.
- Leave callback participation open for future system skill families without naming future domain extensions as `misc` or baking this mechanism into DeepSci only.

## Capabilities

### New Capabilities

- `user-skill-callbacks`: Defines the User Skill Callback concept, callback stages, registry refs, CLI surface, source validation, deterministic resolution, precedence rules, and participating-skill application contract.

### Modified Capabilities

- `cli-topic-context-resolution`: Allow Research Topic Config and Effective Topic Context to carry User Skill Callback registry refs as declarative instruction-customization refs without treating callback material as runtime truth or provider implementation bodies.
- `isomer-cli-project-discovery`: Expose the generic `project skill-callbacks` command group under `isomer-cli project`.
- `research-paradigm-skills`: Require production `isomer-deepsci-*` top-level workflows to resolve and apply User Skill Callbacks at `begin` and `end` stages during the first rollout.

## Impact

- Affected CLI: `src/isomer_labs/cli/` gains a generic project-scoped `skill-callbacks` surface with JSON-friendly outputs and deterministic diagnostics.
- Affected config: Research Topic Config parsing and validation recognize callback registry refs while continuing to reject runtime state, secret material, and executable provider payloads in config files.
- Affected assets: initial participating `src/isomer_labs/assets/system_skills/research-paradigm/deepsci/isomer-deepsci-*/SKILL.md` files gain concise callback resolution guidance.
- Affected validation and tests: project config validation, CLI tests, system-skill validation, and DeepSci skill validation cover callback registry shape, callback source checks, command output, and participating-skill instructions.
- No breaking change is intended for existing projects without callback registry refs; participating skills treat missing callbacks as an empty successful resolution.
