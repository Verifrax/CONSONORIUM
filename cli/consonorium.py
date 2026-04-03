#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
INVENTORY_FIXTURE = ROOT / "fixtures" / "sovereign" / "inventory.json"

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
    "publish-checks": "Publish runtime verdicts to check surfaces.",
    "publish-epoch-candidate": "Publish candidate epoch material toward ORBISTIUM.",
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
        "mode": mode
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
            "edges": fixture["edges"]
        }
    )
    return payload

def scaffold_payload(mode: str) -> dict:
    payload = base_payload(mode)
    payload.update(
        {
            "status": "scaffold",
            "summary": SUMMARY[mode]
        }
    )
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
    else:
        payload = scaffold_payload(args.mode)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
