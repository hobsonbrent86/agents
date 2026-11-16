#!/usr/bin/env python3
"""Proposes a bank rule when the same merchant shows up at least three times."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    counts = {}
    category = {}
    for txn in data["transactions"]:
        counts[txn["merchant"]] = counts.get(txn["merchant"], 0) + 1
        category[txn["merchant"]] = txn["category"]
    rows = [
        {"merchant": merchant, "category": category[merchant], "seen": count}
        for merchant, count in counts.items()
        if count >= data["minimum"]
    ]
    return {"ok": len(rows) == 1 and rows[0]["merchant"] == "CLOUD HOST", "summary": f"{len(rows)} rules proposed", "rows": rows}


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
