# Publish Sync

## Workflow

1. Require an approved current privacy plan, known visibility, explicit remote-mutation approval, and a matching Publication Binding. Require `exclusive_snapshot` authority for planned fallback replacement or deletion, not for an ordinary no-op, create, or fast-forward update. Require separate conflict decisions where applicable.
2. Resolve current context and binding. Reuse a retained Topic Publication Copy only when it is clean, matches the binding, and is based on the exact planned commit. Preserve a dirty, divergent, or structurally invalid copy unchanged and either block or use a separate validated disposable recovery repository. If the copy is missing and the remote publication is history compatible, recover canonical `main` and every exact pinned component ref:

```bash
git -C <new-topic-publication-copy> init
git -C <new-topic-publication-copy> remote add publication <credential-safe-remote>
git -C <new-topic-publication-copy> fetch --no-tags publication main:refs/remotes/publication/main
git -C <new-topic-publication-copy> checkout -b main refs/remotes/publication/main
git -C <sanitized-component-root> fetch --no-tags publication <component-branch>:refs/remotes/publication/<component-branch>
```

3. Observe the complete remote branch and tag set plus remote HEAD, then fetch every selected topic-owned component and canonical `main` without merge and record each fetched commit:

```bash
git -C <publication-repository> ls-remote --heads --tags --symref publication
git -C <publication-repository> fetch --no-tags publication <branch>:refs/remotes/publication/<branch>
```

Validate every selected GitHub reference's normalized upstream locator and exact commit without importing its local checkout history. Any ref, tag, or remote-HEAD change stales the current plan.
4. Reinventory source content and regenerate expected sanitized outputs at source-identical paths, including composed root README, `.isomer-publication/research-record-index.json`, `.isomer-publication/topic-workspace-projection.json`, `.isomer-publication/topic-workspace-version.toml`, and the path-preserved latest-paper link. Keep plan ids, approval timestamps, push attempts, and outcomes in ignored support storage so replanning unchanged content does not create a metadata-only publication commit. Recompute source, output, copy, binding, semantic selection, raw-byte setting, identity transformation, component, reference, generated-navigation, ref-strategy, and remote fingerprints. Stop on stale or blocked state.
5. Apply only safe updates and deletions or explicitly approved conflict resolutions. Overwrite neither side of an unresolved conflict. Remove unapproved projected paths, rescan every eligible output, and verify the complete exact staged tree. Never repair preparation state with pull, merge, rebase, reset, or clean.
6. Process selected component refs in deterministic order. For `no-op`, verify exact commit equality and perform no commit or push. For `create`, use a fresh sanitized root with no source ancestry. For `fast-forward`, start from the exact fetched observed commit, materialize the approved tree, and require that commit as the new commit's only parent. Stage exact approved paths, verify the full index, commit only when the projected tree changed, and use an exact normal push:

```bash
git -C <sanitized-component-root> add -- <approved-component-paths>
git -C <sanitized-component-root> diff --cached --name-only -z
git -C <sanitized-component-root> commit -m <approved-component-message> -- <approved-component-paths>
git -C <sanitized-component-root> push publication <component-commit>:refs/heads/<component-branch>
```

7. For `force-replacement`, require the plan's exact history-incompatibility or history-purge reason and matching `exclusive_snapshot` authority. Create a fresh sanitized root commit, then use a branch-scoped lease against the exact observed commit:

```bash
git -C <sanitized-component-root> push --force-with-lease=refs/heads/<planned-component-branch>:<observed-component-commit> publication <replacement-commit>:refs/heads/<planned-component-branch>
```

8. Record each component strategy, observed base or lease, result, fallback use, and verification immediately. On failure, persist the safe resume point and stop before changing canonical `main`. The previously published `main` remains the authoritative complete publication until the planned new `main` succeeds. A retry must take a fresh complete inventory and may recognize only exact already completed results.
9. After all component refs succeed, construct or update topic-owned same-remote submodules and registered GitHub upstream submodules at approved sanitized relative paths. Pin every exact commit. For a fresh sanitized superproject, add topic-owned deterministic branches from the publication remote and references from their normalized credential-free upstream locators, then verify mode `160000` gitlinks:

```bash
git -C <topic-publication-copy> submodule add -b <component-branch> <credential-safe-remote> <exact-component-relative-path>
git -C <topic-publication-copy> submodule add <credential-safe-github-reference> <exact-reference-relative-path>
git -C <topic-publication-copy> ls-files --stage -- <exact-component-relative-path>
git -C <topic-publication-copy> ls-files --stage -- <exact-reference-relative-path>
git -C <topic-publication-copy> -c protocol.file.allow=always submodule update --init --recursive
```

Stage only approved path-preserved outputs, `.gitmodules`, exact gitlinks, and the `.isomer-publication/` overlay; verify the full index and reject flattened component content. Apply the planned `main` strategy: no commit or push for `no-op`, a sanitized root plus exact normal push for `create`, a direct-child sanitized delta plus exact normal push for `fast-forward`, or a fresh sanitized root plus exact leased fallback for `force-replacement`. Push canonical `main` last:

```bash
git -C <topic-publication-copy> add -- README.md .gitmodules .isomer-publication/research-record-index.json .isomer-publication/topic-workspace-projection.json .isomer-publication/topic-workspace-version.toml <path-preserved-paper-artifact> <exact-gitlink-paths> <approved-source-identical-paths>
git -C <topic-publication-copy> diff --cached --name-only -z
git -C <topic-publication-copy> commit -m <approved-superproject-message> -- README.md .gitmodules .isomer-publication/research-record-index.json .isomer-publication/topic-workspace-projection.json .isomer-publication/topic-workspace-version.toml <path-preserved-paper-artifact> <exact-gitlink-paths> <approved-source-identical-paths>
git -C <topic-publication-copy> push publication <superproject-commit>:refs/heads/main
git -C <topic-publication-copy> push --force-with-lease=refs/heads/main:<observed-main-commit> publication <replacement-superproject-commit>:refs/heads/main
```

When no eligible PDF exists, omit `<path-preserved-paper-artifact>` from the exact stage and commit pathspecs. Never broaden staging to compensate for a conditional path.

10. Report remote HEAD separately. If it does not select `main`, stop before any change unless the user approved a distinct provider-supported default-branch action. Complete that provider action before deleting a branch selected by remote HEAD, and record its success or failure independently from Git ref outcomes.
11. After `main` and any required provider action succeed, delete each exact planned obsolete branch or tag with a lease against its observed commit and record the outcome:

```bash
git -C <topic-publication-copy> push --force-with-lease=refs/heads/<planned-obsolete-branch>:<observed-obsolete-branch-commit> publication :refs/heads/<planned-obsolete-branch>
git -C <topic-publication-copy> push --force-with-lease=refs/tags/<planned-obsolete-tag>:<observed-obsolete-tag-commit> publication :refs/tags/<planned-obsolete-tag>
```

12. Reobserve the complete remote state, verify the exact expected branch and tag set, check every planned parent relationship, require clean publication repositories, and test a fresh recursive clone of canonical `main`. Record ref strategies and outcomes, sanitized commits, exact reference commits, raw-byte settings, generated navigation fingerprints, access and reproduction limitations, remote-HEAD diagnostics, preserved sanitized ancestry or fallback replacement, and completion. If valid Workspace Runtime became available, promote the matching credential-safe binding and current publication state below `<topic.runtime>/topic-git/`.

The resulting repository supports evidence and artifact inspection. It does not restore Workspace Runtime, source Git ancestry, Topic Main worktree administration, or a working Topic Workspace. Any operational reconstruction is manual.

If the request does not map cleanly to these steps, use the native planning tool to build an exact resumable synchronization plan and stop before remote mutation until every privacy, conflict, complete-inventory, ref-strategy, fallback, and push approval is current.

## Guardrails

- DO NOT pull, merge, rebase, reset, or clean.
- DO NOT delete an unplanned remote ref or tag or create a provider repository.
- DO NOT mutate any Source Topic Workspace repository.
- DO NOT push every ref or mirror refs.
- DO NOT force without a fresh exact history-aware plan, an exact observed-commit lease, a recorded fallback reason, and matching exclusive-snapshot authority.
- DO NOT force because a local copy is missing, dirty, divergent, or conflicted.
- DO NOT change remote HEAD through a Git ref push or an unapproved provider action.
- DO NOT push to, mirror, fork, or mutate an upstream reference repository.
