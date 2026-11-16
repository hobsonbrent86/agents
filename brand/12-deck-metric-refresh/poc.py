#!/usr/bin/env python3
"""Replaces slide placeholders with numbers from a local metrics file."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    rows = []
    for slide in data["slides"]:
        body = slide["body"]
        for key, value in data["metrics"].items():
            body = body.replace("{{" + key + "}}", value)
        rows.append({"title": slide["title"], "body": body})
    blob = " ".join(row["body"] for row in rows)
    return {"ok": "{{" not in blob and "1.2M" in blob, "summary": f"{len(rows)} slides refreshed", "rows": rows}


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
