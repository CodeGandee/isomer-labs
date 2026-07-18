## Context

The package manifest currently models 57 independently installable skill directories: 21 core skills, 22 DeepSci skills, and 14 Kaoju skills. The installer flattens every selected directory into an agent host's top-level skill root, the v3 receipt records each flattened skill, and internal inspection treats a complete list of those names as evidence of complete family coverage.

That model conflicts with the intended user surface. Most entries are workflow owners, research stages, service routes, or shared procedures that users should reach through a small set of stable entrypoints. The Imsight skill-handling convention already defines the required parent-owned `subskills/` layout, object-style invocation designators, and public `$skill use <subcommand> to <task>` form.

Several identities must survive the physical regrouping. User Skill Callbacks target system skill names, Skill Binding Projection stores provider-neutral skill ids, research records name producer skills, and internal routes refer to stage owners such as `isomer-deepsci-scout`. These are logical capability identities, not installation-folder requirements. Protected visibility is therefore a packaging and routing property, not an authorization or secrecy boundary.

The completed `separate-kaoju-content-and-latex-templates` implementation is part of the current baseline. Kaoju now has independent named content-template and LaTeX-template state, package-owned role-aware template services, exact LaTeX composition, entrypoint-aware PDF builds, three distinct drift postures, and an applied Topic Workspace contract migration. Regrouping must preserve those semantics and records while replacing only skill discovery, filesystem ownership, and invocation routing.

## Goals / Non-Goals

**Goals:**

- Expose only `isomer-op-entrypoint`, `isomer-ext-deepsci-entrypoint`, and `isomer-ext-kaoju-entrypoint` as ordinary top-level Isomer skills when all extensions are installed.
- Keep every current non-pipeline workflow capability available as a protected, self-contained subskill owned by one public pack.
- Decide command versus subskill form by resource ownership: commands use their containing bundle's resources, while subskills own private resource bundles.
- Preserve the implemented Kaoju content-template and LaTeX-template roles, manager hierarchy, semantic identities, composition contracts, and migrated runtime state while moving its skill resources.
- Preserve protected logical ids for callbacks, Skill Binding Projection, durable records, compatibility lookup, and selective role projection.
- Apply the Imsight subskill layout and invocation notation consistently to entrypoints, protected members, and routed command pages.
- Make installation, upgrade, receipts, inspection, and validation reason about whole public packs and their nested member integrity.
- Provide a safe one-release migration from receipt-tracked flat installations without deleting unrelated user-owned skills.

**Non-Goals:**

- This change does not add an access-control system, encrypt protected content, or prevent an agent that receives a pack from reading its nested files.
- This change does not merge distinct workflow semantics, such as Kaoju trial and reproduction, or rewrite the scientific methods owned by DeepSci and Kaoju.
- This change does not redesign Kaoju named-template services, rerun its Topic Workspace template-contract migration, alter existing template records or managed trees, or collapse content and LaTeX roles into skill or subskill identities.
- This change does not rename the extension ids `deepsci` and `kaoju`, change Project Manifest extension declarations, or redefine Skill Binding Projection as a packaging schema.
- This change does not keep top-level compatibility shim skills for old public or protected names.
- This change does not promote Houmao packaging terms into canonical Isomer domain language.

## Decisions

### 1. Three Public Packs Own All Packaged Skills

Each installed pack is a normal top-level skill directory. Every protected capability is nested below its owner at `subskills/<logical-id>/` and retains its current self-contained bundle, including `SKILL.md`, `agents/openai.yaml`, commands, references, scripts, and assets when present.

Resource ownership determines the capability form. A procedure remains a direct or nested subcommand when it can use resources owned by its containing skill or subskill. A capability becomes a subskill when it needs a private bundle containing its own `SKILL.md`, runtime metadata, scripts, references, commands, assets, templates, or other support files. Private means scoped ownership and lifecycle, not secrecy or access control. A command may have a detail page and child command pages, but those files remain owned by the containing skill or subskill.

| Pack id | Public skill | Package source path | Installed by default |
| --- | --- | --- | --- |
| `core` | `isomer-op-entrypoint` | `operator/isomer-op-entrypoint` | Yes |
| `deepsci` | `isomer-ext-deepsci-entrypoint` | `research-paradigm/deepsci/isomer-ext-deepsci-entrypoint` | No; selecting extension `deepsci` installs it with core |
| `kaoju` | `isomer-ext-kaoju-entrypoint` | `research-paradigm/kaoju/isomer-ext-kaoju-entrypoint` | No; selecting extension `kaoju` installs it with core |

The former `isomer-deepsci-pipeline` and `isomer-kaoju-pipeline` bodies become the public entrypoint bodies. They do not survive as an extra nested pipeline layer. The old ids remain compatibility aliases in catalog metadata.

Alternative considered: retain every current skill as a top-level installation and hide selected names only in documentation. This leaves host discovery noisy and provides no enforceable ownership boundary, so it does not meet the goal.

### 2. Core Members Use One Protected Level and an Area Classification

The core pack stores each existing capability directly under `subskills/`. The manifest classifies members by `area` for documentation and policy without adding artificial category subskills.

| Area | Scoped member | Preserved logical id |
| --- | --- | --- |
| operator | `welcome` | `isomer-op-welcome` |
| operator | `project` | `isomer-op-project-mgr` |
| operator | `gui` | `isomer-op-gui-mgr` |
| operator | `identity` | `isomer-op-switch-identity` |
| operator | `system-skills` | `isomer-op-system-skill-mgr` |
| operator | `toolbox` | `isomer-op-toolbox-mgr` |
| operator | `topic-create` | `isomer-op-topic-creator` |
| operator | `topic-manage` | `isomer-op-topic-mgr` |
| operator | `topic-team` | `isomer-op-topic-team-specialize` |
| service | `topic-env` | `isomer-srv-topic-env-setup` |
| service | `agent-env` | `isomer-srv-agent-env-setup` |
| service | `package-repo` | `isomer-srv-resolve-pkg-repo` |
| service | `houmao` | `isomer-srv-houmao-interop` |
| service | `topic-service` | `isomer-srv-topic-service-agent-support` |
| shared | `bounded-run` | `isomer-misc-bounded-run-tips` |
| shared | `nvidia` | `isomer-misc-nvidia-tools` |
| shared | `package-specifics` | `isomer-misc-pkg-specifics` |
| shared | `tool-packs` | `isomer-misc-tool-packs` |
| shared | `research-ideas` | `isomer-research-idea-recording` |
| shared | `operation-sets` | `isomer-research-operation-set-recording` |

The public entrypoint absorbs the welcome menu as `help`, `show-options`, and the existing visible start-path commands. The protected `welcome` member retains the substantial read-only orientation procedure and can be called by the parent, but it is no longer installed or advertised independently.

Alternative considered: create `operator`, `service`, and `shared` category subskills and nest current skills one level deeper. Those category objects would contain little behavior, increase invocation depth, and complicate selective projection, so area remains metadata.

### 3. Extension Members Keep Their Method Boundaries

DeepSci protected members are `analysis`, `baseline`, `decision`, `experiment`, `figure-polish`, `finalize`, `idea`, `nature-data`, `nature-figure`, `nature-paper2ppt`, `nature-polishing`, `optimize`, `paper-outline`, `paper-plot`, `rebuttal`, `review`, `science`, `scout`, `shared`, `workspace`, and `write`. Each scoped member maps to the existing `isomer-deepsci-<purpose>` logical id and is stored at `isomer-ext-deepsci-entrypoint/subskills/<logical-id>/`.

Kaoju protected members are `acquire`, `audit`, `compare`, `discover`, `examine`, `export`, `frame`, `reproduce`, `shared`, `synthesize`, `trial`, `workspace`, and `write`. Each scoped member maps to the existing `isomer-kaoju-<purpose>` logical id and is stored at `isomer-ext-kaoju-entrypoint/subskills/<logical-id>/`.

The DeepSci public commands remain `empirical-pass`, `hypothesis-pass`, `list-passes`, `paper-pass`, `polish-pass`, `rebuttal-pass`, `revision-pass`, and `submission-pass`, plus `help`. The Kaoju public command inventory remains the accepted survey-intent, compatibility-procedure, and grouped-manager inventory, plus `help`. A task-only invocation may select a protected member without exposing that member as a top-level host skill.

The Kaoju inventory is read from the current role-aware process contract. `manage-paper-template()` remains one entrypoint-owned parent command whose declared children are `list()`, `show()`, `create()`, `copy()`, `update()`, `replace()`, `merge()`, `file()`, `metadata()`, `export()`, `observe()`, `archive()`, `delete()`, and `migrate()`. Deeper command objects preserve the implemented CLI hierarchy, including `file()->put()`, `file()->remove()`, and `metadata()->patch()`. Content versus LaTeX remains explicit command context, represented by `--kind content|latex`, rather than another skill, subskill, or command layer. Terminal invocation of `manage-paper-template()` retains its current task-based action and role resolution. The compatibility command `create-paper-template()` remains content-template-only and routes LaTeX stock work to the manager.

The protected `write` member remains a subskill because it owns private entrypoint metadata, artifact-binding guidance, and paper-production references. The public manager pages remain commands because they use the public entrypoint bundle and route bounded work to `write`. Python modules and checked JSON resources below `isomer_labs.kaoju` remain package-owned machine services queried through `isomer-cli ext kaoju`; regrouping does not copy them into either skill bundle.

Alternative considered: collapse all stages into command pages inside each entrypoint. Each stage retains a private resource bundle with its own skill entrypoint and runtime metadata, and many also own commands, references, scripts, or assets. The resource boundary therefore requires self-contained protected subskills; triggers, callbacks, outputs, and projection needs reinforce that boundary but do not replace the resource-ownership test.

### 4. Public and Internal Invocation Forms Are Deliberately Different

User-facing examples use these forms:

```text
$isomer-op-entrypoint use project to initialize this Project
$isomer-ext-deepsci-entrypoint use empirical-pass to test the selected hypothesis
$isomer-ext-kaoju-entrypoint use build-reading-list to build the accepted survey list
```

An empty invocation is equivalent to `use help`. A task-only invocation lets the public entrypoint select the command or protected member. It must proceed with the selected route or report a real blocker rather than stop at a menu.

Internal pages use scoped object notation such as `isomer-op-entrypoint->project`, `isomer-op-entrypoint->project->init-project()`, `isomer-ext-deepsci-entrypoint->scout`, `isomer-ext-kaoju-entrypoint->manage-survey()->list()`, and `isomer-ext-kaoju-entrypoint->manage-paper-template()->file()->put()`. The parent route table maps each scoped member to its protected logical id and nested bundle path, while each parent command page declares its direct child commands. Every active Markdown page that uses object notation declares the standard `skill_invocation_notation` frontmatter value from the Imsight style guide.

The canonical internal grammar is:

```text
skill-path := skill-name ("->" subskill-name)*
subcommand-chain := subcommand-name "()" ("->" subcommand-name "()")*
invocation := skill-path | skill-path "->" subcommand-chain
```

A bare component invokes a skill or protected subskill entrypoint. Every subcommand component uses `()`, including intermediate commands. In `X->parent()->child()`, `parent()` acts as an object generator that establishes only its declared child-routing or inherited context, and `child()` is the invoked terminal command. The chain does not implicitly execute the standalone terminal workflow of `parent()`. When `X->parent()` is terminal, it invokes the parent's declared standalone workflow, or its declared help, selection, or blocker behavior when the parent is routing-only. Once a subcommand chain begins, a later bare skill or subskill component is invalid. A public command and protected member may share a direct name because `X->Y()` unambiguously names the command while `X->Y` names the protected member.

Alternative considered: require users to type object notation. Object notation describes parent-owned internal routing and is unnecessarily coupled to the protected structure, so it is not the ordinary public prompt syntax.

### 5. Manifest v3 Separates Pack, Capability, and Invocation Identity

`manifest.toml` advances from `isomer-skillset-manifest.v2` to `isomer-skillset-manifest.v3`. The parser exposes first-class `SystemSkillPack` and `SystemSkillCapability` records rather than treating every capability as one installable record.

Each pack record contains:

- `pack_id`, `kind`, `description`, `source_path`, `entry_skill`, `always_available`, and `minimum_compatible_skill_version`;
- `extension_id` for optional extension packs;
- the ordered public command list and legacy public ids;
- the ordered protected logical ids owned by the pack.

Each protected capability record contains:

- stable `logical_id`, owning `pack_id`, `area`, scoped `member_name`, and manifest-relative nested `source_path`;
- canonical `invocation_designator` and optional legacy ids or legacy source paths;
- ordered `dependencies` expressed as logical ids, including valid cross-pack dependencies;
- callback insertion points and an optional per-capability compatibility floor.

The parser validates unique pack ids, public names, logical ids, scoped member names within a pack, source paths, invocation designators, extension ids, aliases, and an acyclic dependency graph. It validates that every protected-member designator is a bare skill path, every component in a subcommand chain has `()`, each child command is declared by its immediate parent, and no bare component follows a command component. These checks also apply when a command and protected member share a direct name. The parser also verifies that every protected path is below its owning pack and that every entrypoint and member contains a valid `SKILL.md`.

The three identity layers remain explicit:

| Identity | Example | Purpose |
| --- | --- | --- |
| Public pack id | `isomer-ext-deepsci-entrypoint` | Host discovery and ordinary user invocation |
| Protected logical id | `isomer-deepsci-scout` | Callbacks, bindings, provenance, catalog lookup, and selective projection |
| Invocation designator | `isomer-ext-deepsci-entrypoint->scout` | Parent-owned runtime routing |

Alternative considered: rename every durable capability id to its object designator. This would couple provider-neutral records to package layout and force migrations of callbacks and research provenance, so logical ids remain stable.

### 6. Protected Projection Uses Dependency Closure

Ordinary public installation always copies or links a complete pack. An internal catalog API resolves one or more protected logical ids to their nested source paths, invocation designators, owning packs, and transitive protected dependencies in deterministic order. Isomer adapters may use that API to project a bounded private capability set to a Topic Actor, Agent Role, Agent Profile, or Service Agent while Skill Binding Projection continues to name logical ids.

The initial dependency audit follows these rules:

- Every DeepSci or Kaoju member that consumes family-wide procedure semantics depends on its family `shared` member.
- Members that create or accept durable research outputs depend on the applicable core `research-ideas` or `operation-sets` member when their current workflow invokes those owners.
- Environment, package, GPU, Houmao, and Topic Service dependencies remain explicit cross-pack logical-id edges rather than copied prose.
- Selecting a member for private projection includes its dependency closure, but does not make those dependencies public user entrypoints.

Protected subskills keep their current full logical-id directory and frontmatter names. The parent uses a shorter scoped `member_name` only as its route key, which preserves standalone private projection compatibility while keeping object notation readable.

Alternative considered: infer dependencies by scanning prose at runtime. Prose inference is unstable and cannot reliably validate a selective projection, so dependencies are manifest-owned and statically checked against active routes.

### 7. Callback and Provenance Resolution Use Logical IDs

Callback registration, listing, and resolution continue to use protected logical ids such as `isomer-deepsci-scout`. The callback insertion-point catalog returns the owning pack and invocation designator in discovery or explained output. A protected member resolves and applies its own `begin` and `end` callbacks at the same workflow boundaries after the parent routes to it.

The old public ids `isomer-deepsci-pipeline` and `isomer-kaoju-pipeline` normalize to the new entrypoint ids for existing callback records and compatibility lookup. New registrations store the canonical entrypoint id and report the deprecated alias. Historical provenance remains unchanged; new provenance may record both the stable logical producer id and current invocation designator when the record schema has a suitable optional field.

Alternative considered: retarget every callback to the parent pack. That would erase stage-specific insertion points and change callback meaning, so callbacks remain attached to the logical capability that executes the workflow.

### 8. Installation Receipts Become Pack-Aware

The target-root receipt advances from `isomer-labs-skill-manifest.v3` to `isomer-labs-skill-manifest.v4`. Each tracked projection is a public pack and records its public name, pack id, source path, projection mode, package and skill versions, and protected member inventory. The protected inventory records logical ids, relative nested paths, invocation designators, and versions so status can detect a missing, extra, mismatched, or incompatible member without creating one top-level receipt record per member.

Selector behavior is:

- no selector installs the core pack;
- `--extension deepsci` or `--extension kaoju` selects core plus the named extension pack;
- all extensions selects all three packs;
- `--skill <public-entrypoint>` selects its owning pack;
- `--skill <protected-logical-id>` is accepted during the migration window, selects the complete owning pack, and emits a deprecation diagnostic;
- an unknown or ambiguous alias fails without mutation.

Status and explicit-root inspection verify the receipt, public projection, and nested protected inventory. A name-only live inventory can report `entrypoint_seen` for a recognized public pack, but it cannot report complete member coverage because host inventory does not prove nested integrity. Complete evidence requires a supported receipt or explicit-root inspection.

Alternative considered: keep the v3 receipt and record every nested member as if it were top-level. That misrepresents the deletion and projection unit and makes upgrades vulnerable to treating nested paths as independent installations.

### 9. Validation Recurses Through Pack Boundaries

`pixi run validate-skills` and package tests enumerate all public packs and protected capabilities from manifest v3. They validate the current entrypoint template, nested `SKILL.md` structure, release-aligned `agents/openai.yaml` versions, local resources, logical identity mapping, parent route table, object-notation grammar and frontmatter, public commands, callback insertion points, dependency closure, callback aliases, flat private-projection fixtures, and preservation of the current role-aware Kaoju process contract.

Validation also rejects:

- a protected logical capability that remains as an independently manifest-listed or packaged top-level skill;
- a public extension name outside `isomer-ext-<extension-id>-entrypoint`;
- a parent route that points outside its pack or bypasses the declared member mapping;
- a protected-member entrypoint designator with `()`, a subcommand component without `()`, a command chain with an undeclared parent-child edge, a bare component after a command component, or a same-name route whose syntax identifies the wrong declared kind;
- a public installer selection that projects a protected member beside its parent;
- stale direct `$isomer-<protected-id>` user instructions in active public guidance, except bounded migration text and logical-id CLI fields.

All 57 `agents/openai.yaml` metadata versions still match `project.version` for every release, including protected members, because private projection and compatibility inspection can observe them independently.

### 10. Documentation Describes Visibility, Not Security

Public installation documentation lists the three public entrypoints and extension selectors. Developer documentation includes the protected mapping, manifest identity layers, callback behavior, receipt migration, and selective projection API. Help output explains that protected means parent-routed and omitted from ordinary top-level discovery. It does not claim filesystem secrecy or an authorization boundary.

Install and upgrade output tells users to refresh the agent host or start a new agent session because many hosts cache skill discovery for the life of a session.

## Risks / Trade-offs

- [Host scanners might recursively discover nested `SKILL.md` files] -> Keep installed subskills below the standard parent-owned `subskills/` boundary, test each supported host fixture, and document any host that does not honor this boundary before enabling it.
- [A missing nested member could make a pack look installed from its top-level name] -> Require v4 receipt or explicit-root evidence for complete coverage and recursively validate the protected inventory.
- [Legacy callbacks or provenance could stop resolving after pipeline rename] -> Normalize declared legacy ids through catalog metadata and keep historical stored values unchanged.
- [Selective projection could omit a shared or service dependency] -> Make dependencies manifest-owned, reject cycles and unknown ids, and project the transitive closure in deterministic order.
- [One pack update replaces more files than a single-skill update] -> Preserve the existing no-force conflict rule, validate the complete staged pack before replacement, and track the pack as one receipt-owned unit.
- [Protected members remain readable to any agent that receives the parent pack] -> State clearly that protected is a visibility and routing classification, then use Skill Binding Projection and private projection when role-level minimization is required.
- [Removing old top-level skills could delete user modifications] -> Remove only paths recorded by a supported Isomer receipt, reject mismatched ownership evidence, and never remove ambient or untracked directories.
- [A large atomic migration can produce broad review noise] -> Move bundles without rewriting method content first, then update routes and metadata in focused commits or task groups while validating after each pack.
- [Kaoju skill relocation could regress the newer template contracts or rerun an already applied data migration] -> Treat the role-aware process, binding, template, composition, drift, and historical-record contracts as immutable migration inputs; update only entry-skill and protected-route identity fields, and test existing migrated Topic Workspace state without mutating it.

## Migration Plan

1. Add manifest v3 parsing, pack and capability data types, logical-id lookup, alias normalization, dependency closure, and recursive validation while retaining read-only support for manifest v2 fixtures.
2. Build the three public pack directories in a staging layout, move each existing bundle into its declared `subskills/<logical-id>/` path, rename the two pipeline entrypoints, and update parent route tables and invocation notation. Base the Kaoju move on the current role-aware skill files and preserve its content-template, LaTeX-template, composition, drift, and historical-record contracts.
3. Update callbacks, extension discovery, Skill Binding resolution helpers, internal inspection, and private projection adapters to consume the new catalog model.
4. Add receipt v4 and pack-based install, status, uninstall, and upgrade behavior. Keep v1 through v3 receipt readers for inspection and managed migration.
5. During an authorized upgrade, validate destination conflicts, stage and validate all selected new packs, write the v4 receipt, and only then remove obsolete top-level paths that the old receipt tracked. If staging or validation fails, leave the old projections and receipt intact. If cleanup fails, report a partial migration with exact retained paths and repair guidance.
6. Update documentation, CLI output, active specs, tests, fixtures, and all packaged skill metadata versions. For the Kaoju process query, replace the public entry-skill identity and protected routes without dropping manager actions, template roles, composition modes, or implementation decisions. Run recursive skill validation and the repository lint, typecheck, unit, and targeted integration suites.
7. Release the regrouping as one migration boundary. Tell users to run the managed upgrade and start a new agent session so host discovery reflects the new public surface.

Rollback before obsolete-path cleanup discards the staged packs and retains the v3 receipt. Rollback after a successful migration installs the previous package release with force through the managed installer; the installer must still refuse to overwrite or delete untracked user paths.

## Open Questions

No product decision blocks implementation. The dependency audit may add edges between already listed logical capabilities, and the exact public help ordering may change during content migration, but neither may introduce another public top-level skill or change the three agreed entrypoint names.
