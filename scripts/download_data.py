"""Week-1 data step. Prints pinned sources + licence notes.

Deliberately does NOT download/redistribute AlphaMissense scores —
the licence is ambiguous (README: CC BY 4.0; distributed copies:
CC BY-NC-SA 4.0). Link to scores; don't mirror them. See
docs/licence-notes.md.
"""
SOURCES = {
    "ClinVar (dated releases — pin the date, the temporal split depends on it)":
        "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/",
    "gnomAD (AF + constraint)": "https://gnomad.broadinstitute.org/downloads",
    "dbNSFP (REVEL/CADD panel)": "https://sites.google.com/site/jpopgen/dbNSFP",
    "AlphaMissense (precomputed missense scores — LINK, do not redistribute)":
        "https://github.com/google-deepmind/alphamissense",
}
if __name__ == "__main__":
    for k, v in SOURCES.items():
        print(f"{k}\n  {v}\n")
    print("Next: build frozen-at-cutoff train set + post-cutoff reclassified test set.")
    print("Write the leakage audit (docs/leakage-audit.md) before any model code.")
