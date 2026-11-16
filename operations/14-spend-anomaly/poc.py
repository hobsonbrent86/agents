#!/usr/bin/env python3
"""Flags a charge that is more than double the usual amount for that vendor."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    grouped = {}
    for charge in data["charges"]:
        grouped.setdefault(charge["vendor"], []).append(charge["amount"])
    rows = []
    for vendor, amounts in grouped.items():
        usual = sorted(amounts)[len(amounts) // 2]
        for amount in amounts:
            if amount > usual * 2:
                rows.append({"vendor": vendor, "amount": amount, "usual": usual})
    return {"ok": rows == [{"vendor": "Cloud Host", "amount": 180, "usual": 42}], "summary": f"{len(rows)} unusual charges", "rows": rows}


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
