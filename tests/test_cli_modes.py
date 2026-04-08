import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "cli" / "consonorium.py"


class TestCliModes(unittest.TestCase):
    def test_audit_mode_is_deterministic(self):
        a = subprocess.check_output([sys.executable, str(CLI), "audit"], text=True)
        b = subprocess.check_output([sys.executable, str(CLI), "audit"], text=True)

        self.assertEqual(a, b)

        data = json.loads(a)
        self.assertEqual(data["mode"], "audit")
        self.assertIn("digest", data)


if __name__ == "__main__":
    unittest.main()
