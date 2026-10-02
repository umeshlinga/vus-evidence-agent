"""Calibration utilities — Platt scaling + ECE/Brier, per gene family.
A probability that means what it says is the whole point of this repo."""
import numpy as np


def platt_fit(scores: np.ndarray, labels: np.ndarray, iters: int = 200, lr: float = 0.1):
    """Fit a,b for p = sigmoid(a*score + b) by gradient descent. Returns (a, b)."""
    a, b = 1.0, 0.0
    s = np.asarray(scores, dtype=float); y = np.asarray(labels, dtype=float)
    for _ in range(iters):
        p = 1 / (1 + np.exp(-(a * s + b)))
        ga = np.mean((p - y) * s); gb = np.mean(p - y)
        a -= lr * ga; b -= lr * gb
    return a, b


def platt_apply(scores, a, b):
    return 1 / (1 + np.exp(-(a * np.asarray(scores, dtype=float) + b)))


def expected_calibration_error(probs, labels, bins: int = 10) -> float:
    p = np.asarray(probs, dtype=float); y = np.asarray(labels, dtype=float)
    edges = np.linspace(0, 1, bins + 1); ece = 0.0
    for i in range(bins):
        m = (p >= edges[i]) & (p < edges[i + 1] if i < bins - 1 else p <= edges[i + 1])
        if m.sum():
            ece += abs(p[m].mean() - y[m].mean()) * m.mean()
    return float(ece)


def brier(probs, labels) -> float:
    return float(np.mean((np.asarray(probs, float) - np.asarray(labels, float)) ** 2))


def auroc(labels, scores) -> float:
    """Rank-based AUROC (Mann-Whitney), no dependencies."""
    labels = np.asarray(labels); scores = np.asarray(scores, float)
    order = np.argsort(scores)
    ranks = np.empty(len(scores)); ranks[order] = np.arange(1, len(scores) + 1)
    # average ranks for ties
    s_sorted = scores[order]
    i = 0
    while i < len(s_sorted):
        j = i
        while j + 1 < len(s_sorted) and s_sorted[j + 1] == s_sorted[i]:
            j += 1
        if j > i:
            ranks[order[i:j + 1]] = ranks[order[i:j + 1]].mean()
        i = j + 1
    pos = labels == 1; n_pos = int(pos.sum()); n_neg = len(labels) - n_pos
    return float((ranks[pos].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg))


def isotonic_fit(scores, labels):
    """Pool-adjacent-violators isotonic regression. Returns (xs, values)."""
    scores = np.asarray(scores, float); labels = np.asarray(labels, float)
    o = np.argsort(scores); xs = list(scores[o]); v = list(labels[o]); w = [1.0] * len(v)
    i = 0
    while i < len(v) - 1:
        if v[i] > v[i + 1]:
            nw = w[i] + w[i + 1]
            v[i] = (v[i] * w[i] + v[i + 1] * w[i + 1]) / nw; w[i] = nw
            del v[i + 1], w[i + 1], xs[i + 1]
            if i: i -= 1
        else:
            i += 1
    return np.array(xs), np.array(v)


def isotonic_apply(model, scores):
    xs, v = model
    idx = np.clip(np.searchsorted(xs, np.asarray(scores, float), side="right") - 1, 0, len(v) - 1)
    return v[idx]
