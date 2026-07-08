## Context

Isomer Labs already has setup-oriented tutorials under `docs/tutorial/`, plus manual and developer references. The missing layer is a research-operator tutorial suite that shows how to conduct an actual research topic after the project and topic workspace exist.

The source case study starts from the local FlashAttention/B200 Topic Workspace and the merged chatlog at `context/topic-chatlogs/merged-timeline.md`, with failure-pattern synthesis in `context/topic-chatlogs/confusion-analysis.md`. The public tutorial links should point to the sanitized repository `https://github.com/CodeGandee/isomer-example-fa4-analytical-model`, but tutorial prose should teach from local example paths and shortened prompt/response interactions.

## Goals / Non-Goals

**Goals:**

- Add a six-page research-workflow tutorial suite under `docs/tutorial/`.
- Keep `docs/tutorial/` focused on project creation plus research workflow, without Web GUI tutorial pages.
- Use the local FlashAttention/B200 Topic Workspace as the concrete example while keeping the workflow reusable for other research topics.
- Teach the user's actual intervention patterns with shortened prompt/response examples: sharpen intent, verify environment, steer passes, demand evidence, refine models, and inspect paper artifacts.
- Keep low-level `isomer-cli` examples under "Under the Hood"; the main tutorial steps should show how users prompt an agent equipped with Isomer system skills.
- Update navigation and validation so the suite is discoverable and checked.

**Non-Goals:**

- Do not add separate tutorials for agent-drift recovery or GUI inspection in this change.
- Do not publish raw chatlogs or long transcript excerpts as tutorial content.
- Do not change research record schemas, GUI behavior, system skills, or CLI behavior.
- Do not make tutorial execution depend on the local `isomer-content/` example workspace being present.

## Decisions

### Use One `docs/tutorial/` Directory

The research-workflow suite will live under the existing `docs/tutorial/` directory. The tutorial section should contain project-creation material and the research workflow pages, while Web GUI usage stays in the manual.

Alternative considered: keep a separate `docs/tutorials/` directory for the research workflow. That made the suite visually distinct, but it created an unnecessary singular/plural split.

### Six Tutorial Pages Match Research Stages

The suite will contain these pages:

- `author-research-intent.md`
- `prepare-topic-environment.md`
- `run-a-human-steered-research-pass.md`
- `validate-with-real-evidence.md`
- `develop-a-white-box-model.md`
- `write-and-inspect-a-paper.md`

This structure follows the actual chatlog arc: topic idea to intent, environment, research passes, evidence, modeling, and paper. The previously discussed drift-recovery and GUI-inspection tutorials are excluded; their lessons become brief pitfalls inside relevant pages.

### Distill the Chatlog into Prompt/Response Moves

Each tutorial should include shortened user prompt, user action, and AI response examples from the chatlog, formatted like `context/topic-chatlogs/merged-timeline.md`: `User Prompt:` or `User Action:` followed by blockquoted user text, then `AI:` followed by blockquoted response text when a response is shown. `User Action:` turns are especially important because manual skill activation through `$<skill-name> <args>` or `/skill-name <args>` is the main Isomer Labs user experience. Tutorials should show the user-facing invocation string such as `$isomer-deepsci-pipeline list passes`, not the internal log wording `Skill activated: ...`. The tutorial value is the reusable operator move, for example "separate emulator evidence from real hardware evidence," and the local Topic Workspace should be the concrete place where readers inspect intent, records, model code, chatlog summaries, and paper artifacts.

Alternative considered: publish long transcript excerpts. That would preserve history but would be harder for a new user to act on and would risk exposing noisy or overly specific details.

### Use a Consistent Tutorial Page Shape

Each page should use a predictable structure:

- Task and starting point.
- Starting point.
- Example user prompt / user action / good AI response interactions.
- Steering prompts for correcting or continuing the agent.
- Under the Hood for CLI and storage mechanics.
- What good looks like.
- Common pitfalls.
- Next tutorial.

This keeps the suite task-first while still leaving room for domain examples, diagrams, and short command snippets.

### Keep CLI Out of the Main Teaching Path

Tutorial steps should show user prompts and manual system-skill activations to an Isomer-equipped agent. Direct `isomer-cli` commands are allowed only in "Under the Hood" sections for debugging or explaining what the agent is doing. Source-checkout Pixi commands belong only in developer or manual-test contexts and should not appear as normal tutorial usage.

## Risks / Trade-offs

- Combining project-creation tutorials and research-workflow tutorials could make the index long → Mitigate by grouping the index into “Project Creation” and “Research Workflow.”
- The FlashAttention/B200 case could feel too domain-specific → Mitigate by presenting it as one concrete prompt/response example and extracting general operator actions.
- Tutorials may drift from skill names or CLI commands → Mitigate by running docs validation and keeping command snippets minimal.
- Local chatlog source may not be present in clean installs → Mitigate by keeping the public sanitized example repository in final links sections while teaching from the local workspace in this repository.

## Migration Plan

1. Create or update `docs/tutorial/index.md` and the six research-workflow tutorial pages.
2. Update `mkdocs.yml` to expose the project-creation and research-workflow pages under one Tutorials section.
3. Update docs validation if required pages are enforced.
4. Run docs validation and MkDocs strict build.
5. Remove Web GUI tutorial references from `docs/tutorial/`; keep Web GUI reference material in the manual.

## Open Questions

- Should each tutorial include short “case study source” notes naming the FlashAttention/B200 example, or should the suite avoid mentioning the local chatlog path entirely?
