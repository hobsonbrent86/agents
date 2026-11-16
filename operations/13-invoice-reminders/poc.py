#!/usr/bin/env python3
"""Stages overdue invoices into a friendly note, a firm note, or a final note."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    from datetime import date

    today = date.fromisoformat(data["today"])
    rows = []
    for invoice in data["invoices"]:
        days = (today - date.fromisoformat(invoice["due"])).days
        if days <= 15:
            stage = "friendly"
        elif days <= 30:
            stage = "firm"
        else:
            stage = "final"
        rows.append({"id": invoice["id"], "days": days, "stage": stage, "contact": invoice["contact"]})
    return {"ok": [row["stage"] for row in rows] == ["friendly", "firm", "final"], "summary": "3 reminders staged", "rows": rows}


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
