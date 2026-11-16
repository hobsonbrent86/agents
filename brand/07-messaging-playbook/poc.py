#!/usr/bin/env python3
"""Assembles a short note for each audience from pain, proof, and a call to action."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    rows = []
    for audience in data["audiences"]:
        copy = f"{audience['name']}: {audience['pain']}. We give you {audience['proof']}. {audience['cta']}."
        rows.append({"audience": audience["name"], "copy": copy})
    return {"ok": len(rows) == 2 and "three tools" in rows[0]["copy"], "summary": f"{len(rows)} audience notes", "rows": rows}


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
