## Context

User Skill Callback resolution is an agent hot path. Participating DeepSci and Kaoju skills call `project skill-callbacks resolve` at `begin` and `end`, and a pipeline may invoke several participating skills. The resolver currently returns `CallbackCommandResult.to_json()`, which is also used by callback registration, installation, listing, showing, disabling, and validation. That shared management serializer includes the Project root, full callback records, registry refs, source aliases, Toolbox registration and effective status, and gated ids.

The current handler also calls full `build_project_state()` before resolving callbacks. As a result, callback queries can report validation problems from unrelated Project capabilities even when the requested callback sources and gating state are valid. The ordinary execution path therefore pays both serialization cost and diagnostic noise.

The stored registry schema and callback ordering rules remain sound. This change separates output projections and validation scopes without changing callback storage, source authorization, precedence, Toolbox gating, or instruction authority.

## Goals / Non-Goals

**Goals:**

- Make ordinary callback resolution cheap and direct for agents.
- Preserve deterministic callback application order and stable callback identity.
- Give agents one unambiguous readable instruction entrypoint for every supported callback source type.
- Retain full provenance and gating explanation through explicit management surfaces.
- Prevent unrelated Project diagnostics from polluting or failing callback execution queries.
- Keep existing callback authority, external-source, secret scanning, insertion-point, and Toolbox gating rules.

**Non-Goals:**

- Change User Skill Callback registry files or Toolbox manifests.
- Inline callback bodies into CLI JSON.
- Automatically execute callback scripts or install callback skill directories.
- Add generic JSON field selection, a global compact-output mode, or a second callback resolution command.
- Suppress diagnostics about the requested callback registries, sources, insertion point, selected topic, or applicable Toolbox gating.

## Decisions

### 1. Ordinary `resolve` returns an execution projection

The default JSON payload keeps the standard CLI envelope and returns an ordered `callbacks` array. Each callback entry contains only `id`, `source_type`, and an absolute `instruction_path`; it includes `external: true` only for an explicitly authorized external source.

`instruction_path` points to the material the agent must read. For `prompt` and `prompt_file`, it is the resolved prompt file. For `skill_dir`, it is `<resolved-directory>/SKILL.md`. Returning an absolute entrypoint removes the need for `project_root`, path aliases, and caller-cwd assumptions. The array order remains the application order produced by the existing scope, priority, and stable-id sort.

The payload does not include echoed skill or stage, scope, status, priority, registry refs, source summaries, Toolbox ids or keys, Toolbox status, registration rows, or gated ids. The resolver has already used those fields to select and order the executable result. Stable callback ids remain because agents need them when reporting conflicts or source failures.

Alternative considered: add `--compact` and keep the current default. This preserves callers but leaves the primary agent path expensive and requires every participating skill to opt into the correct view. The execution projection is therefore the default and the change is explicitly breaking.

Alternative considered: inline callback bodies. This avoids a second file read but makes the CLI responsible for loading arbitrary skill material, duplicates skill-loading semantics, complicates relative references from `SKILL.md`, and increases output with content the agent must process through its normal instruction loader. Locator-only resolution keeps ownership clear.

### 2. `resolve --explain` owns detailed resolution evidence

The new `--explain` option returns the existing management-oriented resolution payload, including full callback records, registry refs, source metadata, effective Toolbox statuses, and gated callback ids. `list`, `show`, and `validate` retain their current detailed roles.

This preserves an operator path for diagnosing precedence, disablement, missing registration, or registry provenance without charging every agent invocation for those fields. No legacy management fields are duplicated into the compact response.

Alternative considered: add a separate `resolve-instructions` command. That would preserve the old command but split one conceptual operation across two names and leave `resolve` poorly aligned with its dominant consumer.

### 3. Resolution uses callback-bounded state and diagnostics

The CLI shall use a purpose-bounded Project state path for ordinary and explained resolution. It loads enough state for Project discovery, explicit or effective topic selection, visible registry refs, the requested packaged insertion point, callback registry and source validation, and applicable Toolbox status. It does not run unrelated environment, template, profile, research-record, or other Project capability validators.

Diagnostics from a visible registry remain relevant even when a malformed row cannot match the requested insertion point, because registry integrity determines whether its active instruction set is trustworthy. Missing or unreadable requested sources, unsupported target pairs, duplicate visible callback ids, and missing Toolbox registrations also remain visible. General Project health stays available through `project validate`, and callback inventory health stays available through `skill-callbacks validate`.

Implementation may add a callback-specific `ProjectValidationScope` or a dedicated state loader, but it must prove through tests that unrelated diagnostics neither enter the response nor change its exit status.

### 4. Participating skills consume locators directly

DeepSci and Kaoju callback workflow guidance will state that agents process compact callback entries in returned order. Agents read `instruction_path` as supplemental material according to `source_type`; a `skill_dir` entrypoint remains supplemental `SKILL.md` material rather than an installed or automatically executed skill. Ordinary workflows do not request `--explain`; they use it only when resolution needs diagnosis.

The repository skill validator will enforce this wording and reject guidance that asks agents to parse management fields during normal callback execution.

### 5. Payload growth is guarded structurally and quantitatively

Tests will assert an exact allowlist for compact top-level and callback-entry fields. A representative one-callback fixture will also have a documented serialized-size ceiling with stable fixture paths, while empty resolution will have its own compact contract assertion. The allowlist is the primary guard; the size ceiling detects formatting or envelope growth that the allowlist alone misses.

## Risks / Trade-offs

- [Existing consumers parse full `resolve` records] → Mark the change as breaking, document `resolve --explain`, `list`, and `show` migration paths, and update all repository consumers in the same change.
- [Absolute paths are longer than relative paths] → One absolute entrypoint is still substantially smaller than `project_root` plus several relative aliases, and it avoids caller-cwd ambiguity.
- [Purpose-bounded validation hides unrelated Project defects] → Keep those diagnostics in `project validate`; test that all callback-relevant integrity and safety failures still surface.
- [A source changes after resolution] → This time-of-check/time-of-use condition already exists because agents read callback files after resolution; this change neither expands source authorization nor weakens source validation.
- [A byte ceiling becomes brittle] → Use stable fixture paths and treat the exact field allowlist as the normative regression check.

## Migration Plan

1. Add the compact execution serializer and absolute instruction-entrypoint normalization without changing registry storage.
2. Add `--explain` and preserve the current detailed resolution payload behind it.
3. Introduce callback-bounded state loading and prove relevant diagnostic retention and unrelated diagnostic exclusion.
4. Update DeepSci and Kaoju skills, validators, CLI documentation, examples, and changelog migration guidance.
5. Update internal and external-facing tests to use compact fields or explicit explanation as appropriate.

No stored-data migration is required. Rollback restores the old default serializer and removes the option; registry and Toolbox state remain compatible in either direction.

## Open Questions

None.
