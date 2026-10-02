"""Week 1 cont. - join AlphaMissense scores to the temporal split.

Key: (chrom, pos, ref, alt) on GRCh38. AlphaMissense file is streamed;
only rows matching a train/test variant are kept (the file is ~700MB gz,
we never load it whole, and we LINK to it - never redistribute it).

Usage:
  python3 scripts/join_alphamissense.py \
      --am data/AlphaMissense_hg38.tsv.gz \
      --train data/processed_v2/train_frozen.csv \
      --test  data/processed_v2/test_reclassified.csv \
      --outdir data/processed_v2

Outputs: train_features.csv, test_features.csv, FEATURE_REPORT.md
(am_score / am_class; coverage reported honestly, by split and label.)
"""
import argparse, csv
from pathlib import Path
import pandas as pd


def load_keys(path):
    df = pd.read_csv(path, dtype=str, usecols=["chrom", "pos", "ref", "alt"])
    return set(zip(df.chrom, df.pos, df.ref, df.alt))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--am", required=True); ap.add_argument("--train", required=True)
    ap.add_argument("--test", required=True); ap.add_argument("--outdir", default="data/processed_v2")
    a = ap.parse_args(); out = Path(a.outdir)

    wanted = load_keys(a.train) | load_keys(a.test)
    print(f"variant keys to match: {len(wanted):,}")
    wanted_df = pd.DataFrame(sorted(wanted), columns=["chrom", "pos", "ref", "alt"])

    hits = {}
    # verified AM header: CHROM POS REF ALT genome uniprot_id transcript_id protein_variant am_pathogenicity am_class
    reader = pd.read_csv(a.am, sep="\t", comment="#", header=None,
                         names=["chrom", "pos", "ref", "alt", "genome", "uniprot_id",
                                "transcript_id", "protein_variant", "am_score", "am_class"],
                         dtype=str, compression="gzip", chunksize=500_000)
    for ch in reader:
        ch["pos"] = ch["pos"].astype(str)
        # AM uses "chr10", ClinVar uses "10" - normalise before matching
        ch["chrom"] = ch.chrom.str.replace("^chr", "", regex=True)
        matched = ch.merge(wanted_df, on=["chrom", "pos", "ref", "alt"], how="inner")
        for row in matched.itertuples(index=False):
            hits[(row.chrom, row.pos, row.ref, row.alt)] = (row.am_score, row.am_class)
    print(f"AlphaMissense matches: {len(hits):,}")

    lines = ["# AlphaMissense feature join\n"]
    for name, src in [("train", a.train), ("test", a.test)]:
        df = pd.read_csv(src, dtype=str)
        df["am_score"] = [hits.get((c, p, r, al), (None, None))[0]
                          for c, p, r, al in zip(df.chrom, df.pos.astype(str), df.ref, df.alt)]
        df["am_class"] = [hits.get((c, p, r, al), (None, None))[1]
                          for c, p, r, al in zip(df.chrom, df.pos.astype(str), df.ref, df.alt)]
        dest = out / f"{name}_features.csv"; df.to_csv(dest, index=False)
        cov = df.am_score.notna().mean()
        lines.append(f"- **{name}**: {len(df):,} rows, AlphaMissense coverage {cov:.1%}")
        if "label" in df:
            for lab in (0, 1):
                sub = df[df.label.astype(str).eq(str(lab))]
                lines.append(f"  - label={lab}: {len(sub):,}, coverage {sub.am_score.notna().mean():.1%}")
        print(lines[-1])

    lines += ["\nMissense-only, precomputed scores only (weights not released).",
              "Scores linked from source, not redistributed. See docs/licence-notes.md."]
    (out / "FEATURE_REPORT.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
