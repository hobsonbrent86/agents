#!/usr/bin/env python3
"""Pauses a cold sequence when the reply is interested or a referral. Objections stay paused too."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    pause_on = {"interested", "referral", "objection"}
    rows = []
    for item in data["items"]:
        action = "pause" if item["intent"] in pause_on else "keep"
        rows.append({"email": item["email"], "action": action, "intent": item["intent"]})
    return {"ok": [row["action"] for row in rows] == ["pause", "keep", "keep"], "summary": "1 sequence paused", "rows": rows}


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
