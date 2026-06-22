# Validation

## Purpose

This generated support document records validation commands and boundaries for the `deepsci-mini` execplan.

## Contents

## Package Validation

Run:

```bash
teams/deepsci-mini/execplan/harness/bin/deepsci-mini validate
```

The command checks required generated files, TOML parseability, JSON schema parseability, SQLite schema loadability, template schema/renderer links, manifest template posture, and process overview blocks.

## Useful Queries

```bash
teams/deepsci-mini/execplan/harness/bin/deepsci-mini query participants
teams/deepsci-mini/execplan/harness/bin/deepsci-mini query topology
teams/deepsci-mini/execplan/harness/bin/deepsci-mini query templates
teams/deepsci-mini/execplan/harness/bin/deepsci-mini control get-mode
teams/deepsci-mini/execplan/harness/bin/deepsci-mini instantiation placeholders
```

## Boundary

Package validation does not require concrete mailboxes, gateway posture, prepared Agent Profiles, live Agent Instances, workspace readiness, or launchability. Those belong to later prepare, validate-loop, launch, and start stages.
