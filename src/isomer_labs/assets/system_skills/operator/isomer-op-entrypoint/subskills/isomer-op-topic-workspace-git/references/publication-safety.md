# Publication Safety

## Destination and Binding

Resolve Project-root `tmp/` and `temp/` through Project location evidence. If the Project is inside Git, use direct `git check-ignore` evidence, including nested negation behavior. Otherwise inspect only the bounded Project-root `.gitignore`. Reuse a safe existing binding, prefer ignored `tmp/`, then ignored `temp/`, then a declared ignored candidate. If none qualifies, plan a bounded managed Project `.gitignore` block and Project-root `tmp/` creation.

The Topic Publication Copy path is `<temporary-root>/topic-workspace-publish/<topic-id>/`. It must stay inside the Project and outside the Source Topic Workspace, Project Config Directory, generated content root, Houmao state, Topic Main, canonical external repositories, Topic Actor Workspaces, and Agent Workspaces.

Reject remote locators with embedded credentials, query parameters, signatures, or fragments. Report only the credential-safe locator and remote name. Authentication stays in Git credential helpers, SSH agents, or user-selected provider tooling. Require visibility `private`, `restricted`, or `public`; `unknown` blocks push.

## Branch Layout

Create fresh sanitized histories with no source Git ancestry:

| Component | Publication Branch |
| --- | --- |
| Topic Main | `topic-owner/main` |
| Topic Actor `<name>` | `per-topic-actor/<name>/main` |
| Agent `<name>` | `per-agent/<name>/main` |
| Sanitized superproject | `topic-workspace/main` |

Select every currently available Isomer-resolved component unless the current plan explicitly excludes it. Report selected, excluded, blocked, and unavailable components. A newly available component invalidates the older plan.

Every `.gitmodules` entry uses the same credential-safe remote, names its deterministic branch, and pins an exact sanitized component commit at the source-relative path. Build the superproject only from sanitized component repositories; never copy source Git metadata or ancestry.

## Synchronization

Fetch every selected deterministic branch without merge before mutation. Classify a missing ref as absent, a proven ancestor or identical ref as compatible, and any other existing ref as incompatible. Normal pushes cover absent and compatible refs. An incompatible ref needs its own current destructive plan and separate approval.

Commit and push component branches first. Then update `.gitmodules`, gitlinks, the projection manifest, and `topic-workspace-version.toml`; commit and push `topic-workspace/main` last. Record every branch result and the safe resume point. Until the final superproject push succeeds, the previous remote `topic-workspace/main` remains the authoritative complete version.

Reconstruct a missing copy only from the validated binding or explicitly resupplied remote, fetched deterministic branches, and sanitized manifests. Reinventory and rescan current source content before any new push.
