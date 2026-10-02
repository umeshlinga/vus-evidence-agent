# The Flagship playbook — what they're building, their hard problems,
# and the external mirror-build that proves you can do the work

You cannot join their lab to prove yourself. You don't need to.
Every company below runs the same loop in public:

**model proposes → data/experiment tests → calibrated evidence decides → system learns**

Build that loop, honestly, on public data, in their stack's idioms —
and a hiring manager can read your repo the way they'd read an
internal design doc. That is the whole strategy.

---

## 1. Lila Sciences (Flagship-founded 2023) — "scientific superintelligence"

**What they're building.** The world's first scientific
superintelligence platform plus fully autonomous labs — "AI Science
Factories" — for life, chemical, and materials sciences. The AI
generates hypotheses, designs experiments, robotics runs them, results
feed back as the reward signal, in real time. Raised $200M seed
(Mar 2025), then ~$235M Series A + $115M from Nvidia (~$1.3B
valuation). Early proof points they cite: genetic-medicine constructs
beating commercial therapeutics, hundreds of novel
antibodies/peptides/binders, and a non-platinum green-hydrogen
catalyst ~1000× cheaper, found in ~4 months.

**Their hard problems (the ones they say out loud):**
- Closing the loop at scale: AI must autonomously run *every* step,
  idea → robotics → measurement → learning. Today humans still move
  samples between machines in some campaigns.
- Asynchronous RL where "experience" arrives from GPUs *and* physical
  instruments with latencies from milliseconds to days.
- Orchestration that treats GPUs, lab robotics, and simulation as one
  system, not three stacks. Large-scale MoE training where
  expert-parallel communication dominates.
- Instrument connectivity/fragmentation — most lab instruments aren't
  connected; maintenance runs 10–20% of equipment cost/year; novel
  hypotheses can require instruments that don't exist yet.
- Science's memory leak: negative results never get published, so the
  same dead ends get re-run. Their asset is a complete run log,
  failures included.

**Your external mirror-build (no lab required):**
An **experiment-loop agent on public data** — a system that proposes a
hypothesis (e.g. "these VUS will reclassify pathogenic"), "runs" it
against a held-out future dataset (post-cutoff ClinVar), scores
itself, logs *every* run including failures, and iterates. That is
exactly this repo's Week 1–3. You are demonstrating the *software*
half of Lila's loop: hypothesis → test → calibrated verdict →
complete audit log. Say that mapping explicitly in the README of any
application to them.

## 2. Generate:Biomedicines (Flagship, 2018) — generative protein therapeutics

**Building:** a generate–build–measure–learn platform that designs
protein sequences for therapeutic goals, produces and characterises
them at scale, and co-optimises function + developability (half-life,
potency, immunogenicity). Lead AI-designed anti-TSLP antibody GB-0895
reached Phase 3 in ~4 years; deals with Amgen (up to ~$1.9B) and
Novartis (~$1B+).

**Hard problems:** in-silico rankings are unverifiable without a wet
lab; developability (will it survive in a body?) is not the same as
binding; immunogenicity of de-novo sequences.

**Mirror-build:** RFdiffusion + ProteinMPNN + structure-prediction
filter against one well-chosen target, with an honest developability
scorecard and a "this is where wet-lab validation would decide"
section. Ranked only 22/35 in the brief — crowded, specialist, uses
none of your clinical edge. **Stretch goal, not flagship.**

## 3. Arc Institute / Tahoe / CZI — the virtual cell

**Building:** perturbation-response prediction — a "virtual cell" that
predicts what a CRISPR/drug perturbation does before you run it.
Arc's State model: embedding on 167M observational cells, transition
model on >100M perturbed cells. Tahoe-100M: 100M cells, 50 lines,
1,138 conditions (CC0). The 2026 Virtual Cell Challenge is redesigned
around zero-shot generalisation to unseen cellular contexts — the
exact capability 2025 showed is missing.

**Hard problems (measured, not vibes):** in the 2025 challenge almost
every model *lost to a simple mean baseline on MAE*. Zero-shot
single-cell foundation models frequently lose to HVG+PCA / scVI
(Genome Biology 2025). Winners were hybrids: deep learning + classical
statistics + protein (ESM-2) embeddings. Arc's own people reportedly
put an "AlphaFold moment" for virtual cells >10 years away — blaming
data quality, not architecture.

**Mirror-build:** Pick №2 in the brief (`hybrid-perturb-bench`, 27/35)
— reproduce the winners' hybrid recipe on public Perturb-seq /
a Tahoe-100M slice, with perturbation-held-out splits, Arc's own
cell-eval metrics, and a public leaderboard **including where you
lose to the mean**. That honesty *is* the deliverable. This is your
second repo, weeks 4–7.

## 4. Recursion / insitro — phenomics + human-genetics ML

**Building:** Recursion: massive standardised perturbation +
imaging ("phenomics") datasets feeding ML for drug discovery
(Roche/Genentech deal up to ~$12B, ~40 programs). insitro: AI-derived
human phenotypes (liver fat/fibrosis) + genetics to find causal
targets (IRS1 → siRNA candidate for MASH).

**Hard problems:** batch effects at industrial scale; a model factor
that captures purity/sex/batch instead of biology; causal target ID
vs correlation.

**Mirror-build:** your Statistical Genetics project, sharpened —
GWAS + fine-mapping + colocalisation + Mendelian randomisation on
public summary stats, with donor/sample-held-out validation and a
covariate-first interpretation. You already claim this work; the repo
makes it *visible*.

## 5. Clinical genomics labs (the hospital side) — VUS

**Building:** diagnostic pipelines that must classify variants under
ACMG, with audit trails, on patient samples, every day.

**Hard problem:** 28.3% of patients in one HBOC/Lynch cohort carried a
VUS (253/663); predictors disagree; management is inconsistent. The
unsolved parts are calibration, temporal validity, provenance — not
AUROC.

**Mirror-build:** **this repo.** Pick №1, 29/35.

---

## The rule for all five

Don't clone their *product*. Clone their *loop*, at public-data
scale, with their failure modes named in your README:

| Their failure mode | Your repo must show |
|---|---|
| Models lose to the mean baseline | Your leaderboard shows the baseline, and where you lose to it |
| Random-split leakage | Temporal / donor-held-out splits, leakage audit written first |
| Uncalibrated confidence | ECE/Brier per subgroup, calibration curves incl. failures |
| LLM invents evidence | Cite-or-decline enforced in code + adversarial tests |
| Negative results vanish | Full run log, failures included |

A repo that does those five things reads as "this person already
works the way we work." That is how you prove yourself without
joining. Build №1 first (weeks 1–3), №2 second (weeks 4–7).

---

## 6. Latch Bio — the question you actually asked ("lagged bio")

**What Latch builds: infrastructure, not science models.** Founded
2021 (Berkeley engineers), $5M seed (Lux) + $28M Series A (Coatue/Lux).
A browser platform so biologists run bioinformatics without touching
cloud: Python SDK that turns workflows into no-code interfaces, cloud
data management, serverless compute, verified pipeline library
(RNA-seq, AlphaFold, single-cell, CRISPR). Now: AI agents + public
agent benchmarks (scBench, SpatialBench, EpiBench, VariantBench),
MCP support so coding agents can drive the platform, Latch
Biosecurity (June 2026 acquisition).

**Can you build "that" externally? Honest split:**
- *The cloud platform itself — no, and don't claim it.* Serverless
  infra, data registry, hundreds of TB customer data, funded team.
  "I built a Latch competitor" is the overclaim recruiters laugh at.
- *The layer on top — absolutely.* Latch's bet is the valuable work
  is analyses/agents on shared infra. A flagship that produces a
  result (calibrated VUS engine, perturbation leaderboard, spatial
  atlas) is exactly what their platform exists to host.

**How you compete in their arena:** publish results, not plumbing;
make every flagship runnable by strangers (one-command Docker/
Nextflow, live demo, reproducible figures — "clone it and run it" is
the no-code promise earned the engineer's way); use their public
benchmark surface (single-cell / spatial / variant = Builds 1–3).
Then say plainly: *"Platforms like Latch solved the infrastructure.
Here's the science layer — open, benchmarked, reproducible."*
A peer's post, not a fan's. Full detail + LinkedIn kit in
`Flagship_Project_Roadmap.html` (Latch section + Post 4).
