#!/usr/bin/env python3
"""Offline release checks for the public disclosure tree."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = list(ROOT.glob("*.md"))
FORBIDDEN = (
    "Ahana",
    "PP-QNI",
    "Q0",
    "Q1",
    "account_commit",
    "proof-first admission",
)
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def main() -> int:
    errors: list[str] = []
    for filename in (".zenodo.json", "EVIDENCE_MANIFEST.json"):
        try:
            json.loads((ROOT / filename).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid JSON {filename}: {exc}")
    for path in DOCS:
        text = path.read_text(encoding="utf-8")
        for term in FORBIDDEN:
            if term.lower() in text.lower():
                errors.append(f"private-design term {term!r} in {path.name}")
        for target in LINK.findall(text):
            if "://" in target or target.startswith("#"):
                continue
            local = target.split("#", 1)[0]
            if local and not (ROOT / local).exists():
                errors.append(f"broken local link {path.name} -> {target}")
    manifest = json.loads((ROOT / "EVIDENCE_MANIFEST.json").read_text(encoding="utf-8"))
    if manifest.get("evidence_bundle_complete"):
        errors.append("manifest claims a completed evidence bundle unexpectedly")
    if errors:
        print("RELEASE CHECK FAILED")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("RELEASE CHECK PASSED")
    print(f"checked {len(DOCS)} Markdown files, two JSON files, and local links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
