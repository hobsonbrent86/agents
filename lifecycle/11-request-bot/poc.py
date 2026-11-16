#!/usr/bin/env python3
"""Works a local request queue. Summaries, reminders, and lists stay on disk."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    rows = []
    for item in data["requests"]:
        if item["kind"] == "remind":
            reply = f"Reminder set: {item['text']}"
        elif item["kind"] == "list":
            reply = "Open: " + "; ".join(data["open_tasks"])
        else:
            reply = "I can remind or list open tasks."
        rows.append({"id": item["id"], "reply": reply})
    return {"ok": rows[2]["reply"].startswith("I can"), "summary": f"{len(rows)} requests handled", "rows": rows}


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
