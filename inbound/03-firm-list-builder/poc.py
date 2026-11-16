#!/usr/bin/env python3
"""Filters a local directory of investment firms by state and firm type."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    kinds = set(data["kinds"])
    rows = [f for f in data["firms"] if f["state"] == data["state"] and f["kind"] in kinds]
    return {"ok": len(rows) == 2, "summary": f"{len(rows)} firms in {data['state']}", "rows": rows}


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
