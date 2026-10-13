"""Assert real REA static-analysis findings for a known, owned JavaScript fixture."""
import json
import sys
from pathlib import Path

if len(sys.argv) != 3:
    raise SystemExit("usage: check_evidence.py EVIDENCE_JSON SUMMARY_JSON")

source, destination = map(Path, sys.argv[1:])
with source.open(encoding="utf-8") as stream:
    data = json.load(stream)
if not isinstance(data, dict) or data.get("isError") is True:
    raise SystemExit("REA did not return a successful object-shaped Evidence record")
if not data.get("evidence_id"):
    raise SystemExit("REA returned no verifiable Evidence ID")
result = data.get("normalized_result")
if not isinstance(result, dict):
    raise SystemExit("REA Evidence contains no normalized_result")
stats = result.get("statistics")
graph = result.get("graph")
if not isinstance(stats, dict) or not isinstance(graph, dict):
    raise SystemExit("REA returned no application graph/statistics")
if stats.get("parsed_javascript_files", 0) < 2 or stats.get("parse_failures") != 0:
    raise SystemExit(f"JavaScript parse did not recover both sources: {stats}")
nodes = graph.get("nodes", [])
edges = graph.get("edges", [])
observed_paths = {
    obs.get("properties", {}).get("path")
    for node in nodes
    for obs in node.get("observations", [])
    if isinstance(obs, dict)
}
if not {"index.js", "math.js"}.issubset(observed_paths):
    raise SystemExit(f"Expected fixture JavaScript modules not recovered: {observed_paths}")
matched_imports = [
    e for e in edges
    if e.get("relation") == "imports"
    and e.get("properties", {}).get("specifier") == "./math.js"
    and e.get("properties", {}).get("resolution_status") == "resolved"
]
if not matched_imports:
    raise SystemExit("REA did not recover the known ./math.js import relationship")
summary = {
    "outcome": "passed",
    "evidence_id": data["evidence_id"],
    "evidence_bytes": source.stat().st_size,
    "parsed_javascript_files": stats["parsed_javascript_files"],
    "parse_failures": stats["parse_failures"],
    "findings": stats.get("findings"),
    "graph_nodes": len(nodes),
    "graph_edges": len(edges),
    "known_import_resolved": True,
    "note": "Verified fixture structural findings; not runtime or behavior parity.",
}
destination.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False))
