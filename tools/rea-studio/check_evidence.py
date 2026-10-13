"""Validate REA's JSON evidence shape without claiming application parity."""
import json
import sys
from pathlib import Path

if len(sys.argv) != 3:
    raise SystemExit("usage: check_evidence.py EVIDENCE_JSON SUMMARY_JSON")

source, destination = map(Path, sys.argv[1:])
if not source.is_file() or source.stat().st_size == 0:
    raise SystemExit("REA produced no evidence")
with source.open(encoding="utf-8") as stream:
    data = json.load(stream)
if not isinstance(data, dict):
    raise SystemExit("REA returned a non-object JSON result")
if data.get("status") in ("error", "failed") or data.get("isError") is True:
    raise SystemExit("REA returned an error result")
summary = {
    "result_type": type(data).__name__,
    "keys": list(data)[:40],
    "bytes": source.stat().st_size,
    "note": "JSON validity and shape only; not proof of behavioral parity.",
}
destination.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False))
