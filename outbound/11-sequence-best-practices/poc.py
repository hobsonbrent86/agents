#!/usr/bin/env python3
"""Applies a short audit: subject length, an opt-out line, a send window, and a step cap."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    fixes = []
    subject = data["subject"]
    if len(subject) > 60:
        subject = subject[:57].rstrip() + "..."
        fixes.append("shorten_subject")
    body = data["body"]
    if "unsubscribe" not in body.lower():
        body = body.rstrip() + " Reply stop to unsubscribe."
        fixes.append("add_opt_out")
    window = data["window"]
    if window == "any":
        window = "weekday 08:00-17:00"
        fixes.append("set_window")
    steps = data["steps"]
    if steps > 5:
        steps = 5
        fixes.append("cap_steps")
    return {
        "ok": fixes == ["shorten_subject", "add_opt_out", "set_window", "cap_steps"],
        "summary": f"{len(fixes)} fixes applied",
        "rows": [{"subject": subject, "body": body, "window": window, "steps": steps, "fixes": fixes}],
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
