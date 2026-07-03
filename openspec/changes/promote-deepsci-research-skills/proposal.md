## Why

The research-paradigm skillset has outgrown the temporary `v1` and `v2` generation model: `v1` is no longer used, while `v2` is the production candidate but still carries suffixes and paths that make it look experimental. Promoting the `v2` skills into a suffixless `deepsci` production surface gives agents one canonical research skillset and removes stale compatibility material.

## What Changes

- **BREAKING** Remove the retired `skillset/research-paradigm/v1/*` skill folders from the active tree instead of preserving them for compatibility.
- **BREAKING** Move the current `skillset/research-paradigm/v2/isomer-rsch-*-v2` skills to `skillset/research-paradigm/deepsci/isomer-rsch-*`.
- **BREAKING** Rename active skill identities, manifests, command examples, placeholder producer and consumer metadata, and routing guidance from `isomer-rsch-*-v2` to `isomer-rsch-*`.
- Rename the skillset manifest group from `deepsci-v2` to `deepsci`.
- Update research-paradigm validation to treat `deepsci` as the only active production generation and to stop requiring `v1`.
- Update operator/admin and CLI documentation that names the research workspace manager or `v2` placeholder binding paths.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `research-paradigm-skills`: Replace the versioned `v1`/`v2` layout with a production `deepsci` layout and suffixless active skill names.
- `research-placeholder-bindings`: Replace active `v2` placeholder-binding references with suffixless `deepsci` skill names and paths.
- `operator-admin-skills`: Update operator boundaries that point research-paradigm bootstrap work to the workspace manager skill.

## Impact

- Affected skillset paths: `skillset/research-paradigm/v1`, `skillset/research-paradigm/v2`, and `skillset/research-paradigm/deepsci`.
- Affected skill identities: every active `isomer-rsch-*-v2` name becomes `isomer-rsch-*`.
- Affected validators and docs: `scripts/validate_research_paradigm_skillset.py`, `scripts/validate_skillsets.py`, `skillset/manifest.toml`, `docs/isomer-cli.md`, research-paradigm README and specs, and operator skill guidance that mentions `isomer-rsch-workspace-mgr-v2`.
- Existing users or agents invoking `v1`, `v2`, or `-v2` names must update to the production `deepsci` path and suffixless skill names.
