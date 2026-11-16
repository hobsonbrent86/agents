#!/usr/bin/env python3
"""Tracks new-hire steps across mail, devices, and apps."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    left = [step for step in data["steps"] if not step["done"]]
    return {"ok": len(left) == 2, "summary": f"{data['hire']} has {len(left)} steps left", "rows": left}


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
