# Publication Safety

## Destination and Binding

Resolve the destination in this order:

1. Safe existing binding.
2. Effectively ignored Project-root `tmp/`.
3. Effectively ignored Project-root `temp/`.
4. Declared ignored candidate.
5. Approved managed Project `.gitignore` block and Project-root `tmp/` creation.

Use direct `git check-ignore` evidence, including nested negation behavior, when the Project is inside Git. Otherwise inspect only the bounded Project-root `.gitignore`.

The Topic Publication Copy path is `<temporary-root>/topic-workspace-publish/<topic-id>/`. It must stay inside the Project and outside:

- the Source Topic Workspace and Project Config Directory;
- the generated content root and Houmao state;
- Topic Main and canonical external repositories;
- Topic Actor Workspaces and Agent Workspaces.

| Binding Check | Rule |
| --- | --- |
| Remote locator | Reject embedded credentials, query parameters, signatures, and fragments |
| Reporting | Show only the credential-safe locator and remote name |
| Authentication | Keep in Git credential helpers, SSH agents, or user-selected provider tooling |
| Visibility | Require `private`, `restricted`, or `public`; `unknown` blocks push |

## Branch Layout

Create initial sanitized histories for topic-owned content with no Source Topic Workspace Git ancestry. A later compatible sanitized publication commit may become the direct parent of the next sanitized delta. The publication remote is an `exclusive_snapshot`: Isomer has authority over the exact planned publication namespace, but compatible sanitized history is retained by default.

| Submodule Kind | Locator | Branch or Commit |
| --- | --- | --- |
| Topic Main | Publication remote | `components/topic-main`, pinned exact sanitized commit |
| Topic Actor `<name>` | Publication remote | `components/topic-actors/<sanitized-name>`, pinned exact sanitized commit |
| Agent `<name>` | Publication remote | `components/agents/<sanitized-name>`, pinned exact sanitized commit |
| Registered GitHub reference | Normalized credential-free upstream GitHub locator | Exact registered upstream commit; no publication branch |
| Sanitized superproject | Publication remote | `main` |

- Select every currently available Isomer-resolved topic-owned component and registered GitHub reference unless the current plan explicitly excludes it.
- Report selected, excluded, blocked, and unavailable components and references.
- Treat a newly available component or reference, changed reference locator, or changed exact commit as a stale-plan event.
- Use the publication remote only for topic-owned components. Use each reference's normalized upstream locator for that reference's `.gitmodules` entry.
- Keep each component and reference gitlink at its resolved Topic Workspace-relative path. Never merge, copy, or flatten component files into the superproject root.
- Treat Topic Actor Workspace and Agent Workspace sources as worktrees in the Topic Main worktree family. Publish ordinary same-remote component submodules and record their Topic Main anchor relationship; never copy source `.git` files or worktree administration.
- Preserve public or private GitHub owner and repository names as organization or source provenance. Keep authentication external.
- Record an access and reproduction limitation when the intended audience cannot resolve a private reference.
- Never copy a canonical external repository's local checkout, `.git` metadata, or history into a topic-owned sanitized component unless an explicit raw-material plan separately approves the exact bytes.
- Use neutral generated author name and email for publication commits.

## Reproduction Outputs

The superproject preserves retained content at its Source Topic Workspace-relative path. It always contains root `README.md`, composing sanitizable source README content with one versioned generated navigation block. It also contains `.isomer-publication/research-record-index.json`, `.isomer-publication/topic-workspace-projection.json`, and `.isomer-publication/topic-workspace-version.toml`.

Link the latest eligible paper from the generated README block at its path-preserved Artifact location. Never create `paper/latest.pdf` or another relocated alias. Git does not represent empty directories; omit an empty source directory unless an approved tracked placeholder already exists.

The default publication includes sanitizable intent, environment declarations, all typed durable record revisions, and exact source identities. Downloaded material bytes and raw experiment-output bytes require explicit current-plan settings.

## Synchronization

One approved Publication Binding grants persistent `exclusive_snapshot` fallback and deletion authority only while remote identity, Research Topic, Topic Workspace, and snapshot mode still match. Every sync still requires a fresh privacy plan, complete remote branch and tag inventory, stale-state validation, exact expected ref and tag set, one strategy per expected ref, and current remote-mutation approval.

Synchronization order:

1. Observe every remote branch, tag, and remote HEAD without merge, and fingerprint that complete state.
2. Classify each expected branch as `no-op`, `create`, `fast-forward`, or `force-replacement`, then build and push selected topic-owned `components/...` branches through their planned strategies.
3. Validate upstream reference commits, then update root README, `.gitmodules`, exact gitlinks, path-preserved source files, and the `.isomer-publication/` overlay.
4. Push canonical `main` last.
5. If remote HEAD selects an obsolete branch, require and complete a separate provider-supported action that selects `main`.
6. Delete every planned obsolete branch and tag only after validating the complete expected snapshot and moving remote HEAD away from any branch scheduled for deletion.
7. Verify exact parent relationships and a fresh recursive clone, then record every ref strategy and result, remote-HEAD diagnostic, provider action, and safe resume point.

Exact commit equality produces `no-op`. An absent ref produces `create`. A differing ref produces `fast-forward` only when its matching binding, supported tracked manifest, canonical topology, pinned component relationship, current history-retention posture, and freshly fetched ancestry prove that it is a compatible sanitized publication base. Missing or contradictory evidence blocks or selects an explicitly approved `force-replacement` fallback; ordinary source changes do not.

Create and fast-forward strategies use exact normal refspecs. Force replacement uses an exact branch-scoped `--force-with-lease` against the planned observed commit under matching `exclusive_snapshot` authority. A privacy, credential, identity, license, or withdrawal decision that requires prior content to become unreachable also replaces canonical `main` when retained superproject ancestry would still reference that content. Provider object retention may outlive the ref replacement and must be reported. The workflow must never use bare `--force`, `--all`, or `--mirror`.

Remote HEAD is provider state, not ordinary Git branch synchronization. Report when it does not select `main` and require a separate explicit provider-supported action before changing the hosted default branch.

A missing Topic Publication Copy may be recovered as disposable projection state from the validated binding, current remote `main`, and exact pinned component refs, then fully reinventoried and regenerated before another push. Missing local state is not a force-replacement reason. Reuse an existing copy only when it is clean, matches the binding, and is based on the exact observed commit. Preserve dirty, divergent, or invalid copies and block or use a separate disposable recovery repository; never merge, rebase, reset, or clean them. Publication recovery does not restore Topic Workspace runtime, source worktrees, source Git relationships, or other operational state. If a working Topic Workspace must be reconstructed, the researcher does that manually from the published evidence and artifacts.
