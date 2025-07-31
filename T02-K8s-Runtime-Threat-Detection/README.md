# Task 2: Runtime Threat Detection in Kubernetes

## Objective
Deploy Falco or Tracee to detect anomalous system calls and runtime behaviors within Kubernetes.

## Tools & Setup
- Kubernetes
- Falco or eBPF-based Tracee
- Slack or Alertmanager for notifications

## Steps
1. Deploy security agents using Helm or DaemonSets.
2. Define rules to detect events like `kubectl exec`, unexpected networking.
3. Forward events to alerting platform.
4. Validate alerting pipeline with test anomalies.

## Deliverables
- Rule configurations
- Alerts triggered by anomaly simulation
- Screenshot or logs from Slack/Alertmanager
