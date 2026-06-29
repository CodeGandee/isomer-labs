"""paper-latex compiler adapter — Markdown manuscript -> LaTeX article -> compiled PDF.

Entrypoint: render(...) per ../ADAPTER-CONTRACT.md (compiler kind), backing `render report`.

Pipeline (degrades gracefully, always records an artifact):
  1. If `pandoc` + a LaTeX engine (xelatex/pdflatex, system or a TinyTeX install) are present:
     pandoc md -> PDF (XeLaTeX), with a Unicode main font when available, NO table of contents by
     default (conference-paper style, like the DeepScientist reference; opt in with params toc=True),
     CJK handling (documentclass=ctexart) when the draft contains CJK, and \\cite resolution when a
     `.bib` is provided. Also writes the intermediate standalone `.tex` next to the PDF.
  2. Else if a LaTeX engine but no pandoc: wrap the Markdown in a minimal article `.tex` and compile it.
  3. Else: emit a standalone `.tex` (no compile) and report PDF pending — never fails the stage.

No hard Python dependency: detection via shutil.which + a TinyTeX probe; compilation via subprocess.

params (all optional): {"title": str, "bib": "<path to .bib>", "engine": "xelatex|pdflatex",
                        "mainfont": str, "toc": bool (default False — no table of contents)}
input_path: the Markdown manuscript draft (the Writer's assembled paper).
out_path:  target PDF path (a sibling `.tex` is written alongside).
"""
from __future__ import annotations
import os
import re
import shutil
import subprocess
from pathlib import Path


class RenderDefect(RuntimeError):
    """A compile produced a non-empty PDF whose *content* is defective (dropped glyphs / empty
    bibliography). The harness (`_run_adapter` in cli.py) turns a raised adapter exception into an
    `ok=False` command envelope (exit 1) and records NO artifact — so a broken render never silently
    reports success. This is the deliberate "report render as non-OK" channel."""


# Raw Unicode math glyphs -> math-mode LaTeX. Injected as `newunicodechar` mappings so a manuscript that
# (incorrectly) carries literal Unicode math in body text still renders under any engine WITHOUT depending
# on a system Unicode font being discoverable via fontconfig/`fc-list`. Authoring math in $...$ is the
# correct path (skill guidance); this is defense-in-depth so a symbol never silently disappears.
_UNICODE_MATH_MAP = {
    "α": r"\alpha", "β": r"\beta", "γ": r"\gamma", "δ": r"\delta",
    "ε": r"\epsilon", "η": r"\eta", "θ": r"\theta", "κ": r"\kappa",
    "λ": r"\lambda", "μ": r"\mu", "ν": r"\nu", "π": r"\pi", "ρ": r"\rho",
    "σ": r"\sigma", "τ": r"\tau", "φ": r"\phi", "χ": r"\chi", "ψ": r"\psi",
    "ω": r"\omega", "Δ": r"\Delta", "Σ": r"\Sigma", "Ω": r"\Omega",
    "≤": r"\le", "≥": r"\ge", "≠": r"\neq", "≈": r"\approx", "≡": r"\equiv",
    "×": r"\times", "·": r"\cdot", "−": "-", "±": r"\pm",
    "→": r"\rightarrow", "←": r"\leftarrow", "↔": r"\leftrightarrow",
    "⇒": r"\Rightarrow", "′": r"\prime", "∞": r"\infty", "∑": r"\sum",
    "∏": r"\prod", "√": r"\surd", "∈": r"\in", "≅": r"\cong", "∂": r"\partial",
}


def _inject_unicode_math_fallback(tex: str):
    """Insert a guarded `newunicodechar` block (mapping any raw Unicode math glyphs present to
    `\\ensuremath{...}`) just before `\\begin{document}`. No-op when the package is unavailable
    (`\\IfFileExists` guard), no target glyph is present, or already injected (idempotent).
    Returns (new_tex, n_glyphs_mapped)."""
    present = [g for g in _UNICODE_MATH_MAP if g in tex]
    if not present or "\\begin{document}" not in tex or "deepresearch-unicode-math-fallback" in tex:
        return tex, 0
    lines = ["% --- deepresearch-unicode-math-fallback: render literal Unicode math with no system-font dep ---",
             "\\IfFileExists{newunicodechar.sty}{%", "  \\usepackage{newunicodechar}%"]
    lines += ["  \\newunicodechar{%s}{\\ensuremath{%s}}%%" % (g, _UNICODE_MATH_MAP[g]) for g in present]
    lines.append("}{}")
    block = "\n".join(lines) + "\n"
    return tex.replace("\\begin{document}", block + "\\begin{document}", 1), len(present)


def _scan_missing_chars(log_text: str):
    """Distinct glyphs LaTeX reported as 'Missing character' (silently dropped from the PDF)."""
    found = []
    for m in re.finditer(r"Missing character: There is no (.+?) \(U\+([0-9A-Fa-f]+)\)", log_text):
        tag = "%s (U+%s)" % (m.group(1), m.group(2).upper())
        if tag not in found:
            found.append(tag)
    return found


def _bbl_nonempty(bbl_path: Path) -> bool:
    """True if a .bbl exists and emitted at least one \\bibitem (a real bibliography, not an empty env)."""
    try:
        return "\\bibitem" in bbl_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return False


def _render_health(tex_path: Path, bib_provided: bool):
    """Inspect compile by-products for defects a non-empty PDF can still hide. Returns a list of
    human-readable problem strings ([] = healthy): dropped glyphs (from the .log) and an empty
    bibliography (.bbl has no \\bibitem although a .bib was supplied)."""
    problems = []
    log_path = tex_path.with_suffix(".log")
    if log_path.exists():
        miss = _scan_missing_chars(log_path.read_text(encoding="utf-8", errors="replace"))
        if miss:
            problems.append("dropped glyphs (LaTeX 'Missing character'): " + ", ".join(miss[:12])
                            + (" …" if len(miss) > 12 else ""))
    if bib_provided:
        bbl = tex_path.with_suffix(".bbl")
        if bbl.exists() and not _bbl_nonempty(bbl):
            problems.append("empty bibliography: a .bib was supplied but the compiled .bbl has no \\bibitem "
                            "(no in-text \\cite/[@key] citations resolved)")
    return problems


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
    """Return (pandoc_path|None, engine_name|None, extra_PATH|None).

    Prefer a **system** TeX engine (usually a complete TeXLive) over a possibly-minimal **TinyTeX**: venue
    styles pull dependencies (e.g. eso-pic) that ship only in a full distribution, and mixing the two trees
    via TEXINPUTS causes l3backend/kernel version skew. So resolve the engine on the system PATH first and
    only fall back to TinyTeX when no engine is on the system PATH (extra is the TinyTeX bin only in that
    fallback)."""
    sys_path = os.environ.get("PATH", "")
    tiny = _find_tinytex_bin()
    engines = ([engine_pref] if engine_pref else []) + ["xelatex", "pdflatex", "lualatex"]
    engine, extra = None, None
    for e in engines:
        if e and shutil.which(e, path=sys_path):
            engine = e
            break
    if not engine and tiny:  # no system engine — fall back to TinyTeX
        tpath = tiny + os.pathsep + sys_path
        for e in engines:
            if e and shutil.which(e, path=tpath):
                engine, extra = e, tiny
                break
    look_path = (extra + os.pathsep + sys_path) if extra else sys_path
    pandoc = shutil.which("pandoc", path=look_path)
    if not pandoc:
        # pypandoc bundles a pandoc binary
        try:
            import pypandoc
            pandoc = pypandoc.get_pandoc_path()
        except Exception:
            pandoc = None
    return pandoc, engine, extra


_TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

# Venue -> its primary conference STYLE stem (a `.sty` loaded onto \documentclass{article}). Venues whose
# official template is a full document class (ACM acmart: asplos2027, sosp2026) have NO injectable style →
# None: this pandoc+style path cannot apply them, and they are reported as unsupported (not silently
# downgraded to generic article). Helper styles (fancyhdr/natbib/algorithm) are NOT the primary style.
_VENUE_PRIMARY_STYLE = {
    "iclr2026": "iclr2026_conference", "icml2026": "icml2026", "neurips2025": "neurips",
    "colm2025": "colm2025_conference", "aaai2026": "aaai2026", "acl": "acl",
    "osdi2026": "usenix-2020-09", "nsdi2027": "usenix-2020-09",
    "asplos2027": None, "sosp2026": None,
}
_VENUE_HELPER_STYLES = {"fancyhdr", "natbib", "algorithm", "algorithmic"}


def _available_venues():
    if not _TEMPLATES_DIR.is_dir():
        return []
    return sorted(d.name for d in _TEMPLATES_DIR.iterdir() if d.is_dir())


def _stage_venue(venue, dest_dir):
    """Stage the venue's LaTeX style + bib-style files FLAT into the build dir so `\\usepackage{<style>}`
    resolves at compile time (latexmk runs from this dir). Returns staging info including the primary `style`
    stem to inject — or `style=None` for full-document-class venues (ACM acmart: asplos2027/sosp2026) that
    this pandoc+style path cannot apply. Unknown venue → staged=False + error. (venue None/"generic" → None.)"""
    import shutil as _sh
    if not venue or venue == "generic":
        return None
    suite = _TEMPLATES_DIR / venue
    if not suite.is_dir():
        return {"venue": venue, "staged": False, "error": f"unknown venue {venue!r}; have {_available_venues()}"}
    dest = Path(dest_dir)
    copied = []
    for f in suite.iterdir():
        if f.is_file() and f.suffix in (".sty", ".bst"):
            _sh.copy2(f, dest / f.name)
            copied.append(f.name)
    style = _VENUE_PRIMARY_STYLE.get(venue, "__infer__")
    if style == "__infer__":  # venue not in the map → heuristic: first non-helper .sty
        cand = [Path(c).stem for c in copied if c.endswith(".sty") and Path(c).stem not in _VENUE_HELPER_STYLES]
        style = cand[0] if cand else None
    return {"venue": venue, "staged": True, "files": copied, "style": style,
            "applicable": style is not None}


def _has_cjk(text):
    return any("㐀" <= ch <= "鿿" for ch in text)


def _resolve_cjk_venue(venue, cjk):
    """Decide venue handling for a (possibly CJK) edition. The venue suites are Latin-conference STYLE
    packages (mathptmx/helvet fonts + \\@maketitle/\\parskip/header redefs for \\documentclass{article});
    bolting one onto `ctexart` corrupts a CJK edition (title overprint, heading collisions, Times-vs-Fandol
    font fights). English-conference venues have no CJK edition, so a CJK manuscript renders in clean
    `ctexart` WITHOUT the Latin venue style — recorded explicitly (cjk_skipped), never a silent generic
    downgrade. Returns (effective_venue, want_venue, cjk_skipped)."""
    want = bool(venue) and venue != "generic"
    if want and cjk:
        return "generic", False, venue
    return venue, want, None


def _unicode_mainfont(extra_path):
    # Best-effort: prefer a glyph-rich serif for raw symbols (≤ β κ ×) when one is discoverable. This is
    # ONLY an optimization — when `fc-list`/fontconfig is absent it returns None and the template default
    # font is used; correct rendering of raw Unicode math no longer depends on it, because
    # `_inject_unicode_math_fallback` maps those glyphs to math-mode commands and `_render_health` fails
    # the render loudly if any glyph is still dropped. So a missing `fc-list` can never silently break output.
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
    """\\usepackage the venue's primary conference style AFTER the COMPLETE \\documentclass[...]{...} block.
    pandoc emits `\\documentclass[` and `]{article}` on separate lines, so a first-line-only regex injects the
    package INSIDE the optional-argument list and breaks every compile — that was the bug that silently dropped
    every venue to generic article. We match the whole class statement (optional args may span newlines) and
    inject right after it. Returns (new_tex, style_stem) or (tex, None) if not applicable."""
    if not venue_info or not venue_info.get("staged"):
        return tex, None
    stem = venue_info.get("style")
    if not stem:
        return tex, None
    pkg = "\\usepackage{%s}\n" % stem
    out, n = re.subn(r"(\\documentclass(?:\[[\s\S]*?\])?\{[^}]*\}[ \t]*\n)",
                     lambda m: m.group(1) + pkg, tex, count=1)
    return (out, stem) if n else (tex, None)


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
    # Default OFF: papers follow standard conference-paper style (title -> abstract -> sections, NO
    # table of contents), matching the DeepScientist reference layout. Opt in per render via params toc=True.
    toc = params.get("toc", False)
    cjk = _has_cjk(md)
    # Venue policy: a real venue template is the default (the caller resolves it). "generic" (or empty) is the
    # EXPLICIT opt-out → plain article is allowed. Any other value MUST apply a real venue or fail loudly —
    # never a silent downgrade to generic article.
    venue_rationale = params.get("venue_rationale")
    # CJK editions render in `ctexart`; Latin-conference venue styles are not applied to them (they corrupt the
    # layout — see _resolve_cjk_venue). cjk_venue_skipped records the skipped venue for the audit trail.
    venue, want_venue, cjk_venue_skipped = _resolve_cjk_venue(params.get("venue"), cjk)
    venue_info = _stage_venue(venue, out_pdf.parent)
    if want_venue:
        if not venue_info or not venue_info.get("staged"):
            raise RenderDefect("paper-latex: unknown venue %r — available: %s. Pass --venue generic only if "
                               "generic article output is explicitly intended." % (venue, _available_venues()))
        if not venue_info.get("applicable"):
            raise RenderDefect("paper-latex: venue %r uses a full document class (e.g. ACM acmart) that this "
                               "pandoc+style render path cannot apply, and acmart is not injectable onto "
                               "pandoc's article preamble. Choose an injectable-style venue (iclr2026, "
                               "neurips2025, osdi2026, nsdi2027, …) or pass --venue generic to opt out." % venue)

    pandoc, engine, extra = _toolchain(params.get("engine"))
    env = dict(os.environ)
    if extra:
        env["PATH"] = extra + os.pathsep + env.get("PATH", "")

    # ---- Path 1: pandoc + LaTeX engine -> PDF (+ .tex) ----
    if pandoc and engine:
        mainfont = params.get("mainfont") or _unicode_mainfont(extra)
        common = ["--pdf-engine=" + engine, "-V", "colorlinks=true"]
        if not want_venue:  # a venue style owns page geometry; passing margin=1in causes an option clash
            common += ["-V", "geometry:margin=1in"]
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
        used_path, n_fig, n_uni, venue_sty = None, 0, 0, None
        try:
            r = subprocess.run([pandoc, str(src), "-s", "-o", str(out_tex)] + common,
                               env=env, capture_output=True, text=True, timeout=300)
            if r.returncode == 0 and out_tex.exists():
                tex = out_tex.read_text(encoding="utf-8")
                tex, n_fig = _svgfix_tex(tex, out_pdf.parent)
                tex, venue_sty = _inject_venue(tex, venue_info)
                tex, n_uni = _inject_unicode_math_fallback(tex)  # render raw Unicode math w/o a system-font dep
                out_tex.write_text(tex, encoding="utf-8")
                if _latexmk(out_tex, engine, env):
                    # latexmk writes <stem>.pdf; ensure it lands at out_pdf
                    built = out_tex.with_suffix(".pdf")
                    if built != out_pdf and built.exists():
                        built.replace(out_pdf)
                    used_path = "latexmk"
        except Exception:
            used_path = None

        # No-silent-venue-fallback gate (OUTSIDE the try so the raise is not swallowed): if a real venue was
        # requested but the venue compile did not produce a PDF, FAIL LOUDLY with the LaTeX error — never drop
        # to generic article behind the operator's back (pass --venue generic to opt out).
        if want_venue and not (used_path and out_pdf.exists() and out_pdf.stat().st_size > 0):
            log_p = out_tex.with_suffix(".log")
            tail = ""
            if log_p.exists():
                errs = [ln for ln in log_p.read_text(encoding="utf-8", errors="replace").splitlines()
                        if ln.startswith("!") or "LaTeX Error" in ln][:6]
                tail = " | ".join(errs)
            raise RenderDefect("paper-latex: venue %r failed to compile (style=%s); NOT falling back to generic "
                               "article. Fix the template/source or pass --venue generic to opt out. LaTeX: %s"
                               % (venue, venue_sty, tail or "see %s" % log_p.name))

        # Post-compile health gate (OUTSIDE the try so a raised RenderDefect is NOT swallowed): a non-empty
        # PDF can still hide dropped glyphs / an empty bibliography. Fail loudly so the harness records no
        # artifact rather than silently shipping a broken paper. Clean papers find no problems and pass.
        if used_path and out_pdf.exists() and out_pdf.stat().st_size > 0:
            problems = _render_health(out_tex, bool(bibname))
            if problems:
                raise RenderDefect(
                    "paper-latex compiled %s but the render is defective: %s. Fix the manuscript source "
                    "(author math in $...$ / \\(...\\) / equation envs; cite with Pandoc [@key]; remove any "
                    "hand-written References section so BibTeX emits the bibliography) and re-render."
                    % (out_pdf.name, "; ".join(problems)))

        if used_path and out_pdf.exists() and out_pdf.stat().st_size > 0:
            return {"ok": True, "out_path": str(out_pdf), "format": "pdf",
                    "summary": f"compiled PDF via pandoc+{engine}+{used_path}"
                               + (f" (+venue:{venue_sty})" if venue_sty else " (generic article)")
                               + (" (+CJK)" if cjk else "")
                               + (f" (venue {cjk_venue_skipped} N/A for CJK→ctexart)" if cjk_venue_skipped else "")
                               + (" (+bibtex)" if bibname else "") + (f" (+figs:{n_fig})" if n_fig else "")
                               + (f" (+uni:{n_uni})" if n_uni else "") + " (render-health: clean)",
                    "meta": {"engine": engine, "pandoc": True, "tex_path": str(out_tex),
                             "bytes": out_pdf.stat().st_size, "cjk": cjk, "mainfont": mainfont,
                             "venue": venue, "venue_style": venue_sty, "venue_rationale": venue_rationale,
                             "venue_info": venue_info, "cjk_venue_skipped": cjk_venue_skipped,
                             "bibtex": bool(bibname), "figs_embedded": n_fig,
                             "unicode_math_fallback": n_uni, "render_health": "clean"}}

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
