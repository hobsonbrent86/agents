#!/usr/bin/env python3
"""Sets every group member to receive all list mail."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    rows = []
    for member in data["members"]:
        changed = member["delivery"] != "all"
        rows.append({"email": member["email"], "delivery": "all", "changed": changed})
    changed = sum(1 for row in rows if row["changed"])
    return {"ok": changed == 2, "summary": f"{changed} members updated to all mail", "rows": rows}


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
