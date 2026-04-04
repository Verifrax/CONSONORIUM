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
    "audit": "Evaluate observed state against law and contracts.",
    "reconcile": "Compute candidate lawful state from observed inputs.",
    "plan-repairs": "Generate mechanically safe repair plans where target state is unambiguous.",
    "apply-mechanical-repairs": "Apply approved mechanical repair actions only.",
    "publish-checks": "Publish deterministic machine verdicts for the sovereign layer.",
    "publish-epoch-candidate": "Publish a deterministic epoch-candidate report derived from sovereign inventory.",
    "quarantine": "Record ambiguous or unsafe state as quarantine-class.",
    "project": "Compile projection surfaces from evaluated state."
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
    payload.update(
        {
            "status": "candidate",
            "summary": SUMMARY["inventory"],
            "repository_count": len(fixture["repositories"]),
            "edge_count": len(fixture["edges"]),
            "repositories": fixture["repositories"],
            "edges": fixture["edges"],
        }
    )
    return payload

def epoch_candidate_payload() -> dict:
    inventory = json.loads(INVENTORY_REPORT.read_text(encoding="utf-8"))
    payload = base_payload("publish-epoch-candidate")
    payload.update(
        {
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
        }
    )
    return payload

def check_report_payload() -> dict:
    inventory = json.loads(INVENTORY_REPORT.read_text(encoding="utf-8"))
    checks = []
    for repo in inventory["repositories"]:
        checks.append(
            {
                "object_id": repo["repo_id"],
                "status": "PASS",
                "severity": "none",
                "summary": f'{repo["repo_id"]} present in sovereign inventory with primary role {repo["primary_role"]}.',
            }
        )

    payload = base_payload("publish-checks")
    payload.update(
        {
            "status": "candidate",
            "summary": SUMMARY["publish-checks"],
            "check_count": len(checks),
            "source_report": "reports/generated/sovereign-inventory-report.json",
            "checks": checks,
        }
    )
    return payload

def scaffold_payload(mode: str) -> dict:
    payload = base_payload(mode)
    payload.update({"status": "scaffold", "summary": SUMMARY[mode]})
    return payload

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="consonorium", description="CONSONORIUM runtime entrypoint")
    sub = parser.add_subparsers(dest="mode", required=True)
    for mode in MODES:
        sub.add_parser(mode, help=SUMMARY[mode])
    return parser

def main() -> int:
    args = build_parser().parse_args()
    if args.mode == "inventory":
        payload = inventory_payload()
    elif args.mode == "publish-epoch-candidate":
        payload = epoch_candidate_payload()
    elif args.mode == "publish-checks":
        payload = check_report_payload()
    else:
        payload = scaffold_payload(args.mode)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
