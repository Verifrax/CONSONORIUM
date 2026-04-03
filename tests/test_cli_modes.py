from __future__ import annotations
import json, subprocess, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "cli" / "consonorium.py"
MODES = ["inventory","audit","reconcile","plan-repairs","apply-mechanical-repairs","publish-checks","publish-epoch-candidate","quarantine","project"]
class CLITest(unittest.TestCase):
    def test_inventory_fixture(self) -> None:
        actual = subprocess.check_output(["python3", str(CLI), "inventory"], text=True)
        expected = (ROOT / "fixtures" / "cli" / "inventory.expected.json").read_text(encoding="utf-8")
        self.assertEqual(actual, expected)
    def test_mode_shape(self) -> None:
        for mode in MODES:
            with self.subTest(mode=mode):
                data = json.loads(subprocess.check_output(["python3", str(CLI), mode], text=True))
                self.assertEqual(data["program"], "consonorium")
                self.assertEqual(data["classification"], "runtime")
                self.assertEqual(data["law_source"], "SYNTAGMARIUM")
                self.assertEqual(data["accepted_state_store"], "ORBISTIUM")
                self.assertTrue(data["deterministic_surface"])
                self.assertEqual(data["mode"], mode)
if __name__ == "__main__":
    unittest.main()
