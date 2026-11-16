#!/usr/bin/env python3
"""Flags scheduled jobs whose last success is older than their interval."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    from datetime import datetime

    now = datetime.fromisoformat(data["now"])
    rows = []
    for job in data["jobs"]:
        last = datetime.fromisoformat(job["last_ok"])
        late_minutes = (now - last).total_seconds() / 60
        if late_minutes > job["every_minutes"]:
            rows.append({"name": job["name"], "late_minutes": int(late_minutes)})
    return {"ok": [row["name"] for row in rows] == ["hourly-ping"], "summary": f"{len(rows)} jobs late", "rows": rows}


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
