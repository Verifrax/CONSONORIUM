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
REPORT = ROOT / "reports" / "generated" / "sovereign-check-report.json"

class CheckReportTest(unittest.TestCase):
    def test_report_matches_cli_output(self) -> None:
        actual = subprocess.check_output(["python3", str(CLI), "publish-checks"], text=True)
        expected = REPORT.read_text(encoding="utf-8")
        self.assertEqual(actual, expected)

    def test_report_shape(self) -> None:
        payload = json.loads(REPORT.read_text(encoding="utf-8"))
        self.assertEqual(payload["mode"], "publish-checks")
        self.assertEqual(payload["classification"], "runtime")
        self.assertEqual(payload["status"], "candidate")
        self.assertEqual(payload["check_count"], REPO_COUNT)
        self.assertEqual(len(payload["checks"]), REPO_COUNT)
        for item in payload["checks"]:
            self.assertEqual(item["status"], "PASS")
            self.assertEqual(item["severity"], "none")

if __name__ == "__main__":
    unittest.main()
