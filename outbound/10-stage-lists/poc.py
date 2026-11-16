#!/usr/bin/env python3
"""Builds static follow-up lists from sequence stage."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    lists = {}
    for person in data["people"]:
        lists.setdefault(person["stage"], []).append(person["email"])
    rows = [{"name": f"Follow up, {stage}", "emails": emails} for stage, emails in sorted(lists.items())]
    return {"ok": len(rows) == 2, "summary": f"{len(rows)} lists", "rows": rows}


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
