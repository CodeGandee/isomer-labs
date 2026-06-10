"""nature-paper2ppt compiler adapter — paper outline -> self-contained HTML slide deck (stdlib only).

python-pptx is not assumed present, so this emits a real, viewable HTML deck (one <section> per slide).
Upgrade path: drop a python-pptx-backed adapter.py at this same ref to emit a true .pptx — no contract
change. Entrypoint: render(...) (compiler kind).

Input JSON: {"title": "...", "author": "...", "slides": [{"title": "...", "bullets": [...], "notes": "..."}]}
Input MD:   "# Deck title" then "## Slide title" sections with "- bullet" lines.
"""
from __future__ import annotations
import html
import json
from pathlib import Path


def _parse(input_path):
    p = Path(input_path)
    if not p.exists():
        raise FileNotFoundError(f"nature-paper2ppt: input not found: {input_path}")
    if p.suffix.lower() == ".json":
        d = json.loads(p.read_text())
        return d.get("title", "Presentation"), d.get("author", ""), d.get("slides", [])
    # Markdown
    title, slides, cur = "Presentation", [], None
    for line in p.read_text().splitlines():
        s = line.strip()
        if s.startswith("## "):
            cur = {"title": s[3:].strip(), "bullets": []}
            slides.append(cur)
        elif s.startswith("# "):
            title = s[2:].strip()
        elif s.startswith(("- ", "* ")) and cur is not None:
            cur["bullets"].append(s[2:].strip())
    return title, "", slides


def render(*, command, input_path, out_path, params, quest_id):
    if not input_path:
        raise ValueError("nature-paper2ppt: --input is required (outline JSON/MD)")
    title, author, slides = _parse(input_path)
    e = html.escape
    css = ("body{margin:0;font-family:Arial,Helvetica,sans-serif;background:#222}"
           "section{box-sizing:border-box;width:100%;min-height:100vh;padding:8% 10%;color:#111;"
           "background:#fff;border-bottom:6px solid #0072B2;page-break-after:always}"
           "h1{font-size:2.4em;color:#0a2b4a}h2{font-size:1.8em;color:#0a2b4a}"
           "li{font-size:1.25em;margin:.4em 0}.notes{margin-top:1.5em;color:#888;font-style:italic;font-size:.95em}")
    out = [f"<!doctype html><html><head><meta charset='utf-8'><title>{e(title)}</title><style>{css}</style></head><body>"]
    out.append(f"<section><h1>{e(title)}</h1>" + (f"<p>{e(author)}</p>" if author else "") + "</section>")
    for sl in slides:
        out.append(f"<section><h2>{e(sl.get('title',''))}</h2><ul>"
                   + "".join(f"<li>{e(b)}</li>" for b in sl.get("bullets", []))
                   + "</ul>"
                   + (f"<div class='notes'>Notes: {e(sl['notes'])}</div>" if sl.get("notes") else "")
                   + "</section>")
    out.append("</body></html>")
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text("".join(out))
    return {"ok": True, "out_path": out_path, "format": "html",
            "summary": f"HTML deck: {len(slides)+1} slides (title + {len(slides)})",
            "meta": {"slides": len(slides) + 1, "title": title, "note": "HTML deck; pptx via a python-pptx adapter at this ref"}}
