#!/usr/bin/env python3
"""Recommends pages we are missing when two or more peers already have them."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    support = {}
    for peer in data["peers"]:
        for kind in peer["types"]:
            support[kind] = support.get(kind, 0) + 1
    recommended = sorted(kind for kind, count in support.items() if count >= 2 and kind not in data["ours"])
    return {"ok": recommended == ["trust"], "summary": f"{len(recommended)} pages recommended", "rows": recommended}


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
