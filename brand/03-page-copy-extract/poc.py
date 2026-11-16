#!/usr/bin/env python3
"""Pulls the title and first heading out of saved HTML."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    import re

    rows = []
    for page in data["pages"]:
        title = re.search(r"<title>(.*?)</title>", page["html"])
        heading = re.search(r"<h1>(.*?)</h1>", page["html"])
        rows.append({"url": page["url"], "title": title.group(1) if title else "", "heading": heading.group(1) if heading else ""})
    return {"ok": rows[0]["heading"] == "Dispatch board", "summary": f"{len(rows)} pages extracted", "rows": rows}


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
