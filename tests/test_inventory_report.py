from __future__ import annotations
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "cli" / "consonorium.py"
FIXTURE = json.loads((ROOT / "fixtures" / "sovereign" / "inventory.json").read_text(encoding="utf-8"))
REPO_COUNT = len(FIXTURE["repositories"])
NODE_COUNT = len(FIXTURE["nodes"])
EDGE_COUNT = len(FIXTURE["edges"])

REPORT = ROOT / "reports" / "generated" / "sovereign-inventory-report.json"

class InventoryReportTest(unittest.TestCase):
    def test_report_matches_cli_output(self) -> None:
        actual = subprocess.check_output(["python3", str(CLI), "inventory"], text=True)
        expected = REPORT.read_text(encoding="utf-8")
        self.assertEqual(actual, expected)

    def test_report_shape(self) -> None:
        payload = json.loads(REPORT.read_text(encoding="utf-8"))
        self.assertEqual(payload["mode"], "inventory")
        self.assertEqual(payload["classification"], "runtime")
        self.assertEqual(payload["repository_count"], REPO_COUNT)
        self.assertEqual(payload["node_count"], NODE_COUNT)
        self.assertEqual(payload["edge_count"], EDGE_COUNT)

if __name__ == "__main__":
    unittest.main()
