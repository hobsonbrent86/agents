#!/usr/bin/env python3
"""Applies reply-to, posting, and moderation changes on a local group record."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    group = dict(data["group"])
    for command in data["commands"]:
        group[command["field"]] = command["value"]
    return {
        "ok": group["reply_to"] == "list" and group["moderation"] == "members",
        "summary": f"updated {group['email']}",
        "rows": [group],
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
