## Why

The topic-main agent guidance introduced by `inject-topic-main-agent-guidance` currently duplicates the same Markdown body across service and operator skill documentation. That makes the guidance hard to update safely and invites drift between setup, inspection, repair, and validation behavior.

## What Changes

- Move the canonical topic-main guidance body into a packaged Jinja2 template asset under `src/isomer_labs/assets/...`.
- Add an `isomer-cli project topic-main-guidance` command group that renders, inspects, and ensures the root `AGENTS.md` and `CLAUDE.md` guidance block for a selected Topic Main Development Repository.
- Keep large guidance prose out of Python code; Python code supplies only marker constants, template resource names, rendering context, inspection, and upsert logic.
- Update topic env setup and Topic Manager skill instructions so they call the CLI guidance commands instead of copying the injected Markdown body.
- Update validation so skill docs must route through the CLI source of truth and must not re-embed the full guidance body.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `isomer-cli-project-discovery`: Add project-scoped topic-main guidance rendering, inspection, and ensure commands backed by a packaged `.j2` template asset.
- `topic-main-development-repository`: Make the root `AGENTS.md` and `CLAUDE.md` guidance content source explicit: the CLI-rendered template is the source of truth.
- `isomer-service-env-setup-skill`: Topic environment setup must invoke or route to the CLI guidance ensure command instead of carrying the full guidance body.
- `topic-manager-skill`: Topic Manager storage inspection and repair must invoke or route to the CLI guidance inspect/ensure commands instead of carrying the full guidance body.

## Impact

- Affected code: `src/isomer_labs/cli/app.py`, `src/isomer_labs/cli/commands/project.py`, a new topic-main guidance module, and a new packaged `.j2` asset under `src/isomer_labs/assets/`.
- Affected tests: CLI tests for render/inspect/ensure behavior and skillset validation tests that prevent copied guidance bodies from reappearing in skill docs.
- Affected skills: `isomer-srv-topic-env-setup` and `isomer-admin-topic-mgr`.
- No new dependency is required because the project already depends on Jinja2.
