#!/usr/bin/env python3
"""Fetch gnomAD allele frequencies for the scored variant universe via the
Ensembl VEP REST API (official, no registration). Bounded and polite:
chunks of 500 variants, cached per chunk on disk, resumable, 1s pause.
AF taken as max(gnomAD-genomes overall, gnomAD-exomes overall) for the ALT
allele among colocated variants. NOTE: Ensembl serves its own gnomAD
freeze - version skew vs gnomAD current is documented in the report.
Only SNVs with coordinates are queried.
"""
import json, time, urllib.request, urllib.error
from pathlib import Path
import pandas as pd

d = Path("data/processed_v2")
cache = Path("data/af_cache"); cache.mkdir(exist_ok=True)
tr = pd.read_csv(d / "train_features.csv").merge(pd.read_csv(d / "train_revel.csv"), on="allele_id", how="left")
te = pd.read_csv(d / "test_features.csv").merge(pd.read_csv(d / "test_revel.csv"), on="allele_id", how="left")
tr_sc = tr.dropna(subset=["am_score", "revel_score"])
te_sc = te.dropna(subset=["am_score", "revel_score"])
# Fit needs a solid train sample, not all 138k: 30k label-stratified sample
# keeps this a bounded, polite API use; eval still uses the FULL scored test.
tr_s = (tr_sc.groupby("label", group_keys=False)
        .apply(lambda g: g.sample(n=min(len(g), 15000), random_state=3)))
uni = pd.concat([tr_s, te_sc])
print(f"train sampled {len(tr_s):,} + test {len(te_sc):,}", flush=True)
uni = uni[(uni.ref.str.len() == 1) & (uni.alt.str.len() == 1)][["allele_id", "chrom", "pos", "ref", "alt"]].drop_duplicates("allele_id")
print(f"universe: {len(uni):,} scored SNVs", flush=True)
uni["vstr"] = uni.chrom.astype(str).str.replace("chr", "", regex=False) + " " + uni.pos.astype(str) + " " + uni.pos.astype(str) + " " + uni.ref + "/" + uni.alt + " 1"
id_by_vstr = dict(zip(uni.vstr, uni.allele_id))
vstrs = list(id_by_vstr)
CH = 200
def fetch(chunk, tag):
    body = json.dumps({"variants": chunk}).encode()
    req = urllib.request.Request("https://rest.ensembl.org/vep/homo_sapiens/region?af_gnomad=1&pick=1",
                                 data=body, headers={"Content-Type": "application/json", "Accept": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r)
        except Exception as e:
            print(f"  {tag} attempt {attempt}: {e}; backing off", flush=True)
            time.sleep(10 * (attempt + 1))
    return None

results = {}
import os
WID, NW = int(os.environ.get("WORKER_ID", "0")), int(os.environ.get("N_WORKERS", "1"))
for i in range(0, len(vstrs), CH):
    if (i // CH) % NW != WID:
        continue
    tag = f"chunk_{i//CH:04d}"
    fp = cache / f"{tag}.json"
    if fp.exists():
        out = json.loads(fp.read_text())
    else:
        out = fetch(vstrs[i:i + CH], tag)
        if out is None:
            print(f"{tag}: FAILED permanently, skipping", flush=True)
            continue
        fp.write_text(json.dumps(out))
        time.sleep(1.0)
    for v in out:
        vs = v.get("input")
        if vs not in id_by_vstr:
            continue
        alt = vs.split()[-2].split("/")[-1] if "/" in vs else None
        best = None
        for cv in v.get("colocated_variants", []):
            fr = cv.get("frequencies", {}).get(alt or "", {})
            for k in ("gnomadg", "gnomade"):
                if k in fr:
                    best = fr[k] if best is None else max(best, fr[k])
        if best is not None:
            results[id_by_vstr[vs]] = best
    if (i // CH) % 20 == 0:
        print(f"  {tag}: cumulative AF hits {len(results):,}", flush=True)

s = pd.Series(results, name="gnomad_af"); s.index.name = "allele_id"
s.to_csv(d / "gnomad_af_ensembl.csv")
print(f"DONE: AF for {len(s):,} of {len(uni):,} variants -> data/processed_v2/gnomad_af_ensembl.csv")
