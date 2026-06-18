# action: polish (figure-polish → render-inspect-revise QA on an existing figure)
`$HARNESS --via skill:deepresearch-figure/polish:<role> render polish --quest-id <q> --artifact-id <q>:fig-<name>-p \
  --ref runs/<q>/figures/<name>-polished.pdf --input runs/<q>/figures/<name>.pdf`
Run the self-review checklist (figure-polish/references/checklist.md); the house style removes frames/spines.
