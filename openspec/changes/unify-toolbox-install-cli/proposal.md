## Why

Toolbox installation currently exposes two overlapping install concepts: `project toolboxes install` registers Toolbox identity/status/source, while `project skill-callbacks install` materializes callbacks from the same Toolbox manifest. Users reasonably expect "install this Toolbox" to make the Toolbox effective as a bundle, while still needing lower-level primitives for loose callbacks, runtime params, and migration work that is not packaged as a Toolbox yet.

## What Changes

- Make `project toolboxes install <toolbox-dir>` the canonical high-level operation for installing a Toolbox bundle at Project or topic-owned scope.
- Expand Toolbox installation to validate the Toolbox manifest, upsert the Toolbox registration, install declared callback records, optionally register declared runtime-param default bundles, and report effective callback/runtime-param status.
- Preserve lower-level commands for direct manipulation: `project skill-callbacks register` for loose callback material, `project skill-callbacks install` as a callback-manifest/repair primitive, and `project toolbox-params` for runtime-param definitions, imports, overrides, lookup, and validation.
- Clarify scope semantics across the command families: Toolbox registration and runtime params may use `project`, `research_topic`, `topic_actor`, and `topic_agent` where supported; callback records remain installable at `project` or `research_topic` scope unless callback storage is later expanded.
- Update documentation, help text, tests, and OpenSpec-facing use cases so "Toolbox install" means bundle installation, while primitive commands are described as escape hatches rather than a second user-facing install path.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `toolbox-runtime-configuration`: Toolbox installation semantics change from registration-only to bundle orchestration, while preserving direct registration/status/runtime-param management.
- `toolbox-callback-manifests`: Toolbox callback installation becomes a lower-level primitive used by high-level Toolbox installation, and callback manifest semantics must compose with Toolbox bundle installation.
- `user-skill-callbacks`: Direct callback commands remain available for non-Toolbox or not-yet-Toolbox material, with clear scope and validation behavior.
- `isomer-cli-project-discovery`: CLI help and command grouping must present `project toolboxes install` as the canonical Toolbox install surface and keep primitive command groups discoverable without implying duplicate install concepts.

## Impact

- Affected CLI surface: `project toolboxes install`, `project skill-callbacks install`, `project skill-callbacks register`, `project toolbox-params`, help text, JSON/text output, and examples.
- Affected Python modules: Project CLI command definitions and handlers, Toolbox registration helpers, Toolbox callback installation helpers, runtime-param import helpers, effective Toolbox/callback/runtime-param reporting.
- Affected docs and design artifacts: Toolbox Creator Skill use cases, CLI reference, Toolbox callback manifest docs, runtime-param docs, and any examples that currently instruct users to run separate install commands for one Toolbox.
- Affected tests: CLI tests for Toolbox install at Project and Research Topic scope, callback primitive tests, runtime-param import tests, compatibility tests for existing command behavior, and diagnostics for conflicts or gated Toolbox status.
