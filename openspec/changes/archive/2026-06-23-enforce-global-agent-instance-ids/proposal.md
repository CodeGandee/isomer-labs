# Enforce Globally Unique Agent Instance ids

## Why

ADR 0023 accepted that Agent Instance ids are globally unique by design and that Agent Workspaces use the flat layout `<topic-workspace>/agents/<agent-instance-id>/`. The current implementation in `src/isomer_labs/runtime/store.py` generates team-scoped ids such as `{team_id}-{role}`, and tests/profile fixtures still reference the old placeholder layout `agent-workspaces/<profile>/<role>`. This drift blocks Project-level validation, risks workspace path collisions, and contradicts the accepted architecture.

## What Changes

- Change Agent Instance id generation to produce globally unique ids across the Project.
- Update Agent Workspace path planning to derive paths from the globally unique Agent Instance id.
- Add Workspace Runtime validation that rejects duplicate Agent Instance ids at the Project level.
- Update existing unit tests and profile fixtures to remove the stale `agent-workspaces/<profile>/<role>` placeholder references.
- Keep the default Agent Workspace path as `<topic-workspace>/agents/<agent-instance-id>/`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `workspace-runtime-persistence`: add the requirement that Agent Instance ids are globally unique and that Workspace Runtime validates uniqueness across the Project.

## Impact

- `src/isomer_labs/runtime/store.py`: Agent Instance id generation and Agent Workspace creation.
- `src/isomer_labs/runtime/validation*.py`: add cross-project duplicate Agent Instance id checks.
- `tests/unit/test_isomer_cli.py`: update profile fixtures and assertions that use the old `agent-workspaces/<profile>/<role>` layout.
- `src/isomer_labs/paths.py`: no functional change, but the resolver now receives globally unique ids as intended.
