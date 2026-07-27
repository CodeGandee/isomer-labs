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

Create fresh sanitized histories for topic-owned content with no source Git ancestry. The publication remote is an `exclusive_snapshot`: its current planned refs and tags represent the current publication, not retained publication history.

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

One approved Publication Binding grants persistent `exclusive_snapshot` authority only while remote identity, Research Topic, Topic Workspace, and snapshot mode still match. Every sync still requires a fresh privacy plan, complete remote branch and tag inventory, stale-state validation, exact expected ref and tag set, and current remote-mutation approval.

Synchronization order:

1. Observe every remote branch, tag, and remote HEAD without merge, and fingerprint that complete state.
2. Build and push selected topic-owned `components/...` branches.
3. Validate upstream reference commits, then update root README, `.gitmodules`, exact gitlinks, path-preserved source files, and the `.isomer-publication/` overlay.
4. Push canonical `main` last.
5. If remote HEAD selects an obsolete branch, require and complete a separate provider-supported action that selects `main`.
6. Delete every planned obsolete branch and tag only after validating the complete expected snapshot and moving remote HEAD away from any branch scheduled for deletion.
7. Record every ref result, remote-HEAD diagnostic, provider action, and safe resume point.

Exact commit equality is the only reusable-ref match; ancestry does not preserve publication history. The plan may force-replace `main`, `topic-workspace/main`, source-style component branches, prior publication commits, and any other planned publication ref, and may delete obsolete refs and tags. It must never use `--all` or `--mirror`.

Remote HEAD is provider state, not ordinary Git branch synchronization. Report when it does not select `main` and require a separate explicit provider-supported action before changing the hosted default branch.

A missing Topic Publication Copy may be recovered as disposable projection state from the validated binding and current remote `main`, then fully reinventoried and regenerated before another push. Publication recovery does not restore Topic Workspace runtime, source worktrees, source Git relationships, or other operational state. If a working Topic Workspace must be reconstructed, the researcher does that manually from the published evidence and artifacts.
