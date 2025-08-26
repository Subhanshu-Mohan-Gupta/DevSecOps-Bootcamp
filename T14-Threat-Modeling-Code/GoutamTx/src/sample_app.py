# Sample app with inline ThreatSpec annotations
# STRIDE examples included in comments.

# @component SampleApp:Web
# @component SampleApp:API
# @component SampleApp:DB

# Data flows:
# @connects SampleApp:Web to SampleApp:API with HTTPS
# @connects SampleApp:API to SampleApp:DB with SQL

# Mitigated threat:
# @threat SQL Injection (#sqli)
# @control Parameterized Queries (#param)
# @mitigates SampleApp:API against SQL Injection with Parameterized Queries
# @severity high

# Unmitigated critical (will make gate fail if baseline not updated):
"""
@exposes SampleApp:API to Authentication Bypass (#auth_bypass):
  description: Missing JWT validation on admin endpoints
  impact: critical
  stride: Spoofing
"""

def handler(event, context):
    # intentionally insecure sample
    return {"status": "ok"}

