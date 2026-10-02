# Model report - AlphaMissense alone, temporal test

Scored subsets only (missense SNVs with a precomputed score):
train 138,972 / test 10,373.

## Test results (variants reclassified AFTER the 2024 freeze)
- **raw am_score**: AUROC=0.921 ECE=0.040 Brier=0.113
- **Platt (fit on 2024 train)**: AUROC=0.921 ECE=0.157 Brier=0.141

AUROC is identical for raw and Platt (monotonic transform) - the point
of calibration is that ECE/Brier improve and the number means what it
says. If they don't improve, that is reported too.

## Calibrated ECE by gene (test, n>=50 scored)
  - BRCA2: n=158, calibrated ECE=0.240
  - BRCA1: n=138, calibrated ECE=0.208
  - ADGRV1: n=130, calibrated ECE=0.265
  - DNAH11: n=118, calibrated ECE=0.313
  - DMD: n=97, calibrated ECE=0.311
  - KMT2D: n=94, calibrated ECE=0.307
  - RAI1: n=94, calibrated ECE=0.293
  - ABCA4: n=86, calibrated ECE=0.420
  - MUTYH: n=86, calibrated ECE=0.225
  - SCN1A: n=83, calibrated ECE=0.288
  - NF1: n=81, calibrated ECE=0.203
  - LDLR: n=74, calibrated ECE=0.424
  - USH2A: n=74, calibrated ECE=0.428
  - GCK: n=71, calibrated ECE=0.359
  - FBN1: n=68, calibrated ECE=0.302

## Honest limits
Single-feature model. Coverage: train 12.6%, test 37.4% of variants
have any AlphaMissense score (missense only). Ensemble with REVEL/CADD
(dbNSFP, registration-gated) and gnomAD AF is the next Week 2 step.
Temporal labels remain partly predictor-influenced - see leakage audit.
