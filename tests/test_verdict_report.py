import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "generated" / "sovereign-verdict-report.json"

class VerdictReportTest(unittest.TestCase):
    def test_report_loads(self):
        payload = json.loads(REPORT.read_text(encoding="utf-8"))
        self.assertEqual(payload["mode"], "publish-verdict")
        self.assertEqual(payload["verdict_count"], len(payload["verdicts"]))

    def test_report_shape(self):
        payload = json.loads(REPORT.read_text(encoding="utf-8"))
        item = payload["verdicts"][0]
        self.assertEqual(
            sorted(item.keys()),
            [
                "contradictions",
                "execution_ref",
                "law_ref",
                "proof_ref",
                "reason_codes",
                "state_ref",
                "verdict",
                "verdict_id",
                "verifier_version",
            ],
        )

if __name__ == "__main__":
    unittest.main()
