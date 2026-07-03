## Why

Topic-local agents and actors often start by reading repository rule files such as `AGENTS.md` or `CLAUDE.md` inside the Topic Main Development Repository. Those files need Isomer-specific operating guidance, especially that the repository uses Pixi as the primary package manager and that topic-specific facts should be queried through `isomer-cli`, without freezing concrete topic, actor, agent, or external path details into tracked prose.

## What Changes

- Add an Isomer-managed fenced guidance block to root-level `AGENTS.md` and `CLAUDE.md` in each Topic Main Development Repository.
- Create those rule files when they do not exist, and append or update the Isomer block when they already exist.
- State that Pixi is the primary package manager and execution environment, Python must be invoked through Pixi, and system Python, ambient virtualenvs, plain `python`, and plain `pip` should not be treated as the source of truth.
- Direct agents to query topic-specific context, paths, and actor information with `isomer-cli` rather than hardcoding topic ids, actor names, agent names, Pixi bindings, runtime paths, credentials, or external repository paths.
- Add inspection and repair guidance through the Topic Manager so operators can detect and refresh missing or stale guidance blocks after initial setup.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `isomer-service-env-setup-skill`: Topic environment setup now ensures topic-main agent rule guidance during Topic Main Development Repository preparation.
- `topic-main-development-repository`: Topic-main repositories now carry tracked, idempotent `AGENTS.md` and `CLAUDE.md` guidance files with Isomer-specific Pixi and CLI rules.
- `topic-manager-skill`: Topic Manager storage inspection reports the guidance block posture and offers an explicit repair route for missing or stale blocks.

## Impact

- Affected skills: `skillset/service/isomer-srv-topic-env-setup` and `skillset/operator/isomer-admin-topic-mgr`.
- Affected specs: topic environment setup, Topic Main Development Repository behavior, and Topic Manager storage inspection or repair.
- No new runtime dependency is required.
- Existing topic-main repositories may receive appended or updated tracked Markdown files, but unrelated user-authored content in those files must be preserved.
