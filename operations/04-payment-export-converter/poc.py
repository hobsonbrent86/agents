#!/usr/bin/env python3
"""Turns a payment export into ledger import rows."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    rows = []
    for payment in data["payments"]:
        net = payment["amount"] - payment["fee"]
        rows.append({"date": payment["created"], "amount": net, "memo": payment["description"], "account": "4000"})
    return {"ok": rows[0]["amount"] == 1165, "summary": f"{len(rows)} ledger rows", "rows": rows}


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
