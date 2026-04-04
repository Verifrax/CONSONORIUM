from __future__ import annotations
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "cli" / "consonorium.py"
FIXTURE = json.loads((ROOT / "fixtures" / "sovereign" / "inventory.json").read_text(encoding="utf-8"))
EXPECTED = ROOT / "fixtures" / "cli" / "inventory.expected.json"

class CLITest(unittest.TestCase):
    def test_inventory_fixture_matches(self) -> None:
        actual = subprocess.check_output(["python3", str(CLI), "inventory"], text=True)
        expected = EXPECTED.read_text(encoding="utf-8")
        self.assertEqual(actual, expected)

    def test_inventory_contains_live_repo_census(self) -> None:
        payload = json.loads(subprocess.check_output(["python3", str(CLI), "inventory"], text=True))
        self.assertEqual(payload["mode"], "inventory")
        self.assertEqual(payload["classification"], "runtime")
        self.assertEqual(payload["repository_count"], len(FIXTURE["repositories"]))
        self.assertEqual(payload["edge_count"], len(FIXTURE["edges"]))

        repo_ids = {repo["repo_id"] for repo in payload["repositories"]}
        self.assertIn("SYNTAGMARIUM", repo_ids)
        self.assertIn("ORBISTIUM", repo_ids)
        self.assertIn("CONSONORIUM", repo_ids)

    def test_modes_emit_valid_payloads(self) -> None:
        modes = [
            "inventory",
            "audit",
            "reconcile",
            "plan-repairs",
            "apply-mechanical-repairs",
            "publish-checks",
            "publish-epoch-candidate",
            "quarantine",
            "project",
        ]
        for mode in modes:
            with self.subTest(mode=mode):
                payload = json.loads(subprocess.check_output(["python3", str(CLI), mode], text=True))
                self.assertEqual(payload["program"], "consonorium")
                self.assertEqual(payload["classification"], "runtime")
                self.assertEqual(payload["law_source"], "SYNTAGMARIUM")
                self.assertEqual(payload["accepted_state_store"], "ORBISTIUM")
                self.assertTrue(payload["deterministic_surface"])
                self.assertEqual(payload["mode"], mode)

if __name__ == "__main__":
    unittest.main()
