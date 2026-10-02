#!/usr/bin/env python3
"""WithoutMLP: tiny from-scratch NumPy MLP, fused decoupled math.
Signals: am_score (primary) + exp-gated gene prior (licence-free derived).
Trained on 2023-12-31-or-earlier labelled data, calibrated on a TRAIN-time
holdout, tested ONLY on post-2024 reclassifications. sklearn only fits the
isotonic/Platt maps - the forecaster itself is hand-rolled NumPy.
"""
import numpy as np, pandas as pd
from vus_agent.calibrate import auroc, expected_calibration_error as ece, brier, isotonic_fit, isotonic_apply
rng = np.random.default_rng(13)
d = "data/processed_v2"
tr = pd.read_csv(f"{d}/train_features.csv").dropna(subset=["am_score"]); te = pd.read_csv(f"{d}/test_features.csv").dropna(subset=["am_score"])
m = 10.0
rate = tr.label.mean()
sm = tr.groupby("gene").label.agg(["sum", "count"])
prior_map = ((sm["sum"] + m * rate) / (sm["count"] + m)).to_dict()
def feats(df):
    prior = df.gene.map(prior_map).fillna(rate).to_numpy()[:, None]
    am = df.am_score.to_numpy()[:, None]
    gate = np.exp(-np.abs(am - 0.5) * 4.0)          # abstains where AM already sure
    return np.hstack([am, prior * gate]), am, prior * gate, gate
Xtr, amtr, prtr, _ = feats(tr); Xte, amte, prte, gte_ = feats(te)
ytr = tr.label.to_numpy(float); yte = te.label.to_numpy()
n = len(Xtr); idx = rng.permutation(n); cut = int(0.85 * n)
itr, ica = idx[:cut], idx[cut:]

class WithoutMLP:
    def __init__(s, d_in=2, h=16):
        s.W1 = rng.normal(0, 0.5, (d_in, h)); s.b1 = np.zeros(h)
        s.W2 = rng.normal(0, 0.5, (h, h));   s.b2 = np.zeros(h)
        s.W3 = rng.normal(0, 0.5, (h, 1));   s.b3 = np.zeros(1)
    def forward(s, X):
        z1 = X @ s.W1 + s.b1; a1 = np.tanh(z1)
        z2 = a1 @ s.W2 + s.b2; a2 = np.tanh(z2)
        lo = (a2 @ s.W3 + s.b3).ravel()
        return 1 / (1 + np.exp(-lo)), (X, a1, a2, lo)
    def step(s, X, y, lr=0.05):
        p, (X, a1, a2, lo) = s.forward(X)
        g = (p - y) / len(y)
        dW3 = a2.T @ g[:, None]; db3 = g.sum(keepdims=True)
        dz2 = (g[:, None] @ s.W3.T) * (1 - a2 ** 2)
        dW2 = a1.T @ dz2; db2 = dz2.sum(0)
        dz1 = (dz2 @ s.W2.T) * (1 - a1 ** 2)
        dW1 = X.T @ dz1; db1 = dz1.sum(0)
        for W, dW in [(s.W1, dW1), (s.W2, dW2), (s.W3, dW3)]:
            W -= lr * dW
        s.b1 -= lr * db1; s.b2 -= lr * db2; s.b3 -= lr * db3
        return float(np.mean(-(y * np.log(p + 1e-12) + (1 - y) * np.log(1 - p + 1e-12))))

net = WithoutMLP()
for ep in range(300):
    loss = net.step(Xtr[itr], ytr[itr])
    if ep % 100 == 0: print(f"  epoch {ep}: loss {loss:.4f}")
raw_cal, _ = net.forward(Xtr[ica]); raw_te, _ = net.forward(Xte)
def fit_platt(x, y, iters=300, lr=0.5):
    a, b, xm, xs_ = 1.0, 0.0, x.mean(), x.std() + 1e-9
    z = (x - xm) / xs_
    for _ in range(iters):
        p = 1 / (1 + np.exp(-(a * z + b))); g = p - y
        a -= lr * float(np.mean(g * z)); b -= lr * float(np.mean(g))
    return (a, b, xm, xs_)
def platt_predict(model, x):
    a, b, xm, xs_ = model
    return 1 / (1 + np.exp(-(a * (x - xm) / xs_ + b)))
iso = isotonic_fit(raw_cal, ytr[ica]); pla = fit_platt(raw_cal, ytr[ica])
for name, p in [("raw", raw_te), ("+isotonic(train-holdout)", isotonic_apply(iso, raw_te)), ("+Platt(train-holdout)", platt_predict(pla, raw_te))]:
    print(f"  WithoutMLP {name:26s} AUROC {auroc(yte, p):.3f}  ECE {ece(yte, p):.3f}  Brier {brier(yte, p):.3f}")

# permutation importance on test (SHAP-equivalent honesty check, model-agnostic)
base = auroc(yte, raw_te)
for j, nm in enumerate(["am_score", "gated prior"]):
    Xp = Xte.copy(); Xp[:, j] = rng.permutation(Xp[:, j])
    pp, _ = net.forward(Xp)
    print(f"  permute {nm:12s} AUROC drop {base - auroc(yte, pp):.3f}")
pd.DataFrame({"gene": te.gene, "label": yte, "prob_raw": raw_te, "prob_isotonic": isotonic_apply(iso, raw_te)}).to_csv(f"{d}/test_predictions_mlp.csv", index=False)
print("  wrote test_predictions_mlp.csv")
