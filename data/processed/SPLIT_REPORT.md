# Temporal split report - ClinVar frozen at 2024-01

- Cutoff snapshot rows (GRCh38): 2,366,650
- Current snapshot rows (GRCh38): 4,578,190
- **Train** (labelled at cutoff, frozen): 1,103,657 (pathogenic=240,752, benign=862,905)
- **Test** (uncertain at cutoff -> reclassified by now): 27,748 (pathogenic=8,856, benign=18,892)
- Near-duplicate guard removed: 0 test rows sharing gene+name with train

## Why this split
Random ClinVar splits leak: a variant reclassified using predictor scores
reappears, with those scores as features, in both train and test. Here no
test label existed at train time. Caveat (stated, not hidden): post-cutoff
reclassifications are themselves partly predictor-influenced.

## Next (Week 1 cont.)
Join AlphaMissense (link, don't redistribute) + dbNSFP (REVEL/CADD) + gnomAD AF,
then Week 2: ensemble + isotonic/Platt calibration, ECE/Brier per gene family,
SHAP. Week 3 agent cites these retrieved records or declines.
