# Leakage audit (write this BEFORE any model code)

## The leak
Most published variant models train and test on random ClinVar splits.
A variant reclassified in 2024 was often reclassified *using* the same
predictor scores and submissions that appear as features. Random
splits put that variant (or its near-duplicates) in both train and
test — the model is graded on evidence it has already seen.

## The fix used here
- Pin a dated ClinVar release. **Train:** classifications frozen at
  cutoff date D. **Test:** only variants whose classification *changed
  after D*.
- Join features (AlphaMissense / dbNSFP / gnomAD) as of D where the
  source allows dating; where it doesn't, say so per-feature.
- Near-duplicate guard: same variant / same codon across splits goes
  to train only.

## The honest caveat
Post-cutoff reclassification labels are themselves partly
predictor-influenced. The temporal split removes the direct leak; it
does not make labels pure. This is stated in the README, not buried.
