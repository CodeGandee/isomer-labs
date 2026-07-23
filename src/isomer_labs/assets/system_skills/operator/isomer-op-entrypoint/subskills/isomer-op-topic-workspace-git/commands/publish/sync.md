# Publish Sync

## Workflow

1. Require an approved current privacy plan, known visibility, and explicit remote-mutation approval. Require separate conflict decisions and separate branch-specific destructive approval where applicable.
2. Resolve current context and binding. If the Topic Publication Copy is missing, reconstruct only from the validated binding or resupplied credential-safe remote and deterministic sanitized branches:

```bash
git -C <new-topic-publication-copy> init
git -C <new-topic-publication-copy> remote add publication <credential-safe-remote>
git -C <new-topic-publication-copy> fetch --no-tags publication topic-workspace/main:refs/remotes/publication/topic-workspace/main
git -C <new-topic-publication-copy> checkout -b topic-workspace/main refs/remotes/publication/topic-workspace/main
```

3. Fetch every selected component and superproject branch without merge, then record each fetched commit. Run ancestry checks against exact planned commits. Ref changes stale prior force permission.
4. Reinventory source content and regenerate expected sanitized outputs. Recompute source, output, copy, binding, component, and remote fingerprints. Stop on stale or blocked state.
5. Apply only safe updates and deletions or explicitly approved conflict resolutions. Overwrite neither side of an unresolved conflict. Rescan every eligible output.
6. For each selected component, initialize or reuse only its sanitized publication repository, stage exact approved paths, verify the full index, commit when changed, and push its explicit ref:

```bash
git -C <sanitized-component-root> add -- <approved-component-paths>
git -C <sanitized-component-root> diff --cached --name-only -z
git -C <sanitized-component-root> commit -m <approved-component-message> -- <approved-component-paths>
git -C <sanitized-component-root> push publication <component-commit>:refs/heads/<component-branch>
```

7. For an exact incompatible branch with fresh separate approval, replace only that branch and exact commit:

```bash
git -C <sanitized-component-root> push --force publication <replacement-commit>:refs/heads/<approved-component-branch>
```

8. Record each component outcome immediately. On failure, persist the safe resume point and stop before changing the superproject. The previously published superproject remains authoritative.
9. After all component refs succeed, construct or update same-remote submodules at source-relative paths and pin exact commits. For a fresh sanitized superproject, add each exact deterministic branch from the same credential-safe remote and verify mode `160000` gitlinks:

```bash
git -C <topic-publication-copy> submodule add -b <component-branch> <credential-safe-remote> <exact-component-relative-path>
git -C <topic-publication-copy> ls-files --stage -- <exact-component-relative-path>
git -C <topic-publication-copy> -c protocol.file.allow=always submodule update --init --recursive
```

Stage only `.gitmodules`, exact gitlinks, the projection manifest, and `topic-workspace-version.toml`; verify the full index, commit, and push last:

```bash
git -C <topic-publication-copy> add -- .gitmodules <exact-gitlink-paths> <projection-manifest> topic-workspace-version.toml
git -C <topic-publication-copy> diff --cached --name-only -z
git -C <topic-publication-copy> commit -m <approved-superproject-message> -- .gitmodules <exact-gitlink-paths> <projection-manifest> topic-workspace-version.toml
git -C <topic-publication-copy> push publication <superproject-commit>:refs/heads/topic-workspace/main
```

10. Record branch outcomes, sanitized commits, and completion. If valid Workspace Runtime became available, promote the matching credential-safe binding and current publication state below `<topic.runtime>/topic-git/`.

Never pull, merge, rebase, reset, clean, delete a remote branch, create a provider repository, mutate any Source Topic Workspace repository, push every ref, mirror refs, or force without a fresh exact destructive plan.

If the request does not map cleanly to these steps, use the native planning tool to build an exact resumable synchronization plan and stop before remote mutation until every privacy, conflict, branch, and push approval is current.
