## Why

The Project Web GUI now depends on several topic read models having stable required fields, but those frontend-facing contracts are scattered across endpoint specs and implementation code. We need a dedicated documentation and schema layer so agents can produce extra metadata freely while the GUI can validate the fields it actually needs.

## What Changes

- Add UI contract documentation pages under `docs/ui/contracts/`, with one page per GUI-usable data shape.
- Add Python schemas under `src/isomer_labs/` for GUI-facing read models and artifact payload fragments that the GUI consumes.
- Make the schemas permissive by default: required GUI fields are checked, unknown extra fields are preserved or ignored according to caller needs.
- Define a validation path that backend read APIs, tests, and future agent-produced fixtures can use before handing data to the TypeScript GUI.
- Keep the existing canonical Workspace Runtime and query-index storage contracts authoritative; these schemas describe GUI consumption, not a new storage format.

## Capabilities

### New Capabilities
- `project-web-data-contracts`: Documents GUI-usable data contracts and provides permissive schema checks for the required fields consumed by Project Web.

### Modified Capabilities
- `project-web-gui`: The GUI and web backend must treat documented UI contracts as the handoff surface for topic views and validate required fields before rendering where practical.

## Impact

- Adds documentation under `docs/ui/contracts/`.
- Adds schema modules under `src/isomer_labs/`, plus unit tests.
- Touches Project Web backend/read-model code only where needed to validate or expose contract-safe payloads.
- Does not require database migration, query-index schema changes, or changes to agent payload authorship beyond clearer contract guidance.
