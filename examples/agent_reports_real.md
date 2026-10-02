# Agent reports on REAL variants (temporal test set)

Agent may summarise **10,373 of 27,748** reclassified variants; it declines the rest (no AlphaMissense score - the honest majority). Future labels shown here are evaluation-only, never agent evidence.

## Confident pathogenic-leaning

# NM_000492.4(CFTR):c.1373G>T (p.Gly458Val) (CFTR)
**Verdict:** evidence summary (not a clinical classification)
**Calibrated P(pathogenic):** 0.996

## Evidence (every claim cited)
- [AlphaMissense] score=0.961 class=likely_pathogenic <AM:7:117548804:G>T>
- [ClinVar (frozen 2024-01)] status then: Uncertain significance <CLINVAR:allele22171>
- [Gene prior (frozen train)] gene=CFTR <GENEPRIOR:CFTR:frozen2024>

*(future truth, evaluation only: label=1, now 'Likely pathogenic')*

# NM_000492.4(CFTR):c.3873G>C (p.Gln1291His) (CFTR)
**Verdict:** evidence summary (not a clinical classification)
**Calibrated P(pathogenic):** 0.996

## Evidence (every claim cited)
- [AlphaMissense] score=0.975 class=likely_pathogenic <AM:7:117642593:G>C>
- [ClinVar (frozen 2024-01)] status then: Conflicting interpretations of pathogenicity <CLINVAR:allele22191>
- [Gene prior (frozen train)] gene=CFTR <GENEPRIOR:CFTR:frozen2024>

*(future truth, evaluation only: label=1, now 'Pathogenic/Likely pathogenic')*

# NM_000492.4(CFTR):c.3746G>A (p.Gly1249Glu) (CFTR)
**Verdict:** evidence summary (not a clinical classification)
**Calibrated P(pathogenic):** 0.996

## Evidence (every claim cited)
- [AlphaMissense] score=0.988 class=likely_pathogenic <AM:7:117642466:G>A>
- [ClinVar (frozen 2024-01)] status then: Conflicting interpretations of pathogenicity <CLINVAR:allele22255>
- [Gene prior (frozen train)] gene=CFTR <GENEPRIOR:CFTR:frozen2024>

*(future truth, evaluation only: label=1, now 'Pathogenic/Likely pathogenic')*

## Confident benign-leaning

# NM_006267.5(RANBP2):c.1754C>T (p.Thr585Met) (RANBP2)
**Verdict:** evidence summary (not a clinical classification)
**Calibrated P(pathogenic):** 0.002

## Evidence (every claim cited)
- [AlphaMissense] score=0.075 class=likely_benign <AM:2:108751993:C>T>
- [ClinVar (frozen 2024-01)] status then: Conflicting interpretations of pathogenicity <CLINVAR:allele23402>
- [Gene prior (frozen train)] gene=RANBP2 <GENEPRIOR:RANBP2:frozen2024>

*(future truth, evaluation only: label=1, now 'Pathogenic/Likely pathogenic')*

# NM_032119.4(ADGRV1):c.14309G>A (p.Arg4770His) (ADGRV1)
**Verdict:** evidence summary (not a clinical classification)
**Calibrated P(pathogenic):** 0.002

## Evidence (every claim cited)
- [AlphaMissense] score=0.065 class=likely_benign <AM:5:90791138:G>A>
- [ClinVar (frozen 2024-01)] status then: Conflicting interpretations of pathogenicity <CLINVAR:allele55435>
- [Gene prior (frozen train)] gene=ADGRV1 <GENEPRIOR:ADGRV1:frozen2024>

*(future truth, evaluation only: label=0, now 'Benign/Likely benign')*

# NM_032119.4(ADGRV1):c.463A>G (p.Ile155Val) (ADGRV1)
**Verdict:** evidence summary (not a clinical classification)
**Calibrated P(pathogenic):** 0.002

## Evidence (every claim cited)
- [AlphaMissense] score=0.062 class=likely_benign <AM:5:90622606:A>G>
- [ClinVar (frozen 2024-01)] status then: Conflicting interpretations of pathogenicity <CLINVAR:allele55495>
- [Gene prior (frozen train)] gene=ADGRV1 <GENEPRIOR:ADGRV1:frozen2024>

*(future truth, evaluation only: label=0, now 'Benign/Likely benign')*

## Honest misses (model disagreed with the future)

# NM_138413.4(HOGA1):c.289C>T (p.Arg97Cys) (HOGA1)
**Verdict:** evidence summary (not a clinical classification)
**Calibrated P(pathogenic):** 0.493

## Evidence (every claim cited)
- [AlphaMissense] score=0.166 class=likely_benign <AM:10:97598852:C>T>
- [ClinVar (frozen 2024-01)] status then: Conflicting interpretations of pathogenicity <CLINVAR:allele15070>
- [Gene prior (frozen train)] gene=HOGA1 <GENEPRIOR:HOGA1:frozen2024>

*(future truth, evaluation only: label=1, now 'Pathogenic/Likely pathogenic')*

# NM_000312.4(PROC):c.629C>T (p.Pro210Leu) (PROC)
**Verdict:** evidence summary (not a clinical classification)
**Calibrated P(pathogenic):** 0.493

## Evidence (every claim cited)
- [AlphaMissense] score=0.126 class=likely_benign <AM:2:127426178:C>T>
- [ClinVar (frozen 2024-01)] status then: Conflicting interpretations of pathogenicity <CLINVAR:allele15700>
- [Gene prior (frozen train)] gene=PROC <GENEPRIOR:PROC:frozen2024>

*(future truth, evaluation only: label=1, now 'Pathogenic/Likely pathogenic')*

# NM_000404.4(GLB1):c.601C>T (p.Arg201Cys) (GLB1)
**Verdict:** evidence summary (not a clinical classification)
**Calibrated P(pathogenic):** 0.493

## Evidence (every claim cited)
- [AlphaMissense] score=0.134 class=likely_benign <AM:3:33058221:G>A>
- [ClinVar (frozen 2024-01)] status then: Conflicting interpretations of pathogenicity <CLINVAR:allele15964>
- [Gene prior (frozen train)] gene=GLB1 <GENEPRIOR:GLB1:frozen2024>

*(future truth, evaluation only: label=1, now 'Pathogenic/Likely pathogenic')*

## Declines (adversarial by construction: evidence removed / absent)

# NM_000274.4(OAT):c.192_193del (p.Gly65fs) (OAT)
**Verdict:** insufficient evidence — remains VUS

## Evidence (every claim cited)
- [ClinVar (frozen 2024-01)] status then: Conflicting interpretations of pathogenicity <CLINVAR:allele15217>

# NM_004628.5(XPC):c.566_567del (p.Tyr189fs) (XPC)
**Verdict:** insufficient evidence — remains VUS

## Evidence (every claim cited)
- [ClinVar (frozen 2024-01)] status then: Conflicting interpretations of pathogenicity <CLINVAR:allele15297>

# NM_015272.5(RPGRIP1L):c.697A>T (p.Lys233Ter) (RPGRIP1L)
**Verdict:** insufficient evidence — remains VUS

## Evidence (every claim cited)
- [ClinVar (frozen 2024-01)] status then: Conflicting interpretations of pathogenicity <CLINVAR:allele16107>
