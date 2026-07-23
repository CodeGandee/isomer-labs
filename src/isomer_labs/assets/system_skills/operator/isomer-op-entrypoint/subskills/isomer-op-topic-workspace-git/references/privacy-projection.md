# Privacy Projection

Inventory current files through Isomer-resolved semantic Topic Workspace surfaces. Local root HEAD, index, tracked-file list, and commit state are diagnostics only, never publication authority.

Assign every considered path exactly one disposition:

| Disposition | Meaning |
| --- | --- |
| `track` | Copy reviewed current content unchanged. |
| `template` | Create an approved placeholder-bearing or explicitly sanitized output only in the publication copy. |
| `exclude` | Omit private, runtime, disposable, unapproved, or irrelevant material and record a reason. |
| `component` | Build an independently sanitized component repository and represent it as a submodule. |
| `block` | Stop until size, format, credential, private-key, signed-URL, license, or ambiguity risk is resolved. |

Never transfer `.git` directories, `.git` worktree files, configs, objects, refs, reflogs, indexes, worktree administration data, credential stores, remote configuration, or source history. Exclude Workspace Runtime, `state.sqlite`, local environments, caches, logs, temporary material, canonical external repositories, credentials, and unapproved records by default.

Structured templates use descriptive placeholders such as `${OPENAI_API_KEY}`. Arbitrary text requires an explicitly reviewed sanitized output. Unsupported binaries and archives block instead of receiving automatic masking. Leave every source byte unchanged and rescan every resulting file before it is eligible for a publication commit.

The tracked projection manifest and `topic-workspace-version.toml` contain only schema version, binding and plan ids, creation time, relative mappings, dispositions, transformations, output fingerprints, deterministic branches, and sanitized commits. They omit absolute source paths, source remotes, credentials, sensitive excerpts, raw private diffs, excluded content, and source Git configuration.

Compare expected sanitized output with the last generated fingerprint and current copy. Update only an unchanged prior output or an explicitly resolved conflict. Remove only an output whose source disappeared and whose current fingerprint still matches the last generated value. Preserve destination-only or simultaneous edits as conflicts and overwrite neither side. Persist the conflict and safe resume point without raw private content.
