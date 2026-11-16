#!/usr/bin/env python3
"""Runs search and pause commands against a local sequence store."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    store = {row["id"]: dict(row) for row in data["sequences"]}
    log = []
    for command in data["commands"]:
        if command["op"] == "search":
            hits = [row for row in store.values() if command["name"].lower() in row["name"].lower()]
            log.append({"op": "search", "hits": [row["id"] for row in hits]})
        elif command["op"] == "pause":
            store[command["id"]]["status"] = "paused"
            log.append({"op": "pause", "id": command["id"]})
    return {"ok": store["s1"]["status"] == "paused", "summary": "search then pause", "rows": list(store.values()), "log": log}


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
