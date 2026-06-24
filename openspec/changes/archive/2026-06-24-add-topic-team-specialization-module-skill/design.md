## Context

`isomer-admin-topic-team-specialize` already belongs in the operator skillset because Topic Team Specialization is an operator-facing workflow, not a runtime adapter detail. This redo narrows the change around the skill bundle shape: use the `skill-creator` model for concise skill packaging, use the Imsight style for executable skill structure, and keep Isomer's canonical Topic Team Specialization boundaries intact.

The target workflow still adapts one Domain Agent Team Template for one Research Topic. The skill copies selected template material into the Research Topic's fixed Topic Agent Team Profile Bundle under `<topic-workspace>/team-profile/`, works inside the copied template root such as `<topic-workspace>/team-profile/execplan/` for `deepsci-mini`, and produces human-readable guide and plan artifacts before structured packet/profile validation. Help, project awareness, template inspection, topic context resolution, placeholder reconciliation, topic profile drafting, review approval, materialization, and launch orchestration live as short local subcommands inside this module skill.

## Goals / Non-Goals

**Goals:**

- Maintain `isomer-admin-topic-team-specialize` as one coherent module-level operator skill for Topic Team Specialization.
- Shape the skill as a lean Codex skill bundle with minimal `SKILL.md` frontmatter, `agents/openai.yaml`, local subcommand pages in `references/`, local support references for required domain/runtime knowledge, no `evals/`, and no auxiliary docs.
- Format the skill and each subcommand page according to the Imsight style guide: near-top `## Workflow`, numbered steps, concise workflow lines, detail sections for longer rules, and a fallback for freeform tasks.
- Incorporate former helper-skill behavior as local subcommands so the module no longer calls separate skills for its normal workflow, and include a `help` subcommand for usage information.
- Split the entrypoint workflow into manual single-subcommand mode, guided `step-by-step` mode, and automatic `fast-forward` mode.
- Preserve `team-specialization-guide.md`, `team-specialization-plan.md`, generated-guide fenced block marking, pre-adaptation checklist, and post-adaptation `Final Report`.
- Keep copied material inside the Topic Agent Team Profile Bundle and keep Domain Agent Team Template source material generic.
- Validate the skill with skill-creator validation and repository skillset validation.

**Non-Goals:**

- Do not add `evals/` to this skill or require subagent benchmark scaffolding for this change.
- Do not keep standalone operator skill folders whose behavior is incorporated as local subcommands.
- Do not make the module skill an approval, materialization, runtime recording, or launch surface.
- Do not create a second active Topic Agent Team Profile Bundle or profile id for one Research Topic.
- Do not edit Domain Agent Team Template source while specializing a topic.

## Decisions

### Decision: Use a Lean Skill-Creator Bundle

The target skill bundle should contain only the files needed for another agent to use the skill: `SKILL.md`, `agents/openai.yaml`, and directly useful local subcommand pages under `references/`. The `SKILL.md` frontmatter should contain only `name` and `description`, and `agents/openai.yaml` should expose deterministic UI metadata with a default prompt that names `$isomer-admin-topic-team-specialize`.

Alternative considered: keep `evals/` inside the skill for future benchmarking. The user clarified that this skill does not need eval artifacts, so validation and manual checks are enough for this change.

### Decision: Keep Required Support References Local

The module skill should not refer to project-global support files such as `.imsight-arts/...` or `docs/runtime-and-files.md` for information needed to execute the skill. Instead, it should include local `references/isomer-domain-language.md` and `references/runtime-and-file-boundaries.md` pages that contain the domain vocabulary and placement rules needed by the workflow.

Alternative considered: keep pointers to the canonical project docs. That reduces duplication, but it makes the skill less portable and violates the self-contained skill-bundle rule.

### Decision: Use Short Local Subcommands for Former Helper Calls

The module should not call separate operator skills for its normal workflow. Instead, it should expose a `## Subcommands` table and one-level local pages named with short verb-object ids: `resolve-project`, `inspect-template`, `resolve-context`, `map-placeholders`, `draft-profile`, `approve-profile`, `materialize-profile`, `launch-team`, `fast-forward`, and `step-by-step`, plus the literal `help` command for usage output. This keeps the module self-contained while preserving the conceptual boundaries of each operation.

Alternative considered: keep longer descriptive noun-phrase page names or keep a helper function map that points to standalone operator skills. Longer names are less command-like, and external helper references make the module depend on separate skill invocation.

### Decision: Add a Help Subcommand

The module should expose `help` as a local subcommand that prints what `isomer-admin-topic-team-specialize` does, how to invoke it, available manual and automatic modes, subcommands, outputs, and guardrails. If the skill is invoked without a prompt, it should default to `help`. `help` is an intentional single-word exception to the short verb-object naming convention because it behaves like a standard CLI help command.

Alternative considered: keep help text only in `SKILL.md`. That makes the information visible to agents after skill load, but it gives callers no explicit subcommand to request usage output.

### Decision: Split Default, Manual, Guided, and Automatic Operation

The entrypoint workflow should first choose among default help mode, manual mode, guided mode, and automatic mode. Default help mode handles empty invocations by running `help`. Manual mode lets a caller run exactly one local subcommand, such as `inspect-template` or `map-placeholders`. Guided mode runs `step-by-step`, which follows the same required specialization path as `fast-forward` while explaining each step and waiting for user confirmation before continuing. Automatic mode runs `fast-forward`, which executes the full specialization path through copied material adaptation, `Final Report`, and draft profile outputs, then stops before approval, materialization, or launch unless the user explicitly asks for those boundary subcommands.

Alternative considered: make the entrypoint always run the full sequence. That is convenient, but it prevents manual specialization and debugging of one bounded step.

### Decision: Remove Incorporated Standalone Skills

The standalone operator skill folders for project awareness, template inspection, topic context resolution, placeholder reconciliation, topic profile drafting, profile review approval, profile materialization, and team launch orchestration should be removed once their behavior is present as local subcommands. Service Request routing is not part of the topic-team-specialize workflow. This leaves one canonical operator entrypoint and avoids two active sources of workflow truth.

Alternative considered: keep the standalone folders as compatibility surfaces. That keeps older prompts working, but it preserves the duplication that the module skill is meant to remove.

### Decision: Use Imsight Workflow Formatting

`SKILL.md` and each subcommand page should place a `## Workflow` near the top and make that workflow the executable entrypoint. Steps should be numbered and concise. Longer rules belong in sections such as generated guide rules, plan structure, subcommand routing, output contract, guardrails, reference routing, and exit criteria. Each workflow should end with a fallback that tells the agent to build and execute a step-by-step plan from the available constraints when the default procedure does not match the user's task.

Alternative considered: keep a narrative operating model as the main entrypoint. That explains intent, but it makes the skill less predictable for agents that expect a direct workflow.

### Decision: Keep Topic Team Specialization as the Domain Boundary

The module skill may resolve project/topic context, inspect a Domain Agent Team Template, copy material into `<topic-workspace>/team-profile/`, read or create `team-specialization-guide.md`, write `team-specialization-plan.md`, adapt copied material, append a `Final Report`, and report packet/profile inputs. It must stop before claiming approval, materialization, launch readiness, or Agent Team Instance creation.

Alternative considered: let the module skill own the full path through launch. That would hide Topic Team Instantiation Packet approval, Topic Agent Team Profile validation, Workspace Runtime recording, and Execution Adapter preflight inside one broad skill.

### Decision: Keep Guide and Plan in the Copied Template Root

For `deepsci-mini`, the copied template root is `<topic-workspace>/team-profile/execplan/`, so the skill should place `team-specialization-guide.md` and `team-specialization-plan.md` there. If the guide is missing from copied material, the skill should synthesize it from copied template files and include the visible generated-guide fenced block. The plan should exist before adaptation and gain a `Final Report` after adaptation.

Alternative considered: put guide and plan at `team-profile/` root. That makes them easy to find but separates them from the copied template material they explain.

### Decision: Validate Both Skill Structure and Domain Terms

Validation should combine skill-creator's `quick_validate.py`, repository skillset validation, OpenSpec validation, and focused tests or manual checks that verify required Topic Team Specialization terms. The validator should not require `evals/`; instead it should check concrete bundle structure, local reference integrity, manifest metadata, Imsight workflow shape, required guide/plan terms, and `deepsci-mini` guide coverage.

Alternative considered: rely only on `pixi run test`. Unit tests are useful, but they do not by themselves catch malformed skill frontmatter, missing UI metadata, stale local references, or style drift in operator skills.

## Risks / Trade-offs

- The module skill becomes too broad -> Keep approval, materialization, runtime recording, and launch orchestration as explicit boundary subcommands with validation and provenance checks.
- Removing `evals/` reduces benchmark evidence -> Use focused validation commands and manual smoke checks for this operator skill.
- Generated guides look authoritative -> Require the exact visible generated-guide fenced block and include generated-guide status in the final report.
- Plan and packet duplicate information -> Treat `team-specialization-plan.md` as human-readable adaptation rationale and the Topic Team Instantiation Packet as structured validation and provenance input.
- Imsight formatting drifts over time -> Add validation or tests for near-top workflow, numbered steps, and fallback text in both `SKILL.md` and local subcommand pages.

## Migration Plan

1. Update `skillset/operator/isomer-admin-topic-team-specialize/SKILL.md` so it follows the Imsight entrypoint structure, defaults empty invocations to `help`, selects local subcommands from a table, supports `step-by-step` and `fast-forward`, and keeps longer rules in detail sections.
2. Keep `skillset/operator/isomer-admin-topic-team-specialize/agents/openai.yaml` synchronized with the skill name, short description, and default prompt.
3. Add local subcommand pages under `skillset/operator/isomer-admin-topic-team-specialize/references/`, give each page a short verb-object filename except `help.md`, and give each page its own near-top numbered `## Workflow` and fallback. Do not include `route-service` in this module workflow.
4. Remove `skillset/operator/isomer-admin-topic-team-specialize/evals/` and avoid adding auxiliary docs that do not directly support skill execution.
5. Keep or update `teams/deepsci-mini/execplan/team-specialization-guide.md` as the source guide for the primary supported template.
6. Remove standalone operator skill folders whose behavior is now represented by local subcommands.
7. Add local support references for Isomer domain language and runtime/file boundaries, then remove project-global support-file references from the skill bundle.
8. Update operator skillset docs and validation so the module skill is discoverable, no-`evals/`, self-contained, and checked for required subcommands plus the Topic Team Specialization guide/plan contract.
9. Run skill-creator validation, repository skillset validation, OpenSpec validation, and focused tests or smoke checks.
