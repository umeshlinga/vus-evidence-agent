#!/usr/bin/env python3
"""Week 3: run the evidence agent on REAL temporal-test variants.
Evidence available at prediction time ONLY (frozen-2024 worldview):
  1. AlphaMissense score          -> record AM:chr:pos:ref>alt
  2. Frozen ClinVar status (sig_then, allele id) -> CLINVAR record
  3. Gene prior from frozen train labels        -> GENEPRIOR record
The future reclassification (sig_now / label) is NEVER evidence; it is
used only afterwards to check whether the agent's summary was right.
Below 3 evidence items the agent declines - by design (MIN_EVIDENCE).
"""
import sys
sys.path.insert(0, "src")
import pandas as pd
from vus_agent.features import VariantFeatures
from vus_agent.agent import assess, render, EvidenceItem
import vus_agent.agent as A

d = "data/processed_v2"
te = pd.read_csv(f"{d}/test_features.csv")
pr = pd.read_csv(f"{d}/test_predictions_ensemble.csv")[["allele_id", "prob_ensemble"]]
df = te.merge(pr, on="allele_id", how="left")

def build(row):
    f = VariantFeatures(variant_id=str(row["name"]), gene=str(row["gene"]))
    ev = []
    if pd.notna(row.get("am_score")):
        ev.append(EvidenceItem("AlphaMissense", f"score={row.am_score:.3f} class={row.am_class}",
                               f"AM:{row.chrom}:{row.pos}:{row.ref}>{row.alt}"))
    ev.append(EvidenceItem("ClinVar (frozen 2024-01)", f"status then: {row.sig_then}",
                           f"CLINVAR:allele{row.allele_id}"))
    if pd.notna(row.get("prob_ensemble")) and pd.notna(row.get("am_score")):
        ev.append(EvidenceItem("Gene prior (frozen train)", f"gene={row.gene}",
                               f"GENEPRIOR:{row.gene}:frozen2024"))
    return f, ev, (float(row.prob_ensemble) if pd.notna(row.get("prob_ensemble")) else None)

def assess_real(row):
    f, ev, prob = build(row)
    if len(ev) < A.MIN_EVIDENCE or prob is None:
        return {"variant": f.variant_id, "gene": f.gene,
                "verdict": "insufficient evidence — remains VUS",
                "calibrated_prob_pathogenic": None,
                "citations": [e.record_id for e in ev],
                "evidence": [f"[{e.source}] {e.detail} <{e.record_id}>" for e in ev]}
    return {"variant": f.variant_id, "gene": f.gene,
            "verdict": "evidence summary (not a clinical classification)",
            "calibrated_prob_pathogenic": round(prob, 3),
            "citations": [e.record_id for e in ev],
            "evidence": [f"[{e.source}] {e.detail} <{e.record_id}>" for e in ev]}

rows = [assess_real(r) for _, r in df.iterrows()]
spoken = [r for r in rows if r["calibrated_prob_pathogenic"] is not None]
lab = df.label.to_numpy()
print(f"test variants: {len(rows):,} | agent may summarise: {len(spoken):,} ({100*len(spoken)/len(rows):.1f}%) | declines: {len(rows)-len(spoken):,}")

df["spoken"] = [r["calibrated_prob_pathogenic"] is not None for r in rows]
ok = ((df.prob_ensemble >= 0.5).astype(int) == df.label)
print(f"among spoken, prob>=0.5 agrees with future reclassification: {100*ok[df.spoken].mean():.1f}%")

out = ["# Agent reports on REAL variants (temporal test set)", "",
       f"Agent may summarise **{len(spoken):,} of {len(rows):,}** reclassified variants; "
       f"it declines the rest (no AlphaMissense score - the honest majority). "
       "Future labels shown here are evaluation-only, never agent evidence.", ""]
show = df[df.spoken].nlargest(3, "prob_ensemble").index.tolist() + \
       df[df.spoken].nsmallest(3, "prob_ensemble").index.tolist() + \
       df[df.spoken & ~ok].head(3).index.tolist()
titles = ["## Confident pathogenic-leaning", "## Confident benign-leaning", "## Honest misses (model disagreed with the future)"]
k = 0
for gi in range(3):
    out.append(titles[gi]); out.append("")
    for i in show[gi*3:(gi+1)*3]:
        r = rows[i]
        out.append(render(r)); out.append("")
        out.append(f"*(future truth, evaluation only: label={int(df.label[i])}, now '{df.sig_now[i]}')*"); out.append("")
out.append("## Declines (adversarial by construction: evidence removed / absent)"); out.append("")
dec = df[~df.spoken].head(3)
for i in dec.index:
    out.append(render(rows[i])); out.append("")
open("examples/agent_reports_real.md", "w").write("\n".join(out))
print("wrote examples/agent_reports_real.md")
