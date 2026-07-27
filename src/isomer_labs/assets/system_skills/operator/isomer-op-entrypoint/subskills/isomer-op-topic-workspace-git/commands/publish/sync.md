# Publish Sync

## Workflow

1. Require an approved current privacy plan, known visibility, explicit remote-mutation approval, and a matching one-time `exclusive_snapshot` authority. Require separate conflict decisions where applicable; do not repeat branch-specific destructive prompts while that authority remains valid.
2. Resolve current context and binding. If the Topic Publication Copy is missing, recover disposable projection state only from the validated binding or resupplied credential-safe remote and canonical `main`:

```bash
git -C <new-topic-publication-copy> init
git -C <new-topic-publication-copy> remote add publication <credential-safe-remote>
git -C <new-topic-publication-copy> fetch --no-tags publication main:refs/remotes/publication/main
git -C <new-topic-publication-copy> checkout -b main refs/remotes/publication/main
```

3. Observe the complete remote branch and tag set plus remote HEAD, then fetch every selected topic-owned component and canonical `main` without merge and record each fetched commit:

```bash
git -C <publication-repository> ls-remote --heads --tags --symref publication
git -C <publication-repository> fetch --no-tags publication <branch>:refs/remotes/publication/<branch>
```

Validate every selected GitHub reference's normalized upstream locator and exact commit without importing its local checkout history. Any ref, tag, or remote-HEAD change stales the current plan.
4. Reinventory source content and regenerate expected sanitized outputs at source-identical paths, including composed root README, `.isomer-publication/research-record-index.json`, `.isomer-publication/topic-workspace-projection.json`, `.isomer-publication/topic-workspace-version.toml`, and the path-preserved latest-paper link. Recompute source, output, copy, binding, semantic selection, raw-byte setting, identity transformation, component, reference, generated-navigation, and remote fingerprints. Stop on stale or blocked state.
5. Apply only safe updates and deletions or explicitly approved conflict resolutions. Overwrite neither side of an unresolved conflict. Rescan every eligible output.
6. For each selected component, initialize or reuse only its sanitized publication repository, stage exact approved paths, verify the full index, commit when changed, and push its explicit ref:

```bash
git -C <sanitized-component-root> add -- <approved-component-paths>
git -C <sanitized-component-root> diff --cached --name-only -z
git -C <sanitized-component-root> commit -m <approved-component-message> -- <approved-component-paths>
git -C <sanitized-component-root> push publication <component-commit>:refs/heads/<component-branch>
```

7. Force-replace each exact planned component ref under the matching exclusive-snapshot authority:

```bash
git -C <sanitized-component-root> push --force publication <replacement-commit>:refs/heads/<planned-component-branch>
```

8. Record each component outcome immediately. On failure, persist the safe resume point and stop before changing canonical `main`. Do not describe a legacy branch or prior commit as authoritative.
9. After all component refs succeed, construct or update topic-owned same-remote submodules and registered GitHub upstream submodules at approved sanitized relative paths. Pin every exact commit. For a fresh sanitized superproject, add topic-owned deterministic branches from the publication remote and references from their normalized credential-free upstream locators, then verify mode `160000` gitlinks:

```bash
git -C <topic-publication-copy> submodule add -b <component-branch> <credential-safe-remote> <exact-component-relative-path>
git -C <topic-publication-copy> submodule add <credential-safe-github-reference> <exact-reference-relative-path>
git -C <topic-publication-copy> ls-files --stage -- <exact-component-relative-path>
git -C <topic-publication-copy> ls-files --stage -- <exact-reference-relative-path>
git -C <topic-publication-copy> -c protocol.file.allow=always submodule update --init --recursive
```

Stage only approved path-preserved outputs, `.gitmodules`, exact gitlinks, and the `.isomer-publication/` overlay; verify the full index, reject flattened component content, commit, and push canonical `main` last:

```bash
git -C <topic-publication-copy> add -- README.md .gitmodules .isomer-publication/research-record-index.json .isomer-publication/topic-workspace-projection.json .isomer-publication/topic-workspace-version.toml <path-preserved-paper-artifact> <exact-gitlink-paths> <approved-source-identical-paths>
git -C <topic-publication-copy> diff --cached --name-only -z
git -C <topic-publication-copy> commit -m <approved-superproject-message> -- README.md .gitmodules .isomer-publication/research-record-index.json .isomer-publication/topic-workspace-projection.json .isomer-publication/topic-workspace-version.toml <path-preserved-paper-artifact> <exact-gitlink-paths> <approved-source-identical-paths>
git -C <topic-publication-copy> push --force publication <superproject-commit>:refs/heads/main
```

When no eligible PDF exists, omit `<path-preserved-paper-artifact>` from the exact stage and commit pathspecs. Never broaden staging to compensate for a conditional path.

10. Report remote HEAD separately. If it does not select `main`, stop before any change unless the user approved a distinct provider-supported default-branch action. Complete that provider action before deleting a branch selected by remote HEAD, and record its success or failure independently from Git ref outcomes.
11. After `main` and any required provider action succeed, delete each exact planned obsolete branch or tag and record the outcome:

```bash
git -C <topic-publication-copy> push publication :refs/heads/<planned-obsolete-branch>
git -C <topic-publication-copy> push publication :refs/tags/<planned-obsolete-tag>
```

12. Record ref outcomes, sanitized commits, exact reference commits, raw-byte settings, generated navigation fingerprints, access and reproduction limitations, remote-HEAD diagnostics, and completion. If valid Workspace Runtime became available, promote the matching credential-safe binding and current publication state below `<topic.runtime>/topic-git/`.

The resulting repository supports evidence and artifact inspection. It does not restore Workspace Runtime, source Git ancestry, Topic Main worktree administration, or a working Topic Workspace. Any operational reconstruction is manual.

If the request does not map cleanly to these steps, use the native planning tool to build an exact resumable synchronization plan and stop before remote mutation until every privacy, conflict, complete-snapshot, and push approval is current.

## Guardrails

- DO NOT pull, merge, rebase, reset, or clean.
- DO NOT delete an unplanned remote ref or tag or create a provider repository.
- DO NOT mutate any Source Topic Workspace repository.
- DO NOT push every ref or mirror refs.
- DO NOT force without a fresh exact complete-snapshot plan and matching exclusive-snapshot authority.
- DO NOT change remote HEAD through a Git ref push or an unapproved provider action.
- DO NOT push to, mirror, fork, or mutate an upstream reference repository.
