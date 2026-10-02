"""End-to-end demo on tiny synthetic data — no downloads, CPU only.

Shows the full loop: features -> Platt-calibrated probability ->
cited evidence summary -> refusal path when evidence is thin.

Run:  PYTHONPATH=src python3 -m vus_agent.demo
"""
import numpy as np

from .agent import assess, render
from .calibrate import brier, expected_calibration_error, platt_apply, platt_fit
from .features import VariantFeatures

rng = np.random.default_rng(7)

# Synthetic training set: score ~ true pathogenicity + noise (demo only)
n = 400
true_p = rng.beta(2, 5, n)
labels = (rng.random(n) < true_p).astype(int)
raw_scores = np.clip(true_p + rng.normal(0, 0.18, n), 0, 1)

a, b = platt_fit(raw_scores, labels)
cal = platt_apply(raw_scores, a, b)
print(f"Demo calibration: ECE raw={expected_calibration_error(raw_scores, labels):.3f} "
      f"-> calibrated={expected_calibration_error(cal, labels):.3f} | Brier={brier(cal, labels):.3f}\n")


def score(f: VariantFeatures) -> float:
    """Toy ensemble: mean of available predictors -> calibrated."""
    vals = [v for v in (f.alphamissense, f.revel) if v is not None]
    if not vals:
        return None
    return float(platt_apply([np.mean(vals)], a, b)[0])


cases = [
    VariantFeatures("BRCA1:c.5095C>T", "BRCA1", alphamissense=0.94, revel=0.91,
                    cadd_phred=28.0, gnomad_af=0.0, gene_constraint_pli=0.99,
                    clinvar_submissions=["sub-2024-pathogenic-1"]),
    VariantFeatures("TTN:c.12345A>G", "TTN", alphamissense=0.41),  # thin evidence -> must decline
]

for f in cases:
    print(render(assess(f, score(f))))
    print("\n---\n")
