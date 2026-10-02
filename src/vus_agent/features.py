"""Feature join for one variant. All fields optional — missing evidence
is a first-class signal for the agent's refusal path, not an error."""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class VariantFeatures:
    variant_id: str            # e.g. "BRCA1:c.5095C>T"
    gene: str
    alphamissense: Optional[float] = None      # 0..1, precomputed missense only
    revel: Optional[float] = None              # dbNSFP panel
    cadd_phred: Optional[float] = None
    gnomad_af: Optional[float] = None          # population allele frequency
    gene_constraint_pli: Optional[float] = None
    clinvar_submissions: list = field(default_factory=list)  # retrieved records

    def evidence_count(self) -> int:
        vals = [self.alphamissense, self.revel, self.cadd_phred,
                self.gnomad_af, self.gene_constraint_pli]
        return sum(v is not None for v in vals) + len(self.clinvar_submissions)
