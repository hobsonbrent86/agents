#!/usr/bin/env python3
"""Flags accounts whose latest week of use fell well below the prior week."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    rows = []
    for account in data["accounts"]:
        ratio = account["latest_week"] / account["prior_week"]
        if ratio < data["drop_limit"]:
            rows.append({"name": account["name"], "ratio": round(ratio, 2)})
    return {"ok": [row["name"] for row in rows] == ["Northline"], "summary": f"{len(rows)} accounts at risk", "rows": rows}


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
