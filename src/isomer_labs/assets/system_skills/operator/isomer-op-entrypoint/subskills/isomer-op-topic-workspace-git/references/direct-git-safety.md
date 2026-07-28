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
| Fetch or push | Use explicit branch, tag, and ref arguments from the complete current plan |
| Normal push | Use `git -C <publication-repository> push publication <commit>:refs/heads/<branch>` for `create` and `fast-forward` |
| No-op | Verify exact remote equality and create no commit or push |
| Exclusive snapshot fallback | Require matching one-time `exclusive_snapshot` authority, a fresh complete remote inventory, exact observed-commit lease, recorded incompatibility or purge reason, expected ref and tag set, push order, and current mutation approval |
| Force-replacement push | Use `git -C <publication-repository> push --force-with-lease=refs/heads/<branch>:<observed-commit> publication <replacement-commit>:refs/heads/<branch>`; never use bare `--force` |
| Remote HEAD | Observe separately; require an explicit provider-supported action because a Git ref push does not change the hosted default branch |

A stale plan, an incomplete remote inventory, an unresolved destination conflict, an unusable local copy without separate recovery, or an index path outside the approved set blocks mutation. Any observed ref, tag, remote-HEAD, compatibility-evidence, or strategy change stales the current publication plan.

Non-Git helpers may inventory paths, classify privacy, render placeholders, compute fingerprints, compare projections, validate schemas, and write approved support files.

Report a blocker and leave user state unchanged when a prohibition applies.

## Guardrails

- DO NOT rely on ambient cwd or broad staging.
- DO NOT pull, auto-merge, rebase, reset, or clean.
- DO NOT rewrite Source Topic Workspace or nested source history.
- DO NOT push every ref, mirror a repository, force an unlisted ref, or delete an unplanned ref or tag.
- DO NOT use force replacement to bypass a missing, dirty, divergent, or conflicted Topic Publication Copy.
- DO NOT run a provider repository-creation flow.
- DO NOT treat remote HEAD as a normal pushed branch or change it without a separate explicit provider action.
- DO NOT unstage or discard user content implicitly.
- DO NOT let a non-Git helper execute Git, accept arbitrary commands, or act as a hidden Git wrapper.
