# action: plot (paper-plot → matplotlib vector figure)
`$HARNESS --via skill:deepresearch-figure/plot:<role> render plot --quest-id <q> --artifact-id <q>:fig-<name> \
  --ref runs/<q>/figures/<name>.pdf --input <data.json|csv> --kind scatter|bar|line [--y-label <l>]`
Render to `.pdf` so it embeds. Pick `--kind` to match the data (predicted-vs-measured → scatter; ablation → bar).
