"""Week 2, ensemble slice - AlphaMissense + gene prior (train-only).

Features (all legitimately available at prediction time):
  x1 = am_score
  x2 = smoothed per-gene pathogenic rate in the FROZEN train set
       prior = (gene_pathogenic + 10 * global_rate) / (gene_n + 10)

Logistic regression by gradient descent (numpy only). Calibration:
Platt + isotonic (binned) fitted on a train HOLDOUT (20% of scored train,
never on test). Evaluated once on the temporal test set, per gene too.

Comparators in the same table: AM raw, AM Platt-on-train (from train_model.py).
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, "src")
from vus_agent.calibrate import brier, expected_calibration_error, platt_apply, platt_fit


def auroc(s, y):
    return float((pd.Series(s).rank().to_numpy()[y == 1].sum()
                  - (y == 1).sum() * ((y == 1).sum() + 1) / 2)
                 / ((y == 1).sum() * (y == 0).sum()))


def fit_logreg(X, y, iters=400, lr=0.3):
    X = (X - X.mean(0)) / (X.std(0) + 1e-9)
    w = np.zeros(X.shape[1]); b = 0.0
    for _ in range(iters):
        p = 1 / (1 + np.exp(-(X @ w + b)))
        w -= lr * (X.T @ (p - y)) / len(y); b -= lr * np.mean(p - y)
    mu, sd = X.mean(0), X.std(0)
    return w, b, mu, sd


def isotonic_bins(scores, labels, bins=20):
    edges = np.quantile(scores, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    idx = np.clip(np.digitize(scores, edges[1:-1]), 0, bins - 1)
    means = np.array([labels[idx == i].mean() if (idx == i).any() else np.nan for i in range(bins)])
    # PAVA-lite: cumulative monotonic enforcement
    means = np.maximum.accumulate(np.where(np.isnan(means), 0, means))
    return edges, means


def isotonic_apply(scores, edges, means):
    idx = np.clip(np.digitize(scores, edges[1:-1]), 0, len(means) - 1)
    return means[idx]


def main():
    tr = pd.read_csv("data/processed_v2/train_features.csv")
    te = pd.read_csv("data/processed_v2/test_features.csv")
    tr = tr[tr.am_score.notna()].copy(); te = te[te.am_score.notna()].copy()

    glob = tr.label.mean()
    stats = tr.groupby("gene").label.agg(["sum", "count"])
    prior_map = ((stats["sum"] + 10 * glob) / (stats["count"] + 10)).to_dict()
    for df in (tr, te):
        df["gene_prior"] = df.gene.map(prior_map).fillna(glob)

    rng = np.random.default_rng(11)
    tr = tr.sample(frac=1, random_state=11).reset_index(drop=True)
    cut = int(0.8 * len(tr)); fit, hold = tr.iloc[:cut], tr.iloc[cut:]

    feats = ["am_score", "gene_prior"]
    w, b, mu, sd = fit_logreg(fit[feats].to_numpy(), fit.label.to_numpy())
    def predict(df):
        X = (df[feats].to_numpy() - mu) / sd
        return 1 / (1 + np.exp(-(X @ w + b)))

    hold_p, test_p = predict(hold), predict(te)
    a, bb = platt_fit(hold_p, hold.label.to_numpy())
    edges, means = isotonic_bins(hold_p, hold.label.to_numpy())
    y = te.label.to_numpy()

    variants = {
        "AM raw": te.am_score.to_numpy(float),
        "Ensemble raw (AM+gene prior)": test_p,
        "Ensemble + Platt (train holdout)": platt_apply(test_p, a, bb),
        "Ensemble + isotonic (train holdout)": isotonic_apply(test_p, edges, means),
    }
    lines = [f"- **{k}**: AUROC={auroc(v, y):.3f} ECE={expected_calibration_error(v, y):.3f} Brier={brier(v, y):.3f}"
             for k, v in variants.items()]

    te["prob_ensemble"] = variants["Ensemble + isotonic (train holdout)"]
    gene_rows = []
    for gene, sub in te.groupby("gene"):
        if len(sub) >= 50:
            gene_rows.append((gene, len(sub), expected_calibration_error(sub.prob_ensemble, sub.label.to_numpy())))
    gene_rows.sort(key=lambda x: -x[1])
    gene_txt = "\n".join(f"  - {g}: n={n}, ECE={e:.3f}" for g, n, e in gene_rows[:15])
    te[["allele_id", "gene", "name", "label", "am_score", "gene_prior", "prob_ensemble"]].to_csv(
        "data/processed_v2/test_predictions_ensemble.csv", index=False)

    report = f"""# Model report 2 - ensemble (AM + gene prior), temporal test

Scored-only: train {len(tr):,} / test {len(te):,}. Gene prior is computed
from the frozen train labels ONLY (smoothed, m=10); test genes unseen in
train fall back to the global train rate {glob:.3f}.

## Test results (reclassified after 2024)
{chr(10).join(lines)}

## Isotonic-calibrated ECE by gene (test, n>=50)
{gene_txt}

## Reading this honestly
AM raw (previous report): AUROC=0.921 ECE=0.040 Brier=0.113; AM Platt
fit on all of 2024 train degraded to ECE=0.157. The ensemble table above
is judged against those two lines - improvement must show on ECE/Brier
without touching the test set for fitting. gnomAD AF (downloaded
separately) and dbNSFP REVEL/CADD (registration-gated) are the next
features; SHAP requires the scikit-learn/XGBoost step.
"""
    Path("data/processed_v2/MODEL_REPORT_2.md").write_text(report)
    print(report)


if __name__ == "__main__":
    main()
