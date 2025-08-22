import json, pathlib
m = json.load(open('threatmodel/threatmodel.json'))
components = {c['name'] for c in m.get('components', [])}
edges = [(c['from'], c['to'], c.get('description','')) for c in m.get('connects', [])]

lines = ["flowchart LR"]
for name in sorted(components):
    nid = name.replace(':','_').replace(' ','_')
    lines.append(f'    {nid}["{name}"]')
for f,t,d in edges:
    fid = f.replace(':','_').replace(' ','_')
    tid = t.replace(':','_').replace(' ','_')
    label = d.replace('"','\\"') if d else ''
    lines.append(f'    {fid} -->|"{label}"| {tid}')

out = pathlib.Path('diagrams'); out.mkdir(exist_ok=True)
(out/'dfd.mmd').write_text('\n'.join(lines), encoding='utf-8')
print('Wrote diagrams/dfd.mmd')

