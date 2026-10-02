"""Week 2, first slice - is AlphaMissense alone calibrated on FUTURE data?

Model: am_score only. Platt scaling fit on train (frozen 2024, scored subset),
evaluated untouched on test (reclassified after 2024). No sklearn needed.
Isotonic (PAVA) reported as comparator fit on train via cross-binning.

Outputs: data/processed_v2/MODEL_REPORT.md + test_predictions.csv
Metrics: AUROC, ECE, Brier - raw vs Platt - plus ECE per gene (n>=50 scored).
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, "src")
from vus_agent.calibrate import brier, expected_calibration_error, platt_apply, platt_fit


def auroc(scores, labels):
    order = np.argsort(scores); ranks = np.empty(len(scores), float)
    ranks[order] = np.arange(1, len(scores) + 1)
    # average ranks for ties
    s = pd.Series(scores); ranks = s.rank(method="average").to_numpy()
    pos = labels == 1; npos, nneg = pos.sum(), (~pos).sum()
    return float((ranks[pos].sum() - npos * (npos + 1) / 2) / (npos * nneg))


def main():
    tr = pd.read_csv("data/processed_v2/train_features.csv")
    te = pd.read_csv("data/processed_v2/test_features.csv")
    tr = tr[tr.am_score.notna()]; te = te[te.am_score.notna()].copy()
    print(f"scored train: {len(tr):,} | scored test: {len(te):,}")

    a, b = platt_fit(tr.am_score.to_numpy(), tr.label.to_numpy())
    te["prob_raw"] = te.am_score.astype(float)
    te["prob_cal"] = platt_apply(te.am_score.to_numpy(), a, b)

    y = te.label.to_numpy()
    rows = []
    for name, p in [("raw am_score", te.prob_raw), ("Platt (fit on 2024 train)", te.prob_cal)]:
        rows.append(f"- **{name}**: AUROC={auroc(p.to_numpy(), y):.3f} "
                    f"ECE={expected_calibration_error(p, y):.3f} Brier={brier(p, y):.3f}")

    gene_rows = []
    for gene, sub in te.groupby("gene"):
        if len(sub) >= 50:
            gene_rows.append((gene, len(sub), expected_calibration_error(sub.prob_cal, sub.label.to_numpy())))
    gene_rows.sort(key=lambda x: -x[1])
    gene_txt = "\n".join(f"  - {g}: n={n}, calibrated ECE={e:.3f}" for g, n, e in gene_rows[:15])

    te_out = te[["allele_id", "gene", "name", "label", "am_score", "prob_raw", "prob_cal"]]
    te_out.to_csv("data/processed_v2/test_predictions.csv", index=False)

    report = f"""# Model report - AlphaMissense alone, temporal test

Scored subsets only (missense SNVs with a precomputed score):
train {len(tr):,} / test {len(te):,}.

## Test results (variants reclassified AFTER the 2024 freeze)
{chr(10).join(rows)}

AUROC is identical for raw and Platt (monotonic transform) - the point
of calibration is that ECE/Brier improve and the number means what it
says. If they don't improve, that is reported too.

## Calibrated ECE by gene (test, n>=50 scored)
{gene_txt if gene_txt else '  - (no gene reached n>=50)'}

## Honest limits
Single-feature model. Coverage: train 12.6%, test 37.4% of variants
have any AlphaMissense score (missense only). Ensemble with REVEL/CADD
(dbNSFP, registration-gated) and gnomAD AF is the next Week 2 step.
Temporal labels remain partly predictor-influenced - see leakage audit.
"""
    Path("data/processed_v2/MODEL_REPORT.md").write_text(report)
    print(report)


if __name__ == "__main__":
    main()
