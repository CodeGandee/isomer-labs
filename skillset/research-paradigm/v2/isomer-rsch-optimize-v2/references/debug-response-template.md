# Debug Response Template

Use this reference when a strategically valuable candidate failed for a concrete and likely fixable reason. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **State the concrete failure**. Record error, failed command or check, status, affected candidate, and evidence source.
2. **Retrieve relevant prior lessons**. Use <OPTIMIZATION_MEMORY_CARD> or local attempt records when similar failures or repair lessons exist.
3. **Classify root cause**. Mark structural, local, environmental, data, evaluation, dependency, or unknown.
4. **Choose the minimal fix**. Keep the original solution intent and comparability surface unchanged unless the bug proves the design invalid.
5. **Define the next check**. State bounded smoke, unit, validation, or quick evaluation needed after the fix.
6. **Set archive threshold**. State what result proves the candidate should be archived instead of debugged again.

## Preferences

- Prefer targeted fixes over broad rewrites (if the root cause is local, otherwise route back to brief or loop).
- Prefer archive over debug when the failure is strategic rather than local (if candidate no longer beats alternatives, otherwise stop repair).
- Prefer reusing prior failure lessons before changing code (if no relevant lesson exists, otherwise proceed with evidence).

## Constraints

- <DEBUG_RESPONSE> must not introduce a new performance mechanism under a debug label.
- Debug must preserve keep-unchanged conditions for comparability.
- Repeated failure without a new root cause or evidence change should route to archive, decision, or blocker.
- Post-fix validation must be defined before editing.

## Quality Gates

- Error gate: concrete failure and evidence source are stated.
- Lesson gate: relevant prior lessons are checked or marked absent.
- Cause gate: likely root cause and uncertainty are explicit.
- Fix gate: minimal fix and keep-unchanged contract are named.
- Check gate: next validation and archive threshold are stated.

## Template

### Error

- concrete error:
- candidate:
- evidence source:

### Retrieved Lesson

- relevant prior attempt:
- reuse decision:

### Root Cause

- likely cause:
- confidence:

### Minimal Fix

- fix:
- keep unchanged:

### Next Check

- check:
- pass signal:

### Archive Threshold

- archive if:
