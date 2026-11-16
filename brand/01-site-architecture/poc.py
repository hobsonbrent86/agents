#!/usr/bin/env python3
"""Splits sitemap URLs into core product pages and secondary marketing pages."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    core_bits = ("/product", "/pricing", "/security", "/platform")
    rows = []
    for url in data["urls"]:
        path = "/" + url.split("/", 3)[-1]
        kind = "core" if any(bit in path for bit in core_bits) else "secondary"
        rows.append({"url": url, "kind": kind})
    core = sum(1 for row in rows if row["kind"] == "core")
    return {"ok": core == 3, "summary": f"{core} core pages, {len(rows) - core} secondary", "rows": rows}


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
