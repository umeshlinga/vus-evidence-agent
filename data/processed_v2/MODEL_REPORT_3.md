# Model Report 3 — WithoutMLP (from-scratch NumPy forecaster), 2026-10-02

Network: 2-16-16-1 tanh MLP in raw NumPy (fused decoupled gradients, seed 13,
300 epochs, loss 0.703 -> 0.266). Inputs: AlphaMissense score + gene prior
gated by exp(-|am-0.5|*4) so the prior only speaks where AM is uncertain.
Trained on ≤2024-01 ClinVar; tested ONLY on post-2024 reclassifications
(n=10,373 with AM scores). Calibration maps fitted on a train-time holdout.

| variant | AUROC | ECE | Brier |
|---------|-------|-----|-------|
| WithoutMLP raw | 0.947 | 0.192 | 0.097 |
| + isotonic (train holdout) | 0.947 | 0.175 | 0.090 |
| + Platt (train holdout) | 0.947 | 0.182 | 0.102 |

Permutation importance (test AUROC drop): am_score 0.360, gated prior 0.043.

HONEST READING: the hand-built MLP does NOT beat the simple linear ensemble
(Model Report 2: AUROC 0.959, isotonic ECE 0.017). Its raw probabilities are
sharper (Brier 0.097 vs 0.176) but its calibration transfers worse - the
isotonic map fitted on its saturated holdout scores barely helps on future
data. More model is not more truth; the linear model + isotonic stays our
headline. Interpretability is via permutation importance (model-agnostic),
not SHAP values, and is labelled as such everywhere.

gnomAD AF: not a feature - the allele-number download is locus-level AN
with no AC/alt, so it cannot yield a variant allele frequency
(docs/gnomad-note.md). AF joins later via per-chromosome sites VCF or API.
