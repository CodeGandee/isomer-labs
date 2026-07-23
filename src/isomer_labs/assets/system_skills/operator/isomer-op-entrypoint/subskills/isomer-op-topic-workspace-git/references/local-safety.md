# Local Tracking Safety

Local status and planning are read-only. Local init, ignore, and commit require a valid `topic.runtime` resolved by read-only query and write only schema-validated files below `<topic.runtime>/topic-git/`. Missing runtime routes to its owning initialization workflow; Topic Git does not initialize it.

Local tracking is enabled only when `git -C <source-topic-workspace> rev-parse --show-toplevel` equals the canonical Source Topic Workspace. An ancestor Project repository does not enable the layer. Before root initialization, walk only filesystem ancestors, collect each distinct ancestor Git top level, and prove the Source Topic Workspace plus relevant existing content is absent from that ancestor's index and effectively ignored. A tracked or unignored relationship blocks initialization. Never edit an ancestor ignore file or remove an ancestor index entry.

The root managed ignore block excludes Workspace Runtime, `state.sqlite`, local environments, caches, logs, temporary surfaces, credentials, canonical external repositories, Topic Main, registered Topic Actor Workspaces, and selected-team Agent Workspaces. Preserve all user rules outside the managed block. An ignore rule does not hide already tracked content; report it as a blocker.

Local plans select exact whole files. Warn about secret-like content without printing or persisting detected values. The optional `topic-workspace-local-version.toml` records relative semantic labels, branches, commit SHAs, and dirty booleans and states that the root commit does not preserve uncommitted nested content.

Local operations do not discover, add, modify, fetch, pull, or push remotes. Publication binding, copy, visibility, conflicts, and remote state are irrelevant to a valid local operation.
