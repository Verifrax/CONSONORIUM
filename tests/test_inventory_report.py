from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads((ROOT / "fixtures" / "sovereign" / "inventory.json").read_text(encoding="utf-8"))
REPO_COUNT = len(FIXTURE["repositories"])
EDGE_COUNT = len(FIXTURE["edges"])

import json
import subprocess
import unittest

CLI = ROOT / "cli" / "consonorium.py"
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
        self.assertEqual(payload["edge_count"], EDGE_COUNT)

if __name__ == "__main__":
    unittest.main()
