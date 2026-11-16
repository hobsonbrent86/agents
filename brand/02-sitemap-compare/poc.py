#!/usr/bin/env python3
"""Puts three competitor URL lists next to each other."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    rows = [{"host": host, "pages": len(paths), "paths": paths} for host, paths in data["sites"].items()]
    return {"ok": len(rows) == 3, "summary": "3 sitemaps compared", "rows": rows}


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
