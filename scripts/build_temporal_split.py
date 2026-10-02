"""Week 1 - the honest temporal split. This script IS the scientific claim.

Train = ClinVar classifications frozen at the cutoff snapshot (2024-01).
Test  = variants that were VUS / conflicting / unclassified at cutoff and
        were RECLASSIFIED to Pathogenic/Likely-pathogenic or Benign/Likely-benign
        in the current snapshot.

No random split. No variant whose test label existed at train time leaks in.
Near-duplicate guard: same (gene, name) vs train -> test row dropped.

Low-memory by design: both snapshots are streamed in chunks, never loaded
whole (each .txt is multiple GB; this VM has ~7GB RAM).

Usage:
  python3 scripts/build_temporal_split.py \
      --cutoff data/variant_summary_2024-01.txt.gz \
      --current data/variant_summary_current.txt.gz \
      --outdir data/processed

Outputs: train_frozen.csv, test_reclassified.csv, SPLIT_REPORT.md
"""
import argparse, csv
from pathlib import Path
import pandas as pd

PATHOGENIC = {"Pathogenic", "Likely pathogenic", "Pathogenic/Likely pathogenic"}
BENIGN = {"Benign", "Likely benign", "Benign/Likely benign"}
UNCERTAIN = {"Uncertain significance", "Conflicting classifications of pathogenicity",
             "Conflicting interpretations of pathogenicity", "not provided", ""}

COLS = ["#AlleleID", "Type", "Name", "GeneSymbol", "ClinicalSignificance",
        "LastEvaluated", "ReviewStatus", "NumberSubmitters", "Assembly",
        "Chromosome", "PositionVCF", "ReferenceAlleleVCF", "AlternateAlleleVCF"]
# COLS index: 0 allele,1 type,2 name,3 gene,4 sig,5 last_eval,6 review,7 n_sub,8 assembly,9 chrom,10 pos,11 ref,12 alt


def label(sig):
    if sig in PATHOGENIC: return 1
    if sig in BENIGN: return 0
    return None


def chunks(path):
    yield from pd.read_csv(path, sep="\t", usecols=COLS, dtype=str,
                           compression="gzip", chunksize=200_000, low_memory=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cutoff", required=True)
    ap.add_argument("--current", required=True)
    ap.add_argument("--cutoff-date", default="2024-01")
    ap.add_argument("--outdir", default="data/processed")
    a = ap.parse_args()
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)

    # Pass 1: cutoff snapshot -> train rows out, sig map + train (gene,name) keys
    old_sig, train_keys, old_coord = {}, set(), {}
    n_old = n_train = n_train_p = 0
    with open(out / "train_frozen.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["allele_id","gene","name","type","significance","label","chrom","pos","ref","alt"])
        for ch in chunks(a.cutoff):
            ch = ch[ch["Assembly"].eq("GRCh38")][COLS]
            n_old += len(ch)
            for r in ch.itertuples(index=False):
                old_sig[r[0]] = r[4]
                # coordinates only for uncertain-at-cutoff alleles (test candidates)
                if r[4] in UNCERTAIN:
                    old_coord[r[0]] = (r[9], r[10], r[11], r[12])
                lab = label(r[4])
                if lab is not None:
                    w.writerow([r[0], r[3], r[2], r[1], r[4], lab, r[9], r[10], r[11], r[12]])
                    train_keys.add((r[3], r[2])); n_train += 1; n_train_p += lab
    print(f"cutoff GRCh38 rows: {n_old:,} | train frozen: {n_train:,} (P={n_train_p:,})")

    # Pass 2: current snapshot -> test = uncertain then, labelled now
    n_new = n_test = n_test_p = n_guard = 0
    with open(out / "test_reclassified.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["allele_id","gene","name","type","sig_then","sig_now","label","last_evaluated","chrom","pos","ref","alt"])
        for ch in chunks(a.current):
            ch = ch[ch["Assembly"].eq("GRCh38")][COLS]
            n_new += len(ch)
            for r in ch.itertuples(index=False):
                then = old_sig.get(r[0])
                if then is None or then not in UNCERTAIN: continue
                lab = label(r[4])
                if lab is None: continue
                if (r[3], r[2]) in train_keys: n_guard += 1; continue
                coord = old_coord.get(r[0], (r[9], r[10], r[11], r[12]))
                w.writerow([r[0], r[3], r[2], r[1], then, r[4], lab, r[5], coord[0], coord[1], coord[2], coord[3]])
                n_test += 1; n_test_p += lab
    print(f"current GRCh38 rows: {n_new:,} | test reclassified: {n_test:,} (P={n_test_p:,}) | guard dropped: {n_guard:,}")

    report = f"""# Temporal split report - ClinVar frozen at {a.cutoff_date}

- Cutoff snapshot rows (GRCh38): {n_old:,}
- Current snapshot rows (GRCh38): {n_new:,}
- **Train** (labelled at cutoff, frozen): {n_train:,} (pathogenic={n_train_p:,}, benign={n_train-n_train_p:,})
- **Test** (uncertain at cutoff -> reclassified by now): {n_test:,} (pathogenic={n_test_p:,}, benign={n_test-n_test_p:,})
- Near-duplicate guard removed: {n_guard:,} test rows sharing gene+name with train

## Why this split
Random ClinVar splits leak: a variant reclassified using predictor scores
reappears, with those scores as features, in both train and test. Here no
test label existed at train time. Caveat (stated, not hidden): post-cutoff
reclassifications are themselves partly predictor-influenced.

## Next (Week 1 cont.)
Join AlphaMissense (link, don't redistribute) + dbNSFP (REVEL/CADD) + gnomAD AF,
then Week 2: ensemble + isotonic/Platt calibration, ECE/Brier per gene family,
SHAP. Week 3 agent cites these retrieved records or declines.
"""
    (out / "SPLIT_REPORT.md").write_text(report)
    print("\n" + report)


if __name__ == "__main__":
    main()
