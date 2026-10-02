# Model report 2 - ensemble (AM + gene prior), temporal test

Scored-only: train 138,972 / test 10,373. Gene prior is computed
from the frozen train labels ONLY (smoothed, m=10); test genes unseen in
train fall back to the global train rate 0.379.

## Test results (reclassified after 2024)
- **AM raw**: AUROC=0.921 ECE=0.040 Brier=0.113
- **Ensemble raw (AM+gene prior)**: AUROC=0.959 ECE=0.251 Brier=0.176
- **Ensemble + Platt (train holdout)**: AUROC=0.959 ECE=0.276 Brier=0.187
- **Ensemble + isotonic (train holdout)**: AUROC=0.958 ECE=0.017 Brier=0.078

## Isotonic-calibrated ECE by gene (test, n>=50)
  - BRCA2: n=158, ECE=0.086
  - BRCA1: n=138, ECE=0.064
  - ADGRV1: n=130, ECE=0.020
  - DNAH11: n=118, ECE=0.070
  - DMD: n=97, ECE=0.082
  - KMT2D: n=94, ECE=0.062
  - RAI1: n=94, ECE=0.038
  - ABCA4: n=86, ECE=0.072
  - MUTYH: n=86, ECE=0.128
  - SCN1A: n=83, ECE=0.027
  - NF1: n=81, ECE=0.231
  - LDLR: n=74, ECE=0.104
  - USH2A: n=74, ECE=0.278
  - GCK: n=71, ECE=0.067
  - FBN1: n=68, ECE=0.066

## Reading this honestly
AM raw (previous report): AUROC=0.921 ECE=0.040 Brier=0.113; AM Platt
fit on all of 2024 train degraded to ECE=0.157. The ensemble table above
is judged against those two lines - improvement must show on ECE/Brier
without touching the test set for fitting. gnomAD AF (downloaded
separately) and dbNSFP REVEL/CADD (registration-gated) are the next
features; SHAP requires the scikit-learn/XGBoost step.
