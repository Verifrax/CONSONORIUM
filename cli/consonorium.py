#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
MODES = ["inventory","audit","reconcile","plan-repairs","apply-mechanical-repairs","publish-checks","publish-epoch-candidate","quarantine","project"]
def payload(mode: str) -> dict:
    base = {
        "program": "consonorium",
        "version": VERSION,
        "law_source": "SYNTAGMARIUM",
        "accepted_state_store": "ORBISTIUM",
        "classification": "runtime",
        "deterministic_surface": True,
        "mode": mode,
        "status": "scaffold"
    }
    if mode == "inventory":
        base["runtime_modes"] = MODES
    return base
p = argparse.ArgumentParser(prog="consonorium")
sub = p.add_subparsers(dest="mode", required=True)
for m in MODES:
    sub.add_parser(m)
args = p.parse_args()
print(json.dumps(payload(args.mode), indent=2, ensure_ascii=False))
