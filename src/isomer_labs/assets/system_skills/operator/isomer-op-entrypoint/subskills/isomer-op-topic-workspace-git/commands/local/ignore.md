# Local Ignore

## Workflow

1. Require valid Workspace Runtime, enabled local root tracking, and an approved current local plan.
2. Recompute repository identity, HEAD, complete index, relevant working-content fingerprints, and root `.gitignore` fingerprint. Stop when the plan is stale.
3. Before adding an ignore rule, inspect exact tracked paths:

```bash
git -C <source-topic-workspace> ls-files -- <approved-ignore-path-1> <approved-ignore-path-2>
```

4. Block any already tracked sensitive path and explain that ignore rules do not remove tracked content. Do not change the index.
5. Replace only the stable Isomer local managed block in the root `.gitignore`; preserve every user-authored line outside it. Apply the same approved block twice in memory and require identical output before writing.
6. Verify effective behavior:

```bash
git -C <source-topic-workspace> check-ignore -v --no-index -- <approved-ignore-paths>
git -C <source-topic-workspace> status --porcelain=v2 --untracked-files=all
git -C <source-topic-workspace> ls-files --stage
```

7. Write current local support state below `<topic.runtime>/topic-git/` and report the exact changed block.

Do not untrack a path, rewrite history, or inspect publication state.

If the request does not map cleanly to these steps, use the native planning tool to isolate the managed ignore mutation and stop until its exact current plan and approval are known.
