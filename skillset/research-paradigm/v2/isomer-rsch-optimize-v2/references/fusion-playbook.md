# Fusion Playbook

Use this reference when the frontier justifies combining complementary optimization lines. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Verify fusion eligibility**. Confirm at least two lines have real strengths, those strengths are complementary, and one line alone is no longer improving fast enough.
2. **Profile source lines**. For each line, record strongest mechanism, strongest evidence, main weakness, and what must survive the fusion.
3. **Define the fusion claim**. State what is being fused, why it addresses a real bottleneck, and why strengths are complementary rather than redundant.
4. **Preserve comparability**. State what remains unchanged and what comparison surface must survive.
5. **Plan bounded validation**. Create <FUSION_PLAN> with first validation step and evidence that would prove the fusion worthwhile.

## Preferences

- Prefer fusion only after real source-line strengths exist (if one line is merely weak, otherwise do not fuse it).
- Prefer complementary mechanisms over combining everything (if strengths overlap, otherwise route to exploit or stop).
- Prefer returning to brief when the fusion hypothesis is underspecified (if fusion is clear, otherwise avoid premature implementation).

## Constraints

- <FUSION_PLAN> must identify source lines, strengths, weaknesses, keep-unchanged conditions, and validation signal.
- Fusion must not combine two same-mechanism lines under different names.
- Fusion must not combine two weak lines without clear strengths.
- Fusion must not be justified merely because multiple branches exist.

## Quality Gates

- Eligibility gate: two or more lines have real, complementary strengths.
- Mechanism gate: fusion object and bottleneck are concrete.
- Comparability gate: keep-unchanged contract is explicit.
- Validation gate: first bounded check and success signal are defined.
