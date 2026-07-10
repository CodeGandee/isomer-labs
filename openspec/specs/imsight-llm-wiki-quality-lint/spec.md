# Purpose

Define the quality-lint capability of `imsight-llm-wiki`, which extends health checks with overlong-page, orphan-concept, frontmatter, and opt-in stale-article detection.

## Requirements

### Requirement: Lint quality scans detect stale articles when explicitly requested
The enhanced `lint` subcommand SHALL detect stale wiki articles only when the user explicitly requests a stale check with a threshold.

#### Scenario: User runs lint with stale check
- **WHEN** the user invokes lint with `--stale` or `--stale-days N`
- **THEN** it SHALL report articles whose `updated:` date is older than the threshold and whose sources have newer material

#### Scenario: Stale check not requested
- **WHEN** the user invokes lint without `--stale`
- **THEN** it SHALL NOT report articles as stale solely based on age

### Requirement: Lint quality scans detect overlong pages
The enhanced `lint` subcommand SHALL detect wiki pages exceeding the 1200-word recommended maximum.

#### Scenario: Overlong page detected
- **WHEN** lint runs and finds a page over 1200 words
- **THEN** it SHALL report the page with a recommendation to split

### Requirement: Lint quality scans detect orphan concepts
The enhanced `lint` subcommand SHALL detect concept pages with no inbound wikilinks.

#### Scenario: Orphan concept detected
- **WHEN** lint runs and finds a `wiki/concepts/` page with no inbound links
- **THEN** it SHALL report the page and suggest backlink opportunities or removal

### Requirement: Lint quality scans validate frontmatter
The enhanced `lint` subcommand SHALL validate that every wiki page has required YAML frontmatter fields.

#### Scenario: Missing frontmatter field
- **WHEN** lint runs and finds a wiki page missing `title`, `type`, `created`, `updated`, `sources`, or `tags`
- **THEN** it SHALL report the missing fields

### Requirement: Quality lint writes a report
The enhanced `lint` subcommand SHALL write findings to `outputs/lint-report-<YYYY-MM-DD>.md`.

#### Scenario: Lint with quality issues
- **WHEN** lint detects quality issues
- **THEN** it SHALL write a report file in addition to chat output

### Requirement: Quality lint does not auto-fix
The enhanced `lint` subcommand SHALL report quality issues and wait for user confirmation before applying fixes.

#### Scenario: User approves a fix
- **WHEN** the user confirms a proposed fix
- **THEN** the skill SHALL apply the smallest edit that resolves the issue
