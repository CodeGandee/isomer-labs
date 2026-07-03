## 1. Data Model and Manifest Policy

- [x] 1.1 Add worker output root and `commit_after_operation` policy fields to Topic Actor manifest parsing, serialization, inspection, and validation.
- [x] 1.2 Add Agent output default and Agent-specific override parsing, serialization, inspection, and validation in Topic Workspace Manifest support.
- [x] 1.3 Validate configured worker output roots as workspace-relative paths and reject absolute paths, parent traversal, Project Config Directory targets, cross-topic targets, and paths outside the selected worker workspace.
- [x] 1.4 Add diagnostics for configured output roots that omit worker identity and could collide when multiple worker branches merge.

## 2. Semantic Surfaces and Path Resolution

- [x] 2.1 Add actor-scoped and agent-scoped semantic labels or resolver support for worker output roots.
- [x] 2.2 Implement default output-root templates under `isomer-managed/worker-output/topic-actors/{topic_actor_name}` and `isomer-managed/worker-output/agents/{agent_name}`.
- [x] 2.3 Extend Workspace Path Resolution so output root queries require Topic Actor or Agent context and return source metadata without creating directories.
- [x] 2.4 Record worker output root path plans during Topic Actor materialization and Agent Workspace setup when dependent records use those paths.

## 3. CLI Query and Materialization

- [x] 3.1 Add an agent-readable CLI query for worker output policy, or extend an existing CLI query, returning absolute root, worker-relative root, worker identity, source metadata, operation-set pattern, and `commit_after_operation`.
- [x] 3.2 Ensure the output-policy query states that `.gitignore` and Git status control whether files are tracked or committable.
- [x] 3.3 Materialize default or configured worker output roots during Topic Actor Workspace materialization.
- [x] 3.4 Materialize default or configured worker output roots during Agent Workspace setup or repair.
- [x] 3.5 Preserve generated and user-edited `.gitignore` behavior without adding tracked placeholder files under output roots.

## 4. Research Skill Guidance

- [x] 4.1 Add shared v2 research-paradigm guidance for resolving worker output policy before writing plain generated files.
- [x] 4.2 Update topic-dependent v2 research skills that write JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, or local summaries to use the resolved worker output root.
- [x] 4.3 Teach those skills to write operation outputs under operation-specific child sets instead of the worker workspace root.
- [x] 4.4 Teach those skills to check `commit_after_operation` after file-writing research operations and commit only when the resolved preference is true.
- [x] 4.5 Preserve existing durable record guidance so accepted Artifacts, Evidence Items, Runs, Decision Records, and View Manifests still use record bindings or `topic.records.*`.

## 5. Validation, Tests, and Documentation

- [x] 5.1 Add unit tests for manifest parsing, output-root validation, commit preference defaults, and actor or agent overrides.
- [x] 5.2 Add unit tests for Workspace Path Resolution and CLI output-policy query behavior for Topic Actors and Agents.
- [x] 5.3 Add materialization tests that verify output roots are created without tracked placeholder files and that `.gitignore` remains the tracking authority.
- [x] 5.4 Extend the research-paradigm validation harness to report active v2 skill guidance that writes plain files without resolving worker output policy or checking `commit_after_operation`.
- [x] 5.5 Update CLI and workspace documentation with examples for querying worker output roots and post-operation commit preference.
- [x] 5.6 Run `pixi run lint`, `pixi run typecheck`, `pixi run test`, and the research-paradigm skill validation command.
