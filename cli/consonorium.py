#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE = ROOT / "fixtures" / "minimal_inventory.json"

def load_fixture(path=None):
    target = Path(path) if path else DEFAULT_FIXTURE
    return json.loads(target.read_text())

def contradiction(status, severity, object_id, message, repairability, quarantine_required, evidence):
    return {
        "status": status,
        "severity": severity,
        "object_id": object_id,
        "message": message,
        "evidence": evidence,
        "repairability": repairability,
        "quarantine_required": quarantine_required,
    }

def run(mode, inventory_path=None):
    fixture = load_fixture(inventory_path)
    result = {
        "mode": mode,
        "law_source": "../SYNTAGMARIUM",
        "previous_state_source": "../ORBISTIUM/current",
        "observed": fixture,
        "contradictions": [],
        "repairs": [],
        "quarantines": [],
    }

    for repo in fixture["repos"]:
        if repo["license"] != "Apache-2.0":
            result["contradictions"].append(
                contradiction(
                    "fail", "hard_fail", repo["repo_id"],
                    "license drift", "mechanical", False,
                    ["repo:license"]
                )
            )
            result["repairs"].append({
                "object_id": repo["repo_id"],
                "class": "license_alignment",
                "target": "LICENSE"
            })

    payload = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["digest"] = "sha256:" + hashlib.sha256(payload).hexdigest()
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=[
        "inventory","audit","reconcile","plan-repairs","apply-mechanical-repairs",
        "publish-checks","publish-epoch-candidate","quarantine","project"
    ])
    parser.add_argument("--inventory", dest="inventory", default=None)
    args = parser.parse_args()
    print(json.dumps(run(args.mode, args.inventory), indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
