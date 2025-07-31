# Secure Software Supply Chain

## Objective
Implement advanced security controls and automation for **Secure Software Supply Chain**.

## Tools & Setup
Cosign, SLSA, in-toto

## Steps
1. Enforce GPG‑signed commits in the repo settings.
2. Generate a Cosign keypair and store it in `cosign-keypair/`.
3. Sign container images in the CI pipeline.
4. Generate provenance attestation using in‑toto or SLSA metadata.
5. Verify signatures during deployment.

## Deliverables
- CI pipeline demonstrating all steps
- Evidence logs or screenshots
- Summary report
