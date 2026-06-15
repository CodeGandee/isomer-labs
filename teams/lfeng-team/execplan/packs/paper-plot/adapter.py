"""paper-plot compiler adapter — real, dependency-free (stdlib only).

Reads CSV/JSON data and writes a self-contained publication-style SVG line+marker plot.
Entrypoint: render(...) per ../ADAPTER-CONTRACT.md (compiler kind).

Input formats:
  CSV : header row; first column = x, each remaining column = a named series.
        epoch,baseline,ours
        1,0.50,0.55
  JSON: {"x_label":"epoch","x":[...],"series":{"baseline":[...],"ours":[...]}}
        or {"x":[...],"y":[...]}  (single series named "y")
        or [{"x":1,"y":0.5}, ...] (single series)
"""
from __future__ import annotations
import csv
import json
import os
from pathlib import Path

_PALETTE = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e", "#17becf"]


def _parse(input_path: str):
    p = Path(input_path)
    if not p.exists():
        raise FileNotFoundError(f"paper-plot: input not found: {input_path}")
    if p.suffix.lower() == ".json":
        data = json.loads(p.read_text())
        if isinstance(data, list):  # [{x,y},...]
            xs = [float(r["x"]) for r in data]
            return "x", xs, {"y": [float(r["y"]) for r in data]}
        xlabel = data.get("x_label", "x")
        xs = [float(v) for v in data["x"]]
        if "series" in data:
            series = {k: [float(v) for v in vs] for k, vs in data["series"].items()}
        else:
            series = {"y": [float(v) for v in data["y"]]}
        return xlabel, xs, series
    # CSV
    with p.open() as f:
        rows = list(csv.reader(f))
    header, body = rows[0], rows[1:]
    xlabel = header[0]
    xs = [float(r[0]) for r in body]
    series = {header[i]: [float(r[i]) for r in body] for i in range(1, len(header))}
    return xlabel, xs, series


def _ticks(lo, hi, n=5):
    if hi == lo:
        hi = lo + 1.0
    return [lo + (hi - lo) * i / (n - 1) for i in range(n)]


def _fmt(v):
    return f"{v:.3g}"


def render(*, command, input_path, out_path, params, quest_id):
    if not input_path:
        raise ValueError("paper-plot: --input is required (CSV/JSON data file)")
    xlabel, xs, series = _parse(input_path)
    title = (params or {}).get("title") or "Result"
    W, H = 720, 460
    ML, MR, MT, MB = 70, 150, 50, 60
    x0, x1, y0, y1 = ML, W - MR, H - MB, MT
    xmin, xmax = min(xs), max(xs)
    allys = [v for vs in series.values() for v in vs]
    ymin, ymax = min(allys), max(allys)
    if ymin == ymax:
        ymin, ymax = ymin - 1, ymax + 1

    def sx(v): return x0 + (0 if xmax == xmin else (v - xmin) / (xmax - xmin)) * (x1 - x0)
    def sy(v): return y0 - (v - ymin) / (ymax - ymin) * (y0 - y1)

    out = []
    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">')
    out.append(f'<rect width="{W}" height="{H}" fill="white"/>')
    out.append(f'<text x="{(x0+x1)/2:.1f}" y="{MT-22}" font-size="17" font-weight="bold" text-anchor="middle">{title}</text>')
    # axes
    out.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="#333" stroke-width="1.2"/>')
    out.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="#333" stroke-width="1.2"/>')
    # y ticks + gridlines
    for t in _ticks(ymin, ymax):
        y = sy(t)
        out.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="#eee" stroke-width="1"/>')
        out.append(f'<line x1="{x0-5}" y1="{y:.1f}" x2="{x0}" y2="{y:.1f}" stroke="#333"/>')
        out.append(f'<text x="{x0-9}" y="{y+4:.1f}" font-size="11" text-anchor="end" fill="#333">{_fmt(t)}</text>')
    # x ticks
    for t in _ticks(xmin, xmax):
        x = sx(t)
        out.append(f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y0+5}" stroke="#333"/>')
        out.append(f'<text x="{x:.1f}" y="{y0+20:.1f}" font-size="11" text-anchor="middle" fill="#333">{_fmt(t)}</text>')
    out.append(f'<text x="{(x0+x1)/2:.1f}" y="{H-14}" font-size="13" text-anchor="middle">{xlabel}</text>')
    # series
    for i, (name, ys) in enumerate(series.items()):
        c = _PALETTE[i % len(_PALETTE)]
        pts = " ".join(f"{sx(x):.1f},{sy(y):.1f}" for x, y in zip(xs, ys))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="2"/>')
        for x, y in zip(xs, ys):
            out.append(f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="3" fill="{c}"/>')
        ly = MT + 6 + i * 20
        out.append(f'<rect x="{x1+18}" y="{ly}" width="14" height="4" fill="{c}"/>')
        out.append(f'<text x="{x1+38}" y="{ly+6}" font-size="12" fill="#333">{name}</text>')
    out.append("</svg>")

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text("\n".join(out))
    return {
        "ok": True,
        "out_path": out_path,
        "format": "svg",
        "summary": f"{len(series)} series x {len(xs)} points -> {os.path.basename(out_path)}",
        "meta": {"series": list(series), "points": len(xs), "x_label": xlabel},
    }
