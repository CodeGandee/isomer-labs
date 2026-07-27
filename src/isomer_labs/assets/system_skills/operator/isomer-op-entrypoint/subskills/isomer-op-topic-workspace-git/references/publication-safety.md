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

Create fresh sanitized histories for topic-owned content with no source Git ancestry:

| Submodule Kind | Locator | Branch or Commit |
| --- | --- | --- |
| Topic Main | Publication remote | `topic-owner/main`, pinned exact sanitized commit |
| Topic Actor `<name>` | Publication remote | `per-topic-actor/<sanitized-name>/main`, pinned exact sanitized commit |
| Agent `<name>` | Publication remote | `per-agent/<sanitized-name>/main`, pinned exact sanitized commit |
| Registered GitHub reference | Normalized credential-free upstream GitHub locator | Exact registered upstream commit; no publication branch |
| Sanitized superproject | Publication remote | `topic-workspace/main` |

- Select every currently available Isomer-resolved topic-owned component and registered GitHub reference unless the current plan explicitly excludes it.
- Report selected, excluded, blocked, and unavailable components and references.
- Treat a newly available component or reference, changed reference locator, or changed exact commit as a stale-plan event.
- Use the publication remote only for topic-owned components. Use each reference's normalized upstream locator for that reference's `.gitmodules` entry.
- Preserve public or private GitHub owner and repository names as organization or source provenance. Keep authentication external.
- Record an access and reproduction limitation when the intended audience cannot resolve a private reference.
- Never copy a canonical external repository's local checkout, `.git` metadata, or history into a topic-owned sanitized component unless an explicit raw-material plan separately approves the exact bytes.
- Use neutral generated author name and email for publication commits.

## Reproduction Outputs

The superproject always contains a generated root `README.md` and portable sanitized research-record index. It contains `paper/latest.pdf` only when one latest unambiguous typed paper Artifact passes build, validation, signature, checksum, size, license, and identity-metadata checks.

The default publication includes sanitizable intent, environment declarations, all typed durable record revisions, and exact source identities. Downloaded material bytes and raw experiment-output bytes require explicit current-plan settings.

## Synchronization

| Ref State | Rule |
| --- | --- |
| Missing | Classify as absent; normal push is eligible |
| Identical or proven ancestor | Classify as compatible; normal push is eligible |
| Other existing ref | Classify as incompatible; require a current destructive plan and separate approval |

Synchronization order:

1. Fetch selected deterministic branches without merge.
2. Commit and push component branches.
3. Validate upstream reference commits, then update generated README and research index, optional latest-paper mapping, `.gitmodules`, gitlinks, the projection manifest, and `topic-workspace-version.toml`.
4. Commit and push `topic-workspace/main` last.
5. Record every branch result and safe resume point.

The previous remote `topic-workspace/main` remains authoritative until the final superproject push succeeds. Reconstruct a missing copy only from validated binding or remote evidence, fetched deterministic branches, and sanitized manifests; reinventory and rescan before pushing.
