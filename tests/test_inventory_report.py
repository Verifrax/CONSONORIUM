import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "cli" / "consonorium.py"
REPORT = ROOT / "reports" / "generated" / "sovereign-inventory-report.json"


class InventoryReportTest(unittest.TestCase):
    def test_report_matches_cli_output(self):
        expected = json.loads(REPORT.read_text(encoding="utf-8"))
        actual = json.loads(
            subprocess.check_output([sys.executable, str(CLI), "inventory"], text=True)
        )
        self.assertEqual(actual, expected)

    def test_report_shape(self):
        payload = json.loads(REPORT.read_text(encoding="utf-8"))

        self.assertEqual(payload["mode"], "inventory")
        self.assertEqual(payload["law_source"], "../SYNTAGMARIUM")
        self.assertEqual(payload["previous_state_source"], "../ORBISTIUM/current")
        self.assertEqual(payload["contradictions"], [])
        self.assertEqual(payload["quarantines"], [])
        self.assertEqual(payload["repairs"], [])

        self.assertIn("digest", payload)
        self.assertTrue(payload["digest"].startswith("sha256:"))

        self.assertIn("observed", payload)
        self.assertEqual(
            sorted(payload["observed"].keys()),
            ["artifacts", "hosts", "packages", "repos"],
        )

        repos = payload["observed"]["repos"]
        self.assertEqual(len(repos), 3)
        self.assertEqual(
            {repo["repo_id"] for repo in repos},
            {"SYNTAGMARIUM", "ORBISTIUM", "CONSONORIUM"},
        )
        self.assertEqual(
            {repo["primary_role"] for repo in repos},
            {"constitutional_law", "world_state", "reconciler"},
        )


if __name__ == "__main__":
    unittest.main()
