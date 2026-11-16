#!/usr/bin/env python3
"""Builds a one-page local dashboard for spend, revenue, and conversions that do not match a click."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    rows = []
    for campaign in data["campaigns"]:
        roas = round(campaign["revenue"] / campaign["spend"], 2)
        rows.append({**campaign, "return": roas})
    body = "".join(
        f"<tr><td>{row['name']}</td><td>{row['spend']}</td><td>{row['revenue']}</td><td>{row['return']}</td><td>{row['ghost_conversions']}</td></tr>"
        for row in rows
    )
    html = (
        "<!doctype html><meta charset='utf-8'><title>Campaigns</title>"
        "<style>body{font-family:sans-serif;background:#111;color:#eee}td,th{padding:8px 12px;border-bottom:1px solid #333}</style>"
        "<h1>Campaigns</h1><table><tr><th>Name</th><th>Spend</th><th>Revenue</th><th>Return</th><th>Unmatched</th></tr>"
        + body
        + "</table>"
    )
    return {"ok": rows[0]["return"] == 2.4, "summary": "dashboard written", "rows": rows, "html": html}


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
