from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "cli" / "consonorium.py"
FIXTURE = ROOT / "fixtures" / "sovereign" / "inventory.json"

MODES = [
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

class CLITest(unittest.TestCase):
    def run_mode(self, mode: str) -> dict:
        raw = subprocess.check_output(["python3", str(CLI), mode], text=True)
        return json.loads(raw)

    def test_inventory_fixture_matches(self) -> None:
        actual = subprocess.check_output(["python3", str(CLI), "inventory"], text=True)
        expected = (ROOT / "fixtures" / "cli" / "inventory.expected.json").read_text(encoding="utf-8")
        self.assertEqual(actual, expected)

    def test_inventory_contains_sovereign_layer(self) -> None:
        payload = self.run_mode("inventory")
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(payload["repository_count"], 3)
        self.assertEqual(payload["edge_count"], 3)
        self.assertEqual(payload["repositories"], fixture["repositories"])
        self.assertEqual(payload["edges"], fixture["edges"])

    def test_all_modes_have_expected_shape(self) -> None:
        for mode in MODES:
            with self.subTest(mode=mode):
                data = self.run_mode(mode)
                self.assertEqual(data["program"], "consonorium")
                self.assertEqual(data["classification"], "runtime")
                self.assertEqual(data["law_source"], "SYNTAGMARIUM")
                self.assertEqual(data["accepted_state_store"], "ORBISTIUM")
                self.assertTrue(data["deterministic_surface"])
                self.assertEqual(data["mode"], mode)

if __name__ == "__main__":
    unittest.main()
