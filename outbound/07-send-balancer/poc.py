#!/usr/bin/env python3
"""Assigns queued mail to inboxes without crossing a daily cap."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    counts = {inbox: 0 for inbox in data["inboxes"]}
    assigned = []
    held = []
    for message in data["queue"]:
        inbox = next((name for name, count in counts.items() if count < data["cap"]), None)
        if inbox is None:
            held.append(message)
            continue
        counts[inbox] += 1
        assigned.append({"message": message, "inbox": inbox})
    return {
        "ok": len(assigned) == 4 and held == ["m5"],
        "summary": f"{len(assigned)} assigned, {len(held)} held",
        "rows": assigned,
        "held": held,
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
