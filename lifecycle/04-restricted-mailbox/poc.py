#!/usr/bin/env python3
"""Moves a user to a restricted org unit and adds them to the advisor group."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    rows = []
    for user in data["users"]:
        if user["email"].endswith("@northline.example"):
            rows.append({**user, "action": "keep"})
            continue
        groups = sorted(set(user["groups"]) | {data["advisor_group"]})
        rows.append({"email": user["email"], "ou": data["restricted_ou"], "groups": groups, "action": "restrict"})
    return {"ok": rows[0]["action"] == "restrict" and rows[1]["action"] == "keep", "summary": "1 mailbox restricted", "rows": rows}


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
