# Operational Guidance

Use this reference when the experiment route needs longer planning, workspace, resource, durable-output, memory, evidence-record, or charting notes rather than only the main control surface. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Choose the planning surface**. Use DEEPSCI:EXPERIMENT-PLAN and DEEPSCI:EXPERIMENT-CHECKLIST when the run is substantial, expensive, branch-sensitive, long-running, or likely to need recovery; otherwise keep the contract small and move to the decisive execution step.
2. **Respect the working boundary**. Modify only the active workspace for this route, treat comparator material as read-only, avoid branch or worktree guesswork, and keep durable outputs within the active Topic Workspace or agreed Isomer artifact surface.
3. **Respect resources and environment constraints**. Follow explicit resource assignments, record GPU or compute constraints when relevant, avoid silently broadening resource scope, and capture enough environment facts for reconstruction.
4. **Define durable outputs early**. Plan DEEPSCI:EXPERIMENT-ARTIFACT-MANIFEST, DEEPSCI:MAIN-RUN-RECORD, metrics, summary, command logs, config pointers, environment facts, and the final route decision before launching the real run.
5. **Use runtime memory selectively**. Query recent Workspace Runtime memory or prior evidence when reopening a tested command path or retrying an old run, and record durable lessons, incident patterns, comparability caveats, or route-changing outcomes before leaving the stage.
6. **Record evidence events at the right level**. Use progress updates for long-running execution, milestone updates for meaningful measured results, decision records for route choices, approval records for risky or expensive changes, and blocker records for incomplete or invalid states.
7. **Prepare connector-facing charts only when useful**. If the stage produces milestone visuals, highlight only the decisive delta and keep the palette calm, restrained, and consistent with the project's plotting style.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer a compact plan when the execution route is simple (if the run is expensive, otherwise use the full plan and checklist).
- Prefer exact workspace and resource facts over inferred branch or hardware assumptions (if the runtime exposes explicit values, otherwise record uncertainty).
- Prefer recording durable lessons only when they prevent repeated failures or preserve reusable experiment knowledge (if the note is just a run record, otherwise keep it in DEEPSCI:MAIN-RUN-RECORD).
- Prefer one concise milestone update after a recorded result over several low-signal chat pings (if the frontier changes during a long run, otherwise update at meaningful checkpoints).
- Prefer charts that show the decisive comparison (if many series are present, otherwise downplay non-decisive context).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- Active experiment work must stay inside the active workspace or explicitly assigned run surface.
- Comparator material must remain read-only.
- Explicit resource assignments must be respected exactly.
- Extra GPUs, broader datasets, new dependencies, or larger budgets must not be consumed silently.
- Durable output gaps must be named in DEEPSCI:EXPERIMENT-RESULT-SUMMARY or DEEPSCI:EXPERIMENT-BLOCKER-RECORD.
- Connector-facing visuals must not imply stronger evidence than the metrics support.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Run-manifest coverage: fraction of required run manifest fields captured for commands, paths, metrics, environment, resources, and provenance when a main run is executed; higher is better.
- Repeated-incident count: number of old command paths or failure patterns retried without checking recent memory or recording a new mitigation; lower is better.

### Checks

- Workspace gate: active workspace, comparator source, output surface, and branch assumptions are explicit.
- Resource gate: assigned resources, environment facts, dependency risks, and reconstruction gaps are recorded.
- Durable-output gate: DEEPSCI:EXPERIMENT-ARTIFACT-MANIFEST accounts for manifest, metrics, summary, command logs, config pointers, environment facts, and route decision.
- Memory gate: prior incidents are checked before repeated command paths, and reusable lessons are recorded before exit.
- Communication gate: progress, milestone, decision, approval, or blocker records match the actual stage state.
- Visual gate: any connector-facing chart highlights the decisive delta without overstating confidence.
