# Open the Web GUI

The web GUI is a single-user viewer for a local Isomer Project. It reads topic overviews, record indexes, graph data, markdown artifacts, JSON payloads, and PDFs from the selected project directory.

Start it from the project root:

```bash
isomer-cli project web serve --root .
```

Open the printed URL in a browser. When an agent or operator writes new topic records, refresh-capable views update from the backend instead of requiring a new project export.

Use the GUI for inspection, and use your normal editor or terminal for raw filesystem browsing.
