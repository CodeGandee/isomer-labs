## 1. Skill Tree Cutover

- [x] 1.1 Move every `skillset/research-paradigm/v2/isomer-rsch-*-v2` directory to `skillset/research-paradigm/deepsci/isomer-rsch-*`.
- [x] 1.2 Delete `skillset/research-paradigm/v1/` from the active working tree.
- [x] 1.3 Confirm no active compatibility folders, symlinks, or aliases remain for `v1`, `v2`, or `-v2` research skills.

## 2. Production Skill Identity Rewrite

- [x] 2.1 Rewrite each promoted `SKILL.md` frontmatter `name` from `isomer-rsch-*-v2` to `isomer-rsch-*`.
- [x] 2.2 Rewrite each promoted `agents/openai.yaml` display name and default prompt to invoke suffixless `$isomer-rsch-*` names.
- [x] 2.3 Rewrite active sibling-skill references, shared-skill references, workflow routing, and package/setup routing inside promoted active guidance to suffixless names.
- [x] 2.4 Preserve `migrate/`, `org/analysis/`, `org/src/`, passive `templates/`, license notices, and provenance material as non-active traceability material where present.

## 3. Manifest, README, and Documentation

- [x] 3.1 Update `skillset/manifest.toml` from `[groups.deepsci-v2]` with `v2` paths to `[groups.deepsci]` with `deepsci` paths.
- [x] 3.2 Rewrite `skillset/research-paradigm/README.md` to describe the production DeepSci root, suffixless skills, deleted v1 skills, and non-active traceability directories.
- [x] 3.3 Update `docs/isomer-cli.md` placeholder-binding examples to use `skillset/research-paradigm/deepsci/*/placeholder-bindings.md` and suffixless producer, consumer, and skill names.
- [x] 3.4 Update operator skill docs and README entries that mention research bootstrap ownership to reference `isomer-rsch-workspace-mgr` under `skillset/research-paradigm/deepsci/`.

## 4. Placeholder Binding and Structured Output Metadata

- [x] 4.1 Rewrite active `placeholder-bindings.md` files to use suffixless `--skill`, `--producer`, `--consumer`, metadata JSON, and prose examples.
- [x] 4.2 Rewrite promoted skill placeholder registries and active references so `isomer-rsch-shared` owns `references/semantic-placeholders.md`.
- [x] 4.3 Confirm structured output bindings still preserve payload-first commands, validation steps, format profile refs, generated content names, and non-structured exclusions.

## 5. Validation Harness Updates

- [x] 5.1 Replace `EXPECTED_V1_SKILLS` and `EXPECTED_V2_SKILLS` with a suffixless production DeepSci inventory in `scripts/validate_research_paradigm_skillset.py`.
- [x] 5.2 Update canonical registry, allow-zone, role-classification, and special-case paths from `v1` or `v2` roots to `deepsci` paths.
- [x] 5.3 Update validation diagnostics and tests to reject active `isomer-rsch-*-v1`, `isomer-rsch-*-v2`, `research-paradigm/v1`, `research-paradigm/v2`, and `deepsci-v2` references while allowing clearly non-active provenance where intended.
- [x] 5.4 Update `scripts/validate_skillsets.py` checks that currently name `isomer-rsch-workspace-mgr-v2`.

## 6. OpenSpec and Integration References

- [x] 6.1 Update main OpenSpec specs affected by the migration after implementation so they describe production DeepSci rather than active v2 behavior.
- [x] 6.2 Update any archived or active change references only when they are active guidance; leave historical provenance untouched when it is clearly archival.
- [x] 6.3 Run repository-wide searches for stale active `isomer-rsch-*-v2`, `isomer-rsch-*-v1`, `research-paradigm/v2`, `research-paradigm/v1`, and `deepsci-v2` references and resolve or classify each hit.

## 7. Verification

- [x] 7.1 Run the research-paradigm validation harness and repair reported layout, naming, placeholder, binding, output-policy, and coupling issues.
- [x] 7.2 Run `pixi run lint`.
- [x] 7.3 Run `pixi run typecheck`.
- [x] 7.4 Run `pixi run test`.
- [x] 7.5 Run `openspec status --change promote-deepsci-research-skills` and confirm the change is apply-ready or complete according to OpenSpec.
