## 1. Tutorial Suite Structure

- [x] 1.1 Create `docs/tutorial/` with an index page that introduces the research-workflow suite.
- [x] 1.2 Add the six tutorial page files with stable slugs from the design.
- [x] 1.3 Update `docs/index.md` and existing tutorial overview pages so readers can find the research-workflow suite.
- [x] 1.4 Update `mkdocs.yml` navigation so project creation and research workflow tutorials live under one Tutorials section.

## 2. Tutorial Page Content

- [x] 2.1 Write `author-research-intent.md` covering topic creation, topic overview refinement, scope clarification, validation standard, expected outcome, and environment gate readiness.
- [x] 2.2 Write `prepare-topic-environment.md` covering dependency setup, host fact capture, required repositories, proxy/dependency handling, and readiness verification.
- [x] 2.3 Write `run-a-human-steered-research-pass.md` covering pass selection, status checks, artifact inspection, continuation decisions, and record preservation.
- [x] 2.4 Write `validate-with-real-evidence.md` covering evidence classes, real-hardware claims, NCU counter evidence, failed-run diagnosis, noisy measurements, and targeted saturation experiments.
- [x] 2.5 Write `develop-a-white-box-model.md` covering formula-to-execution-flow refinement, simulator/source use as references, candidate model comparison, saturated component prediction, and blocking path prediction.
- [x] 2.6 Write `write-and-inspect-a-paper.md` covering requested toolchain/template use, rendered PDF inspection, figure/table fixes, math notation clarity, and central proof placement.

## 3. Case Study and Style

- [x] 3.1 Use the FlashAttention/B200 chatlog analysis as source material through shortened prompt/action/response examples rather than long transcript excerpts.
- [x] 3.2 Add brief common-pitfall notes in relevant pages for proxy success, vague bottleneck labels, failed-run overinterpretation, and uninspected rendered artifacts.
- [x] 3.3 Keep direct `isomer-cli` examples under "Under the Hood" and no normal `pixi run isomer-cli` usage.
- [x] 3.4 Keep each tutorial task-first with task, prompt examples, manual skill-action examples, good AI responses, steering prompts, good outcome, pitfalls, and next tutorial.

## 4. Validation

- [x] 4.1 Update docs validation required pages if the tutorial suite should be enforced.
- [x] 4.2 Search docs for stale `pixi run isomer-cli` tutorial usage and stale links after adding `docs/tutorial/`.
- [x] 4.3 Run `pixi run docs-validate`.
- [x] 4.4 Run `pixi run mkdocs build --strict`.
- [x] 4.5 Run `openspec validate add-research-workflow-tutorial-suite`.
