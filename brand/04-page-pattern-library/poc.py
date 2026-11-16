#!/usr/bin/env python3
"""Counts how peers structure product, solution, and trust pages."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    counts = {}
    for page in data["pages"]:
        counts[page["type"]] = counts.get(page["type"], 0) + 1
    rows = [{"type": key, "sites": value} for key, value in sorted(counts.items())]
    return {"ok": counts.get("trust") == 2, "summary": "pattern counts ready", "rows": rows}


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
