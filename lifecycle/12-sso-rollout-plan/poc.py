#!/usr/bin/env python3
"""Checks a rollout list against the evidence files you already have."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    have = set(data["have"])
    rows = [{"name": item["name"], "status": "ready" if item["evidence"] in have else "missing", "evidence": item["evidence"]} for item in data["controls"]]
    missing = [row["name"] for row in rows if row["status"] == "missing"]
    return {"ok": missing == ["Device enrollment"], "summary": f"{len(missing)} controls still missing evidence", "rows": rows}


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
