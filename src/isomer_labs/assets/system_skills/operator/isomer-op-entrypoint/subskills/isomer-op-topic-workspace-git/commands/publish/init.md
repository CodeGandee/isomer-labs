# Publish Init

## Workflow

1. Require a registered Research Topic and Source Topic Workspace, a credential-safe remote locator and name, visibility `private`, `restricted`, or `public`, an explicit publication-preparation request, and one-time acknowledgement that this remote is an `exclusive_snapshot`. This authority permits exact planned fallback replacement and obsolete-ref deletion; ordinary publication updates preserve compatible sanitized publication history. Workspace Runtime and local tracking are optional.
2. Inspect Project location, `tmp/`, and `temp/`. When the Project has an ancestor or root Git repository, run direct effective-ignore checks against the Project repository:

```bash
git -C <project-git-top-level> check-ignore -v --no-index -- <project-relative-tmp> <project-relative-temp>
```

3. Reuse a safe existing binding, otherwise prefer ignored `tmp/`, then ignored `temp/`, then a declared ignored candidate. If none qualifies, present the exact managed Project `.gitignore` block and `tmp/` creation for approval.
4. Validate that the destination remains inside the Project and outside the Source Topic Workspace, Project Config Directory, generated content root, Houmao state, and every canonical repository or worker workspace.
5. Create the approved ignored Topic Publication Copy and its `.isomer/topic-git/` support root. Add `/.isomer/` to the copy repository's `.git/info/exclude`, without changing a retained source `.gitignore`. Record the schema-valid binding there when Workspace Runtime is missing, or below `<topic.runtime>/topic-git/` when valid runtime exists.
6. Inventory available Isomer-resolved Topic Main, Topic Actor, Agent, intent, environment, records, and non-main `topic.repos.*` surfaces. Prepare the first privacy plan with raw-material and raw experiment-output bytes disabled unless the user explicitly selects either class.
7. Optionally initialize fresh local sanitized repositories for absent refs with neutral publication authorship. A later sync may instead reconstruct a repository from an exact compatible remote publication commit. Never reuse a local researcher's Git author or email:

```bash
git -C <sanitized-component-root> init
git -C <sanitized-component-root> switch -c <deterministic-component-branch>
git -C <sanitized-component-root> config user.name "Isomer Publication"
git -C <sanitized-component-root> config user.email "isomer-publication@invalid"
git -C <topic-publication-copy> init
git -C <topic-publication-copy> switch -c main
git -C <topic-publication-copy> config user.name "Isomer Publication"
git -C <topic-publication-copy> config user.email "isomer-publication@invalid"
```

8. Verify support-root exclusion, canonical `main`, deterministic `components/topic-main`, `components/topic-actors/<sanitized-name>`, and `components/agents/<sanitized-name>` branches, Topic Main anchor relationships, and absence of source Git metadata. Preserve credential-free public or private GitHub organization/repository identities, keep authentication external, and report access limitations and unavailable later-stage components.

A task-only “publish now” request may continue to plan and sync only after the privacy and remote mutation gates in those operations.

If the request does not map cleanly to these steps, use the native planning tool to isolate destination and binding preparation, then stop before mutation until visibility, remote, path, or approval ambiguity is resolved.

## Guardrails

- DO NOT push any ref.
- DO NOT initialize the Source Topic Workspace or Workspace Runtime.
- DO NOT initialize Topic Main, a Topic Actor Workspace, or an Agent Workspace.
