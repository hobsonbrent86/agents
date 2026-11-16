#!/usr/bin/env python3
"""Copies expense categories from a sheet into a table and updates rows that changed."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    table = {row["id"]: dict(row) for row in data["table"]}
    changes = []
    for row in data["sheet"]:
        current = table.get(row["id"])
        if current is None:
            table[row["id"]] = dict(row)
            changes.append({"id": row["id"], "action": "insert"})
        elif current["category"] != row["category"]:
            current["category"] = row["category"]
            changes.append({"id": row["id"], "action": "update"})
    return {"ok": [item["action"] for item in changes] == ["update", "insert"], "summary": f"{len(changes)} category changes", "rows": changes}


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
