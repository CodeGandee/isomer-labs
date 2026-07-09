## Why

The first Idea Timeline implementation made display keys short, but the `I1` shape reads like a row number and makes hidden/deleted gaps harder to interpret. Timeline search and coloring also need to match the intended exploration workflow: one fuzzy text search like Idea Graph, and row colorization as an opt-in preference rather than visual noise by default.

## What Changes

- Change Research Idea display keys from `I<index>` to `I-<index>` for newly assigned and explicitly repaired keys.
- Keep existing display-key stability rules: keys remain topic-scoped, unique, non-reused after allocation, and independent from visible row position.
- Update graph and timeline presentation so visible idea labels use the `I-<index>` shape.
- Replace the Idea Timeline multi-field search UI with one fuzzy text search bar matching the Idea Graph usage pattern.
- Make fuzzy search match any table-entry field, including display key, title, aliases, one-liner, family, status, relation kind, parent labels, and supporting-record fields used by timeline derivation.
- Keep Supporting Records visibility controlled by the existing flag: search may match supporting rows, but supporting rows are only shown when the flag is enabled.
- Change Idea Timeline row colorization to default off, while keeping Project Settings controls to turn it on and configure primary/supporting colors.
- **BREAKING**: Existing `I<index>` display keys in active Workspace Runtime databases must be explicitly migrated or repaired to `I-<index>` if the operator wants the new visible format on old ideas.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `workspace-runtime-persistence`: Research Idea display-key allocation and repair requirements change from `I<index>` to `I-<index>`.
- `project-web-data-contracts`: GUI read contracts must accept and expose the revised display-key format and timeline fuzzy-search state.
- `project-web-gui`: Idea Timeline search, table matching, visible labels, and supporting-row visibility semantics change.
- `project-web-settings`: Idea Timeline row colorization default changes to off while retaining opt-in configurable colors.
- `topic-graph-read-api`: Topic graph node labels and payload expectations must support the revised display-key format for Idea Graph and Idea Timeline consumers.

## Impact

- Affected backend: Workspace Runtime schema/validation/allocation helpers, Research Idea repair path, topic graph read model, and GUI contract validation.
- Affected frontend: Idea Graph label formatting, Idea Timeline search/filter controls and row derivation, settings defaults, local-storage defaults, tests, and generated static assets.
- Affected data: existing topic runtime databases with old `I<index>` keys need an explicit operator-invoked migration or repair; the GUI must not silently rewrite keys while browsing.
- Dependencies: no new runtime or frontend library dependencies are expected.
