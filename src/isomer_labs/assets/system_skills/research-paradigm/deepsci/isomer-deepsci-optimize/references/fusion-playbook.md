# Fusion Playbook

Use this reference when the frontier justifies combining complementary optimization lines. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Verify fusion eligibility**. Confirm at least two lines have real strengths, those strengths are complementary, and one line alone is no longer improving fast enough.
2. **Profile source lines**. For each line, record strongest mechanism, strongest evidence, main weakness, and what must survive the fusion.
3. **Define the fusion claim**. State what is being fused, why it addresses a real bottleneck, and why strengths are complementary rather than redundant.
4. **Preserve comparability**. State what remains unchanged and what comparison surface must survive.
5. **Plan bounded validation**. Create DEEPSCI:FUSION-PLAN with first validation step and evidence that would prove the fusion worthwhile.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer fusion only after real source-line strengths exist (if one line is merely weak, otherwise do not fuse it).
- Prefer complementary mechanisms over combining everything (if strengths overlap, otherwise route to exploit or stop).
- Prefer returning to brief when the fusion hypothesis is underspecified (if fusion is clear, otherwise avoid premature implementation).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- DEEPSCI:FUSION-PLAN must identify source lines, strengths, weaknesses, keep-unchanged conditions, and validation signal.
- Fusion must not combine two same-mechanism lines under different names.
- Fusion must not combine two weak lines without clear strengths.
- Fusion must not be justified merely because multiple branches exist.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Real-strength line count: number of candidate or implementation lines with real, durable strengths before fusion; higher is better until at least two complementary lines exist.
- Fusion-survival coverage: fraction of line strengths that are explicitly marked as must-survive in the fusion plan; higher is better.

### Checks

- Eligibility gate: two or more lines have real, complementary strengths.
- Mechanism gate: fusion object and bottleneck are concrete.
- Comparability gate: keep-unchanged contract is explicit.
- Validation gate: first bounded check and success signal are defined.
