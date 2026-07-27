# Local Tracking Safety

| Area | Rule |
| --- | --- |
| Read-only work | Local status and planning need no runtime mutation |
| Mutating work | Init, ignore, and commit require valid `topic.runtime` and write support only below `<topic.runtime>/topic-git/` |
| Enabled state | Source Topic Workspace must equal `git rev-parse --show-toplevel` |
| Ancestor repositories | Source paths must be absent from ancestor indexes and effectively ignored |
| File selection | Plans use exact whole files |
| Secret warnings | Report path and category without detected values |
| Remote state | Irrelevant to local operations |

Missing runtime routes to its owner; Topic Git does not initialize it.

Before root initialization:

1. Walk only filesystem ancestors.
2. Deduplicate ancestor Git top levels.
3. Prove the Source Topic Workspace and relevant content are absent from every ancestor index.
4. Prove those paths are effectively ignored.

The managed root ignore block excludes:

- Workspace Runtime and `state.sqlite`;
- local environments, caches, logs, temporary surfaces, and credentials;
- canonical external repositories;
- Topic Main, registered Topic Actor Workspaces, and selected-team Agent Workspaces.

Preserve user rules outside the managed block. Already tracked sensitive content is a blocker because ignore rules do not untrack it.

The optional `topic-workspace-local-version.toml` records relative semantic labels, branches, commits, and dirty booleans. It does not preserve uncommitted nested content.

Local operations never discover, add, modify, fetch, pull, or push remotes. They never edit an ancestor ignore file or remove an ancestor index entry.
