# Packaged System Skills

Official non-development Isomer system skills live in this package resource tree. The repository-root `skillset/` directory is a linked authoring view; runtime code must use package-resource helpers rather than derive repository paths.

`manifest.toml` uses `isomer-skillset-manifest.v4` and declares three atomic packs with two ordered public roles each:

| Pack | Public Welcome | Execution Entrypoint | Protected Members |
| --- | --- | --- | --- |
| Core | `operator/isomer-op-welcome/` | `operator/isomer-op-entrypoint/` | 19 members below entrypoint `subskills/` |
| DeepSci | `research-paradigm/deepsci/isomer-ext-deepsci-welcome/` | `research-paradigm/deepsci/isomer-ext-deepsci-entrypoint/` | 21 members below entrypoint `subskills/` |
| Kaoju | `research-paradigm/kaoju/isomer-ext-kaoju-welcome/` | `research-paradigm/kaoju/isomer-ext-kaoju-entrypoint/` | 13 members below entrypoint `subskills/` |

All six welcome and entrypoint siblings are public host-discoverable skills. Use `$<pack>-welcome` for newcomer orientation and typical usage patterns. Use `$<pack>-entrypoint use <subcommand> to <task>` or a task-only entrypoint invocation for concrete work. Selecting either public name installs, upgrades, or removes the complete two-public-role pack. Protected members keep stable logical ids for callbacks, bindings, provenance, compatibility, and private projection, but they are not independent public install units.

Protected is a visibility and routing classification, not a security boundary. A complete installed pack contains readable nested bundles. Role-level minimization uses selective private projection of a protected logical-id dependency closure.

Public skill roots use `SKILL.md`. Manifest-declared protected members use `SKILL-MAIN.md`, and preserved upstream entrypoints use `SKILL-SOURCE.md`, so recursive host scans do not register nested material as independent skills. A public execution entrypoint explicitly loads only the selected member's `SKILL-MAIN.md` and directly required local resources. A deliberately flattened private projection promotes the selected source entrypoint to destination `SKILL.md` because that projection is intended to be host-discoverable.

## Authoring Boundary

Keep a routable unit as a protected subskill when it owns private resources such as its own `SKILL-MAIN.md`, `agents/`, scripts, references, templates, or assets. Keep a procedure as a command when it uses only resources owned by its containing bundle. A parent command may expose child commands without becoming a subskill.

Object notation follows these rules:

- Skills and subskills are bare: `isomer-op-entrypoint->project`.
- Every command component has `()`: `isomer-op-entrypoint->project->init-project()`.
- Parent commands act as object generators: `isomer-ext-kaoju-entrypoint->manage-survey()->list()`.
- A command and subskill may share a name because `X->Y()` is a command and `X->Y` is a subskill.
- A bare component cannot follow a command component.

Every active Markdown page that uses object notation declares the standard `skill_invocation_notation` frontmatter value.

## Namespace Convention

Reserve `isomer-op-welcome` and `isomer-op-entrypoint` for the two core public roles. Reserve `isomer-ext-<extension-id>-welcome` and `isomer-ext-<extension-id>-entrypoint` for extension public roles. Protected logical identities retain responsibility prefixes:

| Prefix | Protected Responsibility |
| --- | --- |
| `isomer-op-*` | Operator workflow capability |
| `isomer-srv-*` | Bounded service support |
| `isomer-misc-*` | Shared helper capability |
| `isomer-research-*` | Paradigm-neutral research recording |
| `isomer-deepsci-*` | DeepSci research capability |
| `isomer-kaoju-*` | Kaoju research capability |

Do not use `isomer-ext-*` for protected helpers or a generic capability bucket. Do not add top-level compatibility folders for protected logical ids or former pipeline aliases.

## Catalog and Resources

When a public pack or protected member starts or stops resolving User Skill Callbacks, update the manifest insertion-point metadata with the workflow text. Callback identity remains the protected logical id. When one protected member depends on another, declare the logical-id dependency instead of reading a sibling path.

Kaoju process, semantic, binding, schema, template, composition, migration, validation, and build resources remain package-owned under `isomer_labs.kaoju`. Skills query them through `isomer-cli ext kaoju`; do not copy those resources into the public pack or protected writer bundle.

All public and protected `agents/openai.yaml` files must set `metadata.version` exactly equal to `project.version`, including release candidates. Treat `minimum_compatible_skill_version` as a separate compatibility policy.

Run `pixi run validate-skills` after catalog, routing, resource, callback, dependency, or version changes.
