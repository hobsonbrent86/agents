#!/usr/bin/env python3
"""Sorts the day's social touches by warmth and fit."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    rows = []
    for touch in data["touches"]:
        score = data["warmth"][touch["warmth"]] * 10 + data["tier"][touch["tier"]]
        rows.append({**touch, "score": score})
    rows.sort(key=lambda row: row["score"], reverse=True)
    return {"ok": [row["name"] for row in rows] == ["Ada", "Bea", "Sam"], "summary": "queue sorted", "rows": rows}


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
