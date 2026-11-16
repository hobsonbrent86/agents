#!/usr/bin/env python3
"""Writes a weekly usage line for each account."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    lines = [f"Week of {data['week']}"]
    for account in data["accounts"]:
        lines.append(f"{account['name']}: {account['active_users']} active users, {account['events']} events.")
    return {"ok": len(lines) == 3, "summary": lines[0], "rows": data["accounts"], "markdown": "\n".join(lines)}


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
