#!/usr/bin/env python3
"""Sets an advisor-style group to invite only, list replies, and moderated posts."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    group = dict(data["group"])
    group.update({"join": "invite", "reply_to": "list", "moderation": "on"})
    return {"ok": group["join"] == "invite" and group["reply_to"] == "list", "summary": "advisor defaults applied", "rows": [group]}


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
