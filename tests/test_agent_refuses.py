"""Adversarial tests: the agent must decline, never invent.

These are the tests that make the repo credible to a hiring manager:
fabricated citations and missing records produce a refusal, not prose.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from vus_agent.agent import MIN_EVIDENCE, assess
from vus_agent.features import VariantFeatures


def test_thin_evidence_declines():
    f = VariantFeatures("TTN:c.12345A>G", "TTN", alphamissense=0.41)
    r = assess(f, calibrated_prob=0.9)  # confident model, no evidence base
    assert r["verdict"].startswith("insufficient evidence")
    assert r["calibrated_prob_pathogenic"] is None


def test_no_model_score_declines():
    f = VariantFeatures("BRCA1:c.5095C>T", "BRCA1", alphamissense=0.9, revel=0.9,
                        cadd_phred=25.0, gnomad_af=0.0)
    r = assess(f, calibrated_prob=None)
    assert r["verdict"].startswith("insufficient evidence")


def test_full_evidence_is_cited():
    f = VariantFeatures("BRCA1:c.5095C>T", "BRCA1", alphamissense=0.94, revel=0.91,
                        cadd_phred=28.0, gnomad_af=0.0, gene_constraint_pli=0.99)
    r = assess(f, calibrated_prob=0.87)
    assert len(r["citations"]) >= MIN_EVIDENCE
    assert all("<" in e and ">" in e for e in r["evidence"])  # every claim cited


if __name__ == "__main__":
    test_thin_evidence_declines(); test_no_model_score_declines(); test_full_evidence_is_cited()
    print("all refusal/citation tests passed")
