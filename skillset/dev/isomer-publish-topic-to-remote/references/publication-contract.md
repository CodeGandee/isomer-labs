# Topic Publication Contract

## Purpose and Authority

A Topic Publication Copy exposes the current state of one Source Topic Workspace so another researcher can inspect its evidence, trace decisions, and reproduce the work. It is a disposable projection, not a Project Topic Workspace, canonical source, history-preserving mirror, backup, or promise of automatic restoration.

The source filesystem is the content authority. Root and nested Git repositories are diagnostic inputs for provenance and component resolution, but their indexes and commits do not limit which current source files may enter the publication.

Remote publication is opt-in. The target must have a credential-safe locator, declared visibility (`public`, `private`, or `restricted`), an approved Publication Binding, and authentication supplied outside publication artifacts.

## Context Resolution

Resolve the Project and exact Research Topic through the CLI:

```text
isomer-cli --print-json project self location
isomer-cli --print-json project self check --scope topic --topic <topic-id>
isomer-cli --print-json project context show --topic <topic-id>
isomer-cli --print-json project workspaces list
isomer-cli --print-json project paths list --topic <topic-id>
isomer-cli --print-json project paths get topic.runtime --topic <topic-id>
isomer-cli --print-json project paths get topic.repos.main --topic <topic-id>
isomer-cli --print-json project topic-actors list --topic <topic-id>
isomer-cli --print-json project team-instances list --topic <topic-id>
isomer-cli --print-json project runtime inspect --topic <topic-id>
```

Use only queries supported by the installed CLI and record unavailable surfaces. Topic registration is sufficient for publication; a live Workspace Runtime is not required. Never find the target by scanning sibling Topic Workspaces or guessing from path names.

## Default Publication Set

Publish these items when they exist and pass sanitization:

| Content | Publication Rule |
|---|---|
| Intent | Retain the topic's research intent at its Source Topic Workspace-relative path. |
| Environment declarations and settings | Retain reproducibility-relevant environment configuration after identity and credential sanitization. |
| Durable research records | Retain typed record revisions and lineage, including failures, rejections, and supersessions. |
| Latest paper | Retain the latest eligible validated PDF at its original relative Artifact path and link it from the root README. Never create `paper/latest.pdf`. |
| Topic Main | Publish as a fresh sanitized same-remote submodule branch. |
| Topic Actors | Publish approved actor repositories as fresh sanitized same-remote submodule branches. |
| Agents | Publish selected agent repositories as fresh sanitized same-remote submodule branches. |
| Third-party references | Represent registered GitHub repositories as submodules at their normalized upstream locator and exact observed commit. |
| Root README | Preserve sanitizable source README content and add one versioned reproduction-navigation block, including the latest paper link when available. |
| Projection metadata | Generate the research-record index, projection manifest, version record, and root `.gitmodules` when applicable. |

The default generated paths are:

```text
README.md
.gitmodules
.isomer-publication/research-record-index.json
.isomer-publication/topic-workspace-projection.json
.isomer-publication/topic-workspace-version.toml
```

All other retained content must keep its Source Topic Workspace-relative path. Git does not represent empty directories.

## Optional Heavy Content

The following content is excluded unless the current plan explicitly selects it:

| Optional Class | Examples |
|---|---|
| Downloaded raw materials | Paper files, source archives or trees, datasets, model weights |
| Raw experiment outputs | NCU reports, logs, dumps, generated datasets, checkpoints |

Changing either selection invalidates the prior plan. Repeat privacy, size, access, license, mutation, and verification review.

## Path Dispositions

Assign exactly one disposition to every considered source path:

| Disposition | Meaning |
|---|---|
| `track` | Copy sanitized content at the same relative path. |
| `template` | Render a sanitized replacement at the same relative path. |
| `exclude` | Omit the path and record the reason. |
| `component` | Replace a nested repository with a gitlink and submodule declaration. |
| `block` | Stop publication until the risk or ambiguity is resolved. |

Record the source fingerprint, destination mapping, disposition, and reason in the projection manifest. Default exclusions include Git control data, local credential stores, Workspace Runtime databases, caches, disposable temporary files, unregistered scratch data, unselected heavy content, and unapproved private actor or agent output.

## Identity and Privacy

Preserve organization identity and public research provenance. Public or private GitHub owners and repositories are organization identity, so their repository names and locators may remain when needed for provenance or submodule resolution. Preserve cited researcher names, organizations, DOIs, dataset identities, public source URLs, exact commits, hardware models, driver versions, and tool versions.

Sanitize an individual researcher's local identity:

| Sensitive Value | Replacement or Action |
|---|---|
| Username or home path | `${RESEARCHER_USER}` or `${RESEARCHER_HOME}` |
| Local Git author or email | `${RESEARCHER_NAME}` or `${RESEARCHER_EMAIL}` |
| Local hostname | `${LOCAL_HOST}` |
| Non-public IP address | `${LOCAL_IP}` |
| Hardware serial or unique local identifier | A stable non-identifying placeholder |
| Identity-bearing actor or agent name | A stable role or pseudonym without a published reverse map |
| Token, password, private key, cookie, signed URL, or other credential | Block publication; never retain even an excerpt |

Textual content may be templated when the result stays reproducible. Unsupported binary or archive content that may contain credentials or personal identity must block publication; filename masking is insufficient. Rescan every generated file, component commit, Git metadata surface, and final recursive clone.

Use a neutral publication author for fresh commits. Do not expose the local Git author's name or email.

## Repository Projection

Publish each topic-owned nested repository as a fresh sanitized branch on the same publication remote:

| Component | Deterministic Branch |
|---|---|
| Topic Main | `components/topic-main` |
| Topic Actor `<name>` | `components/topic-actors/<sanitized-name>` |
| Agent `<name>` | `components/agents/<sanitized-name>` |
| Superproject | `main` |

Topic Actor and Agent directories may be source worktrees of Topic Main. In the remote snapshot they become ordinary same-remote submodules at their original paths. Record their Topic Main anchor relationships. Manual reconstruction is required if someone later wants a working Topic Workspace.

Create fresh, identity-sanitized component commits without source ancestry. Commit and publish components first, then stage their exact gitlinks in the superproject. A component path must have mode `160000`; flattened component files are invalid. Detect sanitized-name collisions before assigning deterministic branches and block until every component has a unique stable mapping.

For a registered third-party GitHub reference, preserve its normalized upstream locator and exact commit. Do not copy or rewrite its upstream history, and never push to its remote.

## Publication Binding

A Publication Binding associates one remote identity, Research Topic, Source Topic Workspace, canonical branch, and publication mode. An `exclusive_snapshot` binding may authorize replacement of that remote's selected publication references, but every synchronization still requires:

- a fresh source inventory and sanitized projection;
- a fresh full remote heads, tags, and symbolic-HEAD inventory;
- current user authorization for the exact remote mutation plan;
- exact expected branch and tag sets;
- a stale-plan check immediately before mutation.

The remote represents current state, not source history. Fresh parentless sanitized commits are valid when the plan declares them.
