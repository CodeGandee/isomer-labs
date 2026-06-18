"""Reference knowledge-pack adapter.

Read-only: `cards()` indexes this pack's references/ (and templates/) so `knowledge cards` can
surface the methodology files; agents then read the named file for the full procedure/checklist/
template. No state writes; no cross-quest data (this is loop-wide methodology, not quest data)."""
from __future__ import annotations
import pathlib

_DIR = pathlib.Path(__file__).resolve().parent


def _first_heading(p: pathlib.Path) -> str:
    try:
        for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            s = line.strip().lstrip("#").strip()
            if s:
                return s[:200]
    except OSError:
        pass
    return p.stem


def cards(query: str | None = None, quest_id: str | None = None):
    out = []
    for sub in ("references", "templates"):
        d = _DIR / sub
        if not d.is_dir():
            continue
        for f in sorted(d.glob("*.md")) + sorted(d.glob("*.py")) + sorted(d.glob("*.mplstyle")):
            out.append({"title": f.stem, "summary": _first_heading(f),
                        "ref": f"{_DIR.name}/{sub}/{f.name}", "kind": "methodology"})
    if query:
        q = query.lower()
        out = [c for c in out if q in (c["title"] + " " + c["summary"]).lower()]
    return out


def render(**kwargs):
    # Reference packs are read-only methodology; they back no render/manuscript command.
    return {"note": "reference pack: methodology only; read the indexed files via `knowledge cards`."}
