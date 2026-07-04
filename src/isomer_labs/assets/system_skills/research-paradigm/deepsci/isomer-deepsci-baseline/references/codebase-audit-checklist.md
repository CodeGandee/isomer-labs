# Codebase Audit Checklist

Use this reference only when attach, import, or verify-local-existing is not enough and a source audit is truly needed. Typical triggers are reproduce-from-source, repair with code changes, or an unclear evaluation entrypoint. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Confirm audit necessity**. Start a source audit only when lighter routes cannot establish comparator trust.
2. **Record source identity**. Capture repository, package, version, tag, commit, source paper, and baseline variant in <CODEBASE_AUDIT_RECORD>.
3. **Map execution and evaluation**. Identify main entrypoints, scripts likely to be run directly, evaluation path, command or endpoint, configuration, data loading, preprocessing, metrics computation, outputs, checkpoints, and logs.
4. **Identify implementation structure**. Record key classes, functions, model components, data modules, metric modules, and service boundaries that affect trust.
5. **Check practical constraints**. Record external services, downloads, credentials, hardware assumptions, brittle setup, undocumented environment needs, and expected cost.
6. **Summarize trust risks**. State what the baseline does, how it runs, how it is evaluated, and the main risks or bottlenecks so later stages do not reopen the whole source.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer a focused audit of evaluation-critical paths (if a full audit adds no comparator trust, otherwise skip it).
- Prefer source-native commands and configs when they preserve paper comparability (if they differ, otherwise record deviations).
- Prefer documenting risks that affect trust, not every file in the repository (if a module is irrelevant to comparison, otherwise omit it).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- <CODEBASE_AUDIT_RECORD> must not become a broad codebase tour detached from comparator trust.
- Source audit should not precede attach, import, or verify-local-existing when those routes are concrete and trustworthy.
- External service, download, credential, hardware, and brittle environment constraints must be recorded when they affect feasibility or comparability.
- Later stages should be able to understand how the baseline runs and is evaluated without reopening the source from scratch.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Audit-path coverage: fraction of source identity, execution entrypoint, evaluation path, config, data flow, metric computation, outputs, checkpoints, logs, and trust-risk fields recorded; higher is better.
- Unresolved trust-risk count: number of environment, hardware, service, credential, download, setup, or comparability risks still unresolved after the audit; lower is better.

### Checks

- Necessity gate: reproduce or repair needs the audit.
- Identity gate: source, version, package, or commit is recorded.
- Execution gate: entrypoints, evaluation path, config, data, metrics, outputs, and checkpoints are mapped.
- Constraint gate: environment, hardware, services, downloads, and credentials that affect trust are visible.
- Summary gate: <CODEBASE_AUDIT_RECORD> explains baseline behavior, run path, evaluation path, and risks.
