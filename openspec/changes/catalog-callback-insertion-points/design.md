## Context

The current callback implementation accepts callback targets by checking that a skill name appears among active packaged system skill directories and that the stage is one of the hardcoded values `begin` or `end`. That is too broad: many packaged system skills do not actually resolve callbacks, and future optional system extensions may not be installed in every Project operator even though their catalog metadata ships with Isomer.

The packaged system-skill manifest already acts as the package-owned catalog for skill groups and manifest-relative skill paths. It is the right place to describe catalog facts such as core versus extension groups, callback stage definitions, and which skill paths expose callback insertion points. The Project Manifest is the right place to record user-declared operator facts such as "this Project operator has extension `deepsci` installed."

## Goals / Non-Goals

**Goals:**
- Make callback insertion points queryable through `isomer-cli` without scraping `SKILL.md` files or Python constants.
- Store callback insertion point declarations in `src/isomer_labs/assets/system_skills/manifest.toml`.
- Distinguish core packaged system skills from optional system extensions in the manifest.
- Let users record Project operator system extensions in `.isomer-labs/manifest.toml`.
- Make default insertion-point listing include core points plus Project-declared extension points.
- Keep CLI output honest about whether availability is known, user-declared, or catalog-only.
- Use manifest-declared insertion points for User Skill Callback and Toolbox callback target validation.

**Non-Goals:**
- Do not inspect or manage manually copied operator skill files.
- Do not make Isomer verify that every user-declared extension skill is physically installed.
- Do not mutate packaged system skill directories, `SKILL.md` files, or the packaged manifest during Project callback operations.
- Do not make optional extension insertion points appear by default unless the user declares the extension installed in the Project Manifest.

## Decisions

### Decision: Store Catalog Metadata in the Packaged System-Skill Manifest

Add group metadata, stage definitions, and per-skill insertion-point declarations to `assets/system_skills/manifest.toml`. Keep `groups.<name>.skills` as the membership source of truth and attach skill metadata by manifest-relative path:

```toml
schema_version = "isomer-skillset-manifest.v2"

[groups.core]
kind = "core"
always_available = true
skills = ["operator/isomer-op-entrypoint"]

[groups.deepsci]
kind = "extension"
extension_id = "deepsci"
always_available = false
skills = ["research-paradigm/deepsci/isomer-deepsci-scout"]

[callback_insertion_point_stages.begin]
label = "Begin"
description = "After mandatory context or entry-fit checks and before the first skill-specific action."

[callback_insertion_point_stages.end]
label = "End"
description = "After tentative outputs exist and before final response, handoff, or treating the workflow as complete."

[skill_metadata."research-paradigm/deepsci/isomer-deepsci-scout"]
callback_insertion_points = ["begin", "end"]
```

Alternative considered: derive insertion points by scanning `SKILL.md` for `skill-callbacks resolve` commands. That would be brittle, slow, and less clear than a manifest contract.

### Decision: Treat Project Operator Extensions as User-Declarations

Add Project Manifest storage for operator system extensions:

```toml
[operator.system_extensions]
installed = ["deepsci"]
```

The field means "the user declares this Project operator has this optional system extension installed." It does not mean Isomer verified the operator filesystem. The first implementation should use a simple string list rather than a table array, because no audit metadata is required yet.

Alternative considered: attempt to inspect the Project operator skillset. This is unreliable because users can manually copy skills into locations Isomer does not own or normalize.

### Decision: Add a Dedicated System-Extensions CLI Group

Expose Project operator memory through:

```bash
isomer-cli project system-extensions list
isomer-cli project system-extensions remember <extension-id>
isomer-cli project system-extensions forget <extension-id>
```

`list` reports catalog extension ids and whether each is Project-declared. `remember` validates that the id is a known optional extension and writes it to the Project Manifest. `forget` removes the id and leaves user skill files untouched.

Alternative considered: nest this under `project skill-callbacks extensions`. That would hide a Project-level operator fact under one consumer of the fact.

### Decision: Add Catalog-Backed Callback Insertion-Point Discovery

Expose insertion points through:

```bash
isomer-cli project skill-callbacks insertion-points
```

Default behavior lists core insertion points plus insertion points from Project-declared operator extensions. Filters allow explicit catalog slices:

```bash
isomer-cli project skill-callbacks insertion-points --extension deepsci
isomer-cli project skill-callbacks insertion-points --all-catalog-extensions
isomer-cli project skill-callbacks insertion-points --core-only
```

Each row includes `target_skill`, `skill_path`, `group`, optional `extension_id`, `stage`, stage description, and availability provenance such as `core_always_available`, `project_manifest_user_declared`, or `catalog_requested_not_verified`.

Alternative considered: make the command list all catalog extensions by default. That would produce insertion points that may be meaningless for a Project whose operator does not have those extension skills installed.

### Decision: Validate Callback Targets Against Declared Insertion Points

User Skill Callback registration, resolution, registry validation, and Toolbox callback manifest loading should validate the pair `(target_skill, stage)` against the packaged insertion-point catalog. Extension points can be accepted for known optional extensions because users may manually install them, but diagnostics and JSON output should distinguish Project-declared extension points from explicit catalog queries.

Alternative considered: keep validating every active packaged skill with `begin` and `end`. That preserves compatibility with broad targets but exposes nonfunctional callback targets as if they were meaningful.

## Risks / Trade-offs

- User declares an extension installed but the operator lacks the files -> CLI output can overstate practical availability. Mitigation: output `installation_verified = false` and `availability_basis = "project_manifest_user_declared"` for extension points.
- Manifest metadata drifts from `SKILL.md` callback workflow steps -> callback discovery becomes stale. Mitigation: add tests that compare declared insertion points for known callback-aware packaged skills with expected stage declarations, and document that callback-aware skill changes must update the manifest.
- Unknown third-party or locally copied extensions cannot contribute insertion points -> the first version only covers Isomer-known packaged system extensions. Mitigation: keep the Project Manifest field scoped to known system extensions and revisit external extension catalogs later.
- Changing validation may reject callbacks that target packaged skills without manifest-declared points. Mitigation: this is intentional catalog tightening; diagnostics should name the missing insertion point and suggest querying `project skill-callbacks insertion-points`.
