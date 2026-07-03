# Comparability Contract

Use this reference when deciding whether a baseline is truly usable downstream.

## Minimum or core contract

Make these fields explicit:

- task identity
- dataset identity
- split contract
- evaluation script or path
- required metric keys
- metric directions
- source commit or package identity
- known deviations

A core contract is enough for a `comparison_ready` baseline.
Expand to a fuller contract only when later paper claims, variant-heavy comparison, or publication really need it.

## Verdict logic

- usable now
- usable with caveats
- blocked

If later `experiment` work would have to keep guessing the comparison contract, the baseline is not ready.
