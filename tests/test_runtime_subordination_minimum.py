import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class RuntimeSubordinationMinimumTest(unittest.TestCase):
    def test_runtime_boundary_object_and_index(self):
        boundary = json.loads((ROOT / "runtime/current/runtime-subordination-0001.json").read_text(encoding="utf-8"))
        index = json.loads((ROOT / "runtime/current/index.json").read_text(encoding="utf-8"))

        self.assertEqual(boundary["object_type"], "RuntimeSubordinationBoundary")
        self.assertEqual(boundary["status"], "ACTIVE_TRUTH")
        self.assertIn("must not directly mutate constitutional law surfaces", boundary["forbidden_mutations"])
        self.assertIn("must not directly mutate accepted-state surfaces", boundary["forbidden_mutations"])

        self.assertEqual(index["object_type"], "RuntimeBoundaryIndex")
        self.assertEqual(index["status"], "ACTIVE_TRUTH")
        self.assertIs(index["historical"], False)
        self.assertEqual(index["current_runtime_boundary_ref"], "runtime/current/runtime-subordination-0001.json")

    def test_existing_runtime_tests_are_pinned(self):
        boundary = json.loads((ROOT / "runtime/current/runtime-subordination-0001.json").read_text(encoding="utf-8"))

        expected = {
            "tests/test_check_report.py",
            "tests/test_audit_report.py",
            "tests/test_verdict_report.py",
            "tests/test_repair_plan.py",
            "tests/test_apply_mechanical_repairs.py",
            "tests/test_quarantine_report.py",
            "tests/test_projection_report.py",
        }

        found = set(boundary["deterministic_evaluator_test_refs"])
        found |= set(boundary["repair_planner_test_refs"])
        found |= set(boundary["quarantine_planner_test_refs"])
        found |= set(boundary["projection_compiler_test_refs"])

        self.assertTrue(expected.issubset(found))
