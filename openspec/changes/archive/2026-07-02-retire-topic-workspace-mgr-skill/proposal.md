## Why

The rename to `isomer-admin-topic-mgr` has migrated active routing away from `isomer-admin-topic-workspace-mgr`, so keeping a callable compatibility wrapper now teaches the wrong entrypoint and keeps obsolete command names alive. Removing the old skill entirely makes the operator surface unambiguous: initialized-topic management belongs only to `isomer-admin-topic-mgr`.

## What Changes

- **BREAKING**: Remove `skillset/operator/isomer-admin-topic-workspace-mgr/` entirely instead of keeping it as a deprecated compatibility wrapper.
- **BREAKING**: Users and skills must no longer invoke `$isomer-admin-topic-workspace-mgr` or retired subcommands such as `topic-workspace`, `resolve-workspace`, `manage-actors`, `plan-agents`, `create-worktrees`, `validate-worktrees`, or `install-packages`.
- Update active routing, manifest entries, operator documentation, validator checks, and unit fixtures so `isomer-admin-topic-mgr` is the only initialized-topic management skill.
- Replace wrapper-acceptance validation with retirement validation that rejects a revived `isomer-admin-topic-workspace-mgr` folder or user-facing routing guidance.
- Keep historical OpenSpec archive material as history, but ensure active specs, active skill docs, and validation-facing fixtures no longer present the old skill as callable.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `topic-workspace-manager-skill`: Retire the old skill completely; the repository must not keep a compatibility wrapper or executable route for `isomer-admin-topic-workspace-mgr`.
- `operator-admin-skills`: Remove the old workspace-manager wrapper from active operator inventory, routing guidance, manifest expectations, and validator acceptance.

## Impact

- Deletes `skillset/operator/isomer-admin-topic-workspace-mgr/`.
- Updates `skillset/manifest.toml`, `skillset/operator/README.md`, and any active skill routing text that still names the old skill.
- Updates `scripts/validate_skillsets.py` and `tests/unit/test_validate_skillsets.py` so validation rejects the old folder instead of checking wrapper mappings.
- Updates OpenSpec delta specs and tasks so the completed rename is followed by full retirement rather than wrapper retention.
