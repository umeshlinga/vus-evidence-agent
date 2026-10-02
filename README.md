# vus-evidence-agent

**Calibrated VUS reclassification with an evidence-citing agent.**
Clinical variant interpretation, done honestly.

> Not for clinical use. Research / portfolio project only.

## The problem this solves

Variants of Uncertain Significance (VUS) are the daily bottleneck of
clinical genomics. Predictors disagree, most published models are trained
and tested on random ClinVar splits (leaking variants that were
reclassified using the same evidence), and an AUROC of 0.99 tells a lab
nothing about whether a "90% pathogenic" call is right 90% of the time.

The gap is not another AUROC point. The gap is:

1. **Temporal validity** — train on classifications frozen at a cutoff,
   test only on variants reclassified *after* it.
2. **Calibration** — a probability that means what it says, reported per
   gene family (ECE / Brier), including where calibration fails.
3. **Evidence provenance** — every claim in a report cited to a retrieved
   record, with an explicit allowed answer:
   *"insufficient evidence — remains VUS."*

That third piece is the differentiator. It is an LLM/RAG agent with a
hard rule: **cite, or decline. Never invent.**

## Why this project, why now

This is Pick №1 (29/35) from the Flagship AI-Bioinformatics research
brief (Oct 2, 2026). It is the only candidate that uses all three of my
edges at once:

- clinical variant interpretation (ACMG framework, Cipla clinical
  diagnostics work),
- NGS pipeline engineering (GATK / BWA / VEP, reproducible workflows),
- agentic AI with cited, traceable evidence (my Agentic AI Framework
  for Genetic Evidence Discovery project).

It runs on CPU with fully public data. No controlled-access data on the
critical path.

## Build (3 weeks)

| Week | Deliverable |
|---|---|
| 1 | Dated ClinVar snapshots; frozen-at-cutoff train set + post-cutoff reclassified test set; AlphaMissense + dbNSFP + gnomAD features joined; leakage audit in `docs/leakage-audit.md` |
| 2 | Ensemble (logistic, AM + gene prior) + isotonic/Platt calibration; per-gene ECE/Brier; permutation importance; calibration failures published, not hidden |
| 3 | Evidence agent: retrieval over ClinVar frozen records + predictor records; ACMG-style cited summaries; adversarial tests proving the agent refuses rather than invents; real-variant reports in `examples/agent_reports_real.md` |
| Later | dbNSFP (REVEL/CADD) + gnomAD AF ablations; Docker/Nextflow one-command run |

## Data (all open)

- **ClinVar** — dated releases, pinned by date (the temporal split depends on it)
- **gnomAD** — population context. Note: the light allele-number TSV is
  locus-level AN only and cannot yield allele frequency (see
  `docs/gnomad-note.md`); true AF joins later via per-chromosome sites VCF
  or API, and the model ships honestly without AF until then.
- **dbNSFP** — predictor panel (REVEL / CADD class), optional ablation.
  Currently deferred: bulk download needs institutional-email registration.
- **AlphaMissense** — precomputed missense scores. *Link to the scores,
  do not redistribute them* — the licence is ambiguous (README says
  CC BY 4.0; distributed copies have been labelled CC BY-NC-SA 4.0).
  Weights are not released, so no novel-variant scoring beyond the
  precomputed predictions. See `docs/licence-notes.md`.

## Results (real, temporal test — post-2024 reclassifications only)

| Model | AUROC | ECE | Brier |
|---|---|---|---|
| AlphaMissense alone | 0.921 | 0.040 | 0.113 |
| AlphaMissense + Platt (fit on 2024) | 0.921 | 0.157 | 0.141 |
| Ensemble (AM + gene prior) raw | 0.959 | 0.251 | 0.176 |
| Ensemble + isotonic (fit on train holdout) | 0.958 | 0.017 | 0.078 |

Temporal split: train frozen at 2024-01 (1,103,657 variants); test = 27,748
variants ClinVar reclassified after the freeze (AlphaMissense covers 37.4%).
Evidence agent reports on 10,373/27,748 (37.4%) and declines the rest;
per-gene calibrated ECE 0.020–0.128 for most genes, with honest failures
NF1 (0.231) and USH2A (0.278). Full detail in `data/processed_v2/`:
`SPLIT_REPORT.md`, `FEATURE_REPORT.md`, `MODEL_REPORT.md`,
`MODEL_REPORT_2.md`, and `examples/agent_reports_real.md`.

## Run the demo (no downloads, CPU, 10 seconds)

```bash
cd ~/workspace/vus-evidence-agent
PYTHONPATH=src python3 -m vus_agent.demo
PYTHONPATH=src python3 tests/test_agent_refuses.py
```

Full pipeline reproduction (needs the downloaded ClinVar/AlphaMissense files):
```bash
python3 scripts/build_temporal_split.py
python3 scripts/join_alphamissense.py
python3 scripts/train_ensemble.py
python3 scripts/train_mlp.py
PYTHONPATH=src python3 scripts/run_agent_real.py
```

The demo uses a tiny synthetic variant table to show the full loop:
features → calibrated probability → cited evidence summary → and the
refusal path when evidence is insufficient.

## Repo map

```
src/vus_agent/
  features.py     feature join: AlphaMissense + dbNSFP panel + gnomAD AF + constraint
  calibrate.py    Platt / isotonic calibration, ECE + Brier per gene family
  agent.py        evidence agent — cite-or-decline, enforced in code
  demo.py         runnable end-to-end demo on synthetic data
scripts/
  download_data.py  prints pinned source URLs + licence notes (does not redistribute scores)
docs/
  leakage-audit.md  why random ClinVar splits leak, and the temporal-split design
  licence-notes.md  AlphaMissense / State / RFdiffusion licence watch-outs
  flagship-playbook.md  what Lila / Flagship-type startups build, their hard problems,
                        and the external mirror-build for each
examples/
  example-report.md  a sample ACMG-style cited report + a sample refusal
tests/
  test_agent_refuses.py  adversarial: fabricated citation / missing record → must decline
```

## Honest limits (say them out loud)

- Temporal reclassification labels are themselves partly
  predictor-influenced. That circularity is discussed, not hidden.
- AlphaMissense scores cover missense only, precomputed only.
- A calibrated probability is not a clinical classification. ACMG
  classification remains a human, guideline-driven judgement.

## How this maps to the companies I want to work at

Flagship-type startups (Lila Sciences, Generate:Biomedicines,
Recursion, insitro, Arc) all run the same loop: **model proposes →
experiment/data tests → calibrated evidence decides → system learns.**
Their hard problems and the external mirror-build for each are in
`docs/flagship-playbook.md`. This repo is the clinical-genomics
instance of that loop, built entirely from public data.
