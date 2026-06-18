"""paper-latex compiler adapter — Markdown manuscript -> LaTeX article -> compiled PDF.

Entrypoint: render(...) per ../ADAPTER-CONTRACT.md (compiler kind), backing `render report`.

Pipeline (degrades gracefully, always records an artifact):
  1. If `pandoc` + a LaTeX engine (xelatex/pdflatex, system or a TinyTeX install) are present:
     pandoc md -> PDF (XeLaTeX), with a Unicode main font when available, a table of contents,
     CJK handling (documentclass=ctexart) when the draft contains CJK, and \\cite resolution when a
     `.bib` is provided. Also writes the intermediate standalone `.tex` next to the PDF.
  2. Else if a LaTeX engine but no pandoc: wrap the Markdown in a minimal article `.tex` and compile it.
  3. Else: emit a standalone `.tex` (no compile) and report PDF pending — never fails the stage.

No hard Python dependency: detection via shutil.which + a TinyTeX probe; compilation via subprocess.

params (all optional): {"title": str, "bib": "<path to .bib>", "engine": "xelatex|pdflatex",
                        "mainfont": str, "toc": bool}
input_path: the Markdown manuscript draft (the Writer's assembled paper).
out_path:  target PDF path (a sibling `.tex` is written alongside).
"""
from __future__ import annotations
import os
import re
import shutil
import subprocess
from pathlib import Path


def _find_tinytex_bin():
    # Common TinyTeX locations under any user home + the conventional ~/.TinyTeX.
    homes = [Path.home()]
    if Path("/home").exists():
        homes += [p for p in Path("/home").glob("*") if p.is_dir()]
    if Path("/root").exists():
        homes.append(Path("/root"))
    for home in homes:
        binroot = home / ".TinyTeX" / "bin"
        if not binroot.exists():
            continue
        for c in binroot.glob("*"):
            if (c / "xelatex").exists() or (c / "pdflatex").exists():
                return str(c)
    return None


def _toolchain(engine_pref=None):
    """Return (pandoc_path|None, engine_name|None, extra_PATH|None)."""
    extra = _find_tinytex_bin()
    path_env = (extra + os.pathsep + os.environ.get("PATH", "")) if extra else os.environ.get("PATH", "")
    def which(x):
        return shutil.which(x, path=path_env)
    pandoc = which("pandoc")
    if not pandoc:
        # pypandoc bundles a pandoc binary
        try:
            import pypandoc
            pandoc = pypandoc.get_pandoc_path()
        except Exception:
            pandoc = None
    engine = None
    for e in ([engine_pref] if engine_pref else []) + ["xelatex", "pdflatex", "lualatex"]:
        if e and which(e):
            engine = e
            break
    return pandoc, engine, extra


_TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"


def _available_venues():
    if not _TEMPLATES_DIR.is_dir():
        return []
    return sorted(d.name for d in _TEMPLATES_DIR.iterdir() if d.is_dir())


def _stage_venue(venue, dest_dir):
    """Copy the venue LaTeX suite (.sty/.bst/.bib/.tex) next to the output so a venue-faithful compile is
    possible. pandoc cannot synthesize an arbitrary venue style, so we stage the official files and let the
    Writer author/compile main.tex against them; the default Markdown->PDF path still runs for a preview."""
    import shutil as _sh
    if not venue:
        return None
    suite = _TEMPLATES_DIR / venue
    if not suite.is_dir():
        return {"venue": venue, "staged": False, "error": f"unknown venue {venue!r}; have {_available_venues()}"}
    target = Path(dest_dir) / f"venue-{venue}"
    target.mkdir(parents=True, exist_ok=True)
    copied = []
    for f in suite.iterdir():
        if f.is_file():
            _sh.copy2(f, target / f.name)
            copied.append(f.name)
    return {"venue": venue, "staged": True, "venue_dir": str(target), "files": copied}


def _has_cjk(text):
    return any("㐀" <= ch <= "鿿" for ch in text)


def _unicode_mainfont(extra_path):
    # Prefer a glyph-rich serif for math symbols (≤ β κ ×); fall back to None (template default).
    try:
        out = subprocess.run(["fc-list"], capture_output=True, text=True, timeout=20).stdout
    except Exception:
        out = ""
    for f in ("DejaVu Serif", "TeX Gyre Termes", "Noto Serif"):
        if f.lower() in out.lower():
            return f
    return None


def _svgfix_tex(tex: str, build_dir: Path):
    """Rewrite \\includesvg[..]{x.svg} -> \\includegraphics[..]{x.pdf} when a sibling .pdf exists (the figure
    embeds cleanly without an SVG converter — the exact failure that left q1's figures unembedded). Returns
    (new_tex, n_fixed)."""
    n = 0
    def repl(m):
        nonlocal n
        opt, path = m.group(1) or "", m.group(2)
        pdf = path[:-4] + ".pdf"
        cand = pdf if pdf.startswith("/") else (build_dir / pdf)
        if Path(cand).exists() or (build_dir / Path(pdf).name).exists():
            n += 1
            return f"\\includegraphics{opt}{{{pdf}}}"
        return m.group(0)
    new = re.sub(r"\\includesvg(\[[^\]]*\])?\{([^}]+\.svg)\}", repl, tex)
    return new, n


def _inject_venue(tex: str, venue_info):
    """Best-effort: \\usepackage the venue's conference style after \\documentclass so the compile picks up
    venue formatting. Non-fatal; if the venue style conflicts the caller retries without it."""
    if not venue_info or not venue_info.get("staged"):
        return tex, None
    styles = [f for f in venue_info.get("files", []) if f.endswith(".sty")
              and ("conference" in f or venue_info["venue"].split("20")[0] in f or "icml" in f or "neurips" in f)]
    if not styles:
        return tex, None
    stem = Path(styles[0]).stem
    pkg = f"\\usepackage{{venue-{venue_info['venue']}/{stem}}}\n"
    out = re.sub(r"(\\documentclass[^\n]*\n)", r"\1" + pkg.replace("\\", "\\\\"), tex, count=1)
    return out, stem


def _latexmk(tex_path: Path, engine: str, env) -> bool:
    """Compile tex -> pdf with latexmk (runs bibtex when \\bibliography is present). True on a non-empty PDF."""
    if not shutil.which("latexmk", path=env.get("PATH")):
        return False
    flag = {"xelatex": "-pdfxe", "lualatex": "-pdflua"}.get(engine, "-pdf")
    try:
        subprocess.run(["latexmk", flag, "-interaction=nonstopmode", "-halt-on-error", tex_path.name],
                       cwd=str(tex_path.parent), env=env, capture_output=True, text=True, timeout=600)
    except Exception:
        return False
    pdf = tex_path.with_suffix(".pdf")
    return pdf.exists() and pdf.stat().st_size > 0


def render(*, command, input_path, out_path, params, quest_id):
    params = params or {}
    src = Path(input_path) if input_path else None
    if not src or not src.exists():
        raise FileNotFoundError(f"paper-latex: manuscript draft not found: {input_path}")
    md = src.read_text(encoding="utf-8")
    out_pdf = Path(out_path)
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    out_tex = out_pdf.with_suffix(".tex")
    title = params.get("title")
    bib = params.get("bib")
    toc = params.get("toc", True)
    cjk = _has_cjk(md)
    venue_info = _stage_venue(params.get("venue"), out_pdf.parent)

    pandoc, engine, extra = _toolchain(params.get("engine"))
    env = dict(os.environ)
    if extra:
        env["PATH"] = extra + os.pathsep + env.get("PATH", "")

    # ---- Path 1: pandoc + LaTeX engine -> PDF (+ .tex) ----
    if pandoc and engine:
        mainfont = params.get("mainfont") or _unicode_mainfont(extra)
        common = ["--pdf-engine=" + engine, "-V", "geometry:margin=1in", "-V", "colorlinks=true"]
        if toc:
            common += ["--toc", "--toc-depth=2"]
        if title:
            common += ["-M", "title=" + title]
        if cjk:
            common += ["-V", "documentclass=ctexart"]
        if mainfont and engine in ("xelatex", "lualatex"):
            common += ["-V", "mainfont=" + mainfont, "-V", "monofont=DejaVu Sans Mono"]
        # Bibliography: when a .bib is given, emit natbib \cite + \bibliography (real BibTeX pass via latexmk)
        # rather than citeproc-inlined text, and copy the bib into the build dir so bibtex resolves it.
        bibname = None
        if bib and Path(bib).exists():
            import shutil as _sh
            bibname = "references"
            dst = out_pdf.parent / (bibname + ".bib")
            if Path(bib).resolve() != dst.resolve():  # guard: --bib may already be the build-dir references.bib
                _sh.copy2(bib, dst)
            common += ["--natbib", "--bibliography=" + bibname + ".bib"]

        # Emit a standalone .tex, then post-process (figure embedding + venue) and compile via latexmk
        # (so BibTeX runs and figures embed). Falls back to pandoc-direct-pdf if anything is missing.
        used_path = None
        try:
            r = subprocess.run([pandoc, str(src), "-s", "-o", str(out_tex)] + common,
                               env=env, capture_output=True, text=True, timeout=300)
            if r.returncode == 0 and out_tex.exists():
                tex = out_tex.read_text(encoding="utf-8")
                tex, n_fig = _svgfix_tex(tex, out_pdf.parent)
                tex, venue_sty = _inject_venue(tex, venue_info)
                out_tex.write_text(tex, encoding="utf-8")
                if _latexmk(out_tex, engine, env):
                    # latexmk writes <stem>.pdf; ensure it lands at out_pdf
                    built = out_tex.with_suffix(".pdf")
                    if built != out_pdf and built.exists():
                        built.replace(out_pdf)
                    used_path = "latexmk"
                elif venue_sty:  # venue style may have broken the compile — retry without it
                    tex2, _ = _svgfix_tex(out_tex.read_text(encoding="utf-8"), out_pdf.parent)
                    tex2 = re.sub(r"\\usepackage\{venue-[^}]+\}\n", "", tex2)
                    out_tex.write_text(tex2, encoding="utf-8")
                    if _latexmk(out_tex, engine, env):
                        built = out_tex.with_suffix(".pdf")
                        if built != out_pdf and built.exists():
                            built.replace(out_pdf)
                        used_path = "latexmk (venue dropped)"
        except Exception:
            used_path = None

        if used_path and out_pdf.exists() and out_pdf.stat().st_size > 0:
            return {"ok": True, "out_path": str(out_pdf), "format": "pdf",
                    "summary": f"compiled PDF via pandoc+{engine}+{used_path}" + (" (+CJK)" if cjk else "")
                               + (" (+bibtex)" if bibname else "") + (f" (+figs:{n_fig})" if n_fig else ""),
                    "meta": {"engine": engine, "pandoc": True, "tex_path": str(out_tex),
                             "bytes": out_pdf.stat().st_size, "cjk": cjk, "mainfont": mainfont,
                             "venue": venue_info, "bibtex": bool(bibname), "figs_embedded": n_fig}}

        # Fallback: original pandoc-direct PDF (today's behavior — no regression)
        common_fb = [c for c in common if c not in ("--natbib",) and not c.startswith("--bibliography")]
        if bib and Path(bib).exists():
            common_fb += ["--citeproc", "--bibliography=" + str(bib)]
        proc = subprocess.run([pandoc, str(src), "-o", str(out_pdf)] + common_fb,
                              env=env, capture_output=True, text=True, timeout=600)
        if proc.returncode == 0 and out_pdf.exists() and out_pdf.stat().st_size > 0:
            return {"ok": True, "out_path": str(out_pdf), "format": "pdf",
                    "summary": f"compiled PDF via pandoc+{engine} (direct fallback)" + (" (+CJK)" if cjk else ""),
                    "meta": {"engine": engine, "pandoc": True, "tex_path": str(out_tex) if out_tex.exists() else None,
                             "bytes": out_pdf.stat().st_size, "cjk": cjk, "mainfont": mainfont, "venue": venue_info,
                             "note": "latexmk path unavailable; used pandoc-direct (citeproc, includesvg)"}}
        err = (proc.stderr or proc.stdout or "")[-600:]
        _emit_tex_fallback(md, out_tex, title)
        return {"ok": True, "out_path": str(out_tex), "format": "tex",
                "summary": f"PDF compile failed ({engine}); emitted standalone .tex",
                "meta": {"engine": engine, "pandoc": True, "compile_error_tail": err, "pdf": False, "venue": venue_info}}

    # ---- Path 3: no toolchain -> emit standalone .tex only ----
    _emit_tex_fallback(md, out_tex, title)
    return {"ok": True, "out_path": str(out_tex), "format": "tex",
            "summary": "no pandoc/LaTeX toolchain found; emitted standalone .tex (PDF pending)",
            "meta": {"engine": engine, "pandoc": bool(pandoc), "pdf": False, "venue": venue_info,
                     "hint": "install pandoc + a LaTeX engine (or TinyTeX) to auto-compile the PDF"}}


def _emit_tex_fallback(md, out_tex, title):
    """Minimal Markdown->LaTeX wrap so a compilable-ish .tex always exists (headings, paragraphs, code)."""
    def esc(s):
        for a, b in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("$", r"\$"),
                     ("#", r"\#"), ("_", r"\_"), ("{", r"\{"), ("}", r"\}")):
            s = s.replace(a, b)
        return s
    body, in_code = [], False
    for line in md.splitlines():
        if line.strip().startswith("```"):
            body.append(r"\begin{verbatim}" if not in_code else r"\end{verbatim}")
            in_code = not in_code
            continue
        if in_code:
            body.append(line)
            continue
        m = re.match(r"^(#{1,3})\s+(.*)$", line)
        if m:
            lvl = {1: "section", 2: "subsection", 3: "subsubsection"}[len(m.group(1))]
            body.append("\\%s{%s}" % (lvl, esc(m.group(2))))
        elif line.strip() == "":
            body.append("")
        else:
            body.append(esc(line))
    tex = ("\\documentclass[11pt]{article}\n\\usepackage[margin=1in]{geometry}\n"
           "\\usepackage{amsmath,amssymb,booktabs,graphicx,hyperref}\n"
           + ("\\title{%s}\n" % esc(title) if title else "")
           + "\\begin{document}\n" + ("\\maketitle\n" if title else "")
           + "\n".join(body) + "\n\\end{document}\n")
    out_tex.write_text(tex, encoding="utf-8")
