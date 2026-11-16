#!/usr/bin/env python3
"""Turns before and after operating numbers into a short case note."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    before = data["before"]
    after = data["after"]
    note = (
        f"{data['customer']} moved on-time delivery from {before['on_time']} percent to {after['on_time']} percent. "
        f"Cost per job moved from {before['cost_per_job']} to {after['cost_per_job']}."
    )
    return {"ok": "Redcedar Logistics" in note, "summary": "case note drafted", "rows": [{"note": note}]}


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
