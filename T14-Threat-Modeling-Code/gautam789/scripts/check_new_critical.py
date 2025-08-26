import json, sys, os

THREATS = 'threatmodel/threats.json'
BASE = 'threatmodel/baseline_critical.json'

if not os.path.exists(THREATS):
    print('❌ threats.json not found. Run `threatspec run` first.')
    sys.exit(2)

with open(THREATS) as f:
    threats_data = json.load(f)
with open(BASE) as f:
    baseline = json.load(f)

accepted = set(map(str.lower, baseline.get('accepted_critical_ids', [])))
critical_ids = set()

# Iterate over dict values
for t in threats_data.get('threats', {}).values():
    ident = (t.get('identifier') or t.get('id') or t.get('name') or '').strip().lower()
    # If you have severity stored elsewhere (ThreatSpec by default doesn't add severity), default to 'critical'
    sev = (t.get('severity') or t.get('data', {}).get('severity') or 'critical').strip().lower()

    if sev == 'critical' and ident:
        if not ident.startswith('#'):
            ident = f'#{ident}'
        critical_ids.add(ident)

new_crit = sorted([c for c in critical_ids if c not in accepted])
if new_crit:
    print('❌ New critical threats detected:')
    for c in new_crit:
        print(' -', c)
    sys.exit(1)

print('✅ No new critical threats beyond the baseline.')

