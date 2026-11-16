#!/usr/bin/env python3
"""Clusters headlines that share a topic and keeps the outlet leaning next to each one."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    topics = ("freight", "storm", "transit", "tax")
    clusters = {}
    for item in data["items"]:
        words = [topic for topic in topics if topic in item["title"].lower()]
        key = words[0] if words else "other"
        clusters.setdefault(key, []).append(item)
    rows = [{"topic": topic, "count": len(items), "leanings": sorted({item["leaning"] for item in items})} for topic, items in clusters.items()]
    return {"ok": any(row["topic"] == "freight" and row["count"] == 2 for row in rows), "summary": f"{len(rows)} topics", "rows": rows}


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
