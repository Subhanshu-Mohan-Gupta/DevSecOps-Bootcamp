# T20 – Runtime Memory Exploit Detection with eBPF

## 🎯 Objective
Detect suspicious syscalls at runtime (e.g., `ptrace`, `setns`, `capset`) using eBPF tooling.

## 🛠️ Deliverables
- Write a minimal eBPF program (or Tracee rule) to capture suspicious syscalls.
- Package it into a Kubernetes DaemonSet for cluster-wide monitoring.
- Simulate an exploit attempt (container escape, ptrace attack).
- Export logs into ELK / Loki.

## 🚀 Steps
1. Implement eBPF program in `ebpf/` (C or Python via BCC).
2. Create Kubernetes manifests in `k8s/` to deploy as DaemonSet.
3. Add CI workflow to validate the YAML syntax and ensure program compiles.
4. Document how to simulate an attack and confirm logs are captured.

## ✅ Validation
- DaemonSet runs on K8s.
- Exploit attempt logs appear in stdout / file.
- CI workflow passes checks.
