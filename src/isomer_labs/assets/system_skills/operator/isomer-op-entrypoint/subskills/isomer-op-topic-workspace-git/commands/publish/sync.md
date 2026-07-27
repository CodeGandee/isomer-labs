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

3. Fetch every selected topic-owned component and superproject branch without merge, then record each fetched commit. Validate every selected GitHub reference's normalized upstream locator and exact commit without importing its local checkout history. Run ancestry checks against exact planned commits. Ref changes stale prior force permission.
4. Reinventory source content and regenerate expected sanitized outputs, including root README, the portable research-record index, the stable latest-paper mapping, and reproduction limitations. Recompute source, output, copy, binding, semantic selection, raw-byte setting, identity transformation, component, reference, generated-navigation, and remote fingerprints. Stop on stale or blocked state.
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
9. After all component refs succeed, construct or update topic-owned same-remote submodules and registered GitHub upstream submodules at approved sanitized relative paths. Pin every exact commit. For a fresh sanitized superproject, add topic-owned deterministic branches from the publication remote and references from their normalized credential-free upstream locators, then verify mode `160000` gitlinks:

```bash
git -C <topic-publication-copy> submodule add -b <component-branch> <credential-safe-remote> <exact-component-relative-path>
git -C <topic-publication-copy> submodule add <credential-safe-github-reference> <exact-reference-relative-path>
git -C <topic-publication-copy> ls-files --stage -- <exact-component-relative-path>
git -C <topic-publication-copy> ls-files --stage -- <exact-reference-relative-path>
git -C <topic-publication-copy> -c protocol.file.allow=always submodule update --init --recursive
```

Stage only approved sanitized outputs, `.gitmodules`, exact gitlinks, the projection manifest, and `topic-workspace-version.toml`; verify the full index, commit, and push last:

```bash
git -C <topic-publication-copy> add -- README.md research-record-index.json paper/latest.pdf .gitmodules <exact-gitlink-paths> <approved-sanitized-root-paths> <projection-manifest> topic-workspace-version.toml
git -C <topic-publication-copy> diff --cached --name-only -z
git -C <topic-publication-copy> commit -m <approved-superproject-message> -- README.md research-record-index.json paper/latest.pdf .gitmodules <exact-gitlink-paths> <approved-sanitized-root-paths> <projection-manifest> topic-workspace-version.toml
git -C <topic-publication-copy> push publication <superproject-commit>:refs/heads/topic-workspace/main
```

When no eligible PDF exists, omit `paper/latest.pdf` from the exact stage and commit pathspecs. Never broaden staging to compensate for a conditional path.

10. Record branch outcomes, sanitized commits, exact reference commits, raw-byte settings, generated navigation fingerprints, access and reproduction limitations, and completion. If valid Workspace Runtime became available, promote the matching credential-safe binding and current publication state below `<topic.runtime>/topic-git/`.

If the request does not map cleanly to these steps, use the native planning tool to build an exact resumable synchronization plan and stop before remote mutation until every privacy, conflict, branch, and push approval is current.

## Guardrails

- DO NOT pull, merge, rebase, reset, or clean.
- DO NOT delete a remote branch or create a provider repository.
- DO NOT mutate any Source Topic Workspace repository.
- DO NOT push every ref or mirror refs.
- DO NOT force without a fresh exact destructive plan.
- DO NOT push to, mirror, fork, or mutate an upstream reference repository.
