## Why

The compacted skill packs expose execution entrypoints but no independent newcomer surface that teaches what each pack is designed to do, which task language maps to which route, or how to form a reliable entrypoint request. Users should be able to invoke a read-only welcome skill first, learn representative usage patterns and canonical commands, and then move deliberately to the pack's execution entrypoint.

## What Changes

- **BREAKING** Restore `isomer-op-welcome` as an independently discoverable top-level core skill instead of protected member `isomer-op-entrypoint->welcome`, and stop treating the core entrypoint as the owner of welcome procedure resources.
- Add independently discoverable `isomer-ext-deepsci-welcome` and `isomer-ext-kaoju-welcome` skills beside their existing `isomer-ext-*-entrypoint` execution skills.
- Give each welcome skill a read-only, newcomer-oriented default experience that explains the pack's purpose, representative workflows, required context, canonical public command ids, natural-language routing cues, exact invocation examples, expected action, mutation posture, and next step.
- Require a curated typical-use-case guide plus a complete command-and-intent map. The guide must adapt pack metadata into useful teaching language rather than copy entrypoint tables or subskill frontmatter verbatim.
- Keep welcome and execution roles explicit: welcome skills orient and recommend; entrypoint skills interpret a selected command or concrete task and proceed through protected members or report a blocker.
- Preserve existing entrypoint names and protected capability ids. Empty entrypoint invocation and existing entrypoint help or onboarding command forms delegate to the independent welcome skill for at least one minor release, but welcome content has one public owner.
- Evolve the packaged catalog from one public skill per pack to an ordered public-skill inventory with exactly one execution entrypoint and one welcome skill per core or extension pack. Protected capabilities remain nested under the execution entrypoint.
- Make group, extension, and public-skill selectors resolve to a complete pack so installation, upgrade, status, receipt integrity, and uninstall handle both public projections atomically.
- Advance managed receipt and inspection contracts so a pack is verified only when all declared public skills and all protected entrypoint members are present, correctly identified, version-compatible, and receipt-owned.
- Update installation and user documentation to recommend the relevant welcome skill for newcomers and the corresponding entrypoint for informed task execution.
- Extend validation and tests to enforce independent welcome layout, identity, read-only posture, use-case teaching quality, command coverage, pack membership, projection migration, and entrypoint handoff consistency.

## Capabilities

### New Capabilities

- `pack-welcome-skills`: Defines the independent core, DeepSci, and Kaoju welcome skills, their newcomer teaching contract, typical-use-case and command-map content, read-only behavior, and handoff to execution entrypoints.

### Modified Capabilities

- `packaged-system-skills`: Allow each pack to declare multiple public skills with distinct welcome and entrypoint roles while retaining protected capabilities below the entrypoint.
- `system-skill-installer-cli`: Select, project, receipt, inspect, upgrade, and uninstall every public skill in a pack as one managed unit.
- `system-skill-namespaces`: Reserve `isomer-op-welcome` and `isomer-ext-<extension-id>-welcome` as public welcome identities alongside public entrypoint identities.
- `packaged-system-skill-template-format`: Validate welcome-specific structure, self-contained resources, teaching tables, command coverage, and cross-surface handoffs.
- `isomer-op-entrypoint-skill`: Remove welcome as a protected owner route and keep the entrypoint focused on informed-user route-and-proceed execution, with bounded compatibility delegation for former welcome commands.
- `isomer-admin-welcome-skill`: Restore the core welcome capability as an independent public skill and redefine its default output around newcomer education and concrete usage patterns.
- `operator-admin-skills`: Expose both `isomer-op-welcome` and `isomer-op-entrypoint` as top-level core skills while leaving other operator owners protected.
- `isomer-deepsci-pipeline`: Add a separate DeepSci welcome surface while retaining `isomer-ext-deepsci-entrypoint` as the execution entrypoint and protected-member owner.
- `kaoju-research-extension`: Add a separate Kaoju welcome surface while retaining `isomer-ext-kaoju-entrypoint` as the execution entrypoint and protected-member owner.
- `research-paradigm-skills`: Include and validate independent extension welcome skills in the production DeepSci and Kaoju pack layouts.
- `isomer-internal-system-skill-inspection`: Report each public skill and require complete welcome, entrypoint, and protected-member evidence before classifying a pack as verified.
- `isomer-documentation-system-guide`: Teach welcome-first onboarding separately from informed entrypoint execution in installation, quickstart, and packaged-skill guidance.

## Impact

The change affects packaged skill assets, manifest parsing and catalog models, public-skill identity normalization, materialization, CLI selection, managed receipts and migration, explicit-root and live-inventory inspection, extension discovery output, callback catalog ownership metadata, validators, user documentation, and installer tests. Existing `isomer-op-entrypoint`, `isomer-ext-deepsci-entrypoint`, and `isomer-ext-kaoju-entrypoint` invocation names remain valid; protected logical ids and Project extension ids remain stable. Managed upgrades must create the three new top-level welcome projections, remove the nested core welcome only after replacement validation, preserve unrelated or untracked paths, and require an agent-host refresh before newly projected welcome skills become discoverable.
