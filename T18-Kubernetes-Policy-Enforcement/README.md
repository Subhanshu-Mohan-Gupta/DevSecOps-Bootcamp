# Kubernetes Policy‑as‑Code

## Objective
Implement advanced security controls and automation for **Kubernetes Policy‑as‑Code**.

## Tools & Setup
Kyverno

## Steps
1. Install Kyverno in the cluster.
2. Add policy to disallow privileged containers and require read‑only root filesystems.
3. Run `kubectl apply -f policies/` as part of CI test deployment.
4. Block non‑compliant manifests automatically.

## Deliverables
- CI pipeline demonstrating all steps
- Evidence logs or screenshots
- Summary report
