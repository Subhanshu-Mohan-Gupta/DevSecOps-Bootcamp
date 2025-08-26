import json, pathlib
m = json.load(open('threatmodel/threatmodel.json'))
components = {c['name'] for c in m.get('components', [])}
edges = [(c['from'], c['to'], c.get('description','')) for c in m.get('connects', [])]

lines = ["@startuml","skinparam shadowing false","skinparam defaultTextAlignment left"]
for name in sorted(components):
    cid = name.replace(':','_').replace(' ','_')
    lines.append(f'class {cid} as "{name}"')
for f,t,d in edges:
    fid = f.replace(':','_').replace(' ','_')
    tid = t.replace(':','_').replace(' ','_')
    label = d.replace('"','\\"') if d else ''
    lines.append(f'{fid} --> {tid} : {label}')
lines.append("@enduml")

out = pathlib.Path('diagrams'); out.mkdir(exist_ok=True)
(out/'dfd.puml').write_text('\n'.join(lines), encoding='utf-8')
print('Wrote diagrams/dfd.puml')

