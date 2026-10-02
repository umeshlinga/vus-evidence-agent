# 12-week sequence (from Flagship_Project_Roadmap.html, 2026-10-02)

One engineering spine across all three: data versioning, held-out evaluation, calibration/uncertainty reporting. Build 1 ships first — CPU-only, widest audience.

| Weeks | Build | Ship |
|---|---|---|
| W1–3.5 | 1 · vus-evidence-agent (this repo) | ClinVar temporal split → calibrated model (XGBoost/logistic, isotonic/Platt, SHAP, ECE/Brier per gene family) → cited-evidence agent → Nextflow + Docker + CI, README limits plain |
| W4–7 | 2 · hybrid-perturb-bench | Harness+baselines → GEARS + winners' hybrid → honest leaderboard → W7 stretch: cell-line held-out |
| W8–11 | 3 · heart-niche-atlas (+ neuro) | cell2location bake-off (alpha 20 vs 200) vs NNLS → Squidpy niches w/ uncertainty → Allen mouse→human transfer benchmark |
| W12 | Consolidation | Cross-links, pinned LinkedIn posts, portfolio integration. KPMP kidney = optional disease-contrast second act |

Rejected 4th: RFdiffusion+ProteinMPNN binder design (22/35 — unverifiable without wet lab, crowded, no clinical edge). Training a new sc foundation model rejected outright (2025 benchmarks + compute).
