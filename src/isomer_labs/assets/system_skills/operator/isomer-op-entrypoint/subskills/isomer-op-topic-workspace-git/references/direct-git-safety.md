# Direct Git Safety

## Command Contract

Invoke the installed Git executable directly. Every repository command has this shape:

```bash
git -C <validated-resolved-repository> <subcommand> <exact-options-and-arguments>
```

| Operation | Contract |
| --- | --- |
| Pre-mutation check | Revalidate repository top level, Git directory, HEAD, index, relevant content, plan fingerprint, binding, components, and fetched refs |
| Staging | Use exact paths with `git -C <repository> add -- <paths>` |
| Index verification | Inspect the complete staged set with `git -C <repository> diff --cached --name-only -z` |
| Fetch or push | Use explicit branch and ref arguments |
| Normal push | Use `git -C <publication-repository> push publication <commit>:refs/heads/<branch>` |
| Forced replacement | Require a fresh destructive plan with fetched commit, replacement commit, displaced commits, push order, warnings, and separate branch-scoped approval |

A stale plan or an index path outside the approved set blocks mutation. Any fetched-ref change stales prior force approval.

Non-Git helpers may inventory paths, classify privacy, render placeholders, compute fingerprints, compare projections, validate schemas, and write approved support files.

Report a blocker and leave user state unchanged when a prohibition applies.

## Guardrails

- DO NOT rely on ambient cwd or broad staging.
- DO NOT pull, auto-merge, rebase, reset, clean, or delete a remote branch.
- DO NOT rewrite Source Topic Workspace or nested source history.
- DO NOT push every ref, mirror a repository, or force an unlisted branch.
- DO NOT run a provider repository-creation flow.
- DO NOT unstage or discard user content implicitly.
- DO NOT let a non-Git helper execute Git, accept arbitrary commands, or act as a hidden Git wrapper.
