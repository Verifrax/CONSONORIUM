import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "cli" / "consonorium.py"
REPORT = ROOT / "reports" / "generated" / "sovereign-audit-report.json"


class AuditReportTest(unittest.TestCase):
    def test_report_matches_cli_output(self):
        expected = json.loads(REPORT.read_text(encoding="utf-8"))
        actual = json.loads(
            subprocess.check_output([sys.executable, str(CLI), "audit"], text=True)
        )
        self.assertEqual(actual, expected)

    def test_report_shape(self):
        payload = json.loads(REPORT.read_text(encoding="utf-8"))
        self.assertIsInstance(payload, dict)
        self.assertEqual(payload["mode"], "audit")


if __name__ == "__main__":
    unittest.main()
