# Storage Layer

This developer guide is a practical reference for a Project Operator Session that needs to read from or write to Isomer-managed storage. In canonical Isomer language, "storage layer" is a guide phrase for the combination of Project configuration, Topic Workspace files, semantic workspace surface labels, Workspace Path Resolution, Workspace Runtime records, and adapter-owned payload files.

## Mental Model

Isomer storage is label-first. Commands and agents should ask for a semantic workspace surface label, then use the returned path. They should not assemble important paths from directory names unless the path is purely local and disposable.

The main layers are:

- **Project Config Directory**: `.isomer-labs/` stores Project discovery and configuration, especially the Project Manifest and Research Topic Config files. It is not the place for Runtime state, research outputs, command logs, or rich Artifacts.
- **Project Manifest**: `.isomer-labs/manifest.toml` declares Research Topics, Topic Workspaces, Project defaults, Pixi bindings, and profile or instance refs. `isomer-cli` discovers the Project through this file.
- **Topic Workspace**: the Project Manifest-declared directory for one Research Topic. It owns the Topic Workspace Manifest, Pixi manifest and lockfile, Topic Agent Team Profile Bundle, Topic Main Development Repository, non-main topic repositories, Agent Workspaces, owner-preserved records, Workspace Runtime, and adapter material.
- **Topic Workspace Manifest**: `<topic-workspace>/topic-workspace.toml` binds semantic labels to paths or templates. A binding has `label`, `path`, and `storage_profile`.
- **Semantic workspace surface label**: the stable storage API, such as `topic.records.artifacts`, `topic.repos.main`, `topic.repos.main.projections.readonly`, `topic.runtime.db`, `agent.workspace`, or `custom.datasets.raw`.
- **Storage profile**: the meaning attached to a path, such as durable topic records, topic repository, agent worktree, disposable topic directory, or adapter runtime directory. Isomer uses this profile because a path string alone cannot say who owns a directory, whether it is durable, or whether it is safe to share.
- **Workspace Runtime**: `state.sqlite` inside the Topic Workspace. It stores compact durable records, including Path Plan records, readiness records, lifecycle records, Agent Team Instance records, Agent Workspace records, handoffs, validation issues, and adapter refs.
- **Path Plan record**: a frozen runtime record that maps a semantic label and scope to a concrete path. Once runtime records depend on a path, Isomer preserves the recorded path instead of silently following later manifest edits.
- **Topic Git support**: schema-validated optional local-tracking and publication files below `<topic.runtime>/topic-git/`. Before Workspace Runtime exists, publication-only support may live below the ignored Topic Publication Copy `.isomer/topic-git/` root.

## Resolution Order

For normal path reads, Workspace Path Resolution favors durable truth before current configuration:

1. Recorded Path Plan in Workspace Runtime.
2. Supported semantic environment variables such as `ISOMER_PATH__TOPIC__RECORDS__ARTIFACTS`.
3. Compatibility environment variables such as `ISOMER_TOPIC_WORKSPACE_ARTIFACTS_DIR`.
4. Topic Workspace Manifest bindings.
5. Project Manifest defaults where applicable.
6. The built-in `isomer-default.v1` layout.

Use `--configured` with `project paths get` when you specifically want the current manifest or environment answer instead of a recorded Path Plan.

## Read Storage

Start by selecting a Research Topic and resolving the Effective Topic Context:

```bash
isomer-cli --print-json project context show --topic my-topic
```

Resolve one storage surface:

```bash
isomer-cli --print-json project paths get topic.records.artifacts --topic my-topic
isomer-cli --print-json project paths get topic.repos.main --topic my-topic
isomer-cli --print-json project paths get agent.private_artifacts --topic my-topic --agent alice
```

List known labels and their resolution status:

```bash
isomer-cli --print-json project paths list --topic my-topic
isomer-cli --print-json project paths list --topic my-topic --agent alice
```

Explain why a path was selected:

```bash
isomer-cli --print-json project paths explain topic.records.artifacts --topic my-topic
isomer-cli --print-json project paths explain custom.datasets.raw --topic my-topic
```

Inspect or validate runtime records:

```bash
isomer-cli --print-json project runtime inspect --topic my-topic
isomer-cli --print-json project runtime validate --topic my-topic
```

## Put Durable Topic Material

For durable topic-level outputs, prefer an owner-preserved records label. The common starting point is `topic.records.artifacts`:

```bash
isomer-cli --print-json project paths get topic.records.artifacts --topic my-topic
```

After resolving the path, write the file under a clear subdirectory such as `experiments`, `analysis`, `figures`, `paper`, `decisions`, `evidence`, `findings`, or `handoffs`. The resolved path is the storage authority, not the default directory name.

If the material needs its own named surface, register a `custom.*` label instead of inventing an untracked convention:

```bash
isomer-cli --print-json project paths register custom.datasets.raw --topic my-topic --path data/raw --storage-profile topic_records_dir --create
isomer-cli --print-json project paths get custom.datasets.raw --topic my-topic
```

Use a storage profile that matches the material. For durable topic records, `topic_records_dir` is usually appropriate. For a supporting topic repository, use `topic_repo`.

## Put Repository Material

Use `topic.repos.main` for the Topic Main Development Repository. This is the shared code-bearing topic repository and the normal source for Agent Workspace worktrees.

```bash
isomer-cli --print-json project paths get topic.repos.main --topic my-topic
```

For a non-main supporting repository, use the helper command:

```bash
isomer-cli --print-json project repos create inner_group.some_repo_name --topic my-topic
isomer-cli --print-json project paths get topic.repos.inner_group.some_repo_name --topic my-topic
```

The helper registers a grouped `topic.repos.<group...>.<repo-name>` label with `storage_profile = "topic_repo"` and creates the configured target unless `--no-create` is selected. Topic environment setup decides whether that repository should also appear inside `topic.repos.main.projections.readonly` or `topic.repos.main.projections.writable`.

## Put Agent Material

Agent-scoped labels need an Agent Name or Agent Instance context unless the current working directory is already inside that Agent Workspace.

```bash
isomer-cli --print-json project paths get agent.workspace --topic my-topic --agent alice
isomer-cli --print-json project paths get agent.private_artifacts --topic my-topic --agent alice
isomer-cli --print-json project paths get agent.public_share --topic my-topic --agent alice
isomer-cli --print-json project paths get agent.scratch --topic my-topic --agent alice
```

Use `agent.private_artifacts` for agent-owned outputs before they are promoted into topic-level records. Use `agent.public_share` only for peer-readable material that should remain agent-owned. Use `agent.scratch` for drafts and intermediate work that may later be promoted. Agent material is not automatically accepted as a topic Artifact, Evidence Item, Decision Record, or Provenance Record.

Implemented tmp/ surfaces use `topic.tmp`, `topic.repos.main.tmp`, and `agent.tmp`; they are local, ignored, disposable, and not durable evidence. Use these labels only for sweepable transient files.

## Put Runtime Records

Do not write `state.sqlite` directly. Use `isomer-cli` commands that own the record type:

```bash
isomer-cli --print-json project runtime init --topic my-topic
isomer-cli --print-json project runtime prepare --topic my-topic --actor operator
isomer-cli --print-json project team-instances create --topic my-topic --id ati-my-topic-deepsci
isomer-cli --print-json project handoffs dispatch --topic my-topic --agent-team-instance ati-my-topic-deepsci --source-agent-instance ati-my-topic-deepsci-lead --target-agent-instance ati-my-topic-deepsci-scout --run run-first-pass --message "Inspect the topic repository and report blockers."
```

Runtime commands create or update Path Plans, readiness records, lifecycle records, Agent Team Instance records, Agent Workspace records, handoff records, adapter refs, and validation issues. They also report side effects through the `mutated` flag in JSON output.

Topic Git never edits `state.sqlite`. Local init, ignore, and commit require a valid runtime and persist only namespaced files under `<topic.runtime>/topic-git/`. Publication can begin before runtime and keeps its binding, plan, conflicts, and outcomes in the ignored Topic Publication Copy support root. A later approved publication mutation may promote a matching credential-safe binding into runtime support.

## Put Topic Publication Material

Use `$isomer-op-entrypoint use topic-git to <task>` for optional Source Topic Workspace root tracking or sanitized remote publication. Isomer CLI supplies read-only context and semantic paths; the operator runs Git directly against validated paths.

Topic Publication Copies belong under effectively ignored Project-root temporary storage, normally `tmp/topic-workspace-publish/<topic-id>/`. They stay outside the Source Topic Workspace, Project Config Directory, generated content root, Houmao state, canonical repositories, and worker workspaces. The copy is disposable projection state, not durable source authority.

Tracked publication files contain sanitized outputs, a Publication Projection Manifest, `topic-workspace-version.toml`, and exact submodule gitlinks. Copy-local `.isomer/topic-git/` support is never eligible for publication commits. See [Topic Workspace Git](../manual/topic-workspace-git.md) for privacy dispositions, same-remote branches, reconstruction, conflict rules, and component-first push ordering.

## Put Adapter Material

Adapter material belongs under the Topic Workspace runtime support surface and is created by adapter commands. For Houmao-backed execution, the adapter writes manifests, command payloads, logs, inspection snapshots, stop outcomes, handoff payloads, observations, and normalization payloads under the adapter root.

Use adapter-facing CLI commands rather than writing adapter manifests by hand:

```bash
isomer-cli --print-json project team-instances launch-material prepare ati-my-topic-deepsci --topic my-topic --adapter houmao
isomer-cli --print-json project team-instances launch ati-my-topic-deepsci --topic my-topic --adapter houmao
isomer-cli --print-json project team-instances inspect-live ati-my-topic-deepsci --topic my-topic --adapter houmao --integrity
```

Adapter command payloads are durable records when Isomer stores and references them through Workspace Runtime. Secret-like fields are redacted before storage.

## Change Storage Layout

Use path lifecycle commands instead of editing the Topic Workspace Manifest by hand:

```bash
isomer-cli --print-json project paths register custom.datasets.raw --topic my-topic --path data/raw --storage-profile topic_records_dir --create
isomer-cli --print-json project paths update custom.datasets.raw --topic my-topic --path data/raw-v2 --create
isomer-cli --print-json project paths unregister custom.datasets.raw --topic my-topic
isomer-cli --print-json project paths reset topic.repos.main --topic my-topic
```

`unregister` and `reset` do not delete filesystem targets and do not rewrite historical Path Plans. If runtime records already depend on an old path, validation should report drift rather than pretending the old records moved.

## What Not to Store

Keep these out of `.isomer-labs/` and Research Topic Config files:

- Runtime state.
- command outputs.
- live process ids.
- provider payloads.
- rich Artifact bodies.
- Evidence Items, Findings, Gates, Decision Records, and Provenance Records.
- credentials, tokens, API keys, passwords, or secret material.

Keep these out of durable topic records unless explicitly promoted:

- generated Pixi environment directories.
- temporary files under `topic.tmp`, `topic.repos.main.tmp`, or `agent.tmp`.
- uncommitted Agent Workspace scratch material.
- untracked agent-owned or topic-owned projection material.
- GUI Runtime State.

## Common Recipes

Create a durable topic records directory for raw data:

```bash
isomer-cli --print-json project paths register custom.datasets.raw --topic my-topic --path data/raw --storage-profile topic_records_dir --create
```

Create a supporting topic repository:

```bash
isomer-cli --print-json project repos create tools.benchmarks --topic my-topic
```

Find where an agent should place private outputs:

```bash
isomer-cli --print-json project paths get agent.private_artifacts --topic my-topic --agent experimenter
```

Check whether runtime truth exists and is coherent:

```bash
isomer-cli --print-json project runtime inspect --topic my-topic
isomer-cli --print-json project runtime validate --topic my-topic --require-ready-readiness
```

Compare recorded and configured storage answers:

```bash
isomer-cli --print-json project paths explain topic.repos.main --topic my-topic
isomer-cli --print-json project paths get topic.repos.main --topic my-topic --configured
```
