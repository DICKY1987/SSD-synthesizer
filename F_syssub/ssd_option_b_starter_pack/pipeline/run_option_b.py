#!/usr/bin/env python3
"""Option B Orchestrator (stub): multi-pass, quality-gated SSD builder.
This script demonstrates the stages and expected file IO. Replace TODOs with your LLM calls.
"""
import json, sys, pathlib, time, hashlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)

def sha256_text(t: str) -> str:
    return hashlib.sha256(t.encode("utf-8")).hexdigest()

def ingest_sources(cfg):
    corpus = []
    for i, src in enumerate(cfg.get("sources", []), start=1):
        p = pathlib.Path(src["path"])
        text = p.read_text(encoding="utf-8", errors="ignore")
        corpus.append({
            "id": f"SRC-{i:04d}",
            "uri": str(p),
            "kind": src.get("kind","doc"),
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
            "sha256": sha256_text(text),
            "text": text
        })
    return corpus

def chunk_text(text, max_len=1800):
    # naive chunker by paragraphs
    parts, buf = [], []
    for line in text.splitlines():
        buf.append(line)
        if sum(len(b)+1 for b in buf) > max_len:
            parts.append("\n".join(buf)); buf=[]
    if buf: parts.append("\n".join(buf))
    return parts

def classify_chunks(corpus, routing_rules):
    # naive routing: keyword matching
    routed = []
    for src in corpus:
        chunks = chunk_text(src["text"])
        for idx, ch in enumerate(chunks):
            dest = None
            for rule in routing_rules:
                if any(k.lower() in ch.lower() for k in rule["match"]):
                    dest = rule["to_section"]; break
            if dest:
                routed.append({"section": dest, "source_id": src["id"], "locator": f"{src['uri']}#chunk{idx}", "text": ch})
    return routed

def extract_fields(routed):
    # TODO: replace with LLM extractors. We emit placeholder fields with low confidence.
    fields_by_section = {}
    for r in routed:
        fields_by_section.setdefault(r["section"], []).append({
            "id": f"{r['section']}.auto_field_{hash(r['text'])%10000}",
            "name": "AUTO-EXTRACTED",
            "value": r["text"][:120] + ("..." if len(r["text"])>120 else ""),
            "confidence": 0.55,
            "evidence": [{ "source_id": r["source_id"], "locator": r["locator"], "snippet_hash": hashlib.sha256(r["text"][:200].encode()).hexdigest(), "excerpt": r["text"][:200] }]
        })
    return fields_by_section

def build_ssd(meta, fields_by_section, routing_rules):
    ssd = {"meta": meta, "sections": {}}
    for sec, fields in fields_by_section.items():
        ssd["sections"][sec] = {"title": "", "fields": fields}
    return ssd

def validate_coverage(ssd, required_sections):
    present = sum(1 for s in required_sections if s in ssd["sections"])
    return present / max(1, len(required_sections))

def median_conf(ssd):
    vals=[]
    for s in ssd["sections"].values():
        for f in s["fields"]:
            vals.append(f.get("confidence", 1.0))
    vals.sort()
    return vals[len(vals)//2] if vals else 0.0

def main():
    cfg_path = ROOT / "pipeline" / "config.yaml"
    if not cfg_path.exists():
        print("Missing pipeline/config.yaml"); sys.exit(1)
    import yaml
    cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
    routing_rules = yaml.safe_load((ROOT / "routing" / "routing_rules.yaml").read_text(encoding="utf-8"))
    required = yaml.safe_load((ROOT / "validators" / "coverage_rules.yaml").read_text(encoding="utf-8"))["required_sections"]

    corpus = ingest_sources(cfg)
    routed = classify_chunks(corpus, routing_rules)
    fields_by_section = extract_fields(routed)

    meta = {
        "system_name": cfg.get("system_name","Unknown"),
        "version": cfg.get("version","0.1.0"),
        "doc_id": cfg.get("doc_id","SSD-STUB"),
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "source_corpus": [{k:v for k,v in src.items() if k!='text'} for src in corpus]
    }
    ssd = build_ssd(meta, fields_by_section, routing_rules)

    ssd_json = OUT / "SSD.json"
    ssd_json.write_text(json.dumps(ssd, ensure_ascii=False, indent=2), encoding="utf-8")

    # Simple gate checks
    cov = validate_coverage(ssd, required)
    med = median_conf(ssd)
    report = f"""# Gap & Gate Report
- Coverage (required sections present): {cov:.2%}
- Median confidence: {med:.2f}
- Notes: Replace placeholder extractor with LLM section-specific extractors for quality gains.
"""
    (OUT / "gap_report.md").write_text(report, encoding="utf-8")

    # Render markdown view
    import subprocess, sys
    subprocess.run([sys.executable, str(ROOT / "renderers" / "ssd_markdown_renderer.py"), str(ssd_json)], check=False, stdout=(OUT / "SSD.md").open("w", encoding="utf-8"))

    print("Done. See 'out/SSD.json', 'out/SSD.md', and 'out/gap_report.md'.")

if __name__ == "__main__":
    main()
