## 1. Inventory and Asset Move

- [x] 1.1 Run focused searches for `isomer-op-houmao-interop`, `isomer-srv-houmao-interop`, `operator/isomer-op-houmao-interop`, and Houmao interop routing across active assets, docs, validators, tests, OpenSpec artifacts, and generated skill catalogs.
- [x] 1.2 Move `src/isomer_labs/assets/system_skills/operator/isomer-op-houmao-interop` to `src/isomer_labs/assets/system_skills/service/isomer-srv-houmao-interop`, preserving references, scenarios, and agent metadata files.
- [x] 1.3 Update the moved skill's `SKILL.md` frontmatter, title, description, operating model, workflow language, subcommand table, output contract, and guardrails so the active skill identity is `isomer-srv-houmao-interop` and the responsibility is service-routed Houmao adapter support.
- [x] 1.4 Update `agents/openai.yaml`, local reference pages, and scenario files under the moved skill so direct invocations and display metadata use `isomer-srv-houmao-interop`.

## 2. Manifest, Documentation, and Routing

- [x] 2.1 Update `src/isomer_labs/assets/system_skills/manifest.toml` so the core group lists `service/isomer-srv-houmao-interop` and no longer lists `operator/isomer-op-houmao-interop`.
- [x] 2.2 Update packaged system-skill README files so the operator inventory excludes Houmao interop and the service inventory includes `isomer-srv-houmao-interop`.
- [x] 2.3 Update `isomer-op-welcome` guidance and references so welcome menus no longer present Houmao interop as a direct owner skill, while relevant user-facing paths route Houmao-specific support through the appropriate operator workflow.
- [x] 2.4 Update other active operator guidance, especially Project Manager and Topic Team Specialization references, so Houmao loop, runtime, launch profile, mailbox, gateway, or template-mapping support routes to `isomer-srv-houmao-interop` only as bounded service support.
- [x] 2.5 Update active OpenSpec guidance that currently classifies Houmao interop as an operator skill, including the complete but unarchived `rename-system-skill-namespaces` artifacts when they are treated as current guidance.

## 3. Validators, Tests, and Generated Catalogs

- [x] 3.1 Update `scripts/validate_skillsets.py` expected inventories, welcome required terms, stale-name checks, service validation checks, and active/passive reference boundaries for `isomer-srv-houmao-interop`.
- [x] 3.2 Update unit tests and fixtures that assert operator owner skills, service skills, manifest paths, direct invocation text, stale skill names, or skillset validation behavior.
- [x] 3.3 Update package asset tests or import/resource tests so the packaged core skill manifest resolves the new service path and rejects the old operator path.
- [x] 3.4 Sync generated or mirrored skill catalogs such as `.kimi-code/skills` so they expose `isomer-srv-houmao-interop` and do not expose `isomer-op-houmao-interop`.

## 4. Validation and Close

- [x] 4.1 Run focused stale-reference searches and confirm active guidance has no current invokable `isomer-op-houmao-interop` references outside clearly passive historical or migration text.
- [x] 4.2 Run `pixi run validate-skills` and `pixi run validate-research-skills`.
- [x] 4.3 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
- [x] 4.4 Run `openspec validate move-houmao-interop-to-service --strict` and `openspec status --change move-houmao-interop-to-service` to confirm the change is apply-ready or complete according to the workflow stage.
