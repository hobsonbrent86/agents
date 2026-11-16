#!/usr/bin/env python3
"""Writes a markdown inventory of groups and who can reach them."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    lines = ["# Groups", "", "| Group | Join | Post |", "| --- | --- | --- |"]
    for group in data["groups"]:
        lines.append(f"| {group['email']} | {group['join']} | {group['who_can_post']} |")
    text = "\n".join(lines)
    return {"ok": "all@northline.example" in text, "summary": f"{len(data['groups'])} groups listed", "markdown": text, "rows": data["groups"]}


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
