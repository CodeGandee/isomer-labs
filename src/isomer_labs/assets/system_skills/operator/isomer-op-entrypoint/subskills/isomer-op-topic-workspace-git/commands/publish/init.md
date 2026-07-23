# Publish Init

## Workflow

1. Require a registered Research Topic and Source Topic Workspace, a credential-safe remote locator and name, visibility `private`, `restricted`, or `public`, and an explicit publication-preparation request. Workspace Runtime and local tracking are optional.
2. Inspect Project location, `tmp/`, and `temp/`. When the Project has an ancestor or root Git repository, run direct effective-ignore checks against the Project repository:

```bash
git -C <project-git-top-level> check-ignore -v --no-index -- <project-relative-tmp> <project-relative-temp>
```

3. Reuse a safe existing binding, otherwise prefer ignored `tmp/`, then ignored `temp/`, then a declared ignored candidate. If none qualifies, present the exact managed Project `.gitignore` block and `tmp/` creation for approval.
4. Validate that the destination remains inside the Project and outside the Source Topic Workspace, Project Config Directory, generated content root, Houmao state, and every canonical repository or worker workspace.
5. Create the approved ignored Topic Publication Copy and its `.isomer/topic-git/` support root. Record the schema-valid binding there when Workspace Runtime is missing, or below `<topic.runtime>/topic-git/` when valid runtime exists.
6. Inventory available Isomer-resolved components, prepare the first privacy plan, and optionally initialize fresh local sanitized repositories:

```bash
git -C <sanitized-component-root> init
git -C <sanitized-component-root> switch -c <deterministic-component-branch>
git -C <topic-publication-copy> init
git -C <topic-publication-copy> switch -c topic-workspace/main
```

7. Verify support-root exclusion, repository identities, branches, and absence of source Git metadata. Report unavailable later-stage components.

Do not push any ref. Do not initialize the Source Topic Workspace, Workspace Runtime, Topic Main, Topic Actor Workspace, or Agent Workspace. A task-only “publish now” request may continue to plan and sync only after the privacy and remote mutation gates in those operations.

If the request does not map cleanly to these steps, use the native planning tool to isolate destination and binding preparation, then stop before mutation until visibility, remote, path, or approval ambiguity is resolved.
