from __future__ import annotations
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "cli" / "consonorium.py"
REPORT = ROOT / "reports" / "generated" / "sovereign-audit-report.json"

class AuditReportTest(unittest.TestCase):
    def test_report_matches_cli_output(self) -> None:
        actual = subprocess.check_output(["python3", str(CLI), "audit"], text=True)
        expected = REPORT.read_text(encoding="utf-8")
        self.assertEqual(actual, expected)

    def test_report_shape(self) -> None:
        payload = json.loads(REPORT.read_text(encoding="utf-8"))
        self.assertEqual(payload["mode"], "audit")
        self.assertEqual(payload["classification"], "runtime")
        self.assertEqual(payload["status"], "candidate")
        self.assertEqual(payload["finding_count"], 3)
        self.assertEqual(len(payload["findings"]), 3)
        for item in payload["findings"]:
            self.assertEqual(item["status"], "PASS")
            self.assertEqual(item["severity"], "none")

if __name__ == "__main__":
    unittest.main()
