#!/usr/bin/env python3
"""Formats a daily pipeline note from local sequence stats. It prints the note instead of posting it."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    stats = data["stats"]
    text = (
        f"Pipeline {data['day']}: sent {stats['sent']}, replies {stats['replies']}, "
        f"positive {stats['positive']}, bounces {stats['bounces']}."
    )
    return {"ok": "positive 2" in text, "summary": text, "rows": [stats]}


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
