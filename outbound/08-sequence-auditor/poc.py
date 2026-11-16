#!/usr/bin/env python3
"""Finds paused sequences, stale next steps, and broken step numbers."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    rows = []
    for seq in data["sequences"]:
        issues = []
        if seq["status"] == "paused":
            issues.append("paused")
        if seq["status"] == "active" and seq["next_at"] < data["today"]:
            issues.append("stale")
        expected = list(range(1, len(seq["steps"]) + 1))
        if seq["steps"] != expected:
            issues.append("broken_steps")
        if issues:
            rows.append({"id": seq["id"], "issues": issues})
    return {"ok": len(rows) == 3, "summary": f"{len(rows)} sequences need attention", "rows": rows}


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
