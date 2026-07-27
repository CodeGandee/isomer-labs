# Privacy Projection

Inventory current files through Isomer-resolved semantic Topic Workspace surfaces. Classify semantic content before file format. Local root HEAD, index, tracked-file list, and commit state are diagnostics only, never publication authority.

Assign every considered path exactly one disposition:

| Disposition | Meaning |
| --- | --- |
| `track` | Copy reviewed current content unchanged. |
| `template` | Create an approved placeholder-bearing or explicitly sanitized output only in the publication copy. |
| `exclude` | Omit private, runtime, disposable, unapproved, or irrelevant material and record a reason. |
| `component` | Represent a sanitized topic-owned component or exact upstream reference as a submodule. |
| `block` | Stop until size, format, credential, private-key, signed-URL, license, or ambiguity risk is resolved. |

## Publication Defaults

| Semantic Class | Default |
| --- | --- |
| Current intent | Track sanitizable source and derived intent |
| Environment declaration | Track Topic Workspace manifest, Pixi declarations and lock, setup targets, Gate records, exact package versions, hardware models, and sanitized commands |
| Durable research record | Track every sanitizable typed revision needed for evidence, decision, failure, rejection, supersession, and provenance lineage |
| Topic Main, Topic Actor, or Agent content | Build a fresh sanitized same-remote component |
| Registered GitHub reference | Preserve normalized credential-free organization/repository identity and exact commit as an upstream submodule |
| Raw-material identity | Track locator, immutable version or digest, retrieval observation, access, license, evidence refs, and limitations |
| Raw experiment result | Track plan, sanitized command, environment identity, normalized result, checksums, verdict, and limitations |
| Validated paper PDF | Track after typed signature, checksum, size, license, validation-lineage, and identity-metadata review |

| Explicit Current-Plan Setting | Default | Effect |
| --- | --- | --- |
| Downloaded raw-material bytes | Disabled | Enable only the exact approved paper, source-tree, dataset, model, or related payload scope |
| Raw experiment-output bytes | Disabled | Enable only the exact approved profiler report, log, generated dataset, dump, checkpoint, or related output scope |

Changing either setting stales the plan and requires renewed privacy, size, access, license, and remote-mutation review.

Default exclusions remain:

- source `.git` directories and worktree files, configuration, objects, refs, reflogs, indexes, worktree administration, topic-owned history, incidental remotes, and credential stores;
- Workspace Runtime, `state.sqlite`, local environments, caches, and temporary material;
- downloaded material bytes and raw experiment-output bytes without their explicit current-plan setting;
- unregistered staging, scratch, and unsupported content that is not a typed durable record or approved publication input.

## Individual Identity and Provenance

| Content | Handling |
| --- | --- |
| Credentials, private keys, tokens, passwords, cookies, signed URLs, authenticated locators | Block; never record the value or excerpt |
| Local username and home path | Replace with `${RESEARCHER_USER}` and `${RESEARCHER_HOME}` |
| Local Git author, personal email, or contact field | Replace with `${RESEARCHER_NAME}` and `${RESEARCHER_EMAIL}` |
| Workstation hostname, IP address, or hardware serial | Replace with `${LOCAL_HOST}`, `${LOCAL_IP}`, or a typed non-identifying placeholder |
| Identity-bearing Topic Actor or Agent name | Replace consistently with a stable role or pseudonym; do not publish the reverse mapping |
| Public or private GitHub owner and repository identity | Preserve when the locator is normalized and credential-free; this is organization or source provenance |
| Cited researcher, organization, DOI, dataset identity, public source URL, exact commit | Preserve as research provenance |
| Hardware model, driver, package, tool, and version | Preserve when needed for reproduction |
| Arbitrary identity-bearing text | Require an explicitly reviewed sanitized output |
| Unsupported binary or archive masking | Block |
| Source content | Leave unchanged |
| Generated output | Rescan before commit eligibility |

Publication commits use neutral generated authorship rather than local Git author configuration.

## Generated Navigation and Lineage

Always generate these files only in the Topic Publication Copy:

| Output | Required Content |
| --- | --- |
| `README.md` | Research Topic, reproduction entry points, limitations, and `Latest paper: [PDF](paper/latest.pdf)` or `Latest paper: not yet available.` |
| `research-record-index.json` | Stable record refs, semantic ids, revision state, fingerprints, and relationships without runtime-only state |
| Projection manifest | Semantic classes, raw-byte settings, relative mappings, dispositions, transformations, component and reference identities, fingerprints, and limitations |
| `topic-workspace-version.toml` | Exact sanitized topic-owned branches and commits |

Resolve the latest paper from one unambiguous typed `KAOJU:PAPER-PDF` and its accepted build and validation lineage. Never use filename order or modification time.

Tracked projection metadata includes:

- schema, binding and plan ids, and creation time;
- semantic classes, raw-byte settings, relative mappings, dispositions, transformations, generated-navigation fingerprints, and reproduction limitations;
- deterministic topic-owned branches and sanitized commits;
- normalized GitHub reference locators, exact commits, visibility, license, and access limitations.

It omits absolute source paths, incidental source remotes, credentials, individual identity values, sensitive excerpts, private diffs, excluded content, and source Git configuration.

Four-way comparison rules:

| State | Action |
| --- | --- |
| Prior output unchanged | Update safely |
| Explicitly resolved conflict | Apply the approved resolution |
| Source removed and output unchanged | Remove safely |
| Destination-only or simultaneous edit | Preserve both sides as a conflict |

Persist conflicts and safe resume points without raw private content.
