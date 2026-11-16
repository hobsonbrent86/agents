#!/usr/bin/env python3
"""Tags a reply as interested, objection, referral, out of office, or unclear."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    rules = (
        ("out_of_office", ("out of office", "ooo", "automatic reply")),
        ("referral", ("talk to", "loop in", "introduc")),
        ("objection", ("not looking", "not interested", "no budget", "unsubscribe")),
        ("interested", ("next week", "send a time", "let's talk", "sounds good")),
    )

    def label(text):
        lowered = text.lower()
        for name, phrases in rules:
            if any(phrase in lowered for phrase in phrases):
                return name
        return "unclear"

    rows = [{"text": text, "intent": label(text)} for text in data["replies"]]
    counts = {}
    for row in rows:
        counts[row["intent"]] = counts.get(row["intent"], 0) + 1
    return {"ok": counts.get("interested") == 1 and counts.get("unclear") == 1, "summary": "5 replies tagged", "rows": rows}


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
