#!/usr/bin/env python3
"""REVEL ablation under the EXACT Model 2 protocol (same fit/isotonics/
prior construction imported from train_ensemble.py, same 80/20 seed-11
split) so the only thing that changes is the feature set:
  M2      [am_score, gene_prior]            (reproduces Model Report 2)
  M2+R    [am_score, gene_prior, revel]
  R+prior [revel_score, gene_prior]         (REVEL-scored subset)
Prior is computed from AM-scored train rows only, as in Model 2 - building
it from the full train instead drops AUROC to ~0.935 and worsens Brier
(the prior must describe the scored population; see MODEL_REPORT_4.md).
"""
import sys
sys.path.insert(0, "src"); sys.path.insert(0, "scripts")
import numpy as np, pandas as pd
from vus_agent.calibrate import auroc, expected_calibration_error as ece, brier
from train_ensemble import fit_logreg, isotonic_bins, isotonic_apply

d = "data/processed_v2"
tr0 = pd.read_csv(f"{d}/train_features.csv").merge(pd.read_csv(f"{d}/train_revel.csv"), on="allele_id", how="left")
te0 = pd.read_csv(f"{d}/test_features.csv").merge(pd.read_csv(f"{d}/test_revel.csv"), on="allele_id", how="left")
print(f"TEST coverage: REVEL {te0.revel_score.notna().mean()*100:.1f}% | AM {te0.am_score.notna().mean()*100:.1f}% | either {te0[['revel_score','am_score']].notna().any(axis=1).mean()*100:.1f}%")

scored_tr = tr0[tr0.am_score.notna()]
glob = scored_tr.label.mean()
stats = scored_tr.groupby("gene").label.agg(["sum", "count"])
prior_map = ((stats["sum"] + 10 * glob) / (stats["count"] + 10)).to_dict()
for df in (tr0, te0):
    df["gene_prior"] = df.gene.map(prior_map).fillna(glob)

def run(name, cols, tr, te):
    tr = tr.sample(frac=1, random_state=11).reset_index(drop=True)
    cut = int(0.8 * len(tr)); fit, hold = tr.iloc[:cut], tr.iloc[cut:]
    w, b, mu, sd = fit_logreg(fit[cols].to_numpy(), fit.label.to_numpy())
    def predict(df):
        X = (df[cols].to_numpy() - mu) / sd
        return 1 / (1 + np.exp(-(X @ w + b)))
    hold_p, test_p = predict(hold), predict(te)
    edges, means = isotonic_bins(hold_p, hold.label.to_numpy())
    y = te.label.to_numpy(); p_iso = isotonic_apply(test_p, edges, means)
    print(f"{name:22s} n_test={len(te):,}  raw AUROC {auroc(y, test_p):.3f} ECE {ece(test_p, y):.3f} Brier {brier(test_p, y):.3f} | "
          f"+isotonic AUROC {auroc(y, p_iso):.3f} ECE {ece(p_iso, y):.3f} Brier {brier(p_iso, y):.3f}")
    return test_p, p_iso

tr_am = tr0[tr0.am_score.notna()].copy(); te_am = te0[te0.am_score.notna()].copy()
run("M2 [AM,prior]", ["am_score", "gene_prior"], tr_am, te_am)
tr_b = tr0.dropna(subset=["am_score", "revel_score"]).copy(); te_b = te0.dropna(subset=["am_score", "revel_score"]).copy()
_, p_iso_r = run("M2+R [AM,prior,REVEL]", ["am_score", "gene_prior", "revel_score"], tr_b, te_b)
tr_r = tr0[tr0.revel_score.notna()].copy(); te_r = te0[te0.revel_score.notna()].copy()
run("R+prior [REVEL,prior]", ["revel_score", "gene_prior"], tr_r, te_r)
out = te_b[["allele_id", "gene", "name", "label", "am_score", "revel_score", "gene_prior"]].copy()
out["prob_m2r_isotonic"] = p_iso_r
out.to_csv(f"{d}/test_predictions_revel.csv", index=False)
print("wrote test_predictions_revel.csv")
