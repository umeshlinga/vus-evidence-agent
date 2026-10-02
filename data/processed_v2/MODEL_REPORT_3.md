# Model Report 3 — WithoutMLP (from-scratch NumPy forecaster), 2026-10-02

Network: 2-16-16-1 tanh MLP in raw NumPy (fused decoupled gradients, seed 13,
300 epochs, loss 0.703 -> 0.266). Inputs: AlphaMissense score + gene prior
gated by exp(-|am-0.5|*4) so the prior only speaks where AM is uncertain.
Trained on ≤2024-01 ClinVar; tested ONLY on post-2024 reclassifications
(n=10,373 with AM scores). Calibration maps fitted on a train-time holdout.

| variant | AUROC | ECE | Brier |
|---------|-------|-----|-------|
| WithoutMLP raw | 0.947 | 0.048 | 0.097 |
| + isotonic (train holdout) | 0.947 | 0.013 | 0.090 |
| + Platt (train holdout) | 0.947 | 0.059 | 0.102 |

Permutation importance (test AUROC drop): am_score 0.360, gated prior 0.043.

HONEST READING: the hand-built MLP does not beat the linear ensemble
(Model Report 2: AUROC 0.958, isotonic ECE 0.017, Brier 0.078). It calibrates
about as well after isotonic (ECE 0.013) but ranks worse (AUROC 0.947) and
scores worse overall (Brier 0.090). More model is not more truth; the linear
model stays our headline. Interpretability is permutation importance
(model-agnostic), labelled as such, not SHAP.

CORRECTION NOTE: the first committed version of this report printed ECE
values computed with an argument-order bug in the ECE call (labels passed
where probabilities belong). A reproduction audit of Model Report 2 caught
it; the table above is recomputed correctly. AUROC and Brier were unaffected.
