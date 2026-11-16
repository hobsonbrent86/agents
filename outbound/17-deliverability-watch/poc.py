#!/usr/bin/env python3
"""Alerts when bounce rate or spam complaints cross a safe line."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    rows = []
    for box in data["mailboxes"]:
        bounce_rate = box["bounces"] / box["sent"]
        complaint_rate = box["complaints"] / box["sent"]
        alerts = []
        if bounce_rate > data["bounce_limit"]:
            alerts.append("bounce")
        if complaint_rate > data["complaint_limit"]:
            alerts.append("complaint")
        if alerts:
            rows.append({"address": box["address"], "alerts": alerts})
    return {"ok": len(rows) == 2, "summary": f"{len(rows)} mailboxes over the line", "rows": rows}


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
