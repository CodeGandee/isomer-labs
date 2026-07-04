## Context

The packaged system skills now use responsibility-bearing namespaces: `isomer-op-*` for user-facing Project Operator Session and Operator Agent skills, `isomer-srv-*` for protected service-routed operational support, `isomer-misc-*` for public cross-domain helpers, and `isomer-<extension-name>-*` for domain extension families. `isomer-op-houmao-interop` currently sits in the operator subtree and is listed by the welcome skill as a direct owner skill, but its content mostly explains, maps, inspects, and constrains Houmao adapter/runtime details. The Isomer domain language treats Houmao concepts as execution-adapter details and treats Service Team work as bounded support commanded by a Project Operator Session or Operator Agent.

## Goals / Non-Goals

**Goals:**

- Move the active Houmao interop skill from `operator/isomer-op-houmao-interop` to `service/isomer-srv-houmao-interop`.
- Rename the skill identity everywhere active guidance, metadata, manifests, validators, tests, and generated skill catalogs present it as invokable.
- Remove Houmao interop from the user-facing operator owner-skill inventory and welcome menu.
- Preserve the useful interop modes: `help`, `explain-loop`, `customize-loop`, `map-template-to-houmao`, and `inspect-runtime`.
- Keep user-facing workflows such as Project lifecycle, Topic Team Specialization, approval, materialization, and launch orchestration under `isomer-op-*`, with service routing only for bounded Houmao support.

**Non-Goals:**

- Do not change Houmao adapter CLI behavior, runtime schemas, launch materialization, handoff dispatch, or live inspection semantics.
- Do not add a compatibility shim, alias folder, or duplicate active skill for `isomer-op-houmao-interop`.
- Do not promote Houmao native terms into Isomer core schema or user-facing operator language.
- Do not move unrelated service skills, DeepSci skills, or misc helper skills.

## Decisions

1. **Rename and move together.** The implementation will create `service/isomer-srv-houmao-interop` and remove `operator/isomer-op-houmao-interop`. Alternative considered: moving the folder while keeping the `isomer-op-*` name, but that would leave the namespace contract inconsistent and keep the old user-facing signal.

2. **Keep the skill as service-routed support, not a public helper.** The skill belongs under `isomer-srv-*` because it supports bounded operational work around the Houmao adapter/runtime and should normally be reached from operator workflows. Alternative considered: `isomer-misc-houmao-interop`, but `misc` is for public cross-domain helper interfaces rather than protected adapter support.

3. **Preserve content while reframing the entrypoint.** The existing subcommands and reference pages remain useful, but frontmatter, prompts, README text, output contracts, and guardrails should describe Service Request-style support at the command of a Project Operator Session or Operator Agent. Alternative considered: splitting explanation, mapping, and inspection into multiple service skills, but the current interop surface is coherent and small.

4. **Remove direct welcome-menu exposure.** `isomer-op-welcome` should route users to visible operator workflows such as `isomer-op-project-mgr` or `isomer-op-topic-team-specialize`; those workflows may route internally to `isomer-srv-houmao-interop` when Houmao-specific support is needed. Alternative considered: listing a service skill in the welcome menu with a warning, but that weakens the distinction between user-facing operator skills and service-routed support.

5. **Update active OpenSpec guidance that says the opposite.** The complete but unarchived `rename-system-skill-namespaces` change currently classifies Houmao interop as an operator skill. Implementation should revise active guidance or final synchronized specs so the active planning record no longer contradicts this change. Alternative considered: ignoring completed OpenSpec artifacts, but they still act as active guidance until archived or superseded.

6. **Treat the rename as breaking.** Active validators should reject `isomer-op-houmao-interop` as an invokable current skill outside passive historical or migration contexts. Alternative considered: keeping a temporary wrapper, but that would preserve the wrong responsibility boundary.

## Risks / Trade-offs

- [Risk] Existing users or agents may still call `isomer-op-houmao-interop`. -> Mitigation: update visible docs and generated skill catalogs, fail stale invocations through validation, and avoid a shim so the bad route is obvious.
- [Risk] Operator workflows may lose discoverability for Houmao troubleshooting. -> Mitigation: keep operator workflow docs saying that Houmao-specific support is routed to `isomer-srv-houmao-interop` when relevant, while the visible first command remains an operator skill.
- [Risk] Active complete OpenSpec changes may keep conflicting inventory text. -> Mitigation: include active OpenSpec guidance in the implementation search list and revise or supersede current guidance before validation.
- [Risk] The service skill could start owning launch or profile decisions. -> Mitigation: preserve guardrails that launch, approval, profile materialization, and Topic Team Specialization remain operator-owned or adapter-owned as appropriate.

## Migration Plan

1. Move the packaged skill directory from `src/isomer_labs/assets/system_skills/operator/isomer-op-houmao-interop` to `src/isomer_labs/assets/system_skills/service/isomer-srv-houmao-interop`.
2. Rewrite active skill identity text in `SKILL.md`, `agents/openai.yaml`, references, scenarios, READMEs, manifest entries, and direct invocation examples.
3. Remove `isomer-op-houmao-interop` from the operator owner-skill inventory, welcome menu, welcome required terms, and operator validation fixtures.
4. Add `isomer-srv-houmao-interop` to service inventory docs, service validation expectations, package asset tests, and manifest checks.
5. Update active OpenSpec artifacts and generated/synced skill catalogs such as `.kimi-code/skills` so current guidance has one active identity.
6. Run focused stale-name searches for `isomer-op-houmao-interop`, then run `pixi run validate-skills`, `pixi run validate-research-skills`, `pixi run lint`, `pixi run typecheck`, `pixi run test`, and `openspec validate move-houmao-interop-to-service --strict`.

Rollback is a normal git revert of source-controlled packaged assets, validators, tests, docs, and planning artifacts. No persisted runtime records or user Topic Workspaces need migration because this change only renames packaged skill assets and active guidance.

## Open Questions

None. The target active identity is `isomer-srv-houmao-interop`.
