# Local Init

## Workflow

1. Require an explicit local-init request and a valid resolved `topic.runtime`. Stop and route runtime initialization to its owner when missing.
2. Run local status. If the Source Topic Workspace is already a valid top level, report safe reuse and preserve history, branches, index, remotes, and user configuration. If `.git` is corrupt, outside the root, or belongs to another worktree, block without repair.
3. Walk only the Source Topic Workspace's filesystem parents. At each parent, use `git -C <parent> rev-parse --show-toplevel`, deduplicate top levels, and compute the Source Topic Workspace path relative to that top level.
4. For every ancestor top level, run exact read-only evidence:

```bash
git -C <ancestor-top-level> ls-files -- <source-relative-path>
git -C <ancestor-top-level> check-ignore -v --no-index -- <source-relative-path> <relevant-existing-child-paths>
```

5. Block when any ancestor tracks the Source Topic Workspace or relevant content, or effective ignore evidence fails. Report the exact ancestor and prerequisite. Do not edit that repository.
6. Present the exact root initialization, managed `.gitignore` block, support-file write, and verification plan. Obtain explicit approval against the current fingerprints.
7. Revalidate every assumption, update the root managed ignore block, then initialize directly:

```bash
git -C <source-topic-workspace> init
git -C <source-topic-workspace> rev-parse --show-toplevel
git -C <source-topic-workspace> rev-parse --git-dir
git -C <source-topic-workspace> status --porcelain=v2 --untracked-files=all
git -C <source-topic-workspace> check-ignore -v --no-index -- <resolved-nested-paths>
```

8. Require the returned top level to equal the Source Topic Workspace. Write schema-valid local state below `<topic.runtime>/topic-git/` and report changed paths.

Do not add or inspect a remote, remove ancestor index entries, edit an ancestor ignore file, or initialize nested workspaces.

If the request does not map cleanly to these steps, use the native planning tool to build an exact local-init plan and stop before mutation until the ambiguity or missing approval is resolved.
