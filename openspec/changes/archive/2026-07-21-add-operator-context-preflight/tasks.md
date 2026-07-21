## 1. Ambient Location and Alignment Model

- [x] 1.1 Add typed ambient-location and alignment result models with stable workspace-kind, source, verdict, expected-cwd, and diagnostic fields.
- [x] 1.2 Implement canonical cwd classification across Project root, registered Topic Workspace, Topic Main, Topic Actor Workspace, Agent Workspace, nested custom paths, and outside-project locations using most-specific semantic path matching.
- [x] 1.3 Implement scope-aware alignment for Project, topic, Topic Actor, and Agent operations while distinguishing explicit overrides, manifest fallbacks, unresolved targets, and blocking conflicts.
- [x] 1.4 Add unit tests for default-topic and sole-manifest-actor separation, symlink or nested-path handling, ambiguous equal-specificity matches, explicit cross-topic targeting, and worker-cwd mismatch.

## 2. Progressive Self Query CLI

- [x] 2.1 Add payload builders and concise text rendering for `project self location` and `project self check` without changing existing `project self identity` fields.
- [x] 2.2 Register the new commands, `--scope` values, existing context selectors, deterministic JSON envelopes, and side-effect-free command handlers.
- [x] 2.3 Add the new commands to `project self queries`, CLI help, examples, and generated Topic Main progressive-query guidance.
- [x] 2.4 Add CLI tests covering Project root, two Topic Workspaces, Topic Main, Topic Actor and Agent Workspaces, text output, JSON output, explicit overrides, manifest fallbacks, conflicts, and no-mutation guarantees.

## 3. Kaoju Paper Selected-Context Reporting

- [x] 3.1 Add a compact selected-context serializer for Kaoju named-template and TeX composition or build services with Research Topic id, Topic Workspace id and path, and relevant resolution sources.
- [x] 3.2 Attach selected-context metadata to named-template, `init-tex`, `tex-status`, and `build-pdf` successes and structured failures, including `template_not_found` and composition blockers, without searching sibling Research Topics or embedding full Effective Topic Context.
- [x] 3.3 Add multi-topic tests proving that an omitted selector reports the manifest-default lookup, an explicit selector targets the requested topic across template and composition commands, and default LaTeX export remains on the selected Topic Workspace writing-template exchange surface.
- [x] 3.4 Add intent-routing tests proving that a named LaTeX template edit request uses `manage-paper-template()->export()` while a paper-specific TeX fill or repair request uses `KAOJU:PAPER-DRAFT-TEX` and never mutates named stock implicitly.

## 4. Operator and Research Skill Contracts

- [x] 4.1 Update the current `isomer-op-entrypoint` workflow and references to classify scope, run context-sensitive preflight, convert prompt targets to explicit selectors, pin resolved targets, and reject unmanaged recovery while preserving the committed independent welcome delegation.
- [x] 4.2 Update `isomer-op-switch-identity` core and command pages to maintain a complete session-local posture envelope, check the selected worker, propagate selectors, preserve cwd discipline, and keep manifest defaults distinct from active posture.
- [x] 4.3 Update the shared latest-context preflight so prompt-selected targets are queried explicitly, retained across subsequent commands, and rechecked after an intentional scope change.
- [x] 4.4 Update production research and Kaoju paper guidance so typed calls use pinned selectors, named LaTeX stock exchange remains distinct from agent-fill paper TeX, and a failed export cannot become an actor-local or arbitrary filesystem copy without a separate explicit user request.
- [x] 4.5 Extend packaged-skill validators and positive and negative fixtures for mandatory preflight, selector propagation, session-only switch posture, context-conflict blocking, and no-copy fallback behavior.

## 5. Documentation and Verification

- [x] 5.1 Update the domain-language and CLI documentation to distinguish ambient location, Effective Context, task target, manifest fallback, and acting posture without presenting any as access-control identity.
- [x] 5.2 Add a manual multi-topic acceptance check that reproduces the Project-root Kaoju export case and verifies explicit topic retention and canonical export placement.
- [x] 5.3 Run focused self-query, context-resolution, Kaoju template and TeX composition, research-skill, and packaged-skill validation tests and resolve failures.
- [x] 5.4 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test` and record the final validation result.
