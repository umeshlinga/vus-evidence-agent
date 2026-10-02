// Week 3.5 stub — wraps the evidence agent so the repo runs like a lab pipeline would.
params.variant = null
process ASSESS_VARIANT {
  input: val variant_id
  output: stdout
  script: "PYTHONPATH=src python3 -m vus_agent.demo"
}
workflow { if (!params.variant) { log.info "vus-evidence-agent: demo mode (see README)" } }
