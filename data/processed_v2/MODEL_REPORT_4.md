# Model Report 4 — REVEL ablation (second predictor, no registration), 2026-10-02

REVEL v1.3 from its public Zenodo record (7072866; MD5 verified against the
record: 3ea2bc33e6b5455fc7e9899da863b5fe). No dbNSFP registration - by the
project owner's explicit decision. One row per transcript in the source;
we take the MAX across transcripts (dbNSFP convention), stated openly.
Same Model 2 protocol (fit functions imported from train_ensemble.py,
prior from AM-scored train rows, 80/20 seed-11 split, isotonic on the
train holdout). Test = post-2024 reclassifications only.

Coverage (test, n=27,748): REVEL 39.7% | AlphaMissense 37.4% | either 39.8%.
Both predictors are missense-only, so REVEL barely widens coverage (+0.1pt
combined). Its value, if any, had to come from signal, not reach.

| model | n_test | AUROC | ECE (iso) | Brier (iso) |
|-------|--------|-------|-----------|-------------|
| M2 [AM, prior] (Model Report 2) | 10,373 | 0.958 | 0.017 | 0.078 |
| R+prior [REVEL, prior] | 11,023 | 0.952 | 0.019 | 0.081 |
| M2+R [AM, prior, REVEL] | 10,357 | 0.968 | 0.023 | 0.066 |

READING: adding REVEL buys real discrimination (AUROC 0.958 -> 0.968) and a
better Brier (0.078 -> 0.066) at essentially unchanged calibration
(ECE 0.017 -> 0.023). REVEL alone is roughly AM's peer. We adopt M2+R as the
current best model; per-gene ECE for M2+R and agent re-runs follow.

METHOD NOTE (a trap we fell into and document): building the gene prior
from ALL frozen-train rows instead of only AM-scored rows silently drops
AUROC to 0.933-0.935 (Brier 0.101) - the prior must describe the scored
population the model actually serves, not the whole database.

## Isotonic-calibrated ECE by gene — M2+R (test, n>=50)
  - BRCA2: n=158, ECE=0.041
  - BRCA1: n=138, ECE=0.082
  - ADGRV1: n=130, ECE=0.016
  - DNAH11: n=118, ECE=0.054
  - DMD: n=97, ECE=0.069
  - KMT2D: n=94, ECE=0.069
  - RAI1: n=94, ECE=0.028
  - ABCA4: n=86, ECE=0.023
  - MUTYH: n=86, ECE=0.083
  - SCN1A: n=83, ECE=0.046
  - NF1: n=81, ECE=0.117
  - LDLR: n=74, ECE=0.059
  - USH2A: n=74, ECE=0.290
  - GCK: n=71, ECE=0.030
  - FBN1: n=68, ECE=0.042
