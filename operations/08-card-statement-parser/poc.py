#!/usr/bin/env python3
"""Parses statement lines into dated expenses and assigns a category."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    rows = []
    for line in data["lines"]:
        date, merchant, amount = line.rsplit("  ", 2)
        merchant = merchant.strip()
        category = "uncategorized"
        for rule in data["rules"]:
            if rule["contains"] in merchant.upper():
                category = rule["category"]
        rows.append({"date": date.strip(), "merchant": merchant, "amount": float(amount), "category": category})
    return {"ok": rows[0]["category"] == "hosting" and rows[1]["amount"] == 9.5, "summary": f"{len(rows)} statement lines", "rows": rows}


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
