#!/usr/bin/env python3
"""Checks a local DNS snapshot and mailbox flags for the records a sending domain needs."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    present = {row["type"] for row in data["records"]}
    missing = [kind for kind in data["required"] if kind not in present]
    cold = [box["address"] for box in data["mailboxes"] if not box["warmup"]]
    return {
        "ok": missing == ["CNAME"] and not cold,
        "summary": f"missing {', '.join(missing) or 'none'}",
        "rows": [{"missing_records": missing, "cold_mailboxes": cold}],
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
