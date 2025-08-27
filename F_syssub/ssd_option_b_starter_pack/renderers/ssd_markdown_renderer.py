import json, sys, pathlib

def render_field(f):
    unit = f.get("unit")
    unit_str = f" ({unit})" if unit else ""
    return f"- **{f['name']}**{unit_str}: {json.dumps(f['value'], ensure_ascii=False)} (conf={f.get('confidence',1.0):.2f})"

def main(path):
    data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    lines = []
    meta = data.get("meta", {})
    lines.append(f"# SSD — {meta.get('system_name','Unknown')} v{meta.get('version','?')}")
    lines.append("")
    lines.append(f"- Doc ID: {meta.get('doc_id','')}")
    lines.append(f"- Created: {meta.get('created_at','')}")
    lines.append("")
    for sec in sorted(data.get("sections", {}).keys(), key=lambda s: [int(x) for x in s.split('.')]):
        sec_obj = data["sections"][sec]
        lines.append(f"## Section {sec} — {sec_obj.get('title','')}")
        for f in sec_obj.get("fields", []):
            lines.append(render_field(f))
        lines.append("")
    print("\n".join(lines))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ssd_markdown_renderer.py SSD.json")
        sys.exit(1)
    main(sys.argv[1])
