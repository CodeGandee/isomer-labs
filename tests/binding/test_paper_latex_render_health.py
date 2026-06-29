#!/usr/bin/env python3
"""regression suite — paper-latex adapter render-health gate + unicode math fallback.

The paper-latex compiler adapter must NOT silently report success on a broken render. After a compile it
inspects the by-products and FAILS LOUDLY (the harness turns a raised adapter exception into ok=False +
records no artifact) when either:
  - the LaTeX .log reports 'Missing character' (a glyph was dropped from the PDF), or
  - a .bib was supplied but the compiled .bbl has no \\bibitem (empty bibliography / no resolved citations).
A clean paper (no missing chars, non-empty .bbl) still passes. None of this depends on `fc-list`: raw
Unicode math glyphs are mapped to math-mode via an injected `newunicodechar` block.

Run:  python3 tests/binding/test_paper_latex_render_health.py   (exits non-zero on any failure)
"""
import importlib.util, pathlib, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
ADAPTER = ROOT / "execplan" / "packs" / "paper-latex" / "adapter.py"
PASSED, FAILED = [], []


def _load():
    spec = importlib.util.spec_from_file_location("paper_latex_adapter", ADAPTER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_cli():
    """Import the harness cli module (for the venue-policy helpers). Returns None if it cannot import."""
    try:
        src = ROOT / "execplan" / "harness" / "src"
        if str(src) not in sys.path:
            sys.path.insert(0, str(src))
        spec = importlib.util.spec_from_file_location("ds_cli_for_test", src / "cli.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except Exception:
        return None


def check(label, cond, detail=""):
    (PASSED if cond else FAILED).append(label)
    print(("  PASS " if cond else "  FAIL ") + label + (("  -- " + detail) if detail and not cond else ""))


def main():
    a = _load()

    # ---- _scan_missing_chars ----
    log = ("Missing character: There is no ρ (U+03C1) in font [lmroman10-regular]:mapping=tex-text;!\n"
           "Missing character: There is no ρ (U+03C1) in font [lmroman10-regular]:mapping=tex-text;!\n"
           "Missing character: There is no ≤ (U+2264) in font [lmroman10-regular]:mapping=tex-text;!\n"
           "Underfull \\hbox (badness 3260) in paragraph at lines 485--489\n")
    miss = a._scan_missing_chars(log)
    check("scan finds distinct missing glyphs (dedup ρ, keep ≤)", len(miss) == 2, str(miss))
    check("scan reports the codepoint tag", any("U+03C1" in m for m in miss), str(miss))
    check("scan clean log -> none", a._scan_missing_chars("This is a clean log.\n") == [])

    # ---- _bbl_nonempty ----
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        empty = td / "empty.bbl"
        empty.write_text("\\begin{thebibliography}{0}\n\\end{thebibliography}\n")
        full = td / "full.bbl"
        full.write_text("\\begin{thebibliography}{7}\n\\bibitem{x} X et al.\n\\end{thebibliography}\n")
        check("bbl with no \\bibitem is empty", a._bbl_nonempty(empty) is False)
        check("bbl with a \\bibitem is non-empty", a._bbl_nonempty(full) is True)
        check("missing bbl file is non-empty=False", a._bbl_nonempty(td / "nope.bbl") is False)

        # ---- _render_health: writes a fake tex+log+bbl, checks problem detection ----
        def health(stem, logtxt, bbltxt, bib_provided):
            tex = td / (stem + ".tex"); tex.write_text("x")
            (td / (stem + ".log")).write_text(logtxt)
            if bbltxt is not None:
                (td / (stem + ".bbl")).write_text(bbltxt)
            return a._render_health(tex, bib_provided)

        clean_log = "Output written on paper.xdv (6 pages).\n"
        good_bbl = "\\begin{thebibliography}{7}\n\\bibitem{x} X\n\\end{thebibliography}\n"
        empty_bbl = "\\begin{thebibliography}{0}\n\\end{thebibliography}\n"

        p1 = health("p1", log, good_bbl, True)
        check("health flags dropped glyphs", any("Missing character" in p or "dropped glyph" in p for p in p1), str(p1))

        p2 = health("p2", clean_log, empty_bbl, True)
        check("health flags empty bibliography when bib provided",
              any("empty bibliography" in p for p in p2), str(p2))

        p3 = health("p3", clean_log, empty_bbl, False)
        check("health IGNORES empty bbl when NO bib provided (no false positive)", p3 == [], str(p3))

        p4 = health("p4", clean_log, good_bbl, True)
        check("CLEAN paper passes (no problems) -- preserves success", p4 == [], str(p4))

        p5 = health("p5", log, empty_bbl, True)
        check("health reports BOTH defects together", len(p5) == 2, str(p5))

    # ---- _inject_unicode_math_fallback ----
    tex = ("\\documentclass{article}\n\\usepackage{lmodern}\n\\begin{document}\n"
           "where $rho$ is wrong but here is raw ρ and ≤ 10\\% and S ≥ 16384.\n\\end{document}\n")
    out, n = a._inject_unicode_math_fallback(tex)
    check("inject maps the raw glyphs present", n >= 3, "n=%d" % n)
    check("inject adds a guarded newunicodechar block", "\\IfFileExists{newunicodechar.sty}" in out
          and "\\newunicodechar{ρ}{\\ensuremath{\\rho}}" in out)
    check("inject places block before \\begin{document}",
          out.index("deepresearch-unicode-math-fallback") < out.index("\\begin{document}"))
    out2, n2 = a._inject_unicode_math_fallback(out)
    check("inject is idempotent (no double injection)", n2 == 0 and out2 == out)
    clean_tex = "\\documentclass{article}\n\\begin{document}\nNo raw glyphs, only $\\rho \\le 1$.\n\\end{document}\n"
    out3, n3 = a._inject_unicode_math_fallback(clean_tex)
    check("inject is a no-op when no raw glyphs present", n3 == 0 and out3 == clean_tex)

    # ---- RenderDefect exists and is an exception type ----
    check("RenderDefect is an exception", isinstance(a.RenderDefect("x"), Exception))

    # ---- _inject_venue: documentclass-aware (the bug was injecting INSIDE \documentclass[...]) ----
    # pandoc emits the class across two lines; the venue \usepackage must land AFTER ]{article}, not inside.
    pandoc_tex = "\\PassOptionsToPackage{unicode}{hyperref}\n\\documentclass[\n]{article}\n\\usepackage{xcolor}\n\\begin{document}\nx\n\\end{document}\n"
    vi = {"staged": True, "style": "iclr2026_conference"}
    inj, stem = a._inject_venue(pandoc_tex, vi)
    check("inject returns the style stem", stem == "iclr2026_conference", str(stem))
    check("venue \\usepackage lands AFTER ]{article}, not inside the optional args",
          "]{article}\n\\usepackage{iclr2026_conference}" in inj, repr(inj[:120]))
    check("inject does NOT corrupt the \\documentclass options",
          "\\documentclass[\n\\usepackage" not in inj)
    check("inject no-op when venue not applicable (style=None)",
          a._inject_venue(pandoc_tex, {"staged": True, "style": None}) == (pandoc_tex, None))

    # ---- _stage_venue: primary-style selection + acmart-not-applicable + unknown ----
    with tempfile.TemporaryDirectory() as td:
        iclr = a._stage_venue("iclr2026", td)
        check("stage iclr2026 -> primary style iclr2026_conference + applicable",
              iclr and iclr.get("style") == "iclr2026_conference" and iclr.get("applicable") is True, str(iclr and iclr.get("style")))
        osdi = a._stage_venue("osdi2026", td)
        check("stage osdi2026 -> usenix-2020-09 style + applicable",
              osdi and osdi.get("style") == "usenix-2020-09" and osdi.get("applicable") is True, str(osdi and osdi.get("style")))
        asplos = a._stage_venue("asplos2027", td)
        check("stage asplos2027 (acmart) -> NOT applicable (no injectable style)",
              asplos and asplos.get("staged") is True and asplos.get("applicable") is False, str(asplos))
        unk = a._stage_venue("nope9999", td)
        check("stage unknown venue -> staged False + error", unk and unk.get("staged") is False and "error" in unk, str(unk))
        check("stage 'generic' -> None (explicit opt-out, no staging)", a._stage_venue("generic", td) is None)

    # ---- CJK editions must NOT get a Latin-conference venue style (the paper-zh layout regression) ----
    check("_has_cjk detects Chinese text", a._has_cjk("无拟合第一性原理周期级性能模型") is True)
    check("_has_cjk False for pure Latin", a._has_cjk("A No-Fit Cycle-Level Model") is False)
    check("_has_cjk True for mixed EN+CJK", a._has_cjk("FlashAttention-4 在 B200") is True)
    eff, want, skipped = a._resolve_cjk_venue("osdi2026", True)
    check("CJK + venue -> venue skipped (generic ctexart), recorded",
          eff == "generic" and want is False and skipped == "osdi2026", f"{eff},{want},{skipped}")
    eff, want, skipped = a._resolve_cjk_venue("osdi2026", False)
    check("non-CJK + venue -> venue applied", eff == "osdi2026" and want is True and skipped is None)
    eff, want, skipped = a._resolve_cjk_venue("generic", True)
    check("CJK + explicit generic -> generic, nothing skipped", eff == "generic" and want is False and skipped is None)
    eff, want, skipped = a._resolve_cjk_venue("iclr2026", True)
    check("CJK + iclr -> also skipped (any Latin venue)", eff == "generic" and skipped == "iclr2026")

    # ---- cli venue policy: _infer_venue + _resolve_report_venue precedence ----
    cli = _load_cli()
    if cli is not None:
        check("infer: systems/arch text -> a systems venue (osdi2026/nsdi2027)",
              cli._infer_venue("CUDA Blackwell GPU kernel performance model")[0] in ("osdi2026", "nsdi2027"))
        check("infer: q1 spine style -> osdi2026",
              cli._infer_venue("ML-systems / architecture-performance (MLSys/ISPASS-style)")[0] == "osdi2026")
        check("infer: general ML/AI -> iclr2026 default",
              cli._infer_venue("a deep learning method for image classification")[0] == "iclr2026")
        check("infer: networking -> nsdi2027", cli._infer_venue("datacenter network congestion control")[0] == "nsdi2027")
        check("infer: neurips token -> neurips2025", cli._infer_venue("targeting the neurips venue")[0] == "neurips2025")
        check("resolve: explicit --venue wins", cli._resolve_report_venue(None, "qX", "icml2026")[0] == "icml2026")
        check("resolve: --venue generic is the explicit opt-out", cli._resolve_report_venue(None, "qX", "generic")[0] == "generic")
        check("inferred venues are all renderable in this toolchain",
              all(cli._infer_venue(t)[0] in cli._RENDERABLE_VENUES for t in
                  ("gpu kernel", "deep learning", "network", "nlp parsing", "operating system scheduler")))
    else:
        check("cli module importable for venue-policy tests", False, "could not import cli.py")

    print("\n%d passed, %d failed" % (len(PASSED), len(FAILED)))
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
