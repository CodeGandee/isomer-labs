## Context

Isomer currently resolves Effective Topic Context from explicit selectors, cwd, environment, local context, and Project Manifest defaults. Effective Topic Actor Context and Effective Agent Context similarly support selectors, environment, cwd, and recorded information, while the actor resolver may use the sole active manifest actor as a final default. These values are useful for semantic path resolution, but callers can mistake a default candidate for physical location or an active acting identity.

`isomer-op-switch-identity` deliberately defines an instruction-level Project Operator posture whose main effect is command cwd discipline. A persistent switch lives in the current operator session, not in Workspace Runtime or shared Project state. This boundary is important because multiple operator sessions can use one Project concurrently.

The observed failure crossed these boundaries: the prompt selected one Research Topic, the command ran at the Project root without an explicit topic selector, Effective Topic Context selected the Project Manifest default, and the agent treated the resulting not-found error as permission to copy material to an actor-local directory. The CLI behaved consistently with its selection rules, but neither the agent workflow nor the command result made the target mismatch sufficiently visible.

Since this proposal was created, Kaoju paper production has adopted an agent-fill TeX composition contract. Named `KAOJU:PAPER-TEMPLATE-LATEX` stock can be exported for manual editing, while `init-tex` snapshots that stock and scaffolds a paper-local `KAOJU:PAPER-DRAFT-TEX` whose fill manifest the write agent completes before `build-pdf`. Context preflight must preserve one Research Topic across both workflows without treating named-stock editing and paper-local TeX filling as interchangeable intents.

## Goals / Non-Goals

**Goals:**

- Report canonical ambient location independently from Effective Context defaults.
- Let callers check an intended operation scope and explicit target against ambient context before mutation.
- Preserve deterministic Effective Context precedence while making source strength and overrides visible.
- Make operator entrypoint and research workflows carry one reconciled target through every downstream CLI call.
- Make switched Topic Actor or Agent posture explicit in session planning, cwd selection, command selectors, and provenance.
- Return selected topic metadata with context-sensitive Kaoju named-template, TeX composition, status, and PDF-build successes and failures.
- Keep named LaTeX stock exchange separate from paper-local derived TeX filling and repair.
- Stop ad hoc filesystem recovery when a typed operation fails because of unresolved or conflicting context.

**Non-Goals:**

- Authenticating an OS user, authorizing filesystem access, or treating Effective Agent or Topic Actor Context as a security principal.
- Persisting a global current identity or switch posture in the Project Manifest, Topic Workspace Manifest, local context, or Workspace Runtime.
- Requiring all topic-scoped commands to run from the Topic Workspace or all Project-scoped commands to run from the Project root.
- Removing Project Manifest defaults or the sole-manifest-actor fallback from existing Effective Context resolution.
- Changing the canonical Kaoju template exchange surface or making arbitrary directory copies part of the template service.
- Changing the Kaoju agent-fill composition contract, MyST authority, fill obligations, or PDF build Gates.

## Decisions

### Separate Ambient Location from Effective Context

Add a read-only ambient-location classifier that canonicalizes cwd and matches it only against manifest-registered and semantically resolved workspace boundaries. Its payload reports cwd, workspace kind, matched root, owning Research Topic and Topic Workspace when applicable, worker name when cwd is inside a registered Topic Actor or Agent Workspace, and match provenance.

The classifier uses the most specific valid containing workspace. An Agent Workspace or Topic Actor Workspace match therefore wins over its containing Topic Workspace, and Topic Main is reported separately from the general Topic Workspace. Equal-specificity incompatible matches produce a diagnostic instead of a guess. Project Manifest defaults do not participate because they describe selection fallback, not physical location.

Alternative considered: infer location from the existing Effective Topic, Actor, and Agent Context result. This was rejected because a Project-root process can receive a default topic and sole manifest actor despite being outside both workspaces.

### Add Progressive `project self location` and `project self check` Queries

`project self location` returns ambient facts only. `project self check --scope project|topic|topic-actor|agent` combines that location with existing explicit selectors and Effective Context resolution to report the operation scope, selected target, selection sources, defaults considered, expected worker cwd when applicable, and an alignment verdict.

Alignment is not a blanket cwd gate. An explicit `--topic` may intentionally target a Research Topic from the Project root or another Topic Workspace; the result reports an explicit override and permits the caller to proceed. Implicit incompatible sources, unresolved required targets, and switched worker posture that does not match the selected worker workspace are blockers. A manifest default can select a topic when no stronger target exists, but it is labeled as a fallback and never becomes ambient location or active acting posture.

The new commands are additive progressive slices. Existing `project self identity` retains its Effective Context fields and source metadata for compatibility. The self-query catalog and generated Topic Main guidance add the new queries without turning `self show` into a broad dump.

Alternative considered: replace `self identity` with one consolidated command. This was rejected because identity, location, and intended task target answer different questions, and progressive self queries are already an established CLI contract.

### Keep Acting Posture in the Operator Session

Identity switching creates a session-local posture envelope containing target kind, Research Topic, Topic Actor or Agent name, resolved workspace cwd, persistence mode, and provenance wording. One-task and `act-as` envelopes expire after the bounded task; persistent envelopes remain in operator memory until reset.

The switch skill supplies the envelope to planning rather than expecting the CLI to rediscover it. For each downstream topic- or worker-scoped command, the operator uses the resolved worker cwd when the switch contract requires it and supplies explicit `--topic` plus `--topic-actor` or `--agent` selectors when supported. Before mutation, `project self check` validates the same target. Commands that must run outside the worker cwd retain explicit selectors and state why the other semantic path is required.

Alternative considered: store active switch state in `.isomer-labs/local.toml`, the Project Manifest, or Workspace Runtime. This was rejected because instruction-level posture is session-specific, concurrent sessions would contend over shared state, and the domain model does not treat Project Operator Session posture as durable runtime identity.

### Reconcile and Pin Target Context at the Entrypoint

The operator entrypoint first classifies the requested operation scope, then extracts prompt-supplied Project, Research Topic, Topic Actor, or Agent targets. It invokes the smallest self preflight needed, passing prompt targets as explicit selectors. The resulting target becomes immutable invocation context for the selected route unless the user changes scope or a conflict forces a new decision.

Project-scoped operations do not become topic-scoped merely because Effective Context can resolve a manifest default. Topic-scoped operations with no explicit target may use the configured default, but the entrypoint reports that source and pins the resolved topic on later commands. A named prompt target always becomes an explicit selector. Worker-scoped work additionally requires a selected worker or active switch posture.

Alternative considered: rely on cwd for all downstream commands. This was rejected because agent tool calls can choose workdir independently, some operations legitimately execute outside the selected worker cwd, and Project-root operation is a supported posture.

### Preserve Context on Typed Failures

Context-sensitive Kaoju named-template, `init-tex`, `tex-status`, and `build-pdf` payloads include a compact selected-context block on both success and structured failure. It identifies Research Topic, Topic Workspace, workspace path, and relevant resolution sources without duplicating the full Effective Topic Context. A not-found or composition diagnostic therefore identifies where the lookup occurred and can recommend an explicit topic selector.

The entrypoint and Kaoju write workflow also preserve intent after context resolution. “Export the LaTeX template for me to edit” selects named LaTeX stock exchange through `manage-paper-template()->export()` and its resolved `<exchange-root>/latex/<name>/` path. A request to fill or repair the current paper TeX selects the paper-local `KAOJU:PAPER-DRAFT-TEX` and its fill contract. Neither route silently substitutes the other, and paper-local repair never mutates named stock without a separate explicit request.

Skills treat a typed command failure as a failed operation against the pinned target. They may inspect, correct selectors, or route to the owning setup workflow, but they do not change Research Topic, add an alternate export target, or copy files directly unless the user explicitly requests a separate unmanaged copy operation.

Alternative considered: make the CLI search all registered topics after a not-found result. This was rejected because cross-topic search would weaken deterministic selection and could expose or mutate unintended topic state.

## Risks / Trade-offs

- [Risk] Agents may treat any cwd and target difference as an error even when an explicit cross-topic target is intentional. → Mitigation: distinguish `explicit_override` from blocking conflicts and require cwd alignment only for worker-posture operations that define it.
- [Risk] Canonical path matching may be ambiguous with symlinks, nested registrations, or overlapping custom workspace paths. → Mitigation: resolve paths without requiring existence, prefer the most specific registered semantic root, and reject equal-specificity incompatible matches.
- [Risk] Additional preflight commands increase agent latency and transcript size. → Mitigation: keep `location` and `check` progressive and compact, and require them only for context-sensitive routes rather than orientation-only or context-free commands.
- [Risk] Additive JSON fields or command names may affect strict consumers. → Mitigation: give each new subcommand its own payload slice and output schema tests; preserve existing `self identity` fields.
- [Risk] Skill text can drift from CLI behavior. → Mitigation: add validator checks and unit fixtures for target extraction, explicit selector propagation, switched posture, conflict handling, and no-copy recovery.
- [Risk] Context-preflight edits could regress the recently completed independent welcome and entrypoint routing split. → Mitigation: treat the committed public-pair structure as the implementation baseline and limit context changes to route-and-proceed workflows.
- [Risk] Agents could confuse named LaTeX stock export with the newer paper-local agent-fill TeX workflow. → Mitigation: validate intent-specific routing and test that template edit requests use the exchange surface while paper composition requests use the derived TeX tree.

## Migration Plan

1. Add ambient classification and alignment domain helpers with unit tests covering Project root, Topic Workspace, Topic Main, Topic Actor Workspace, Agent Workspace, nested cwd, custom paths, and ambiguous matches.
2. Register `project self location` and `project self check`, add deterministic text and JSON payloads, and update the progressive query catalog and generated guidance.
3. Add selected-context metadata to Kaoju named-template, `init-tex`, `tex-status`, and `build-pdf` results and structured errors while preserving template state, exchange paths, paper-local TeX state, and build Gates.
4. Update operator entrypoint, identity-switch, shared research preflight, and production research skill guidance plus their validators and fixtures, preserving the independent welcome split and agent-fill composition contract.
5. Update CLI and system-skill documentation, then run focused tests followed by repository lint, typecheck, and unit tests.

No persistent data migration is required. Rollback removes the additive CLI surfaces and skill requirements; existing manifests, Workspace Runtime data, templates, and Effective Context behavior remain valid.

## Open Questions

- Should the alignment verdict names be `aligned`, `explicit_override`, `unresolved`, and `conflict`, or use a more general diagnostic status vocabulary already used by the CLI?
- Should `project self check` accept only `--scope` plus existing selectors, or also expose a convenience `--posture` option that maps to the same explicit Topic Actor or Agent inputs without persisting state?
- Should selected-context metadata remain scoped to context-sensitive Kaoju paper operations in this change, or become a common extension-command envelope in a follow-up change?
