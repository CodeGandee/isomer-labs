# Wiki Contract

The export manifest records its schema and exporter versions, Topic identity, target identity, generation time, selected Artifact ids, semantic ids, scopes, revisions, content checksums, page paths, relationship edges, provenance refs, managed paths, and created, changed, unchanged, stale, and removed path sets.

The stable target contains human-readable Markdown and canonical JSON. The exporter owns only paths listed in the prior valid manifest. It stages updates, replaces recognized managed files, preserves all unrecognized files, and reports stale pages instead of silently erasing provenance.

The viewer manifest records the independently implemented package viewer version, managed asset checksums, wiki target and manifest checksum, deployment target, loopback or approved network binding, port, Run and log refs, and launch time.
