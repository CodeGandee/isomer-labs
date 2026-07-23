# Topic Git Status

## Workflow

1. Resolve one selected Project, Research Topic, and Source Topic Workspace through the read-only context sequence. Resolve `topic.runtime` only to inspect existing support; do not initialize it.
2. Inspect local repository identity:

```bash
git -C <source-topic-workspace> rev-parse --show-toplevel
git -C <source-topic-workspace> rev-parse --git-dir
git -C <source-topic-workspace> rev-parse --verify HEAD
git -C <source-topic-workspace> status --porcelain=v2 --untracked-files=all
git -C <source-topic-workspace> ls-files --stage
```

3. Report local `disabled` when the Source Topic Workspace is not itself the top level, including when an ancestor Project repository contains it. Report `enabled` only for a valid root repository and `invalid` for corrupt or conflicting root Git control state.
4. Inspect schema-valid runtime or copy-local publication binding, copy existence, last projection manifest, conflicts, and outcomes. Do not require local tracking and do not promote copy-local state during status.
5. Report publication as `disabled`, `prepared`, `synchronized`, `stale`, `copy-missing`, or `blocked`.
6. Return separate blockers and next actions for each layer without mutation.

If a command fails because the path is not a repository, treat that as local `disabled` only after confirming no invalid `.git` control path exists.

If the request does not map cleanly to these steps, use the native planning tool to build a read-only status plan from the two layer contracts and current selected context, then execute it or report unresolved context.
