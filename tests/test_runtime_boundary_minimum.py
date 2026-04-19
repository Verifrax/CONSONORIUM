from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def test_runtime_boundary_minimum_surface_present():
    required = [
        "README.md",
        "RUNTIME.md",
        "VERSION",
        "tests/test_runtime_boundary_minimum.py",
        "tests/verify_runtime_boundary_minimum.py",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel

def test_runtime_boundary_minimum_repo_shape_present():
    required_dirs = [
        "app",
        "cli",
        "collectors",
        "compilers",
        "evaluators",
        "graph",
        "normalizers",
        "planners",
        "publishers",
        "tests",
    ]
    for rel in required_dirs:
        assert (ROOT / rel).is_dir(), rel

def test_runtime_boundary_minimum_boundary_lock_present():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    runtime = (ROOT / "RUNTIME.md").read_text(encoding="utf-8")

    required_readme = [
        "reconciliation / repair / projection",
        "does not author constitutional law",
        "does not hold canonical world-state",
        "does not perform sovereign cognition",
        "does not execute",
        "does not verify",
        "does not issue authority-of-record",
        "not terminal recognition",
        "not terminal recourse",
    ]
    for needle in required_readme:
        assert needle in readme, needle

    runtime_needles = [
        "CONSONORIUM",
        "runtime",
    ]
    for needle in runtime_needles:
        assert needle in runtime, needle
