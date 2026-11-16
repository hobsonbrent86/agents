#!/usr/bin/env python3
"""Writes active sequence copy to markdown and JSON for review."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    active = [seq for seq in data["sequences"] if seq["status"] == "active"]
    lines = ["# Active sequences", ""]
    for seq in active:
        lines.append(f"## {seq['name']}")
        for index, step in enumerate(seq["steps"], start=1):
            lines.append(f"{index}. {step['channel']}: {step['body']}")
        lines.append("")
    return {
        "ok": "Old test" not in "\n".join(lines),
        "summary": f"{len(active)} active sequences exported",
        "markdown": "\n".join(lines).strip(),
        "rows": active,
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
