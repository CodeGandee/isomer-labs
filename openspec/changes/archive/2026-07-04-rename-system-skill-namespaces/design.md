## Context

Production system skills now live under `src/isomer_labs/assets/system_skills/`, with repository-root `skillset/` acting as an authoring view. The active manifest and validation harnesses still use older namespaces: `isomer-admin-*` for operator skills and `isomer-rsch-*` for DeepScientist-derived research skills. The desired public contract keeps the `isomer-` product prefix, keeps `isomer-misc-*` for cross-domain helper interfaces, keeps `isomer-srv-*` for protected service-routed support, renames user-facing operator skills to `isomer-op-*`, and renames DeepScientist extension skills to `isomer-deepsci-*`.

## Goals / Non-Goals

**Goals:**

- Rename active user-facing operator skill identities from `isomer-admin-*` to `isomer-op-*`.
- Reclassify the Houmao interop skill from an operator skill to the service namespace as `isomer-srv-houmao-interop`.
- Rename active production DeepSci skill identities from `isomer-rsch-*` to `isomer-deepsci-*`.
- Keep `isomer-misc-*` and `isomer-srv-*` active names stable.
- Document the forward extension convention as `isomer-<extension-name>-<purpose>`.
- Update active packaged assets, authoring view paths, manifest entries, validators, tests, active specs, and active routing references together.
- Preserve passive provenance and archived change text unless it is treated as active runtime guidance.

**Non-Goals:**

- Do not add compatibility folders, aliases, symlinks, or duplicate active shims for old `isomer-admin-*` or `isomer-rsch-*` names.
- Do not move DeepSci skills out of `research-paradigm/deepsci/` or rename the manifest group away from `deepsci`.
- Do not change Isomer CLI command semantics, research record schemas, placeholder meanings, artifact format profiles, or package-resource helper APIs beyond manifest paths.
- Do not rename `isomer-misc-*` to `isomer-ext-*`; extensions are named by domain family.
- Do not rename existing `isomer-srv-*` skills; the change clarifies service responsibility and reclassifies Houmao interop into the service prefix.

## Decisions

1. **Keep the `isomer-` product prefix.** Use `isomer-op-*`, `isomer-srv-*`, `isomer-misc-*`, and `isomer-<extension-name>-*` rather than a shorter `ism-*` namespace. Alternative considered: `ism-*`, which is compact but too generic and loses the product signal.

2. **Treat `misc` as shared helper infrastructure, not an extension family.** Keep `isomer-misc-bounded-run-tips`, `isomer-misc-nvidia-tools`, `isomer-misc-pkg-specifics`, and `isomer-misc-tool-packs` unchanged. Alternative considered: `isomer-ext-*`, which conflicts with the intended model that extension families are named by domain, such as `deepsci`.

3. **Rename user-facing operator skills to `isomer-op-*`.** Map active user-facing operator names mechanically: `isomer-admin-project-mgr` to `isomer-op-project-mgr`, `isomer-admin-topic-creator` to `isomer-op-topic-creator`, `isomer-admin-topic-mgr` to `isomer-op-topic-mgr`, `isomer-admin-topic-team-specialize` to `isomer-op-topic-team-specialize`, and `isomer-admin-welcome` to `isomer-op-welcome`. Alternative considered: keeping `admin`, but these skills are user-facing operator workflows rather than hidden administration internals.

4. **Reclassify Houmao interop to service.** Map `isomer-admin-houmao-interop` to `isomer-srv-houmao-interop` under `service/` because it is bounded Houmao adapter support, not a visible operator owner workflow. Alternative considered: `isomer-op-houmao-interop`, but that would present protected adapter support as a user-facing operator skill.

5. **Rename DeepSci skills to `isomer-deepsci-*`.** Map each active `research-paradigm/deepsci/isomer-rsch-<purpose>` folder to `research-paradigm/deepsci/isomer-deepsci-<purpose>`, including `shared` and `workspace-mgr`. Alternative considered: keeping `rsch`, but the new convention needs the extension family in the skill name, and `deepsci` is already the manifest group and packaged root.

6. **Do not provide compatibility shims.** The rename is a breaking public interface change over packaged static skill assets. Keeping old aliases would make validators, docs, and installed catalogs carry two active names for the same responsibility. Alternative considered: temporary wrapper skills that route old invocations to new names, but that would preserve the ambiguity this change is removing.

7. **Update active references broadly but preserve provenance.** Rewrite active `SKILL.md`, `agents/openai.yaml`, active references, READMEs, placeholder bindings, manifest paths, validators, tests, and active OpenSpec specs. Leave archived changes and passive `org/`, source-copy, and migration notes alone unless active validators treat them as current guidance. Alternative considered: repository-wide replacement, which risks corrupting source lineage and older design notes.

8. **Strengthen validation around stale active names.** Validators should assert that active operator folders use `isomer-op-*`, active Houmao interop uses `isomer-srv-houmao-interop`, active DeepSci folders use `isomer-deepsci-*`, manifest entries match renamed folders, and active guidance does not invoke `isomer-admin-*` or `isomer-rsch-*` except in explicit migration or historical contexts. Alternative considered: relying on search during implementation only, which makes later regressions easy.

## Risks / Trade-offs

- [Risk] External users or agents invoke old skill names after the change. -> Mitigation: mark the rename as breaking, update docs and manifests together, and avoid compatibility shims so failures are direct and visible.
- [Risk] Mechanical replacement changes historical provenance or upstream source copies. -> Mitigation: scope rewrites to active runtime guidance and configure validators with active versus passive path classification.
- [Risk] Placeholder binding metadata keeps stale `--skill`, producer, or consumer values. -> Mitigation: include placeholder binding pages in the rename task and validation pass.
- [Risk] Service skills keep stable names but still route to old operator names. -> Mitigation: update service references and add tests for operator route names in service guidance.
- [Risk] Root `skillset/` symlink authoring view becomes stale after folder moves. -> Mitigation: perform moves in packaged asset directories, then validate the authoring view paths through existing skillset validators and package asset tests.

## Migration Plan

1. Move active packaged user-facing operator skill folders under `src/isomer_labs/assets/system_skills/operator/` from `isomer-admin-*` to `isomer-op-*`, and move Houmao interop to `src/isomer_labs/assets/system_skills/service/isomer-srv-houmao-interop`.
2. Move active packaged skill folders under `src/isomer_labs/assets/system_skills/research-paradigm/deepsci/` from `isomer-rsch-*` to `isomer-deepsci-*`.
3. Rewrite active skill identities in `SKILL.md`, `agents/openai.yaml`, active references, READMEs, `manifest.toml`, placeholder binding pages, and direct invocation examples.
4. Update validators and tests for the new expected inventories, stale-name checks, manifest path checks, and active/passive reference boundaries.
5. Update active OpenSpec specs and design docs that define current skill names, leaving archived changes and passive provenance as history.
6. Run focused searches for stale active `isomer-admin-*` and `isomer-rsch-*`, then run `pixi run validate-skills`, `pixi run validate-research-skills`, `pixi run lint`, `pixi run typecheck`, and `pixi run test` as appropriate.

Rollback is a normal git revert because the change affects source-controlled packaged assets and tests, not persisted runtime records or user Topic Workspaces.

## Open Questions

None. The chosen convention keeps `isomer-misc-*`, keeps existing `isomer-srv-*`, reclassifies Houmao interop to `isomer-srv-houmao-interop`, renames user-facing operator skills to `isomer-op-*`, and treats DeepSci as the first `isomer-<extension-name>-*` family.
