#!/usr/bin/env python3
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

def need(cond, label):
    if cond:
        print(f"[VERIFY] {label}")
    else:
        print(f"[FAIL] {label}")
        errors.append(label)

def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

for rel in [
    "runtime/current/runtime-subordination-0001.json",
    "runtime/current/index.json",
    "runtime/history/README.md",
    "tests/test_check_report.py",
    "tests/test_audit_report.py",
    "tests/test_verdict_report.py",
    "tests/test_repair_plan.py",
    "tests/test_apply_mechanical_repairs.py",
    "tests/test_quarantine_report.py",
    "tests/test_projection_report.py",
]:
    need((ROOT / rel).exists(), f"file-present {rel}")

boundary = load("runtime/current/runtime-subordination-0001.json")
index = load("runtime/current/index.json")

need(boundary["object_type"] == "RuntimeSubordinationBoundary", "runtime-boundary-type")
need(boundary["status"] == "ACTIVE_TRUTH", "runtime-boundary-status")
need(boundary["history_ref"] == "runtime/history/", "runtime-boundary-history-ref")
need(boundary["governing_inputs"]["constitutional_law_ref"].endswith("/SYNTAGMARIUM/blob/main/law/versions/current/law-version-0001.json"), "runtime-law-input-ref")
need(boundary["governing_inputs"]["accepted_epoch_ref"].endswith("/ORBISTIUM/blob/main/epochs/current/accepted-epoch-0001.json"), "runtime-epoch-input-ref")
need("must not directly mutate constitutional law surfaces" in boundary["forbidden_mutations"], "no-direct-law-mutation-guard")
need("must not directly mutate accepted-state surfaces" in boundary["forbidden_mutations"], "no-direct-accepted-state-mutation-guard")

need(index["object_type"] == "RuntimeBoundaryIndex", "runtime-index-type")
need(index["status"] == "ACTIVE_TRUTH", "runtime-index-status")
need(index["historical"] is False, "runtime-index-historical-false")
need(index["current_runtime_boundary_ref"] == "runtime/current/runtime-subordination-0001.json", "runtime-index-binding")
need(index["entries"][0]["runtime_boundary_id"] == boundary["runtime_boundary_id"], "runtime-index-entry-id")
need(index["entries"][0]["path"] == "runtime/current/runtime-subordination-0001.json", "runtime-index-entry-path")

all_refs = set(boundary["deterministic_evaluator_test_refs"])
all_refs |= set(boundary["repair_planner_test_refs"])
all_refs |= set(boundary["quarantine_planner_test_refs"])
all_refs |= set(boundary["projection_compiler_test_refs"])

need("tests/test_check_report.py" in all_refs, "deterministic-evaluator-tests")
need("tests/test_repair_plan.py" in all_refs and "tests/test_apply_mechanical_repairs.py" in all_refs, "repair-planner-tests")
need("tests/test_quarantine_report.py" in all_refs, "quarantine-planner-tests")
need("tests/test_projection_report.py" in all_refs, "projection-compiler-tests")

runtime_md = (ROOT / "RUNTIME.md").read_text(encoding="utf-8")
readme_md = (ROOT / "README.md").read_text(encoding="utf-8")
need("must not directly mutate constitutional law surfaces" in runtime_md, "runtime-md-law-guard")
need("must not directly mutate accepted-state surfaces" in runtime_md, "runtime-md-state-guard")
need("runtime/current/runtime-subordination-0001.json" in readme_md, "readme-runtime-subordination-surface")

if errors:
    print("[FAIL] PHASE 4 / STEP 57 runtime subordination minimum verification failed")
    for e in errors:
        print(f" - {e}")
    sys.exit(1)

print("[PASS] PHASE 4 / STEP 57 runtime subordination minimum verified")
