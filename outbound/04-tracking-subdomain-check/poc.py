#!/usr/bin/env python3
"""Checks that a tracking hostname points at the expected target and is tied to a mailbox."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    cname_ok = data["actual"] == data["expected"]
    mailbox_ok = bool(data.get("mailbox"))
    return {
        "ok": cname_ok and mailbox_ok,
        "summary": "tracking host is healthy" if cname_ok and mailbox_ok else "tracking host needs a fix",
        "rows": [{"host": data["host"], "cname_ok": cname_ok, "mailbox": data["mailbox"]}],
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
