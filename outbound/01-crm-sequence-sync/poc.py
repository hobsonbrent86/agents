#!/usr/bin/env python3
"""Merges sequence step, warmth, and task completion between two local copies. The newer timestamp wins."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    right = {row["email"]: row for row in data["right"]}
    rows = []
    for left in data["left"]:
        other = right.get(left["email"])
        winner = other if other and other["updated"] >= left["updated"] else left
        loser = left if winner is other else other
        merged = dict(winner)
        if loser and loser["task_done"]:
            merged["task_done"] = True
        merged["source"] = "right" if winner is other else "left"
        rows.append(merged)
    return {"ok": rows[0]["warmth"] == "warm" and rows[0]["task_done"], "summary": f"{len(rows)} contacts merged", "rows": rows}


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
