# How this gets shown to companies (prep — post ONLY after real model results)

Status as of 2026-10-02: Week 1 temporal split DONE with real counts
(see data/processed/SPLIT_REPORT.md). Model, calibration curves, and
agent demo on real variants are NOT done yet — nothing is posted
until they exist. No brackets, no invented numbers.

## Sequence
1. Finish Week 1 feature join (AlphaMissense linked, dbNSFP, gnomAD)
   + Week 2 calibrated model (ECE/Brier per gene family, SHAP).
2. Push to github.com/umeshlinga/vus-evidence-agent — Umesh signs in
   himself in the live browser (Leo never takes passwords). Pin repo,
   link from portfolio site.
3. LinkedIn Post 1 (roadmap kit): "AUROC is solved. Calibration is
   not..." with the real reliability-diagram figure attached, repo
   link in first comment.
4. Direct outreach only to people at target companies working on
   variant interpretation / VariantBench-type problems — same
   selectivity rules as job outreach (never mass-connect).

## Proof already in hand for step 1 conversations
- ClinVar 2024-01: 2,366,650 GRCh38 rows -> train frozen 1,103,657
  (240,752 pathogenic / 862,905 benign)
- Current ClinVar: 4,578,190 rows -> test = 27,748 variants uncertain
  at cutoff, reclassified since (8,856 pathogenic / 18,892 benign)
- Reproducible: `python3 scripts/build_temporal_split.py ...`
