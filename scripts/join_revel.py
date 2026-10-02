#!/usr/bin/env python3
"""Join REVEL v1.3 (Zenodo 7072866, MD5-verified, no registration) to the
temporal split. Keys: chr:grch38_pos:ref:alt (SNVs only). REVEL publishes
one row per transcript; dbNSFP convention takes the MAX across transcripts,
and we do the same, saying so in the report. Link-not-redistribute applies
to the raw file exactly as with AlphaMissense.
"""
import csv, subprocess, sys
import pandas as pd

d = "data/processed_v2"
def load_keys(path):
    df = pd.read_csv(path, usecols=["allele_id", "chrom", "pos", "ref", "alt"], dtype={"chrom": str})
    df = df[(df.ref.str.len() == 1) & (df.alt.str.len() == 1)]
    key = df.chrom.str.replace("chr", "", regex=False) + ":" + df.pos.astype(str) + ":" + df.ref + ":" + df.alt
    return dict(zip(key, df.allele_id))

maps = {"train": load_keys(f"{d}/train_features.csv"), "test": load_keys(f"{d}/test_features.csv")}
hits = {"train": {}, "test": {}}
proc = subprocess.Popen(["unzip", "-p", "data/raw/revel-v1.3_all_chromosomes.zip", "revel_with_transcript_ids"],
                        stdout=subprocess.PIPE, text=True, bufsize=1 << 20)
rdr = csv.reader(proc.stdout)
header = next(rdr)
assert header[:8] == ["chr", "hg19_pos", "grch38_pos", "ref", "alt", "aaref", "aaalt", "REVEL"], header
n = 0
for row in rdr:
    n += 1
    if n % 20_000_000 == 0:
        print(f"  streamed {n/1e6:.0f}M rows; hits train={len(hits['train']):,} test={len(hits['test']):,}", flush=True)
    k = f"{row[0]}:{row[2]}:{row[3]}:{row[4]}"
    try:
        s = float(row[7])
    except ValueError:
        continue
    for split, mp in maps.items():
        aid = mp.get(k)
        if aid is not None and s > hits[split].get(aid, -1.0):
            hits[split][aid] = s
proc.wait()
for split in ("train", "test"):
    pd.DataFrame({"allele_id": list(hits[split].keys()), "revel_score": list(hits[split].values())}).to_csv(
        f"{d}/{split}_revel.csv", index=False)
    print(f"{split}: REVEL matched {len(hits[split]):,} of {len(maps[split]):,} SNV variants")
