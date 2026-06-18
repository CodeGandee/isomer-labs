"""paper-plot compiler adapter — publication figures.

Primary path: **matplotlib** vector output (PDF/PNG/SVG by out_path extension; default PDF) so the figure
EMBEDS cleanly in the LaTeX/PDF build via \\includegraphics. Falls back to a stdlib-only SVG when matplotlib
is unavailable (kept so the pack never hard-fails). Entrypoint: render(...) per ../ADAPTER-CONTRACT.md.

Input formats:
  CSV : header row; first column = x, each remaining column = a named series.
  JSON: {"x_label":..,"x":[..],"series":{name:[..]}}  | {"x":[..],"y":[..]}  | [{"x":..,"y":..},..]
params (optional): {"title":str, "kind":"line|scatter|bar", "x_label":str, "y_label":str, "identity":bool}
  - kind defaults to "line"; "scatter" adds an optional y=x identity line (params.identity, default true for
    a predicted-vs-measured shape); "bar" draws grouped bars.
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
        if isinstance(data, list):
            xs = [float(r["x"]) for r in data]
            return "x", xs, {"y": [float(r["y"]) for r in data]}, {}
        xlabel = data.get("x_label", "x")
        xs = [float(v) for v in data["x"]]
        if "series" in data:
            series = {k: [float(v) for v in vs] for k, vs in data["series"].items()}
        else:
            series = {"y": [float(v) for v in data["y"]]}
        meta = {k: data[k] for k in ("y_label", "labels") if k in data}
        return xlabel, xs, series, meta
    with p.open() as f:
        rows = list(csv.reader(f))
    header, body = rows[0], rows[1:]
    xlabel = header[0]
    # categorical x (bar) vs numeric x
    try:
        xs = [float(r[0]) for r in body]
    except ValueError:
        xs = list(range(len(body)))
        return xlabel, xs, {header[i]: [float(r[i]) for r in body] for i in range(1, len(header))}, \
            {"labels": [r[0] for r in body]}
    series = {header[i]: [float(r[i]) for r in body] for i in range(1, len(header))}
    return xlabel, xs, series, {}


def _render_mpl(xlabel, xs, series, meta, params, out_path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    title = params.get("title") or "Result"
    kind = (params.get("kind") or "line").lower()
    ylabel = params.get("y_label") or meta.get("y_label") or ""
    labels = meta.get("labels")
    plt.rcParams.update({"figure.dpi": 300, "savefig.dpi": 300, "font.size": 11,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "pdf.fonttype": 42, "svg.fonttype": "none", "figure.figsize": (6.0, 4.0)})
    fig, ax = plt.subplots()
    names = list(series)
    if kind == "bar":
        import numpy as np
        n, g = len(xs), len(names)
        width = 0.8 / max(1, g)
        idx = np.arange(n)
        for i, nm in enumerate(names):
            ax.bar(idx + i * width, series[nm], width, label=nm, color=_PALETTE[i % len(_PALETTE)])
        ax.set_xticks(idx + width * (g - 1) / 2)
        ax.set_xticklabels(labels or [str(x) for x in xs], rotation=30, ha="right", fontsize=8)
    elif kind == "scatter":
        for i, nm in enumerate(names):
            ax.scatter(xs, series[nm], s=28, color=_PALETTE[i % len(_PALETTE)], label=nm, zorder=3)
        if params.get("identity", True):
            lo = min([min(xs)] + [min(v) for v in series.values()])
            hi = max([max(xs)] + [max(v) for v in series.values()])
            ax.plot([lo, hi], [lo, hi], "--", color="#888", lw=1.0, label="ideal $y=x$", zorder=1)
    else:
        for i, nm in enumerate(names):
            ax.plot(xs, series[nm], marker="o", ms=4, lw=2, color=_PALETTE[i % len(_PALETTE)], label=nm)
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); ax.set_title(title, fontweight="bold")
    ax.grid(True, alpha=0.25, linewidth=0.6)
    if names and not (len(names) == 1 and names[0] == "y"):
        ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path)  # extension drives format (.pdf vector / .png raster / .svg)
    plt.close(fig)
    return out_path


def _render_svg_fallback(xlabel, xs, series, params, out_path):
    """Stdlib-only SVG (kept for environments without matplotlib)."""
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
    def fmt(v): return f"{v:.3g}"

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">',
           f'<rect width="{W}" height="{H}" fill="white"/>',
           f'<text x="{(x0+x1)/2:.1f}" y="{MT-22}" font-size="17" font-weight="bold" text-anchor="middle">{title}</text>',
           f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="#333" stroke-width="1.2"/>',
           f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="#333" stroke-width="1.2"/>']
    for i, (name, ys) in enumerate(series.items()):
        c = _PALETTE[i % len(_PALETTE)]
        pts = " ".join(f"{sx(x):.1f},{sy(y):.1f}" for x, y in zip(xs, ys))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="2"/>')
    out.append(f'<text x="{(x0+x1)/2:.1f}" y="{H-14}" font-size="13" text-anchor="middle">{xlabel}</text>')
    out.append("</svg>")
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text("\n".join(out))
    return out_path


def render(*, command, input_path, out_path, params, quest_id):
    if not input_path:
        raise ValueError("paper-plot: --input is required (CSV/JSON data file)")
    params = params or {}
    xlabel, xs, series, meta = _parse(input_path)
    backend, fmt = "svg-fallback", "svg"
    try:
        import matplotlib  # noqa: F401
        # If the caller asked for .svg but matplotlib is present, prefer a vector PDF sibling that EMBEDS
        # cleanly (\includegraphics) — the .svg path needs an SVG converter at LaTeX time, which is the
        # exact failure that left figures unembedded. Honor an explicit .pdf/.png request as-is.
        op = Path(out_path)
        if op.suffix.lower() == ".svg":
            out_path = str(op.with_suffix(".pdf"))
        _render_mpl(xlabel, xs, series, meta, params, out_path)
        backend, fmt = "matplotlib", Path(out_path).suffix.lstrip(".")
    except Exception:
        out_path = _render_svg_fallback(xlabel, xs, series, params, out_path)
    return {
        "ok": True,
        "out_path": out_path,
        "format": fmt,
        "summary": f"{len(series)} series x {len(xs)} points -> {os.path.basename(out_path)} ({backend})",
        "meta": {"series": list(series), "points": len(xs), "x_label": xlabel, "backend": backend},
    }
