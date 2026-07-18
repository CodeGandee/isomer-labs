## Why

The packaged catalog currently installs every operator, service, helper, and research-stage skill as a top-level user-discoverable skill. This makes the public surface noisy and exposes implementation capabilities that should be reached through a stable entrypoint, so the catalog should adopt Imsight parent/subskill packaging while preserving durable skill identities.

## What Changes

- **BREAKING** Replace flat top-level system-skill projection with three public packs: `isomer-op-entrypoint`, `isomer-ext-deepsci-entrypoint`, and `isomer-ext-kaoju-entrypoint`.
- Place all other Isomer system skills below an owning public pack's `subskills/` tree and classify them as protected members that are routed by the parent instead of independently installed or advertised to users.
- Group core protected members into operator, service, and shared support areas; group DeepSci and Kaoju members by their existing research-stage responsibilities while retaining distinct capabilities such as Kaoju trial versus reproduction.
- Replace the public `isomer-deepsci-pipeline` and `isomer-kaoju-pipeline` identities with the two `isomer-ext-*-entrypoint` identities, moving their command surfaces into the new public entrypoints rather than keeping a second pipeline layer.
- Adopt the Imsight invocation convention: users invoke `$<public-entrypoint> use <subcommand> to <task>`, empty invocation means `help`, bare object components identify skills or subskills, every command component uses `()`, intermediate commands generate the routing context for declared child commands, and pages that use object notation declare the standard notation contract.
- Use private resource ownership as the command-versus-subskill boundary: keep procedures that consume their containing skill or subskill's resources as direct or nested commands, and author a capability as a subskill when it needs its own scoped scripts, references, commands, assets, templates, runtime metadata, or other bundled resources. Private means scoped ownership, not secrecy.
- Treat the implemented Kaoju content-template and LaTeX-template separation as the migration baseline: preserve both named template roles, their independent `main` records, the `KAOJU:PAPER-TEMPLATE-LATEX` stock contract, role-explicit manager actions, exact TeX composition and build behavior, drift semantics, and historical-record posture while changing only skill packaging and routing identities.
- Revise the package manifest to distinguish public packs from protected logical capabilities and to record each member's logical id, owning pack, nested path, invocation designator, dependencies, callback insertion points, and compatibility aliases.
- Preserve existing protected logical ids such as `isomer-deepsci-scout` for Skill Binding Projection, callback targets, durable provenance, and CLI selectors, while resolving execution through the owning public pack. Do not install top-level compatibility shim folders.
- Revise installation receipts, status, inspection, upgrade, uninstall, and migration behavior around public pack projections. Legacy skill selectors resolve to the owning pack with a deprecation diagnostic, and upgrade removes only stale top-level projections tracked by an Isomer receipt.
- Recursively validate each protected subskill and its active resources, dependency closure, invocation notation, identity mapping, callback metadata, and release-aligned version even though only the parent pack is host-discoverable.
- Update packaged skill guidance, public documentation, CLI help, tests, and fixtures to describe the public/protected model and require a host refresh or new agent session after migration.

## Capabilities

### New Capabilities

- `protected-system-skill-routing`: Defines public pack ownership, protected subskill layout, command-versus-subskill resource ownership, nested command invocation, logical identity preservation, dependency closure, and visibility boundaries.

### Modified Capabilities

- `packaged-system-skills`: Change the package catalog and materialization contract from flat skills to public packs with protected members and pack-aware callback metadata.
- `system-skill-installer-cli`: Install, receipt, inspect, upgrade, and uninstall public packs instead of one top-level projection per logical capability.
- `system-skill-namespaces`: Reserve `isomer-ext-<extension-id>-entrypoint` for public extension entrypoints and distinguish those public identities from protected family capability ids.
- `packaged-system-skill-template-format`: Discover and validate active nested subskills recursively rather than treating only manifest-listed top-level roots as active skills.
- `skill-shared-resource-contract`: Route shared procedures through protected subskills using parent-owned invocation designators instead of assuming independently installed `<prefix>-shared` skills.
- `isomer-op-entrypoint-skill`: Make the operator entrypoint the sole public core pack, incorporate welcome/help, and route core protected capabilities and optional public extension entrypoints.
- `isomer-admin-welcome-skill`: Convert welcome from an independently invokable skill into protected operator-entrypoint help and update extension entrypoint names.
- `operator-admin-skills`: Treat operator owners as protected logical capabilities with parent-routed invocation rather than separate public skill folders.
- `isomer-admin-project-manager-skill`: Preserve the Project Manager workflow as a protected member and replace its standalone path and direct invocation contract.
- `isomer-op-gui-mgr-skill`: Preserve GUI management as a protected member and replace its standalone path and direct invocation contract.
- `isomer-op-system-skill-mgr-skill`: Make extension reconciliation pack-aware and route the manager as a protected member of the operator entrypoint.
- `isomer-op-toolbox-mgr-skill`: Preserve Toolbox management as a protected member and replace its standalone path and direct invocation contract.
- `operator-switch-identity-skill`: Preserve identity switching as a protected member and replace its standalone path and direct invocation contract.
- `topic-creator-skill`: Preserve Topic Creator as a protected member and replace its standalone path and direct invocation contract.
- `topic-manager-skill`: Preserve Topic Manager as a protected member and replace its standalone path and direct invocation contract.
- `topic-team-specialization-module-skill`: Preserve Topic Team Specialization as a protected member and replace its standalone path and direct invocation contract.
- `isomer-agent-env-setup-service-skill`: Preserve Agent Workspace environment setup as a selectively projectable protected service member.
- `isomer-service-env-setup-skill`: Preserve Topic Workspace environment setup as a selectively projectable protected service member.
- `isomer-houmao-interop-service-skill`: Preserve Houmao interoperability as a protected service member reached through Isomer routing.
- `isomer-bounded-run-tips-skill`: Preserve bounded-run guidance as protected shared support.
- `isomer-misc-pkg-specifics-skill`: Preserve package-specific guidance as protected shared support.
- `isomer-misc-tool-packs-skill`: Move tool-pack guidance behind protected shared routing rather than exposing it as a public helper by default.
- `isomer-deepsci-pipeline`: Rename the public DeepSci entry surface to `isomer-ext-deepsci-entrypoint` and route all DeepSci stages as protected members.
- `kaoju-research-extension`: Rename the public Kaoju entry surface to `isomer-ext-kaoju-entrypoint` and package all Kaoju capabilities as protected members.
- `research-paradigm-skills`: Change DeepSci and Kaoju production layout, validation, callback participation, and shared-skill routing to nested protected members.
- `isomer-internal-system-skill-inspection`: Classify public pack evidence and protected member integrity without treating name-only live inventory as proof of a complete pack.
- `user-skill-callbacks`: Keep callback targets bound to stable logical capability ids while catalog metadata resolves their protected invocation designators.

## Impact

The change affects packaged assets under `src/isomer_labs/assets/system_skills/`, the manifest parser and package-resource APIs, system-skill CLI selection and projection, receipt schemas and migration, internal inspection, callback catalog resolution, validators, public and developer documentation, and unit and integration fixtures. Existing user installations need a managed upgrade and agent-host refresh; Project extension ids remain `deepsci` and `kaoju`, durable protected logical ids remain valid, and unrelated user-owned skill directories remain untouched. Existing Kaoju Topic Workspace template records, managed trees, exports, drafts, builds, and migration state are data-plane inputs to this packaging change and are not migrated again.
