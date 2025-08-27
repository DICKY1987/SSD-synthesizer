# Option B (Enterprise Loop) — Starter Pack

## What this gives you
- **Machine-readable SSD schema** (`schema/ssd.schema.yaml`)
- **Deterministic routing rules** (`routing/routing_rules.yaml`)
- **Section-specific extractor prompts** (`extractors/`)
- **Quality gates & validators** (`validators/`)
- **Renderer** to Markdown (`renderers/ssd_markdown_renderer.py`)
- **Pipeline orchestrator (stub)** (`pipeline/run_option_b.py`)
- **Templates** for SSD example, gap tickets, acceptance checklist

## Quick start
```bash
cd pipeline
python run_option_b.py
```
Outputs go to `out/`:
- `SSD.json` — the truth
- `SSD.md` — readable view
- `gap_report.md` — coverage & confidence summary

## Next steps
- Replace the stub extractor with calls to your LLM of choice using the prompts in `extractors/`.
- Tighten `validators/coverage_rules.yaml` to match your must-have sections.
- Expand `routing/routing_rules.yaml` over time as you see common patterns.
