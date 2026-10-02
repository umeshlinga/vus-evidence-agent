# gnomAD - what we verified, and the honest route to AF

Downloaded and inspected 2026-10-02: `gnomad.exomes.v4.1.allele_number_all_sites.tsv.bgz` (1.15 GB).
Header: `locus  AN  outside_broad_capture_region  outside_ukb_capture_region  ...`
It is **locus-level allele NUMBER only** - no ref/alt allele, no allele count (AC).
It cannot produce an allele frequency for a specific variant allele. We do
not use it as an AF feature, and we say so rather than relabelling coverage as frequency.

Correct AF routes (from the official downloads page, browser-verified):
- Per-chromosome sites VCFs (`.vcf.bgz` + `.tbi`) - AC/AN/AF in INFO, but ~5 GB for chr22 alone; all chromosomes is tens of GB.
- gnomAD GraphQL API for a small number of variants (rate-limited) - viable for the 10,373 scored test variants as a bounded batch, with polite pacing.
Status: deferred by design. The Week 2 ensemble (AlphaMissense + gene prior + isotonic) stands without AF; AF joins as an ablation when the VCF/API route is run.
