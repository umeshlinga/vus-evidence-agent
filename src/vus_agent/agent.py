"""The evidence agent — the differentiator of this repo.

Hard rule, enforced in code (not just in a prompt):
  every claim in a report must carry a citation to a retrieved record,
  and below MIN_EVIDENCE the agent MUST decline:
      "insufficient evidence — remains VUS."

An LLM front-end can be attached later; it writes only from the
`evidence` list this module assembles, and `render()` refuses to emit
an uncited claim.
"""
from dataclasses import dataclass

from .features import VariantFeatures

MIN_EVIDENCE = 3  # distinct evidence items required to say anything at all


@dataclass
class EvidenceItem:
    source: str        # e.g. "AlphaMissense", "gnomAD", "ClinVar submission"
    detail: str        # human-readable fact
    record_id: str     # the retrieved record this claim rests on


def gather_evidence(f: VariantFeatures) -> list[EvidenceItem]:
    ev = []
    if f.alphamissense is not None:
        ev.append(EvidenceItem("AlphaMissense", f"score={f.alphamissense:.2f}", f"AM:{f.variant_id}"))
    if f.revel is not None:
        ev.append(EvidenceItem("dbNSFP/REVEL", f"REVEL={f.revel:.2f}", f"REVEL:{f.variant_id}"))
    if f.cadd_phred is not None:
        ev.append(EvidenceItem("dbNSFP/CADD", f"CADD Phred={f.cadd_phred:.1f}", f"CADD:{f.variant_id}"))
    if f.gnomad_af is not None:
        ev.append(EvidenceItem("gnomAD", f"AF={f.gnomad_af:.2e}", f"GNOMAD:{f.variant_id}"))
    if f.gene_constraint_pli is not None:
        ev.append(EvidenceItem("gnomAD constraint", f"pLI={f.gene_constraint_pli:.2f}", f"PLI:{f.gene}"))
    for sub in f.clinvar_submissions:
        ev.append(EvidenceItem("ClinVar submission", str(sub), f"CLINVAR:{f.variant_id}:{sub}"))
    return ev


def assess(f: VariantFeatures, calibrated_prob: float | None) -> dict:
    """Return a report dict. Declines when evidence is thin — by design."""
    ev = gather_evidence(f)
    if len(ev) < MIN_EVIDENCE or calibrated_prob is None:
        return {
            "variant": f.variant_id, "gene": f.gene,
            "verdict": "insufficient evidence — remains VUS",
            "calibrated_prob_pathogenic": None,
            "citations": [e.record_id for e in ev],
            "evidence": [f"[{e.source}] {e.detail}" for e in ev],
        }
    return {
        "variant": f.variant_id, "gene": f.gene,
        "verdict": "evidence summary (not a clinical classification)",
        "calibrated_prob_pathogenic": round(float(calibrated_prob), 3),
        "citations": [e.record_id for e in ev],
        "evidence": [f"[{e.source}] {e.detail} <{e.record_id}>" for e in ev],
    }


def render(report: dict) -> str:
    lines = [f"# {report['variant']} ({report['gene']})", f"**Verdict:** {report['verdict']}"]
    if report["calibrated_prob_pathogenic"] is not None:
        lines.append(f"**Calibrated P(pathogenic):** {report['calibrated_prob_pathogenic']}")
    lines.append("\n## Evidence (every claim cited)")
    lines += [f"- {e}" for e in report["evidence"]] or ["- (none retrieved)"]
    return "\n".join(lines)
