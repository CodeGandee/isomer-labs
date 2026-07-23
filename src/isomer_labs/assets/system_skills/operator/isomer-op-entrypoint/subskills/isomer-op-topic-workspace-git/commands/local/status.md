# Local Status

## Workflow

1. Resolve and validate the Source Topic Workspace, `topic.runtime`, Topic Main, registered Topic Actor Workspaces, and selected-team Agent Workspaces through read-only Isomer queries. Runtime may be missing for status.
2. Run:

```bash
git -C <source-topic-workspace> rev-parse --show-toplevel
git -C <source-topic-workspace> rev-parse --git-dir
git -C <source-topic-workspace> rev-parse --verify HEAD
git -C <source-topic-workspace> status --porcelain=v2 --untracked-files=all
git -C <source-topic-workspace> ls-files --stage
git -C <source-topic-workspace> check-ignore -v --no-index -- <resolved-nested-path-1> <resolved-nested-path-2>
```

3. Inspect each resolved nested repository or worktree for its top level, branch, commit, and dirty boolean with direct path-scoped read-only Git. Do not mutate it.
4. Report repository identity, HEAD, index, working tree, ignore posture, nested exclusions, runtime prerequisite, warnings, blockers, and local state.

An ancestor top level means local tracking is `disabled`, not `enabled`. Invalid `.git` state means `invalid`.

If the request does not map cleanly to these steps, use the native planning tool to build a read-only local status plan, then execute it or report the missing selected context.
