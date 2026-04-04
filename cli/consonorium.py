#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
FIXTURE = json.loads((ROOT / "fixtures" / "sovereign" / "inventory.json").read_text(encoding="utf-8"))

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

def repository_list() -> list[dict]:
    return FIXTURE["repositories"]

def node_list() -> list[dict]:
    return FIXTURE.get("nodes", FIXTURE["repositories"])

def edge_list() -> list[dict]:
    return FIXTURE["edges"]

def node_type_counts() -> dict[str, int]:
    counts: dict[str, int] = {}
    for node in node_list():
        t = node.get("type", "<unknown>")
        counts[t] = counts.get(t, 0) + 1
    return dict(sorted(counts.items()))

def object_id(node: dict) -> str:
    return str(
        node.get("repo_id")
        or node.get("package_id")
        or node.get("surface_id")
        or node.get("artifact_id")
        or node.get("badge_id")
        or node.get("fqdn")
        or node.get("id")
        or "<unknown>"
    )

def inventory_payload() -> dict:
    payload = base_payload("inventory")
    payload.update({
        "status": "candidate",
        "summary": SUMMARY["inventory"],
        "repository_count": len(repository_list()),
        "node_count": len(node_list()),
        "edge_count": len(edge_list()),
        "node_type_counts": node_type_counts(),
        "repositories": repository_list(),
        "nodes": node_list(),
        "edges": edge_list(),
    })
    return payload

def audit_payload() -> dict:
    findings = []
    for node in node_list():
        findings.append({
            "object_id": object_id(node),
            "object_type": node.get("type", "<unknown>"),
            "status": "PASS",
            "severity": "none",
            "summary": f'{object_id(node)} present in world inventory as {node.get("type", "<unknown>")}.',
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
    payload = base_payload("reconcile")
    payload.update({
        "status": "candidate",
        "summary": SUMMARY["reconcile"],
        "candidate_id": "sovereign-reconcile-candidate",
        "source_report": "reports/generated/sovereign-inventory-report.json",
        "repository_count": len(repository_list()),
        "node_count": len(node_list()),
        "edge_count": len(edge_list()),
        "contradictions_open": 0,
        "repairs_open": 0,
        "quarantines_open": 0,
        "proposed_state": {
            "repositories": repository_list(),
            "nodes": node_list(),
            "edges": edge_list(),
        },
    })
    return payload

def plan_repairs_payload() -> dict:
    payload = base_payload("plan-repairs")
    payload.update({
        "status": "candidate",
        "summary": SUMMARY["plan-repairs"],
        "plan_count": 0,
        "source_report": "reports/generated/sovereign-inventory-report.json",
        "open_repairs": [],
        "reviewed_object_count": len(node_list()),
        "reviewed_objects": [object_id(node) for node in node_list()],
    })
    return payload

def apply_mechanical_repairs_payload() -> dict:
    payload = base_payload("apply-mechanical-repairs")
    payload.update({
        "status": "candidate",
        "summary": SUMMARY["apply-mechanical-repairs"],
        "applied_count": 0,
        "applied_repairs": [],
        "source_report": "reports/generated/sovereign-inventory-report.json",
        "reviewed_object_count": len(node_list()),
        "reviewed_objects": [object_id(node) for node in node_list()],
    })
    return payload

def epoch_candidate_payload() -> dict:
    payload = base_payload("publish-epoch-candidate")
    payload.update({
        "status": "candidate",
        "summary": SUMMARY["publish-epoch-candidate"],
        "candidate_id": "sovereign-epoch-candidate",
        "source_report": "reports/generated/sovereign-inventory-report.json",
        "repository_count": len(repository_list()),
        "node_count": len(node_list()),
        "edge_count": len(edge_list()),
        "proposed_graph": {
            "repositories": repository_list(),
            "nodes": node_list(),
            "edges": edge_list(),
        },
    })
    return payload

def check_report_payload() -> dict:
    checks = []
    for node in node_list():
        checks.append({
            "object_id": object_id(node),
            "object_type": node.get("type", "<unknown>"),
            "status": "PASS",
            "severity": "none",
            "summary": f'{object_id(node)} present in sovereign inventory as {node.get("type", "<unknown>")}.',
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
    payload = base_payload("quarantine")
    payload.update({
        "status": "candidate",
        "summary": SUMMARY["quarantine"],
        "quarantine_count": 0,
        "source_report": "reports/generated/sovereign-inventory-report.json",
        "open": [],
        "reviewed_object_count": len(node_list()),
        "reviewed_objects": [object_id(node) for node in node_list()],
    })
    return payload

def project_payload() -> dict:
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
        "reviewed_objects": [object_id(node) for node in node_list()],
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
