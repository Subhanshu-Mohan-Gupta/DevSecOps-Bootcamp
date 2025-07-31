# End-to-End Secrets Management & Rotation

## Objective
Implement automated secrets storage and rotation using Vault, and inject secrets at runtime.

## Tools & Setup
- HashiCorp Vault or AWS Secrets Manager
- Kubernetes CSI or Vault Agent Injector
- CronJob or Lambda for rotation

## Steps
1. Setup Vault and enable dynamic secrets.
2. Inject secrets using CSI driver or agent.
3. Implement script to rotate DB credentials.
4. Validate service remains available after rotation.

## Deliverables
- Vault role/config definitions
- Rotation script
- Logs showing credential update and reload
