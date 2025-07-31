# Task 6: Chaos‑Driven Security Testing

## Objective
Simulate security faults in a safe environment to test detection, alerting, and remediation automation.

## Tools & Setup
- Chaos Toolkit or LitmusChaos
- Kubernetes
- SIEM/Alertmanager for validation

## Steps
1. Write chaos experiments to simulate token revocation, network blackholes, pod compromise.
2. Inject faults and observe alerts/logs.
3. Validate automatic remediation (e.g., pod restart).
4. Generate summary report of pass/fail.

## Deliverables
- Chaos experiment definitions
- SIEM/alert output
- Post-mortem report with success/fail analysis
