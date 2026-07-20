## 1. Ambient Location and Alignment Model

- [ ] 1.1 Add typed ambient-location and alignment result models with stable workspace-kind, source, verdict, expected-cwd, and diagnostic fields.
- [ ] 1.2 Implement canonical cwd classification across Project root, registered Topic Workspace, Topic Main, Topic Actor Workspace, Agent Workspace, nested custom paths, and outside-project locations using most-specific semantic path matching.
- [ ] 1.3 Implement scope-aware alignment for Project, topic, Topic Actor, and Agent operations while distinguishing explicit overrides, manifest fallbacks, unresolved targets, and blocking conflicts.
- [ ] 1.4 Add unit tests for default-topic and sole-manifest-actor separation, symlink or nested-path handling, ambiguous equal-specificity matches, explicit cross-topic targeting, and worker-cwd mismatch.

## 2. Progressive Self Query CLI

- [ ] 2.1 Add payload builders and concise text rendering for `project self location` and `project self check` without changing existing `project self identity` fields.
- [ ] 2.2 Register the new commands, `--scope` values, existing context selectors, deterministic JSON envelopes, and side-effect-free command handlers.
- [ ] 2.3 Add the new commands to `project self queries`, CLI help, examples, and generated Topic Main progressive-query guidance.
- [ ] 2.4 Add CLI tests covering Project root, two Topic Workspaces, Topic Main, Topic Actor and Agent Workspaces, text output, JSON output, explicit overrides, manifest fallbacks, conflicts, and no-mutation guarantees.

## 3. Kaoju Selected-Context Reporting

- [ ] 3.1 Add a compact selected-context serializer for Kaoju template services with Research Topic id, Topic Workspace id and path, and relevant resolution sources.
- [ ] 3.2 Attach selected-context metadata to template successes and structured failures, including `template_not_found`, without searching sibling Research Topics or embedding full Effective Topic Context.
- [ ] 3.3 Add multi-topic tests proving that an omitted selector reports the manifest-default lookup, an explicit selector targets the requested topic, and default LaTeX export remains on the selected Topic Workspace writing-template exchange surface.

## 4. Operator and Research Skill Contracts

- [ ] 4.1 Reconcile the active independent-welcome change, then update `isomer-op-entrypoint` workflow and references to classify scope, run context-sensitive preflight, convert prompt targets to explicit selectors, pin resolved targets, and reject unmanaged recovery.
- [ ] 4.2 Update `isomer-op-switch-identity` core and command pages to maintain a complete session-local posture envelope, check the selected worker, propagate selectors, preserve cwd discipline, and keep manifest defaults distinct from active posture.
- [ ] 4.3 Update the shared latest-context preflight so prompt-selected targets are queried explicitly, retained across subsequent commands, and rechecked after an intentional scope change.
- [ ] 4.4 Update production research and Kaoju template-management guidance so typed calls use pinned selectors and a failed export cannot become an actor-local or arbitrary filesystem copy without a separate explicit user request.
- [ ] 4.5 Extend packaged-skill validators and positive and negative fixtures for mandatory preflight, selector propagation, session-only switch posture, context-conflict blocking, and no-copy fallback behavior.

## 5. Documentation and Verification

- [ ] 5.1 Update the domain-language and CLI documentation to distinguish ambient location, Effective Context, task target, manifest fallback, and acting posture without presenting any as access-control identity.
- [ ] 5.2 Add a manual multi-topic acceptance check that reproduces the Project-root Kaoju export case and verifies explicit topic retention and canonical export placement.
- [ ] 5.3 Run focused self-query, context-resolution, Kaoju template, research-skill, and packaged-skill validation tests and resolve failures.
- [ ] 5.4 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test` and record the final validation result.
