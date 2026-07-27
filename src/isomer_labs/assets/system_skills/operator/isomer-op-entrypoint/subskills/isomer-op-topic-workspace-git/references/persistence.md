# Topic Git Persistence

Use separate schema-valid support types for local state, local plans, publication bindings, publication plans, projection manifests, and publication outcomes.

| Lifecycle Posture | Support Location | Rule |
| --- | --- | --- |
| Local mutation | `<topic.runtime>/topic-git/` | Runtime is required |
| Publication before runtime | `<topic-publication-copy>/.isomer/topic-git/` | Ignore and exclude the entire support root from publication |
| Publication after runtime appears | `<topic.runtime>/topic-git/` | The next approved init or sync validates and promotes matching state |
| Read-only status | Existing support location | Never promotes state |

Recovery:

| Loss | Recovery |
| --- | --- |
| Unpushed pre-runtime copy | Prepare publication again |
| Successfully pushed pre-runtime copy | Recover disposable projection state after the user supplies the remote, unless runtime already holds the binding |

Support files may contain stable ids, Project-relative copy paths, credential-safe publication and GitHub reference locators, visibility, `exclusive_snapshot` authority, semantic content classes, raw-byte settings, dispositions, source-identical relative mappings, fingerprints, component branches and commits, Topic Main anchor relationships, exact reference commits, complete remote refs and tags, observed remote HEAD, identity-substitution categories, generated-navigation fingerprints, reproduction limitations, conflicts, outcomes, and resume state.

Support files never contain secrets, credentials, individual identity values, local hostnames or IPs, sensitive excerpts, raw private diffs, source Git configuration, credential-bearing URLs, or publication-irrelevant absolute source paths. Credential-free public or private GitHub organization/repository identities are allowed provenance. Topic Git never edits `state.sqlite`.

The tracked `.isomer-publication/` overlay is portable publication metadata. The ignored `.isomer/topic-git/` support root is local operation state. Neither restores source worktree administration, Workspace Runtime, local identity, or a working Topic Workspace automatically.
