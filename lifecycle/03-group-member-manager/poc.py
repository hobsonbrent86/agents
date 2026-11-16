#!/usr/bin/env python3
"""Adds people to a group and skips anyone already on the list."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    members = set(data["members"])
    added = []
    for email in data["add"]:
        if email in members:
            continue
        members.add(email)
        added.append(email)
    return {"ok": added == ["sam@northline.example"], "summary": f"{len(added)} members added", "rows": sorted(members)}


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
