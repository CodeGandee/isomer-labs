# Project Web GUI

The project web service starts a local FastAPI backend and TypeScript frontend over one Isomer Project directory. It is designed for one user inspecting active topic work while agents or operators continue to write artifacts.

```bash
isomer-cli project web serve --root .
```

The GUI shows semantic project views instead of raw filesystem browsing. Use it for topic overviews, idea lineage, record inspection, markdown preview, JSON payload inspection, PDFs, diagnostics, and future control surfaces.

When a file path appears in the UI, it should be displayed relative to the Topic Workspace when possible. Full absolute paths belong in diagnostics or copyable details, not primary labels.
