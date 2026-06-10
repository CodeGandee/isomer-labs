# Comms Renderers

## Purpose

Jinja2 Markdown renderers (`.md.j2`) for templated mail, applied by `harness email render`. Each emits
the in-body `houmao-email-metadata` block plus a human-readable body.

## Contents

- `task-request.md.j2`, `receipt.md.j2`, `task-result.md.j2`, `self-wakeup.md.j2`: per-family renderers.
