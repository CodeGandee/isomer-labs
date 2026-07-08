# Team Repositories

This developer guide explains Team Repositories, the local filesystem plugin roots that contain Domain Agent Team Templates. Isomer core loads them explicitly through Project configuration or `ISOMER_TEAM_REPOSITORIES`; package code does not derive paths to checkout-local `teams/`, `skillset/`, `tests/`, or other repository-only directories.

## Manifest

A Team Repository root contains `isomer-team-repo.toml`:

```toml
schema_version = "isomer-team-repository.v1"
id = "isomer-local-teams"
status = "active"

[[domain_agent_team_templates]]
id = "deepsci-mini"
path = "teams/deepsci-mini/execplan"
schema_version = "isomer-domain-agent-team-template-ref.v1"
status = "active"
```

Template paths are resolved relative to the Team Repository root and must stay inside that root. Isomer rejects entries that escape with paths such as `../outside`.

## Project Configuration

A Project can opt into one or more Team Repositories:

```toml
[[team_repositories]]
id = "isomer-local-teams"
path = "/path/to/team-repo"
status = "active"
```

`project team-repositories list` shows configured repositories and their templates. `project team-templates list` merges Project-local template registrations with templates from configured Team Repositories. If neither source is configured, the template list is empty.

To register a repository template into a Project Manifest before specialization:

```bash
isomer-cli project --root /path/to/project team-templates register deepsci-mini --from-repository isomer-local-teams --write
```

Agents and operators can also use `ISOMER_TEAM_REPOSITORIES` for local development. The value is a path-list using the platform path separator.

## Migration Notes

Older development builds treated `deepsci-mini` and `deepsci-org` as implicit built-ins under the source checkout. New Projects should configure a Team Repository instead, then select templates by id through the Project default, Topic default, profile, packet, or an explicit `--template` option.

The Isomer package keeps validation and specialization logic in `src/isomer_labs/`. Team definitions remain outside `src/` so they can later move to a separate team repository with manifests.
