# Idea Thinking Flow

Use this reference when idea work needs a more explicit internal reasoning path. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Start from the limitation**. State what fails, where it fails, why it matters, and what evidence says the failure is real.
2. **Split the problem**. Separate symptom, mechanism hypothesis, and consequence for each serious limitation.
3. **Keep competing hypotheses alive**. Preserve one main hypothesis plus two or three competing hypotheses until selection.
4. **Name the lever bucket**. Classify the route as data, model, objective, optimization, inference, evaluation, or infrastructure.
5. **Search with a reason**. Read literature to test a candidate claim, failure explanation, adjacent mechanism, or strongest prior-work overlap.
6. **Build a mechanism map**. Convert papers into mechanisms, assumptions, evidence, boundaries, code touchpoints, and smallest faithful implementation.
7. **Check falsification and reader value**. Name minimal experiment, failure result, confounder, abandonment condition, reader takeaway, and claim value.
8. **Run anti-self-deception checks**. Challenge strongest prior work, weakest assumption, easier baseline tweak, and local-optimum inertia.
9. **End with one research object**. Preserve one falsifiable claim, one code-level plan, one minimal experiment, one abandonment rule, and one relation-to-literature summary.

## Preferences

- Prefer limitation-first thinking over method shopping (if the failure is vague, otherwise sharpen the limitation before proposing mechanisms).
- Prefer competing hypotheses over a single favorite explanation (if one hypothesis is already decisive, otherwise record why alternatives were ruled out).
- Prefer fast falsification and reader value over large speculative mechanisms (if the route is expensive, otherwise justify the evidence-per-run).

## Constraints

- <MECHANISM_FRAMING> must separate symptom, mechanism hypothesis, and consequence.
- A serious route must name its lever bucket before candidate generation.
- A selected route must not remain a bag of possibilities.
- Cross-domain mechanisms must be translated causally rather than metaphorically.

## Quality Gates

### Metrics

- Competing hypothesis count: number of competing hypotheses kept alive before convergence; closer to 2-3 is better.
- Falsification clarity count: number of candidate routes with an explicit failure result or demotion condition; higher is better.

### Checks

- Limitation quality: the failure is concrete, important, and supported by evidence.
- Hypothesis quality: the main hypothesis and competing hypotheses can be distinguished by evidence.
- Mechanism quality: the route has code touchpoints and assumptions, not only a surface metric.
- Research-object quality: the output is one clear object fit for <SELECTED_HYPOTHESIS> or a clear blocker.
