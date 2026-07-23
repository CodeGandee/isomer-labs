# Local Plan

## Workflow

1. Resolve the selected Source Topic Workspace, nested semantic workspace roots, and optional Workspace Runtime. Planning is read-only; missing runtime is a mutation prerequisite, not a planning blocker.
2. Inspect root repository identity, HEAD, complete index, working tree, and root `.gitignore` fingerprints with direct path-scoped Git.
3. Inventory root-owned material without entering resolved nested workspace or canonical repository roots. Classify exact whole files as track, ignore, warning, or blocker. Default runtime, `state.sqlite`, local environments, caches, logs, temporary paths, credentials, and nested workspaces to ignore.
4. Scan exact candidates for secret-like content. Report only path and risk category, never the detected value. Require explicit local-history approval for warned files.
5. Optionally render `topic-workspace-local-version.toml` from read-only nested branch, commit, and dirty evidence. State its pointer-only limitation.
6. Return exact proposed ignore rules, files to stage, commit grouping, repository fingerprint, warnings, blockers, and required approvals. Do not modify or stage a file.

Publication state and remote refs do not enter the local plan fingerprint.

If the request does not map cleanly to these steps, use the native planning tool to build a read-only exact-file planning procedure and report any missing selection or approval boundary.
