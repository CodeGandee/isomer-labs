# Direct Git Safety

## Command Contract

Invoke the installed Git executable directly. Every repository command has this shape:

```bash
git -C <validated-resolved-repository> <subcommand> <exact-options-and-arguments>
```

Before a mutation, repeat repository top-level, Git directory, HEAD, index, relevant working-content, plan fingerprint, binding, component, and fetched-ref checks. Reject a stale plan. Run exact-path staging with `git -C <repository> add -- <path-1> <path-2>` and verify the complete index with `git -C <repository> diff --cached --name-only -z`. A path outside the approved set blocks the commit; do not unstage or discard it implicitly.

Use explicit branch and ref arguments for fetch and push. A normal publication push has the form `git -C <publication-repository> push publication <commit>:refs/heads/<branch>`. One incompatible deterministic branch may use plain force only after a fresh destructive plan records the fetched commit, replacement commit, displaced commits, push order, warnings, and separate branch-scoped approval. Any ref change makes that approval stale.

## Prohibitions

Never rely on ambient cwd or run broad staging. Never pull, auto-merge, rebase, reset, clean, delete a remote branch, rewrite Source Topic Workspace or nested source history, push every ref, mirror a repository, or force an unlisted branch. Never run a provider repository-creation flow. Report the blocker and leave user state unchanged.

Non-Git helpers may inventory semantic paths, classify privacy, render placeholders, compute fingerprints, compare projections, validate schemas, and write approved support files. They must not import or invoke a process runner for Git, accept arbitrary commands, or act as a hidden Git wrapper.
