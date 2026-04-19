#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

def need(cond, label):
    if cond:
        print(f"[VERIFY] {label}")
    else:
        errors.append(label)

readme_path = ROOT / "README.md"
runtime_path = ROOT / "RUNTIME.md"

need(readme_path.exists(), "readme-present")
need(runtime_path.exists(), "runtime-doc-present")
need((ROOT / "VERSION").exists(), "version-present")
need((ROOT / "tests/test_runtime_boundary_minimum.py").exists(), "runtime-minimum-test-present")
need((ROOT / "tests/verify_runtime_boundary_minimum.py").exists(), "runtime-minimum-verifier-present")

for rel in [
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
]:
    need((ROOT / rel).is_dir(), f"dir-present {rel}")

readme = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
runtime = runtime_path.read_text(encoding="utf-8") if runtime_path.exists() else ""

for needle, label in [
    ("reconciliation / repair / projection", "readme-role-surface"),
    ("does not author constitutional law", "readme-not-law"),
    ("does not hold canonical world-state", "readme-not-state"),
    ("does not perform sovereign cognition", "readme-not-cognition"),
    ("does not execute", "readme-not-execution"),
    ("does not verify", "readme-not-verification"),
    ("does not issue authority-of-record", "readme-not-authority"),
    ("not terminal recognition", "readme-not-recognition"),
    ("not terminal recourse", "readme-not-recourse"),
]:
    need(needle in readme, label)

need("CONSONORIUM" in runtime, "runtime-doc-names-surface")
need("runtime" in runtime.lower(), "runtime-doc-runtime-language")

if errors:
    print("\n[FAIL] CONSONORIUM runtime-boundary minimum verification failed")
    for e in errors:
        print(" -", e)
    sys.exit(1)

print("\n[PASS] CONSONORIUM runtime-boundary minimum verified")
