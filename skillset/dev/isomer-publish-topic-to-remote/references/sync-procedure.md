# Topic Publication Synchronization Procedure

## 1. Establish the Target

Resolve the Project and Research Topic through the commands in [publication-contract.md](publication-contract.md). Capture:

- Source Topic Workspace path;
- Topic Main path;
- Topic Actor and selected Agent paths;
- registered third-party repository paths, upstream locators, and commits;
- Topic Git state root;
- Publication Binding and mode;
- credential-safe remote locator and declared visibility.

Use the Project's ignored `tmp/` or `temp/` area for `<temp>/topic-workspace-publish/<topic-id>/` unless the binding records another approved Topic Publication Copy path. Validate that the copy is outside the Source Topic Workspace.

## 2. Inspect Without Mutating

Inspect the source filesystem, nested repository status, relevant Git metadata, environment declarations, durable research records, paper build records, and registered repository topology. Include relevant untracked and uncommitted source files in the inventory.

Read Git state with exact paths:

```text
git -C <validated-path> status --short
git -C <validated-path> rev-parse --show-toplevel
git -C <validated-path> remote -v
git -C <validated-path> rev-parse HEAD
```

Do not pull, fetch into source repositories, stage, commit, clean, reset, or rewrite them.

## 3. Build the Projection Plan

Apply the default and optional-content rules from the publication contract. For every considered path, record:

- source-relative path;
- fingerprint or exact component commit;
- disposition;
- destination-relative path;
- sanitization or template rule;
- exclusion or blocking reason;
- lineage or record identity when applicable.

The root README should preserve sanitizable source README content and add one versioned generated navigation block. That block should state that the repository is a current sanitized publication snapshot, explain the directory layout, link the latest eligible paper at its retained path, identify reproduction entrypoints, describe submodules, and list known limitations. Do not claim that the repository can automatically restore a working Topic Workspace.

Resolve the latest paper from one unambiguous typed `KAOJU:PAPER-PDF` record with accepted build and validation lineage. Confirm its checksum, size, license, and identity metadata. Do not select it by filename order or modification time.

The projection manifest should make the decision path inspectable. The research-record index should expose the retained record graph and revision state, including negative results. The version record should identify the projection contract version and source observation time without exposing local identity.

## 4. Construct the Topic Publication Copy

Create or refresh only the validated disposable copy. Use non-Git helpers for inventory, copying, sanitization, fingerprinting, manifest rendering, and validation. Do not use hidden Git wrappers or Python libraries to conceal Git mutations.

For each topic-owned component:

1. Create a fresh repository in the copy.
2. Materialize only the component's approved sanitized projection.
3. Set a neutral publication author.
4. Stage exact approved paths.
5. Verify the complete index against the component plan.
6. Create the fresh component commit.
7. Record its commit and deterministic branch.

For the superproject:

1. Materialize approved root content at matching Source Topic Workspace-relative paths.
2. Add root publication metadata.
3. Add topic-owned component gitlinks at their original relative paths.
4. Add registered third-party gitlinks at their original relative paths.
5. Render `.gitmodules` with same-remote topic-owned URLs and normalized upstream third-party URLs.
6. Stage exact paths and verify the complete index.
7. Create the fresh `main` commit with a neutral publication author.

## 5. Inventory the Remote

Observe the full remote reference namespace from the Topic Publication Copy:

```text
git -C <copy> ls-remote --heads --tags --symref publication
```

Fetch only selected references when content inspection is required; do not merge them. Record branches, tags, peeled annotated-tag targets, and symbolic HEAD separately.

If symbolic HEAD does not select `main`, plan a distinct provider-side default-branch action. Move symbolic HEAD before deleting an old selected default branch. A Git push alone may not change the provider's default branch.

## 6. Present the Exact Mutation Plan

The plan must state:

| Field | Required Content |
|---|---|
| Remote | Credential-safe locator, declared visibility, binding identity |
| Source | Exact Research Topic and Source Topic Workspace |
| Components | Branch, fresh commit, source-relative gitlink path |
| Superproject | `main` commit and expected parent count |
| Expected refs | Complete exact branch and tag sets after synchronization |
| Updates | Every create or force-update action by exact ref |
| Deletions | Every obsolete branch or tag by exact ref |
| Provider action | Any symbolic-HEAD or visibility change |
| Content options | Whether raw downloads or raw outputs are included |
| Risks | License, privacy, size, access, partial-publish, or unsupported-content limits |

An unknown remote visibility, incomplete inventory, unresolved disposition, or unspecified destructive ref action blocks synchronization.

## 7. Revalidate and Publish

Immediately before the first mutation:

1. Recompute source fingerprints used by the plan.
2. Reobserve the complete remote reference namespace.
3. Confirm the Publication Binding still matches.
4. Confirm the user authorized this exact current plan.

If any value changed, stop and regenerate the plan.

Run direct Git commands against validated paths. Use exact refspecs and exact staging paths. Never use `--all`, `--mirror`, or broad staging.

Publish in this order:

1. create or force-update each exact topic-owned component branch;
2. verify each remote component commit;
3. create or force-update exact `main`;
4. verify remote `main`;
5. perform any separately approved provider symbolic-HEAD action;
6. delete only exact approved obsolete branches and tags;
7. reobserve all heads, tags, and symbolic HEAD.

Record each completed action as it succeeds. If publication stops partway, report the precise remote state and resume only after a new remote observation.

## 8. Verify a Fresh Recursive Clone

Clone into a newly created temporary directory:

```text
git clone --branch main --recurse-submodules <credential-safe-remote> <fresh-temp-dir>
```

Verify:

- remote heads, tags, and symbolic HEAD equal the expected plan;
- the checked-out root commit is the published `main` commit;
- its parent count matches the declared current-state snapshot design;
- `git ls-files` matches the approved projection;
- every topic-owned and third-party component path has mode `160000`;
- each submodule resolves to the exact planned commit;
- no nested component content was flattened into the root tree;
- the recursive clone is clean;
- the root README links the latest eligible paper at its retained path;
- the paper checksum matches the planned Artifact;
- the projection manifest, research-record index, and version record are present and consistent;
- excluded paths, credentials, local identity, non-public network identifiers, and source Git metadata are absent.

Treat a failed recursive clone, missing submodule commit, privacy finding, unexpected ref, or content mismatch as a failed publication verification.

## 9. Persist and Report

Use supported Isomer persistence surfaces. When a Workspace Runtime exists, store Topic Git plans and outcomes beneath `<topic.runtime>/topic-git/`. Before runtime materialization, use the supported copy-local `.isomer/topic-git/` state. Never edit `state.sqlite` or use direct SQL.

Report:

- publication remote and declared visibility;
- root commit and exact remote reference set;
- symbolic HEAD target;
- topic-owned component branch, commit, and path mappings;
- registered third-party submodule commits;
- latest paper path and checksum;
- recursive-clone verification result;
- excluded optional content and other limitations;
- partial actions or remediation if verification failed.
