import importlib.util
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("rea_ai",root/"orchestrator.py")
m=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=m
spec.loader.exec_module(m)
def sample():
    return {"evidence_id":"example","normalized_result":{"statistics":{"parsed_javascript_files":2,"parse_failures":0},
    "graph":{"nodes":[{"observations":[{"properties":{"path":"index.js"}}]},
                      {"observations":[{"properties":{"path":"passage.js"}}]}],
             "edges":[{"relation":"imports","properties":{"specifier":"./passage.js","resolution_status":"resolved"}}]}}}
class Verify(unittest.TestCase):
    def test_graph(self): self.assertEqual(m.examine(sample())["parsed_files"],2)
    def test_fails_missing_import(self):
        x=sample();x["normalized_result"]["graph"]["edges"]=[]
        with self.assertRaises(ValueError):m.examine(x)
    def test_fails_missing_id(self):
        x=sample();del x["evidence_id"]
        with self.assertRaises(ValueError):m.examine(x)
    def test_html_demo(self): m.verify_html((root/"demo.html").read_text())
    def test_html_disallows_remote_code(self):
        x=(root/"demo.html").read_text().replace("render();", "fetch('https://example.com');render();")
        with self.assertRaises(ValueError):m.verify_html(x)
    def test_html_disallows_bad_syntax(self):
        x=(root/"demo.html").read_text().replace("render();","const = broken;render();")
        with self.assertRaises(ValueError):m.verify_html(x)
    def test_no_ack_no_api(self):
        with patch.object(m.urllib.request,"urlopen") as fn:
            with self.assertRaises(PermissionError):m.ask_gemini({},m.MODEL,"dummy","")
            fn.assert_not_called()
    def test_other_model_no_api(self):
        with patch.object(m.urllib.request,"urlopen") as fn:
            with self.assertRaises(PermissionError):m.ask_gemini({},"paid-model","dummy",m.ACK)
            fn.assert_not_called()
    def test_no_key_no_api(self):
        with patch.object(m.urllib.request,"urlopen") as fn:
            with self.assertRaises(PermissionError):m.ask_gemini({},m.MODEL,"",m.ACK)
            fn.assert_not_called()
if __name__=="__main__":unittest.main()
