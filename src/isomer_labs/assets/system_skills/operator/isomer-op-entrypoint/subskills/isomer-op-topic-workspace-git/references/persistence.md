# Topic Git Persistence

Use separate schema-validated support types for local state, local plans, publication bindings, publication plans, projection manifests, and publication outcomes. Local mutation state lives only below `<topic.runtime>/topic-git/`.

Publication can precede Workspace Runtime. During that period, keep its binding, plan, conflicts, projection state, and outcomes below `<topic-publication-copy>/.isomer/topic-git/`. The entire `.isomer/` support root is ignored and excluded from every publication commit.

When Workspace Runtime later becomes available, the next approved `publish init` or `publish sync` validates binding identity against copy-local and remote evidence, then writes the credential-safe binding and current state under `<topic.runtime>/topic-git/`. Status performs no promotion. Do not edit `state.sqlite`.

If an unpushed pre-runtime copy is lost, its plan is lost and publish preparation must run again. If a successfully pushed pre-runtime copy is lost, reconstruct after the user supplies the remote again unless runtime support already holds the binding.

Support files may contain stable ids, Project-relative copy paths, credential-safe locators, visibility acknowledgement, dispositions, relative mappings, fingerprints, component branches and commits, conflict metadata, per-branch outcomes, and resume state. They never contain secret values, credentials, sensitive excerpts, raw private diffs, source Git configuration, credential-bearing URLs, or publication-irrelevant absolute source paths.
