# Extractor: Generic Section
## Behavior
- Map free text to canonical fields using best-effort key-value extraction.
- Return nulls rather than hallucinating.
## Output Envelope
{
  "fields": [ { "name":"", "value":any, "unit": "string|null" } ],
  "_confidence": 0.0..1.0,
  "_evidence": [{ "source_id":"", "locator":"", "excerpt":"" }]
}
