#!/usr/bin/env python3
"""Turns plain routing notes into Gmail filter objects. It does not call Google."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    rows = []
    for index, rule in enumerate(data["rules"], start=1):
        criteria = {}
        if rule.get("from"):
            criteria["from"] = rule["from"]
        if rule.get("subject_contains"):
            criteria["subject"] = rule["subject_contains"]
        rows.append({"id": f"filter_{index}", "criteria": criteria, "action": {"forward": rule["forward_to"]}})
    return {"ok": len(rows) == 2, "summary": f"{len(rows)} filters ready", "rows": rows}


def main() -> None:
    fixture = Path(__file__).resolve().parent / "fixtures" / "sample.json"
    data = json.loads(fixture.read_text())
    result = run(data)
    html = result.pop("html", None)
    if html:
        out = Path(__file__).resolve().parent / "out"
        out.mkdir(exist_ok=True)
        (out / "index.html").write_text(html)
        result["wrote"] = "out/index.html"
    print(json.dumps(result, indent=2))
    if not result.get("ok"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
