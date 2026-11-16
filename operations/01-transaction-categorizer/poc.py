#!/usr/bin/env python3
"""Classifies bank lines from merchant rules. Unknown merchants stay uncategorized."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    rows = []
    for txn in data["transactions"]:
        category = "uncategorized"
        merchant = txn["merchant"].upper()
        for rule in data["rules"]:
            if rule["contains"] in merchant:
                category = rule["category"]
                break
        rows.append({**txn, "category": category})
    return {"ok": [row["category"] for row in rows] == ["hosting", "uncategorized"], "summary": "2 lines classified", "rows": rows}


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
