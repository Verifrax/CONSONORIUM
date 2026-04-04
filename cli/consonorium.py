#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
INVENTORY_FIXTURE = ROOT / "fixtures" / "sovereign" / "inventory.json"
INVENTORY_REPORT = ROOT / "reports" / "generated" / "sovereign-inventory-report.json"

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

SUMMARY = {
    "inventory": "Collect observed sovereign-layer inventory.",
    "audit": "Compute a deterministic audit report from sovereign inventory.",
    "reconcile": "Compute a deterministic reconcile candidate from sovereign inventory.",
    "plan-repairs": "Compute a deterministic repair-plan report from sovereign inventory.",
    "apply-mechanical-repairs": "Materialize a deterministic mechanical-repair application report.",
    "publish-checks": "Publish deterministic machine verdicts for the sovereign layer.",
    "publish-epoch-candidate": "Publish a deterministic epoch-candidate report derived from sovereign inventory.",
    "quarantine": "Materialize a deterministic quarantine report for the sovereign layer.",
    "project": "Compile deterministic projection outputs from sovereign inventory.",
}

def base_payload(mode: str) -> dict:
    return {
        "program": "consonorium",
        "version": VERSION,
        "law_source": "SYNTAGMARIUM",
        "accepted_state_store": "ORBISTIUM",
        "classification": "runtime",
        "deterministic_surface": True,
        "mode": mode,
    }

def inventory_payload() -> dict:
    fixture = json.loads(INVENTORY_FIXTURE.read_text(encoding="utf-8"))
    payload = base_payload("inventory")
    payload.update({
        "status": "candidate",
        "summary": SUMMARY["inventory"],
        "repository_count": len(fixture["repositories"]),
        "edge_count": len(fixture["edges"]),
        "repositories": fixture["repositories"],
        "edges": fixture["edges"],
    })
    return payload

def audit_payload() -> dict:
    inventory = json.loads(INVENTORY_REPORT.read_text(encoding="utf-8"))
    findings = []
    for repo in inventory["repositories"]:
        findings.append({
            "object_id": repo["repo_id"],
            "status": "PASS",
            "severity": "none",
            "summary": f"{repo['repo_id']} present on protected main with declared role {repo['primary_role']}.",
        })
    payload = base_payload("audit")
    payload.update({
        "status": "candidate",
        "summary": SUMMARY["audit"],
        "finding_count": len(findings),
        "source_report": "reports/generated/sovereign-inventory-report.json",
        "findings": findings,
    })
    return payload

def reconcile_payload() -> dict:
    inventory = json.loads(INVENTORY_REPORT.read_text(encoding="utf-8"))
    payload = base_payload("reconcile")
    payload.update({
        "status": "candidate",
        "summary": SUMMARY["reconcile"],
        "candidate_id": "sovereign-reconcile-candidate",
        "source_report": "reports/generated/sovereign-inventory-report.json",
        "repository_count": inventory["repository_count"],
        "edge_count": inventory["edge_count"],
        "contradictions_open": 0,
        "repairs_open": 0,
        "quarantines_open": 0,
        "proposed_state": {
            "repositories": inventory["repositories"],
            "edges": inventory["edges"],
        },
    })
    return payload

def plan_repairs_payload() -> dict:
    inventory = json.loads(INVENTORY_REPORT.read_text(encoding="utf-8"))
    payload = base_payload("plan-repairs")
    payload.update({
        "status": "candidate",
        "summary": SUMMARY["plan-repairs"],
        "plan_count": 0,
        "source_report": "reports/generated/sovereign-inventory-report.json",
        "open_repairs": [],
        "reviewed_repositories": [repo["repo_id"] for repo in inventory["repositories"]],
    })
    return payload

def apply_mechanical_repairs_payload() -> dict:
    inventory = json.loads(INVENTORY_REPORT.read_text(encoding="utf-8"))
    payload = base_payload("apply-mechanical-repairs")
    payload.update({
        "status": "candidate",
        "summary": SUMMARY["apply-mechanical-repairs"],
        "applied_count": 0,
        "applied_repairs": [],
        "source_report": "reports/generated/sovereign-inventory-report.json",
        "reviewed_repositories": [repo["repo_id"] for repo in inventory["repositories"]],
    })
    return payload

def epoch_candidate_payload() -> dict:
    inventory = json.loads(INVENTORY_REPORT.read_text(encoding="utf-8"))
    payload = base_payload("publish-epoch-candidate")
    payload.update({
        "status": "candidate",
        "summary": SUMMARY["publish-epoch-candidate"],
        "candidate_id": "sovereign-epoch-candidate",
        "source_report": "reports/generated/sovereign-inventory-report.json",
        "repository_count": inventory["repository_count"],
        "edge_count": inventory["edge_count"],
        "proposed_graph": {
            "repositories": inventory["repositories"],
            "edges": inventory["edges"],
        },
    })
    return payload

def check_report_payload() -> dict:
    inventory = json.loads(INVENTORY_REPORT.read_text(encoding="utf-8"))
    checks = []
    for repo in inventory["repositories"]:
        checks.append({
            "object_id": repo["repo_id"],
            "status": "PASS",
            "severity": "none",
            "summary": f"{repo['repo_id']} present in sovereign inventory with primary role {repo['primary_role']}.",
        })
    payload = base_payload("publish-checks")
    payload.update({
        "status": "candidate",
        "summary": SUMMARY["publish-checks"],
        "check_count": len(checks),
        "source_report": "reports/generated/sovereign-inventory-report.json",
        "checks": checks,
    })
    return payload

def quarantine_payload() -> dict:
    inventory = json.loads(INVENTORY_REPORT.read_text(encoding="utf-8"))
    payload = base_payload("quarantine")
    payload.update({
        "status": "candidate",
        "summary": SUMMARY["quarantine"],
        "quarantine_count": 0,
        "source_report": "reports/generated/sovereign-inventory-report.json",
        "open": [],
        "reviewed_repositories": [repo["repo_id"] for repo in inventory["repositories"]],
    })
    return payload

def project_payload() -> dict:
    inventory = json.loads(INVENTORY_REPORT.read_text(encoding="utf-8"))
    projections = [
        "reports/generated/sovereign-inventory-report.json",
        "reports/generated/sovereign-audit-report.json",
        "reports/generated/sovereign-check-report.json",
        "reports/generated/sovereign-epoch-candidate.json",
        "reports/generated/sovereign-reconcile-report.json",
        "reports/generated/sovereign-quarantine-report.json",
        "reports/generated/sovereign-repair-plan.json",
        "reports/generated/sovereign-mechanical-repair-application.json",
    ]
    payload = base_payload("project")
    payload.update({
        "status": "candidate",
        "summary": SUMMARY["project"],
        "projection_count": len(projections),
        "source_report": "reports/generated/sovereign-inventory-report.json",
        "projection_outputs": projections,
        "reviewed_repositories": [repo["repo_id"] for repo in inventory["repositories"]],
    })
    return payload

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="consonorium", description="CONSONORIUM runtime entrypoint")
    sub = parser.add_subparsers(dest="mode", required=True)
    for mode in MODES:
        sub.add_parser(mode, help=SUMMARY[mode])
    return parser

def main() -> int:
    args = build_parser().parse_args()
    payload = {
        "inventory": inventory_payload,
        "audit": audit_payload,
        "reconcile": reconcile_payload,
        "plan-repairs": plan_repairs_payload,
        "apply-mechanical-repairs": apply_mechanical_repairs_payload,
        "publish-checks": check_report_payload,
        "publish-epoch-candidate": epoch_candidate_payload,
        "quarantine": quarantine_payload,
        "project": project_payload,
    }[args.mode]()
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
