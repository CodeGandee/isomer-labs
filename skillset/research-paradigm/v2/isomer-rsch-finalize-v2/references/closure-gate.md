# Closure Gate

Use this reference to prevent premature finalization. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Gather closure context**. Build <FINALIZE_CONTEXT_BRIEF> from latest baseline state, accepted runs, analysis reports, writing state, decisions, blockers, package manifests, review state, proofing state, submission state, and current topic documents.
2. **Inventory paper-like deliverables**. If a paper or report bundle exists, check manifest, outline, draft, references, claim-evidence map, evidence ledger, compile report, PDF or export state, and open-source release material when present. For LaTeX/TeX manuscripts, the compile report should name the engine and command, prefer Tectonic, and explain any fallback to TeX Live, `latexmk`, `pdflatex`, `xelatex`, `lualatex`, BibTeX, or Biber.
3. **Validate closure gates**. Confirm required evidence, writing, review, proofing, submission, outline, coverage, language, and package gates before treating the line as final.
4. **Route failed gates**. If a required gate fails, create <FINALIZE_BLOCKER_RECORD> and route through decision or the proper upstream skill instead of forcing closure.
5. **Record legitimacy**. State why finalization is legitimate now or which blocker prevents it.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer route-back through decision when closure legitimacy is uncertain (if all gates pass, otherwise proceed to claim ledger).
- Prefer explicit package inventory over general statements that outputs exist.
- Prefer checking latest durable state over chat memory (if restart or long pause makes state unclear, otherwise recover state first).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- Finalize must not proceed while major evidence, writing, review, proofing, submission, outline, or package gates remain unresolved.
- A paper-like deliverable must not be finalized when coverage, academic outline, language, or package state is only draft-checkpoint or review-package ready.
- Closure context must include latest baseline, run, analysis, writing, decision, blocker, and package or paper state when those exist.
- Failed closure gates must become <FINALIZE_BLOCKER_RECORD> or a route-back decision.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Closure-context coverage: fraction of latest baseline, run, analysis, writing, decision, blocker, package, manifest, review, proofing, submission, and topic-document surfaces checked when present; higher is better.
- Failed-gate count: number of required evidence, writing, review, proofing, submission, outline, coverage, language, or package gates still failing; lower is better.

### Checks

- Inventory completeness: <FINALIZE_CONTEXT_BRIEF> names accepted evidence, writing/package state, decisions, blockers, and manifest-like material when present.
- Gate clarity: passed and failed closure gates are explicit.
- Route legitimacy: closure, pause, archive, publish, or route-back is justified by durable evidence.
- Blocker clarity: <FINALIZE_BLOCKER_RECORD> states the missing gate, why it matters, and the next route.
