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

REPORT = ROOT / "reports" / "generated" / "sovereign-mechanical-repair-application.json"

class ApplyMechanicalRepairsTest(unittest.TestCase):
    def test_report_matches_cli_output(self) -> None:
        actual = subprocess.check_output(["python3", str(CLI), "apply-mechanical-repairs"], text=True)
        expected = REPORT.read_text(encoding="utf-8")
        self.assertEqual(actual, expected)

    def test_report_shape(self) -> None:
        payload = json.loads(REPORT.read_text(encoding="utf-8"))
        self.assertEqual(payload["mode"], "apply-mechanical-repairs")
        self.assertEqual(payload["classification"], "runtime")
        self.assertEqual(payload["status"], "candidate")
        self.assertEqual(payload["applied_count"], 0)
        self.assertEqual(payload["applied_repairs"], [])
        self.assertEqual(payload["reviewed_object_count"], NODE_COUNT)
        self.assertEqual(len(payload["reviewed_objects"]), NODE_COUNT)

if __name__ == "__main__":
    unittest.main()
