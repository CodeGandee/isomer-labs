# Source Identity

## Identity Layers

Keep a conceptual work distinct from its material versions:

1. A **work family** groups related editions, preprints, reports, releases, repositories, datasets, or models when evidence supports that relationship.
2. A **Source Identity** names one immutable or version-pinned material.
3. A **source locator** identifies the exact inspected location inside that material.

## Minimum Identity by Source Class

| Source class | Identity fields |
| --- | --- |
| Paper or report | Title, authors or issuing body, date, stable publication identifier when available, version, and retrieval locator. |
| Source repository | Registered non-main `topic.repos.*` label, requested and resolved source locators, immutable commit or digest, relevant subdirectory, external acquisition method, sanitized command evidence, observation time, access and license posture, relationship basis, limitations, blockers, and provenance refs. |
| Dataset | Dataset name, version or fingerprint, source locator, split or subset, schema posture, license and access posture, and retrieval time. |
| Model | Model name, immutable revision or digest, source locator, configuration, license and access posture, and retrieval time. |

Moving branch names, mutable tags, latest-release labels, and managed symlinks are locators, not immutable identity. Resolve and record the observed immutable revision before source inspection or a claim-bearing Run.

Repository commands do not run through Isomer. Honor user-supplied procedures or select source-appropriate commands externally, verify the intended source and immutable identity, then register the existing target with `project repos register`. Registration alone proves topology, not identity or research acceptance. If external acquisition or verification fails, keep partial content outside Isomer ownership and record only sanitized blocker evidence.

## Work-Family Decisions

Record why materials belong to one work family and which item is primary for each claim. Do not merge similarly titled works, repository forks, derivative datasets, or converted model weights without relationship evidence.

## Drift

When a locator resolves to new content, keep the old Source Identity and add a new one. Record the drift, affected Evidence Items, and whether reinspection is needed.
