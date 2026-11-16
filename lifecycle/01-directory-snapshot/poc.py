#!/usr/bin/env python3
"""Flattens users, groups, and MFA status into rows you can save as CSV."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    rows = []
    for user in data["users"]:
        for group in user["groups"]:
            rows.append({"email": user["email"], "group": group, "mfa": user["mfa"]})
    missing = sorted({row["email"] for row in rows if not row["mfa"]})
    return {"ok": missing == ["sam@northline.example"] and len(rows) == 3, "summary": f"{len(missing)} users without MFA", "rows": rows}


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
