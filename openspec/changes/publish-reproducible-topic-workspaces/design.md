## Context

Topic Workspace publication already uses a disposable Topic Publication Copy, fresh sanitized histories, path-scoped Git, and a state-bound Publication Plan. Its current classifier treats canonical external repositories, unapproved records, PDFs, logs, and other binaries as blanket exclusions or blockers. That protects local state but permits a successful publication that lacks the intent, environment, durable record lineage, exact source versions, and latest paper needed to reproduce a survey.

The Source Topic Workspace remains canonical. Publication must not mutate it, publish Workspace Runtime or `state.sqlite`, reuse source Git ancestry, or store authentication material. The current Topic Git formatting edits are independent presentation improvements and remain compatible with this behavioral change.

## Goals / Non-Goals

**Goals:**

- Make the default Topic Publication Copy sufficient to inspect research intent, reproduce the declared environment, trace decisions and evidence, and retrieve exact referenced material versions.
- Keep downloaded material bytes and raw experiment-output bytes disabled unless the current Publication Plan explicitly selects their semantic classes.
- Preserve credential-free public and private GitHub repository identities as organization and source provenance while removing individual researcher and machine-local identity.
- Represent Topic Main, Topic Actor, and Agent content as fresh sanitized same-remote components, and registered GitHub reference repositories as upstream submodules pinned to exact commits.
- Generate a portable sanitized research-record index and an always-present root README with a deterministic latest-paper link.

**Non-Goals:**

- Publishing Workspace Runtime, `state.sqlite`, source Git metadata, authentication state, local environments, caches, or temporary surfaces.
- Mirroring private repositories, papers, datasets, models, or raw outputs without explicit selection and applicable access and license approval.
- Treating the Topic Publication Copy or its generated index as canonical research state.
- Guaranteeing access to a private reference repository for readers outside its access boundary.

## Decisions

### Classify semantic content before file format

The planner will assign each resolved source surface an implementation-level publication content class: intent, environment declaration, durable research record, topic-owned component, reference repository, raw material bytes, raw experiment-output bytes, private runtime, or other. File-level privacy classification runs after semantic selection. This prevents a root directory walk from treating all `records/` content or all PDFs alike.

Alternative: keep path and suffix rules as the primary classifier. Rejected because the same format can be a required final paper, a downloaded source paper, or an unrelated binary.

### Publish the durable research graph, not the runtime database

Every typed durable research record needed for lineage is eligible by default, including superseded, rejected, failed, blocked, and accepted revisions. Attached raw bytes follow their own content class. A generated sanitized research-record index records stable record refs, semantic ids, revisions, states, checksums, and relationships without absolute paths or runtime-only fields.

Alternative: publish only latest accepted records. Rejected because readers could not reconstruct direction changes, evidence disputes, failed trials, or paper revisions.

### Separate material identity from material bytes

Material manifests, exact locators, immutable versions or digests, retrieval observations, access posture, and license posture are default research records. Downloaded paper bytes, copied source trees, datasets, models, checkpoints, profiler reports, raw logs, and generated-data payloads require explicit per-plan selection. Structured trial plans, commands, normalized results, checks, and limitations remain default records.

Alternative: exclude both identity and bytes. Rejected because reproduction requires the exact material version. Including all bytes by default is also rejected because of size, license, privacy, and repository-history risks.

### Use two submodule sources

Sanitized Topic Main, Topic Actor, and Agent components continue to use deterministic branches in the publication remote. Registered GitHub reference repositories use their normalized credential-free upstream locator and exact reachable commit. Public or private GitHub owner and repository names are organization or source identity and remain visible. A private reference can be recorded and used when the intended audience has access; otherwise the plan reports an explicit access limitation rather than claiming complete reproduction.

Alternative: use the publication remote for every submodule. Rejected because it would copy or mirror third-party repository bytes and history. Copying local external checkouts is reserved for explicit raw-material publication.

### Sanitize individual identity contextually

Sanitization removes supplied local usernames, home paths, local Git author names and emails, workstation hostnames and IP addresses, personal contact fields, identity-bearing actor or agent names, hardware serials, credentials, signed URLs, and sensitive binary metadata. It preserves normalized GitHub repository locators, organization names, cited authors, DOI and dataset identities, public source URLs, exact commits, and reproducibility-relevant hardware models and software versions. Publication commits use neutral generated authorship.

Repository locators are protected provenance contexts: an owner segment that resembles a username is not redacted. Embedded usernames, passwords, tokens, query signatures, and fragments remain forbidden.

### Treat validated paper PDFs as typed publication outputs

The planner may approve a checksummed PDF Artifact after confirming its `%PDF-` signature, size policy, validation lineage, and sanitized metadata. The default copy retains published paper history when safe and always maps the latest unambiguous validated PDF to `paper/latest.pdf`. It never selects by filename or modification time.

Alternative: block every PDF as an unsupported binary. Rejected because the survey paper is a required publication output. Allowing arbitrary PDFs is rejected because downloaded papers remain opt-in raw material.

### Generate publication-only navigation

Every Topic Publication Copy contains a generated `README.md`. It links intent, environment, the portable research-record index, component topology, material-version manifests, reproduction limitations, and the latest paper. When no validated PDF exists, the stable line reads `Latest paper: not yet available.` The README and index are derived projection content and never modify the Source Topic Workspace.

### Bind selection settings to approval

The Publication Plan records the selected semantic classes, raw-material and raw-output opt-ins, typed binary approvals, reference-repository bindings, identity substitutions, reproduction limitations, generated README fingerprint, and research-index fingerprint. These values participate in the plan fingerprint so a changed opt-in or reference commit makes approval stale.

## Risks / Trade-offs

- [Structured records can still contain local identity in free text] → Rescan generated text, require explicit substitutions for observed identities, and block unsupported masking rather than silently publishing.
- [A private GitHub submodule may be unreachable to some readers] → Record visibility and access limitations, and do not claim complete reproduction unless the intended audience can resolve the commit.
- [Historical records increase repository size] → Keep structured lineage by default while placing large payload bytes behind explicit semantic opt-ins and size limits.
- [PDF metadata can leak authoring details] → Require typed PDF validation and sanitized metadata before binary approval.
- [A generated index can drift from source records] → Bind it to record fingerprints and regenerate it for every approved synchronization.
- [Semantic labels may be incomplete in older workspaces] → Report unresolved classification as a blocker or explicit limitation; do not infer canonical surfaces from sibling directories.

## Migration Plan

1. Add delta requirements and update the Topic Git skill pages.
2. Extend projection models and helpers with publication content classes, explicit raw-byte settings, reference-repository bindings, identity sanitization, typed PDF approval, README rendering, and research-index rendering.
3. Include the new settings and reference identities in plan fingerprints and manifests while retaining compatibility defaults for existing callers.
4. Add focused unit and integration tests, then run lint, type checking, and the default unit suite.
5. Existing publication bindings remain valid, but their next plan becomes stale because the default scope and generated outputs change.

Rollback removes the new generated files and returns to the prior classifier. It does not touch the Source Topic Workspace or remote branches without a separately approved synchronization.

## Open Questions

None. The default and explicit-selection boundaries are fixed by the requested reproduction and privacy policy.
