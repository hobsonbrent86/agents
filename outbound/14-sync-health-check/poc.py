#!/usr/bin/env python3
"""Compares two contact copies and reports missing ids and field drift."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    left = {row["id"]: row for row in data["left"]}
    right = {row["id"]: row for row in data["right"]}
    only_left = sorted(set(left) - set(right))
    only_right = sorted(set(right) - set(left))
    drift = [key for key in set(left) & set(right) if left[key] != right[key]]
    healthy = not only_left and not only_right and not drift
    return {
        "ok": only_left == ["p2"] and only_right == ["p3"] and drift == ["p1"],
        "summary": "sync is healthy" if healthy else "sync has gaps",
        "rows": [{"only_left": only_left, "only_right": only_right, "drift": drift}],
    }


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
