#!/usr/bin/env python3
# Generates diagrams/dfd.puml and diagrams/dfd.md from threatmodel/threatmodel.json
import json
from pathlib import Path

MODEL = Path("threatmodel/threatmodel.json")
DIAG_DIR = Path("diagrams")
DIAG_DIR.mkdir(parents=True, exist_ok=True)

def load_model():
    if MODEL.exists():
        return json.loads(MODEL.read_text(encoding="utf-8"))
    return {}

def extract_connections(model):
    conns = []
    # ThreatSpec typically emits connections under "connections" or within nodes.
    if isinstance(model, dict):
        for k in ("connections","connects"):
            if k in model and isinstance(model[k], list):
                for c in model[k]:
                    conns.append(c)
    # fallback: search for dicts with 'from' and 'to'
    def traverse(obj):
        if isinstance(obj, dict):
            if 'from' in obj and 'to' in obj:
                conns.append(obj)
            for v in obj.values():
                traverse(v)
        elif isinstance(obj, list):
            for it in obj:
                traverse(it)
    traverse(model)
    return conns

model = load_model()
conns = extract_connections(model)
if not conns:
    # fallback sample
    conns = [
        {"from":"SampleApp:Web","to":"SampleApp:API","with":"HTTPS"},
        {"from":"SampleApp:API","to":"SampleApp:DB","with":"SQL"}
    ]

# Build set of components and edges
components = set()
edges = []
for c in conns:
    s = c.get("from") or c.get("src") or c.get("source")
    d = c.get("to") or c.get("dst") or c.get("dest")
    lbl = c.get("with") or c.get("via") or ""
    if s and d:
        components.add(s); components.add(d)
        edges.append((s,d,lbl))

# PlantUML
puml_lines = ["@startuml", "skinparam dpi 150", "title Data Flow Diagram"]
alias = {}
for i, c in enumerate(sorted(components)):
    a = f"C{i}"
    alias[c] = a
    puml_lines.append(f'rectangle "{c}" as {a}')
for s,d,lbl in edges:
    line = f"{alias[s]} --> {alias[d]}"
    if lbl:
        line += f" : {lbl}"
    puml_lines.append(line)
puml_lines.append("@enduml")
(Path("diagrams/dfd.puml")).write_text("\n".join(puml_lines), encoding="utf-8")

# Mermaid markdown
merm = ["```mermaid", "flowchart LR"]
for s,d,lbl in edges:
    ms = s.replace(":", "_").replace(" ", "_")
    md = d.replace(":", "_").replace(" ", "_")
    lab = f'|"{lbl}"|' if lbl else ""
    merm.append(f'  {ms}["{s}"] -->{lab} {md}["{d}"]')
merm.append("```")
(Path("diagrams/dfd.md")).write_text("\n".join(merm), encoding="utf-8")

print("diagrams/dfd.puml and diagrams/dfd.md written")

