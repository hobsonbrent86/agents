#!/usr/bin/env python3
"""Searches and updates a local CRM fixture from a short command list."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    records = {row["id"]: dict(row) for row in data["records"]}
    log = []
    for command in data["commands"]:
        if command["op"] == "search":
            hits = [row for row in records.values() if row["email"] == command["email"]]
            log.append({"op": "search", "hits": len(hits)})
        elif command["op"] == "update":
            records[command["id"]]["status"] = command["status"]
            log.append({"op": "update", "id": command["id"], "status": command["status"]})
    return {
        "ok": records["p1"]["status"] == "working",
        "summary": f"{len(log)} commands applied",
        "rows": list(records.values()),
        "log": log,
    }


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
