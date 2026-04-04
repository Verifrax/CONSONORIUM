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
REPORT = ROOT / "reports" / "generated" / "sovereign-epoch-candidate.json"

class EpochCandidateTest(unittest.TestCase):
    def test_report_matches_cli_output(self) -> None:
        actual = subprocess.check_output(["python3", str(CLI), "publish-epoch-candidate"], text=True)
        expected = REPORT.read_text(encoding="utf-8")
        self.assertEqual(actual, expected)

    def test_report_shape(self) -> None:
        payload = json.loads(REPORT.read_text(encoding="utf-8"))
        self.assertEqual(payload["mode"], "publish-epoch-candidate")
        self.assertEqual(payload["classification"], "runtime")
        self.assertEqual(payload["status"], "candidate")
        self.assertEqual(payload["candidate_id"], "sovereign-epoch-candidate")
        self.assertEqual(payload["repository_count"], REPO_COUNT)
        self.assertEqual(payload["edge_count"], EDGE_COUNT)
        self.assertEqual(len(payload["proposed_graph"]["repositories"]), REPO_COUNT)
        self.assertEqual(len(payload["proposed_graph"]["edges"]), EDGE_COUNT)

if __name__ == "__main__":
    unittest.main()
