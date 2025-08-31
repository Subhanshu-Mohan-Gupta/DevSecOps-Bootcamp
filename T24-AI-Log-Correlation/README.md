# T24 – AI-Driven Log Correlation & Threat Hunting

## 🎯 Objective
Aggregate Falco, CloudTrail, and Nginx logs; detect anomalies with AI.

## 🛠️ Deliverables
- Collect logs into `logs/`.
- Write Python analyzer that uses OpenAI API.
- CI job processes sample logs and outputs anomalies.
- Document correlation pipeline.

## 🚀 Steps
1. Place logs under `logs/falco/`, `logs/cloudtrail/`, `logs/nginx/`.
2. Implement `scripts/analyze_logs.py` to read JSON logs.
3. Call OpenAI API (model configurable) for anomaly detection.
4. CI runs script against sample logs.

## ✅ Validation
- Analyzer outputs anomalies summary.
- CI passes with valid JSON output.
