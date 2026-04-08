import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "cli" / "consonorium.py"

def test_modes_are_deterministic():
    a = subprocess.check_output([str(CLI), "audit"], text=True)
    b = subprocess.check_output([str(CLI), "audit"], text=True)
    assert a == b
    data = json.loads(a)
    assert data["mode"] == "audit"
    assert "digest" in data
