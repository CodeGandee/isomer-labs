# Local Commit

## Workflow

1. Require valid Workspace Runtime, enabled local root tracking, an approved exact local plan, a commit message, and explicit approval for every warned file.
2. Recompute repository identity, HEAD, index, ignore file, and approved working-file fingerprints. Stop on stale state or any unexpected staged path. Do not unstage user content.
3. Stage only the approved whole files:

```bash
git -C <source-topic-workspace> add -- <approved-path-1> <approved-path-2>
git -C <source-topic-workspace> diff --cached --name-only -z
git -C <source-topic-workspace> diff --cached --check
```

4. Require the complete staged path set to equal the approved set and recheck staged fingerprints. Then commit:

```bash
git -C <source-topic-workspace> commit -m <approved-message> -- <approved-path-1> <approved-path-2>
git -C <source-topic-workspace> rev-parse HEAD
git -C <source-topic-workspace> status --porcelain=v2 --untracked-files=all
```

5. Persist the resulting local state and report the commit SHA, exact committed paths, remaining worktree state, and warnings.

Do not discover, configure, fetch, pull, or push a remote. Do not inspect or mutate publication state.

If the request does not map cleanly to these steps, use the native planning tool to isolate one exact local commit and stop until the current plan, index scope, warnings, and message are resolved.
