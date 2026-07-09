## Context

`isomer-op-toolbox-mgr` is already documented as an active operator skill and packaged under both `skillset/operator/` and `src/isomer_labs/assets/system_skills/operator/`. The welcome skill is a read-only menu and owner-skill recommendation surface, while the entrypoint skill is the route-and-proceed dispatcher for concrete tasks and CLI-shaped requests.

The current gap is discoverability. Toolbox management exists, but welcome omits it from the owner workflow menu and entrypoint omits it from operator route selection and CLI-family routing.

## Goals / Non-Goals

**Goals:**

- Make project-local Toolbox work visible from `isomer-op-welcome` as an active owner workflow.
- Make concrete Toolbox tasks route through `isomer-op-entrypoint` to `isomer-op-toolbox-mgr`.
- Make explicit Toolbox CLI requests discoverable in entrypoint CLI routing.
- Keep source skillset files and packaged system-skill asset files synchronized.

**Non-Goals:**

- Do not change Toolbox schema, callback registry behavior, Runtime Param resolution, or CLI command implementation.
- Do not make Toolbox work a welcome visible usage path like `start-research-manually`; it is an owner workflow, not a first-run research path.
- Do not route Toolbox work to `isomer-misc-tool-packs`, whose purpose remains installable toolset guidance.

## Decisions

Add Toolbox Manager to welcome as an owner workflow rather than a visible usage path. This keeps the welcome surface consistent: visible usage paths are for common research starts, while owner workflows cover Project, Topic, identity, and Toolbox management.

Add Toolbox Manager to entrypoint's system skill index and routing precedence. Entrypoint owns concrete task dispatch, so it must recognize phrases such as creating a Toolbox, converting a skill into callback material, inserting a callback, listing insertion points, managing Runtime Params, and inspecting effective Toolbox state.

Add Toolbox command families to `cli-index.md`. Explicit CLI requests should route to `isomer-cli project toolboxes ...`, `isomer-cli project skill-callbacks ...`, or `isomer-cli project toolbox-params ...` instead of requiring the operator skill path.

Patch both source and packaged copies. Operator skills live in `skillset/operator/` for source authoring and `src/isomer_labs/assets/system_skills/operator/` for packaged distribution; leaving them divergent would make validation and installed behavior disagree.

## Risks / Trade-offs

- Toolbox might look like another onboarding path → Keep wording as “supported action” or “owner workflow,” not a visible usage path.
- Toolbox CLI routing might bypass owner-skill safety for broad mutations → Preserve the entrypoint rule that workflow-level Toolbox tasks route to `isomer-op-toolbox-mgr`, while explicit CLI command-family requests can use CLI help and safe discovery.
- Source and packaged copies can drift → Update matching files in both trees and validate with repository system-skill asset tests when available.

## Migration Plan

1. Update `isomer-op-welcome` source references and packaged references to include Toolbox Manager in help, options, choose-path, and skill-map guidance.
2. Update `isomer-op-entrypoint` source references and packaged references to include Toolbox Manager in owner-boundary text, input surfaces, routing rules, system skill index, and CLI index.
3. Run focused validation for system skill assets and OpenSpec strict validation for this change.

## Open Questions

None.
