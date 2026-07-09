## Why

Toolbox skills are intended to be routed to by callback prompts or invoked manually by an operator or agent. Treating them as normal implicit auto-invocation skills makes Toolbox behavior harder to predict and conflicts with the callback contract, which treats callback material as supplemental instruction rather than automatic skill execution.

## What Changes

- Revise `isomer-op-toolbox-mgr` guidance so newly authored Toolbox skills default to routed or manual invocation.
- Make Toolbox Manager source scaffolding create `agents/openai.yaml` metadata with `allow_implicit_invocation: false` for Toolbox skills by default.
- Prefer prompt-file callback routers that say which installed Toolbox skill and subcommand to invoke for a purpose.
- Allow skill-directory callback sources only as an explicit exception for supplemental instruction material, not as automatic skill execution.
- Update existing project-local Toolbox skills so their metadata declares routed/manual invocation by default.

## Capabilities

### New Capabilities

- `isomer-op-toolbox-mgr-skill`: operator skill guidance for Toolbox authoring, conversion, callback insertion, and source scaffolding defaults.

### Modified Capabilities

- `gpu-analytical-modeling-toolbox`: existing project-local Toolbox prior skills declare non-implicit routed/manual invocation metadata.
- `user-skill-callbacks`: callback guidance remains explicit that callback material is supplemental instruction, and Toolbox-authored skill routing must not imply automatic skill execution.

## Impact

- Affected assets: `src/isomer_labs/assets/system_skills/operator/isomer-op-toolbox-mgr/` and current project-local Toolbox skills under `skillset/toolboxes/`.
- Affected docs/specs: OpenSpec contracts for Toolbox Manager guidance, GPU analytical modeling Toolbox skill metadata, and User Skill Callback wording.
- No callback resolver, Toolbox manifest schema, installed registry format, or CLI behavior changes are required.
