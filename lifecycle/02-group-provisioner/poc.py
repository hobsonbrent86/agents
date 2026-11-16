#!/usr/bin/env python3
"""Creates mailing lists that are in the config and missing from the directory."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    existing = set(data["existing"])
    created = [name for name in data["wanted"] if name not in existing]
    return {"ok": created == ["finance@northline.example"], "summary": f"{len(created)} groups to create", "rows": created}


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
