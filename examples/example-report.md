# Example report (synthetic — format demo only, not a clinical call)

## Cited summary

# BRCA1:c.5095C>T (BRCA1)
**Verdict:** evidence summary (not a clinical classification)
**Calibrated P(pathogenic):** 0.87

## Evidence (every claim cited)
- [AlphaMissense] score=0.94 <AM:BRCA1:c.5095C>T>
- [dbNSFP/REVEL] REVEL=0.91 <REVEL:BRCA1:c.5095C>T>
- [dbNSFP/CADD] CADD Phred=28.0 <CADD:BRCA1:c.5095C>T>
- [gnomAD] AF=0.00e+00 <GNOMAD:BRCA1:c.5095C>T>
- [gnomAD constraint] pLI=0.99 <PLI:BRCA1>
- [ClinVar submission] sub-2024-pathogenic-1 <CLINVAR:BRCA1:c.5095C>T:sub-2024-pathogenic-1>

## Refusal (the path that matters)

# TTN:c.12345A>G (TTN)
**Verdict:** insufficient evidence — remains VUS

One predictor score is not an evidence base. The agent declines
rather than drafting confident prose around a single number. In a
clinical-shaped workflow, this is the correct output.
