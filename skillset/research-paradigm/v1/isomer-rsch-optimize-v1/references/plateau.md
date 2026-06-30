# Plateau Response

Use this reference when one line keeps producing non-improving results.

## Plateau Indicators

- repeated non-improving results on the same line
- repeated small tweaks with no structural change
- candidate queue filled with near-duplicate mechanisms

## Required Response

1. State that the line is plateauing.
2. Identify the most likely root cause of the plateau.
3. Choose one route: widen search, promote a stronger alternative, fuse with another line, debug a strategically valuable blocked candidate, or stop the line.
4. Record one explicit non-repeat rule so the next pass does not retry the same low-information move.

## Family-Shift Trigger

If recent attempts stay inside one mechanism family without meaningful improvement, the next pass should not be another same-family Tier1 tweak. Choose an orthogonal family, Tier2 or Tier3 shift, fusion, or stop.

## Do Not Do

- keep proposing near-identical local tweaks
- rerun the same unchanged candidate
- fuse without a complementary mechanism
- hide plateau under repeated one-more-tweak loops
