## ADDED Requirements

### Requirement: Audience-oriented docs layout
The documentation SHALL organize public documentation under `docs/tutorial/`, `docs/manual/`, and `docs/developer/` according to reader intent.

#### Scenario: Tutorial pages guide first use
- **WHEN** a new user opens the tutorial section
- **THEN** it SHALL contain task-first pages for installing the tool, creating a first Project, creating a first Research Topic, launching the Project Web GUI, and installing system skills

#### Scenario: Manual pages provide reference
- **WHEN** an operator opens the manual section
- **THEN** it SHALL contain reference pages for CLI usage, Project lifecycle, Research Topics, Topic Workspace structure, Workspace Runtime, research records, Project Web, Houmao adapter behavior, and troubleshooting

#### Scenario: Developer pages preserve maintainer material
- **WHEN** a contributor opens the developer section
- **THEN** it SHALL contain architecture, storage, packaged system skills, UI contracts, docs maintenance, testing, and release-process material

### Requirement: Audience-specific page rewrites
The documentation reorganization SHALL rewrite pages for their target reader and purpose rather than mechanically regrouping old files.

#### Scenario: Existing docs are classified before moving
- **WHEN** implementation reorganizes the current docs tree
- **THEN** every existing top-level docs page SHALL be examined and assigned to tutorial, manual, developer, or UI contract material

#### Scenario: Tutorial tone is task-first
- **WHEN** content is placed under `docs/tutorial/`
- **THEN** it SHALL use a guided, sequential style with minimal theory and copy-paste command examples

#### Scenario: Manual tone is reference-first
- **WHEN** content is placed under `docs/manual/`
- **THEN** it SHALL use precise lookup-oriented language, complete command facts, and explicit mutation boundaries

#### Scenario: Developer tone explains maintenance
- **WHEN** content is placed under `docs/developer/`
- **THEN** it SHALL explain architecture, invariants, validation, release, and maintenance rationale rather than teach a first-use workflow

### Requirement: README published-user entrypoint
The repository README SHALL describe Isomer Labs as a published tool and show the normal user path before the developer checkout path.

#### Scenario: README recommends uv install
- **WHEN** a reader opens `README.md`
- **THEN** the first installation path SHALL recommend `uv tool install isomer-labs`
- **AND** it SHALL show `isomer-cli` commands without requiring `pixi run`

#### Scenario: README links to reorganized docs
- **WHEN** a reader opens `README.md`
- **THEN** it SHALL link to the tutorial, manual, and developer docs sections
- **AND** it SHALL not link to removed flat-page paths as canonical docs

#### Scenario: README keeps developer setup separate
- **WHEN** a contributor needs local checkout instructions
- **THEN** `README.md` SHALL point to developer setup docs that use Pixi rather than presenting Pixi as the primary user install path

### Requirement: Public system-skill install docs
The public docs SHALL explain how to install Isomer system skills into agent surfaces with `npx skills add`.

#### Scenario: Skill install page names npx skills
- **WHEN** a reader opens the system-skill installation tutorial or manual page
- **THEN** it SHALL recommend `npx skills add` for installing agent skills from the Isomer repository
- **AND** it SHALL show examples using `--agent`, `--skill`, and `--yes`

#### Scenario: Skill families are explained
- **WHEN** a reader reviews the system-skill installation docs
- **THEN** the docs SHALL distinguish core operator/service/misc skills from optional DeepSci extension skills
- **AND** they SHALL identify `isomer-op-entrypoint` as the informed-user routing entrypoint

### Requirement: MkDocs navigation reflects docs layout
The MkDocs site SHALL expose the reorganized documentation structure.

#### Scenario: Site navigation has reader sections
- **WHEN** `mkdocs build --strict` runs
- **THEN** the generated site SHALL include navigation entries for Tutorials, Manual, Developer, and UI Contracts

#### Scenario: Moved pages resolve
- **WHEN** MkDocs validates links
- **THEN** links from README-equivalent docs pages and index pages SHALL point to existing files in the reorganized tree

### Requirement: Docs validation follows new locations
The repository documentation validation SHALL enforce the reorganized docs paths without weakening existing checks.

#### Scenario: Required pages use new paths
- **WHEN** docs validation runs
- **THEN** it SHALL require the canonical tutorial, manual, and developer pages instead of the old flat paths

#### Scenario: CLI coverage checks moved reference
- **WHEN** docs validation checks public CLI command coverage
- **THEN** it SHALL inspect the moved CLI reference under `docs/manual/`

#### Scenario: Existing stale-example checks remain
- **WHEN** docs validation scans README and docs pages
- **THEN** it SHALL still report stale command-local Isomer JSON flags, forbidden terms, legacy workspace paths, incomplete semantic path docs, and missing CLI error examples
